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
    comment: Option<String>,
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
            comment: {
                if let Some(comment) = action_data.get("comment").unwrap_or(&Value::Null).as_str() {
                    Some(comment.to_string())
                } else {
                    None
                }
            },
            args: parse_arguments_of_object_data(action_data),
        }
    }

    fn new(comment: Option<&str>, name: &str, args: Vec<Argument>) -> Action {
        Action {
            name: name.to_string(),
            comment: {
                if let Some(comment) = comment {
                    Some(comment.to_string())
                } else {
                    None
                }
            },
            args,
        }
    }
}

/// Accepts both pymodd action and pymodd function data
fn parse_arguments_of_object_data(object_data: &Map<String, Value>) -> Vec<Argument> {
    let mut args = Vec::new();
    object_data
        .iter()
        .filter(|(arg_name, _)| !ARGS_TO_IGNORE.contains(&arg_name.as_str()))
        .for_each(|(arg_name, arg_data)| {
            if arg_name == "conditions"
                || (arg_name == "items" && Function::name_from_data(object_data) == "calculate")
            {
                args.extend(parse_arguments_of_special_argument(arg_data))
            } else {
                args.push(Argument::parse(arg_name, arg_data));
            }
        });
    args
}

/// Calculate function's argument and Condition's arguments are formatted differently by modd.io
fn parse_arguments_of_special_argument(argument_data: &Value) -> Vec<Argument> {
    let mut arguments = Vec::new();
    let empty_array = Vec::new();
    let mut condition_data = argument_data.as_array().unwrap_or(&empty_array).iter();
    arguments.extend([
        Argument::new(
            "operator",
            ArgumentValue::Val(
                condition_data
                    .next()
                    .unwrap_or(&Value::Null)
                    .as_object()
                    .unwrap_or(&Map::new())
                    .get("operator")
                    .unwrap_or(&Value::String("None".to_string()))
                    .clone(),
            ),
        ),
        Argument::new(
            "item_a",
            ArgumentValue::Val(condition_data.next().unwrap_or(&Value::Null).clone()),
        ),
        Argument::new(
            "item_b",
            ArgumentValue::Val(condition_data.next().unwrap_or(&Value::Null).clone()),
        ),
    ]);
    arguments
}

#[derive(Debug, PartialEq, Eq)]
pub struct Argument {
    name: String,
    value: ArgumentValue,
}

impl Argument {
    fn parse(argument_name: &str, argument_data: &Value) -> Argument {
        Argument {
            name: argument_name.to_string(),
            value: match argument_data {
                Value::Object(function_data) => ArgumentValue::Func(Function::parse(function_data)),
                Value::Array(actions_data) => ArgumentValue::Actions(parse_actions(&actions_data)),
                _ => ArgumentValue::Val(argument_data.clone()),
            },
        }
    }

    fn new(name: &str, value: ArgumentValue) -> Argument {
        Argument {
            name: name.to_string(),
            value,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum ArgumentValue {
    Val(Value),
    Actions(Vec<Action>),
    Func(Function),
}

#[derive(Debug, PartialEq, Eq)]
pub struct Function {
    name: String,
    args: Vec<Argument>,
}

impl Function {
    fn parse(function_data: &Map<String, Value>) -> Function {
        Function {
            name: Function::name_from_data(function_data),
            args: parse_arguments_of_object_data(function_data),
        }
    }

    fn new(name: &str, args: Vec<Argument>) -> Function {
        Function {
            name: name.to_string(),
            args,
        }
    }

    fn name_from_data(function_data: &Map<String, Value>) -> String {
        function_data
            .get("function")
            .unwrap_or(&Value::Null)
            .as_str()
            .unwrap_or("null")
            .to_string()
    }
}

#[cfg(test)]
mod tests {
    use crate::game_data::actions::Argument;

    use super::{
        parse_actions, parse_arguments_of_special_argument, Action,
        ArgumentValue::{Actions, Func, Val},
        Function,
    };
    use serde_json::{json, Value};

    #[test]
    fn parse_condition_argument() {
        assert_eq!(
            parse_arguments_of_special_argument(&json!([
                 {
                      "operandType": "boolean",
                      "operator": "=="
                 },
                 true,
                 true
            ]))
            .as_slice(),
            [
                Argument::new("operator", Val(Value::String("==".to_string()))),
                Argument::new("item_a", Val(Value::Bool(true))),
                Argument::new("item_b", Val(Value::Bool(true))),
            ]
        );
    }

    #[test]
    fn parse_calculate_function() {
        assert_eq!(
            Function::parse(
                &json!({
                    "function": "calculate",
                        "items": [
                             {
                                  "operator": "+"
                             },
                             1,
                             5
                        ]
                })
                .as_object()
                .unwrap()
            ),
            Function::new(
                "calculate",
                vec![
                    Argument::new("operator", Val(Value::String("+".to_string()))),
                    Argument::new("item_a", Val(json!(1))),
                    Argument::new("item_b", Val(json!(5))),
                ]
            )
        );
    }

    #[test]
    fn parse_action() {
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
                Some("opens a shop!"),
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

    #[test]
    fn parse_nested_if_statement() {
        assert_eq!(
            parse_actions(
                json!([
                     {
                        "type": "condition",
                        "conditions": [
                            {
                                "operandType": "boolean",
                                "operator": "=="
                            },
                            true,
                            true
                        ],
                        "then": [
                            {
                                "type": "condition",
                                "conditions": [
                                    {
                                        "operandType": "boolean",
                                        "operator": "=="
                                    },
                                    true,
                                    true
                                ],
                                "then": [],
                                "else": []
                               }
                          ],
                          "else": []
                     }
                ])
                .as_array()
                .unwrap()
            )
            .as_slice(),
            [Action::new(
                None,
                "condition",
                vec![
                    Argument::new("operator", Val(Value::String("==".to_string()))),
                    Argument::new("item_a", Val(Value::Bool(true))),
                    Argument::new("item_b", Val(Value::Bool(true))),
                    Argument::new("else", Actions(vec![])),
                    Argument::new(
                        "then",
                        Actions(vec![Action::new(
                            None,
                            "condition",
                            vec![
                                Argument::new("operator", Val(Value::String("==".to_string()))),
                                Argument::new("item_a", Val(Value::Bool(true))),
                                Argument::new("item_b", Val(Value::Bool(true))),
                                Argument::new("else", Actions(vec![])),
                                Argument::new("then", Actions(vec![])),
                            ]
                        ),])
                    ),
                ]
            ),]
        );
    }
}
