use serde_json::{Map, Value};

use crate::project_generator::utils::to_pymodd::{PymoddStructure, ACTIONS_TO_PYMODD_STRUCTURE};

use super::argument::{
    align_arguments_with_pymodd_structure_parameters, parse_arguments_of_object_data, Argument,
};

pub fn parse_actions(actions_data: &Vec<Value>) -> Vec<Action> {
    actions_data
        .iter()
        .map(|action_data| Action::parse(action_data.as_object().unwrap_or(&Map::new())))
        .collect()
}

#[derive(Debug, PartialEq, Eq)]
pub struct Action {
    pub name: String,
    pub comment: Option<String>,
    pub args: Vec<Argument>,
}

impl Action {
    pub fn parse(action_data: &Map<String, Value>) -> Action {
        let action_name = string_value_of_key("type", action_data).unwrap_or(String::from("null"));
        Action {
            comment: string_value_of_key("comment", action_data),
            args: align_arguments_with_pymodd_structure_parameters(
                parse_arguments_of_object_data(action_data),
                &ACTIONS_TO_PYMODD_STRUCTURE
                    .get(&action_name)
                    .unwrap_or(&PymoddStructure::default())
                    .parameters,
            ),
            name: action_name,
        }
    }

    pub fn pymodd_class_name(&self) -> String {
        ACTIONS_TO_PYMODD_STRUCTURE
            .get(&self.name)
            .unwrap_or(&PymoddStructure::default())
            .name
            .clone()
    }
}

fn string_value_of_key(key: &str, data: &Map<String, Value>) -> Option<String> {
    data.get(key)
        .unwrap_or(&Value::Null)
        .as_str()
        .map(|value| value.to_string())
}

#[cfg(test)]
mod tests {
    use crate::game_data::{
        actions::{parse_actions, Action, Argument},
        argument::{
            ArgumentValue::{Actions, Function as Func, Value as Val},
            Function,
        },
    };

    use serde_json::{json, Value};

    impl Action {
        pub fn new(comment: Option<&str>, name: &str, args: Vec<Argument>) -> Action {
            Action {
                name: name.to_string(),
                comment: { comment.map(|comment| comment.to_string()) },
                args,
            }
        }
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
                    Argument::new("shop", Val(Value::String("OJbEQyc7is".to_string()))),
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
                    Argument::new(
                        "conditions",
                        Func(Function::new(
                            "condition",
                            vec![
                                Argument::new("item_a", Val(Value::Bool(true))),
                                Argument::new("operator", Val(Value::String("==".to_string()))),
                                Argument::new("item_b", Val(Value::Bool(true))),
                            ],
                        ))
                    ),
                    Argument::new(
                        "then",
                        Actions(vec![Action::new(
                            None,
                            "condition",
                            vec![
                                Argument::new(
                                    "conditions",
                                    Func(Function::new(
                                        "condition",
                                        vec![
                                            Argument::new("item_a", Val(Value::Bool(true))),
                                            Argument::new(
                                                "operator",
                                                Val(Value::String("==".to_string()))
                                            ),
                                            Argument::new("item_b", Val(Value::Bool(true))),
                                        ],
                                    ))
                                ),
                                Argument::new("then", Actions(vec![])),
                                Argument::new("else", Actions(vec![])),
                            ]
                        ),])
                    ),
                    Argument::new("else", Actions(vec![])),
                ]
            ),]
        );
    }
}
