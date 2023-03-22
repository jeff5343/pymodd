use heck::{ToPascalCase, ToSnakeCase, ToUpperCamelCase};
use serde_json::{Map, Value};

pub fn fetch_modd_io_triggers_data() -> Result<Value, Box<dyn std::error::Error>> {
    Ok(serde_json::from_str::<Value>(
        minreq::get("https://www.modd.io/api/editor-api/?game=two-houses&type=trigger")
            .with_header(
                "User-Agent",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            )
            .send()?
            .as_str()?,
    )?["message"]
        .take())
}

pub fn fetch_modd_io_functions_and_actions_data() -> Result<Value, Box<dyn std::error::Error>> {
    Ok(serde_json::from_str::<Value>(
        minreq::get("https://www.modd.io/api/editor-api/?game=two-houses")
            .with_header(
                "User-Agent",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            )
            .send()?
            .as_str()?,
    )?["message"]
        .take())
}

#[derive(Debug)]
pub struct Object {
    pub name: String,
    category: String,
    parameters: Vec<String>,
}

impl Object {
    pub fn from_object_data(object_data: &Value) -> Object {
        let empty_map = Value::Object(Map::new());
        let wrapped_data = object_data.get("data").unwrap_or(&empty_map);
        Object {
            name: object_data
                .get("key")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
                .to_string(),
            category: wrapped_data
                .get("category")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
                .to_string(),
            parameters: wrapped_data
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

#[derive(Debug, PartialEq)]
pub enum ObjectType {
    Trigger,
    Action,
    Function,
    Undefined,
}

impl ObjectType {
    pub fn from_object_data(object_data: &Value) -> ObjectType {
        if let Some(wrapped_data) = object_data.get("data") {
            match wrapped_data
                .get("type")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none")
            {
                "trigger" => ObjectType::Trigger,
                "action" => ObjectType::Action,
                "function" => ObjectType::Function,
                _ => ObjectType::Undefined,
            }
        } else {
            ObjectType::Undefined
        }
    }
}

pub fn generate_action_function_from_object(object: &Object) -> String {
    let (action_name, action_parameters) = (
        &object.name,
        &object
            .parameters
            .iter()
            .map(|parameter| parameter.to_snake_case())
            .collect::<Vec<String>>(),
    );
    format!(
        "@action\n\
        def {}({}comment=None, disabled=False, run_on_client=False):\n\
            \treturn {{\n\
                \t\t'type': '{action_name}',\n\
                {}\
            \t}}",
        action_name.to_snake_case(),
        if !action_parameters.is_empty() {
            action_parameters.join(", ") + ", "
        } else {
            String::new()
        },
        action_parameters
            .iter()
            .map(|parameter| format!("\t\t'{parameter}': to_dict({parameter}),\n"))
            .collect::<String>()
    )
}

pub fn generate_function_class_from_object(object: &Object) -> String {
    let (function_name, function_category, function_parameters) = (
        &object.name,
        &object.category.to_upper_camel_case(),
        &object
            .parameters
            .iter()
            .map(|parameter| parameter.to_snake_case())
            .collect::<Vec<String>>(),
    );
    format!(
        "class {}({function_category}):\n\
            \tdef __init__(self, {}):\n\
                \t\tself.function = '{function_name}'\n\
                \t\tself.options = {{\n\
                {}\
                \t\t}}",
        function_name.to_pascal_case(),
        if !function_parameters.is_empty() {
            function_parameters.join(", ")
        } else {
            String::new()
        },
        function_parameters
            .iter()
            .map(|parameter| format!("\t\t\t'{parameter}': to_dict({parameter}),\n"))
            .collect::<String>()
    )
}
