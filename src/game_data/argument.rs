use heck::ToSnakeCase;
use serde_json::{Map, Value};

use crate::generator::utils::to_pymodd::{PymoddStructure, FUNCTIONS_TO_PYMODD_STRUCTURE};

use super::actions::{parse_actions, Action};

const ARGS_TO_IGNORE: [&str; 4] = ["type", "function", "vars", "comment"];

/// Accepts both pymodd action and pymodd function data
pub fn parse_arguments_of_object_data(object_data: &Map<String, Value>) -> Vec<Argument> {
    let mut args = Vec::new();
    object_data
        .iter()
        .filter(|(arg_name, _)| !ARGS_TO_IGNORE.contains(&arg_name.as_str()))
        .for_each(|(arg_name, arg_data)| {
            if Function::name_from_data(object_data) == "calculate" && arg_name == "items" {
                args.extend(parse_arguments_of_operator_argument(arg_data));
            } else {
                args.push(match arg_name.as_str() {
                    "conditions" => parse_condition_argument(arg_data),
                    _ => Argument::parse(arg_name, arg_data),
                });
            }
        });
    args
}

fn parse_condition_argument(condition_data: &Value) -> Argument {
    Argument::new(
        "condition",
        ArgumentValue::Function(Function::new(
            "condition",
            parse_arguments_of_operator_argument(condition_data),
        )),
    )
}

/// Arguments of functions Calculate and Condition are formatted differently by modd.io
fn parse_arguments_of_operator_argument(argument_data: &Value) -> Vec<Argument> {
    let mut arguments = Vec::new();
    let empty_array = Vec::new();
    let argument_data = argument_data.as_array().unwrap_or(&empty_array);
    arguments.extend([
        Argument::new(
            "item_a",
            ArgumentValue::Value(argument_data.get(1).unwrap_or(&Value::Null).clone()),
        ),
        Argument::new(
            "operator",
            ArgumentValue::Value(
                argument_data
                    .get(0)
                    .unwrap_or(&Value::Null)
                    .as_object()
                    .unwrap_or(&Map::new())
                    .get("operator")
                    .unwrap_or(&Value::String("None".to_string()))
                    .clone(),
            ),
        ),
        Argument::new(
            "item_b",
            ArgumentValue::Value(argument_data.get(2).unwrap_or(&Value::Null).clone()),
        ),
    ]);
    arguments
}

/// Aligns the arguments to make sure they line up correctly with the structures defined in pymodd
pub fn align_arguments_with_pymodd_structure_parameters(
    mut arguments: Vec<Argument>,
    pymodd_structure_parameters: &Vec<String>,
) -> Vec<Argument> {
    let mut aligned_args: Vec<Option<Argument>> = Vec::new();
    pymodd_structure_parameters.iter().for_each(|parameter| {
        aligned_args.push(
            if let Some(matching_arg_position) = arguments.iter().position(|arg| {
                parameter.contains(&arg.name.to_snake_case())
                    || arg.name.to_snake_case().contains(parameter)
            }) {
                Some(arguments.remove(matching_arg_position))
            } else {
                None
            },
        )
    });
    dbg!(&aligned_args);
    dbg!(&arguments);
    aligned_args
        .into_iter()
        .map(|value| value.unwrap_or_else(|| arguments.remove(0)))
        .collect()
}

#[derive(Debug, PartialEq, Eq)]
pub struct Argument {
    pub name: String,
    pub value: ArgumentValue,
}

impl Argument {
    fn parse(argument_name: &str, argument_data: &Value) -> Argument {
        Argument {
            name: argument_name.to_string(),
            value: match argument_data {
                Value::Object(function_data) => {
                    ArgumentValue::Function(Function::parse(function_data))
                }
                Value::Array(actions_data) => ArgumentValue::Actions(parse_actions(&actions_data)),
                _ => ArgumentValue::Value(argument_data.clone()),
            },
        }
    }

    pub fn new(name: &str, value: ArgumentValue) -> Argument {
        Argument {
            name: name.to_string(),
            value,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum ArgumentValue {
    Value(Value),
    Actions(Vec<Action>),
    Function(Function),
}

#[derive(Debug, PartialEq, Eq)]
pub struct Function {
    name: String,
    pub args: Vec<Argument>,
}

impl Function {
    fn parse(function_data: &Map<String, Value>) -> Function {
        let name = Function::name_from_data(function_data);
        Function {
            args: align_arguments_with_pymodd_structure_parameters(
                parse_arguments_of_object_data(function_data),
                &FUNCTIONS_TO_PYMODD_STRUCTURE
                    .get(&name)
                    .unwrap_or(&PymoddStructure::default())
                    .parameters,
            ),
            name,
        }
    }

    pub fn new(name: &str, args: Vec<Argument>) -> Function {
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

    pub fn pymodd_class_name(&self) -> String {
        FUNCTIONS_TO_PYMODD_STRUCTURE
            .get(&self.name)
            .unwrap_or(&PymoddStructure::default())
            .name
            .clone()
    }
}

#[cfg(test)]
mod tests {
    use crate::generator::utils::to_pymodd::{
        ACTIONS_TO_PYMODD_STRUCTURE, FUNCTIONS_TO_PYMODD_STRUCTURE,
    };

    use super::{
        align_arguments_with_pymodd_structure_parameters, parse_arguments_of_operator_argument,
        Argument, ArgumentValue::Value as Val, Function,
    };
    use serde_json::{json, Value};

    #[test]
    fn align_condition_arguments_with_pymodd() {
        assert_eq!(
            align_arguments_with_pymodd_structure_parameters(
                vec![
                    Argument::new("operator", Val(Value::String("==".to_string()))),
                    Argument::new("item_a", Val(Value::Bool(true))),
                    Argument::new("item_b", Val(Value::Bool(true))),
                ],
                &FUNCTIONS_TO_PYMODD_STRUCTURE
                    .get("condition")
                    .unwrap()
                    .parameters
            )
            .as_slice(),
            [
                Argument::new("item_a", Val(Value::Bool(true))),
                Argument::new("operator", Val(Value::String("==".to_string()))),
                Argument::new("item_b", Val(Value::Bool(true))),
            ]
        )
    }

    #[test]
    fn align_action_arguments_with_pymodd() {
        assert_eq!(
            align_arguments_with_pymodd_structure_parameters(
                vec![
                    Argument::new("variableType", Val(Value::Null)),
                    Argument::new("value", Val(Value::Null)),
                    Argument::new("not_matching", Val(Value::Null)),
                ],
                &ACTIONS_TO_PYMODD_STRUCTURE
                    .get("setPlayerVariable")
                    .unwrap()
                    .parameters
            )
            .as_slice(),
            [
                Argument::new("not_matching", Val(Value::Null)),
                Argument::new("variableType", Val(Value::Null)),
                Argument::new("value", Val(Value::Null)),
            ]
        )
    }

    #[test]
    fn parse_condition_argument() {
        assert_eq!(
            parse_arguments_of_operator_argument(&json!([
                 {
                      "operandType": "boolean",
                      "operator": "=="
                 },
                 true,
                 true
            ]))
            .as_slice(),
            [
                Argument::new("item_a", Val(Value::Bool(true))),
                Argument::new("operator", Val(Value::String("==".to_string()))),
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
                    Argument::new("item_a", Val(json!(1))),
                    Argument::new("operator", Val(Value::String("+".to_string()))),
                    Argument::new("item_b", Val(json!(5))),
                ]
            )
        );
    }
}
