use serde_json::Value;

include!("../../src/project_generator/utils/to_pymodd_maps.rs");
const excluded_actions: [&str; 2] = [
    // these actions do not work in modd.io as of (3/20/2023)
    "addUnitToUnitGroup",
    "addPlayerToPlayerGroup",
];

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let json_response = serde_json::from_str::<Value>(
        minreq::get("https://www.modd.io/api/editor-api/?game=two-houses")
            .with_header(
                "User-Agent",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            )
            .send()?
            .as_str()?,
    )?;
    let modd_objects_data: &Vec<Value> = json_response
        .get("message")
        .unwrap_or(&Value::Null)
        .as_array()
        .expect("invalid data: missing message content");

    let (mut missing_actions, mut missing_functions) = (Vec::new(), Vec::new());

    // find missing actions
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Action {
            let object_key = object_data.get("key").unwrap().as_str().unwrap();
            if ACTIONS_TO_PYMODD_STRUCTURE.get(object_key) == None {
                missing_actions.push(object_key);
            }
        }
    });

    // find missing functions
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Function {
            let object_key = object_data.get("key").unwrap().as_str().unwrap();
            if FUNCTIONS_TO_PYMODD_STRUCTURE.get(object_key) == None {
                missing_functions.push(object_key);
            }
        }
    });

    missing_actions = missing_actions
        .into_iter()
        .filter(|action| !excluded_actions.contains(action))
        .collect();

    dbg!(&missing_actions);
    dbg!(&missing_functions);
    dbg!(&missing_actions.len());
    dbg!(&missing_functions.len());

    Ok(())
}

#[derive(PartialEq)]
enum ObjectType {
    Action,
    Function,
    Undefined,
}

impl ObjectType {
    fn from_object_data(object_data: &Value) -> ObjectType {
        if let Some(wrapped_data) = object_data.get("data") {
            match wrapped_data
                .get("type")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
            {
                "action" => ObjectType::Action,
                "function" => ObjectType::Function,
                _ => ObjectType::Undefined,
            }
        } else {
            ObjectType::Undefined
        }
    }
}
