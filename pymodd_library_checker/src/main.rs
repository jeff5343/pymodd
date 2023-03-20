use serde_json::Value;

include!("../../src/project_generator/utils/to_pymodd_maps.rs");

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
    let modd_data: &Vec<Value> = json_response
        .get("message")
        .expect("message key was not found")
        .as_array()
        .expect("message key did not contain an array");

    let (mut actions, mut functions) = (Vec::new(), Vec::new());

    // parse actions
    modd_data.iter().for_each(|data| {
        if let Some(wrapped_data) = data.get("data") {
            if wrapped_data
                .get("type")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
                == "action"
            {
                actions.push(data.get("key").unwrap());
            }
        }
    });

    // parse functions
    modd_data.iter().for_each(|data| {
        if let Some(wrapped_data) = data.get("data") {
            if wrapped_data
                .get("type")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
                == "function"
            {
                functions.push(data.get("key").unwrap());
            }
        }
    });

    dbg!(&actions);
    dbg!(&functions);
    dbg!(&actions.len());
    dbg!(&functions.len());

    Ok(())
}
