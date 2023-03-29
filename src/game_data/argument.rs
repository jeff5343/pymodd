use heck::ToSnakeCase;
use serde_json::{Map, Value};

use crate::project_generator::utils::to_pymodd_maps::{
    PymoddStructure, FLIP_CONSTANTS_TO_PYMODD_ENUM, FUNCTIONS_TO_PYMODD_STRUCTURE,
    UI_TARGET_CONSTANTS_TO_PYMODD_ENUM,
};

use super::actions::{parse_actions, Action};

const ARGS_TO_IGNORE: [&str; 8] = [
    "type",
    "entityType",
    "vars",
    "function",
    "comment",
    "disabled",
    "runOnClient",
    "hasFixedCSP",
];

/// Accepts both pymodd action and pymodd function data
pub fn parse_arguments_of_object_data(object_data: &Map<String, Value>) -> Vec<Argument> {
    let mut args = Vec::new();
    object_data
        .iter()
        .filter(|(arg_name, _)| !ARGS_TO_IGNORE.contains(&arg_name.as_str()))
        .for_each(|(arg_name, arg_data)| {
            args.extend(match arg_name.as_str() {
                // Calculate Function
                "items" => parse_arguments_of_operator_data(arg_data),
                // Force Function
                "force" => {
                    if arg_data
                        .as_object()
                        .unwrap_or(&Map::new())
                        .contains_key("x")
                    {
                        parse_arguments_of_force_object_data(arg_data)
                    } else {
                        // return a force argument with only one number
                        vec![Argument::parse("force", arg_data)]
                    }
                }
                // Constants
                "target" if arg_data.is_string() => {
                    vec![Argument::new(
                        "target",
                        ArgumentValue::Constant(
                            UI_TARGET_CONSTANTS_TO_PYMODD_ENUM
                                .get(arg_data.as_str().unwrap())
                                .unwrap_or(&arg_data.as_str().unwrap().to_string())
                                .to_owned(),
                        ),
                    )]
                }
                "flip" if arg_data.is_string() => {
                    vec![Argument::new(
                        "flip",
                        ArgumentValue::Constant(
                            FLIP_CONSTANTS_TO_PYMODD_ENUM
                                .get(arg_data.as_str().unwrap())
                                .unwrap_or(&arg_data.as_str().unwrap().to_string())
                                .to_owned(),
                        ),
                    )]
                }
                _ => vec![Argument::parse(arg_name, arg_data)],
            })
        });
    args
}

/// Arguments of functions Calculate and Condition are formatted differently by modd.io
fn parse_arguments_of_operator_data(operator_data: &Value) -> Vec<Argument> {
    let arguments_of_operator_argument = operator_data.as_array().unwrap_or(&Vec::new()).clone();
    vec![
        Argument::parse(
            "item_a",
            &arguments_of_operator_argument
                .get(1)
                .unwrap_or(&Value::Null)
                .clone(),
        ),
        Argument::new(
            "operator",
            ArgumentValue::Value(
                arguments_of_operator_argument
                    .get(0)
                    .unwrap_or(&Value::Null)
                    .as_object()
                    .unwrap_or(&Map::new())
                    .get("operator")
                    .unwrap_or(&Value::Null)
                    .clone(),
            ),
        ),
        Argument::parse(
            "item_b",
            &arguments_of_operator_argument
                .get(2)
                .unwrap_or(&Value::Null)
                .clone(),
        ),
    ]
}

fn parse_arguments_of_force_object_data(force_object_data: &Value) -> Vec<Argument> {
    let force_arguments_to_value = force_object_data.as_object().unwrap_or(&Map::new()).clone();
    vec![
        Argument::new(
            "x",
            ArgumentValue::Value(
                force_arguments_to_value
                    .get("x")
                    .unwrap_or(&Value::Null)
                    .clone(),
            ),
        ),
        Argument::new(
            "y",
            ArgumentValue::Value(
                force_arguments_to_value
                    .get("y")
                    .unwrap_or(&Value::Null)
                    .clone(),
            ),
        ),
    ]
}

/// Aligns the arguments to make sure they line up correctly with the structures defined in pymodd
pub fn align_arguments_with_pymodd_structure_parameters(
    mut arguments: Vec<Argument>,
    pymodd_structure_parameters: &Vec<String>,
) -> Vec<Argument> {
    let mut aligned_args: Vec<Option<Argument>> = Vec::new();
    pymodd_structure_parameters.iter().for_each(|parameter| {
        aligned_args.push(
            arguments
                .iter()
                .enumerate()
                .fold(
                    (None, None),
                    |(closest_matching_arg_index, closest_matching_arg), (i, arg)| {
                        let snake_cased_arg = arg.name.to_snake_case();
                        if (parameter.contains(&snake_cased_arg)
                            || snake_cased_arg.contains(parameter))
                            && snake_cased_arg.len()
                                > closest_matching_arg
                                    .as_ref()
                                    .unwrap_or(&String::new())
                                    .len()
                        {
                            (Some(i), Some(snake_cased_arg))
                        } else {
                            (closest_matching_arg_index, closest_matching_arg)
                        }
                    },
                )
                .0
                .map(|closest_matching_arg_index| arguments.remove(closest_matching_arg_index)),
        )
    });
    aligned_args
        .into_iter()
        .map(|value| {
            value.unwrap_or_else(|| {
                arguments
                    .pop()
                    .unwrap_or(Argument::new("null", ArgumentValue::Value(Value::Null)))
            })
        })
        .collect()
}

#[derive(Clone, Debug, PartialEq, Eq)]
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
                    match Function::name_from_data(function_data).as_str() {
                        // parse getVariable functions into variable IDs for pymodd
                        "getPlayerVariable" | "getEntityVariable" => ArgumentValue::Value(
                            variable_id_from_get_unit_variable_function_data(function_data),
                        ),
                        "getVariable" => ArgumentValue::Value(
                            variable_id_from_get_variable_function_data(function_data),
                        ),
                        _ => ArgumentValue::Function(Function::parse(function_data)),
                    }
                }
                Value::Array(list_data) => {
                    if list_data_contains_operator(&list_data) {
                        // Convert conditions represented as a list by modd.io into a function
                        ArgumentValue::Function(Function::parse_condition_function(&list_data))
                    } else {
                        ArgumentValue::Actions(parse_actions(&list_data))
                    }
                }
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

fn variable_id_from_get_variable_function_data(
    get_variable_function_data: &Map<String, Value>,
) -> Value {
    get_variable_function_data
        .get("variableName")
        .unwrap_or(&Value::Null)
        .to_owned()
}

fn variable_id_from_get_unit_variable_function_data(
    get_entity_variable_function_data: &Map<String, Value>,
) -> Value {
    get_entity_variable_function_data
        .get("variable")
        .unwrap_or(&Value::Object(Map::new()))
        .get("key")
        .unwrap_or(&Value::Null)
        .to_owned()
}

fn list_data_contains_operator(list_data: &Vec<Value>) -> bool {
    list_data.len() == 3
        && list_data.iter().any(|value| {
            value
                .as_object()
                .unwrap_or(&Map::new())
                .contains_key("operator")
        })
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ArgumentValue {
    Value(Value),
    Actions(Vec<Action>),
    Function(Function),
    Constant(String),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Function {
    pub name: String,
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

    fn parse_condition_function(condition_data: &[Value]) -> Function {
        Function::new(
            "condition",
            parse_arguments_of_operator_data(&Value::from(condition_data)),
        )
    }

    pub fn new(name: &str, args: Vec<Argument>) -> Function {
        Function {
            name: name.to_string(),
            args,
        }
    }

    pub fn find_argument_with_name(&self, name: &str) -> Option<&Argument> {
        self.args.iter().find(|arg| arg.name == name)
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
    use crate::{
        game_data::argument::parse_arguments_of_object_data,
        project_generator::utils::to_pymodd_maps::{
            ACTIONS_TO_PYMODD_STRUCTURE, FUNCTIONS_TO_PYMODD_STRUCTURE,
        },
    };

    use super::{
        align_arguments_with_pymodd_structure_parameters, parse_arguments_of_operator_data,
        Argument,
        ArgumentValue::{Function as Func, Value as Val},
        Function,
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
                    Argument::new("entity", Val(Value::Null)),
                    Argument::new("variable", Val(Value::Null)),
                ],
                &FUNCTIONS_TO_PYMODD_STRUCTURE
                    .get("getValueOfEntityVariable")
                    .unwrap()
                    .parameters
            )
            .as_slice(),
            [
                Argument::new("variable", Val(Value::Null)),
                Argument::new("entity", Val(Value::Null)),
            ]
        )
    }

    #[test]
    fn align_missing_arguments_with_pymodd() {
        assert_eq!(
            align_arguments_with_pymodd_structure_parameters(
                vec![Argument::new(
                    "entity",
                    Val(Value::String("test".to_string()))
                ),],
                &ACTIONS_TO_PYMODD_STRUCTURE
                    .get("startUsingItem")
                    .unwrap()
                    .parameters
            )
            .as_slice(),
            [Argument::new(
                "entity",
                Val(Value::String("test".to_string()))
            ),]
        )
    }

    #[test]
    fn parse_force_object_argument() {
        assert_eq!(
            parse_arguments_of_object_data(
                &json!({
                    "force": {
                        "x": 1,
                        "y": 1
                    }
                })
                .as_object()
                .unwrap()
            )
            .as_slice(),
            [
                Argument::new("x", Val(json!(1))),
                Argument::new("y", Val(json!(1)))
            ]
        );
    }

    #[test]
    fn parse_regular_force_argument() {
        assert_eq!(
            parse_arguments_of_object_data(
                &json!({
                    "force": 5,
                })
                .as_object()
                .unwrap()
            )
            .as_slice(),
            [Argument::new("force", Val(json!(5))),]
        );
    }

    #[test]
    fn parse_player_variable_argument() {
        assert_eq!(
            parse_arguments_of_object_data(
                &json!({
                    "variable": {
                        "function": "getPlayerVariable",
                        "variable": {
                            "text": "unit",
                            "dataType": "unit",
                            "entity": "humanPlayer",
                            "key": "OW31JD2"
                        }
                    }
                })
                .as_object()
                .unwrap()
            )
            .as_slice(),
            [Argument::new(
                "variable",
                Val(Value::String("OW31JD2".to_string()))
            )]
        );
    }

    #[test]
    fn parse_get_variable_argument() {
        assert_eq!(
            parse_arguments_of_object_data(
                &json!({
                    "value": {
                        "function": "getVariable",
                        "variableName": "AI"
                    },
                })
                .as_object()
                .unwrap()
            )
            .as_slice(),
            [Argument::new("value", Val(Value::String("AI".to_string())))]
        );
    }

    #[test]
    fn parse_condition_argument() {
        assert_eq!(
            parse_arguments_of_operator_data(&json!([
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
    fn parse_nested_condition_argument() {
        assert_eq!(
            parse_arguments_of_operator_data(&json!([
                 {
                      "operandType": "boolean",
                      "operator": "OR"
                 },
                 [
                      {
                           "operandType": "boolean",
                           "operator": "=="
                      },
                      true,
                      true
                 ],
                 [
                      {
                           "operandType": "boolean",
                           "operator": "=="
                      },
                      true,
                      true
                 ]
            ]))
            .as_slice(),
            [
                Argument::new(
                    "item_a",
                    Func(Function::new(
                        "condition",
                        vec![
                            Argument::new("item_a", Val(Value::Bool(true))),
                            Argument::new("operator", Val(Value::String("==".to_string()))),
                            Argument::new("item_b", Val(Value::Bool(true))),
                        ],
                    )),
                ),
                Argument::new("operator", Val(Value::String("OR".to_string()))),
                Argument::new(
                    "item_b",
                    Func(Function::new(
                        "condition",
                        vec![
                            Argument::new("item_a", Val(Value::Bool(true))),
                            Argument::new("operator", Val(Value::String("==".to_string()))),
                            Argument::new("item_b", Val(Value::Bool(true))),
                        ],
                    )),
                ),
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

    #[test]
    fn parse_nested_calculate_function() {
        assert_eq!(
            Function::parse(
                &json!({
                    "function": "calculate",
                    "items": [
                        {
                            "operator": "+"
                        },
                        1,
                        {
                            "function": "calculate",
                            "items": [
                                {
                                     "operator": "+"
                                },
                                1,
                                5
                            ]
                        }
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
                    Argument::new(
                        "item_b",
                        Func(Function::new(
                            "calculate",
                            vec![
                                Argument::new("item_a", Val(json!(1))),
                                Argument::new("operator", Val(Value::String("+".to_string()))),
                                Argument::new("item_b", Val(json!(5))),
                            ]
                        ))
                    )
                ]
            )
        );
    }
}
