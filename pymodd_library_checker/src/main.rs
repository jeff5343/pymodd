//! find and log actions and functions not implemented in pymodd

use serde_json::{Map, Value};

include!("../../src/project_generator/utils/to_pymodd_maps.rs");
const EXCLUDED_ACTIONS: [&str; 2] = [
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

    let (mut non_included_actions, mut non_included_functions) = (Vec::new(), Vec::new());

    // find non included actions
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Action {
            let action_object = Object::from_object_data(object_data);
            if ACTIONS_TO_PYMODD_STRUCTURE.get(&action_object.name) == None {
                non_included_actions.push(action_object);
            }
        }
    });

    // find non included functions
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Function {
            let function_object = Object::from_object_data(object_data);
            if FUNCTIONS_TO_PYMODD_STRUCTURE.get(&function_object.name) == None {
                non_included_functions.push(function_object);
            }
        }
    });

    non_included_actions = non_included_actions
        .into_iter()
        .filter(|action| !EXCLUDED_ACTIONS.contains(&action.name.as_str()))
        .collect();

    dbg!(&non_included_actions);
    dbg!(&non_included_functions);
    dbg!(&non_included_actions.len());
    dbg!(&non_included_functions.len());

    Ok(())
}

#[derive(Debug, PartialEq)]
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

#[derive(Debug)]
struct Object {
    name: String,
    parameters: Vec<String>,
}

impl Object {
    fn from_object_data(object_data: &Value) -> Object {
        Object {
            name: object_data
                .get("key")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
                .to_string(),
            parameters: object_data
                .get("data")
                .unwrap_or(&Value::Object(Map::new()))
                .get("fragments")
                .unwrap_or(&Value::Null)
                .as_array()
                .unwrap_or(&Vec::new())
                .iter()
                .filter_map(|parameter_data| {
                    parameter_data
                        .get("field")
                        .unwrap_or(&Value::Null)
                        .as_str()
                        .map(|field| field.to_string())
                })
                .collect(),
        }
    }
}
