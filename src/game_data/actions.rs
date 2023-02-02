use serde_json::{Map, Value};

const ARGS_TO_IGNORE: [&str; 4] = ["type", "function", "vars", "comment"];

pub fn parse_actions(actions_data: &Vec<Value>) -> Vec<Action> {
    actions_data
        .iter()
        .map(|action_data| Action::parse(action_data.as_object().unwrap_or(&Map::new())))
        .collect()
}

#[derive(Debug, PartialEq, Eq)]
pub struct Action {
    name: String,
    comment: String,
    args: Vec<Argument>,
}

impl Action {
    pub fn parse(action_data: &Map<String, Value>) -> Action {
        Action {
            name: action_data
                .get("type")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("null")
                .to_string(),
            comment: action_data
                .get("comment")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("null")
                .to_string(),
            args: args_from_object(action_data),
        }
    }

    fn new(comment: &str, name: &str, args: Vec<Argument>) -> Action {
        Action {
            name: name.to_string(),
            comment: comment.to_string(),
            args,
        }
    }
}

fn args_from_object(object: &Map<String, Value>) -> Vec<Argument> {
    let mut args = Vec::new();
    object.iter().for_each(|(arg_name, arg_data)| {
        if !ARGS_TO_IGNORE.contains(&arg_name.as_str()) {
            args.push(Argument::new(
                arg_name.as_str(),
                match arg_data {
                    Value::Object(function_data) => {
                        ArgumentValue::Func(Function::parse(function_data))
                    }
                    _ => ArgumentValue::Val(arg_data.clone()),
                },
            ));
        }
    });
    args
}

#[derive(Debug, PartialEq, Eq)]
pub struct Argument {
    name: String,
    value: ArgumentValue,
}

impl Argument {
    fn new(name: &str, value: ArgumentValue) -> Argument {
        Argument {
            name: name.to_string(),
            value,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum ArgumentValue {
    Func(Function),
    Val(Value),
}

#[derive(Debug, PartialEq, Eq)]
pub struct Function {
    name: String,
    args: Vec<Argument>,
}

impl Function {
    fn parse(function_data: &Map<String, Value>) -> Function {
        Function {
            name: function_data
                .get("function")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("null")
                .to_string(),
            args: args_from_object(function_data),
        }
    }

    fn new(name: &str, args: Vec<Argument>) -> Function {
        Function {
            name: name.to_string(),
            args,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::game_data::actions::Argument;

    use super::{
        parse_actions, Action,
        ArgumentValue::{Func, Val},
        Function,
    };
    use serde_json::{json, Value};

    #[test]
    fn parse_actions_data() {
        assert_eq!(
            parse_actions(
                &json!([
                    {
                        "comment": "opens a shop!",
                        "type": "openShopForPlayer",
                        "player": {
                            "function": "getOwner",
                            "entity": {
                                "function": "getLastCastingUnit",
                                "vars": []
                            },
                            "vars": []
                        },
                        "shop": "OJbEQyc7is",
                        "vars": []
                    }
                ])
                .as_array()
                .unwrap()
            )
            .as_slice(),
            [Action::new(
                "opens a shop!",
                "openShopForPlayer",
                vec![
                    Argument::new(
                        "player",
                        Func(Function::new(
                            "getOwner",
                            vec![Argument::new(
                                "entity",
                                Func(Function::new("getLastCastingUnit", Vec::new()))
                            )]
                        )),
                    ),
                    Argument::new("shop", Val(Value::String("OJbEQyc7is".to_string()))),
                ]
            ),]
        );
    }
}
