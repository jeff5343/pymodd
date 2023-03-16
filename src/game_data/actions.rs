use serde_json::{Map, Value};

use crate::project_generator::utils::to_pymodd_maps::{PymoddStructure, ACTIONS_TO_PYMODD_STRUCTURE};

use super::argument::{
    align_arguments_with_pymodd_structure_parameters, parse_arguments_of_object_data, Argument,
};

pub fn parse_actions(actions_data: &Vec<Value>) -> Vec<Action> {
    actions_data
        .iter()
        .map(|action_data| Action::parse(action_data.as_object().unwrap_or(&Map::new())))
        .collect()
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Action {
    pub name: String,
    pub args: Vec<Argument>,
    pub comment: Option<String>,
    pub ran_on_client: bool,
    pub disabled: bool,
}

impl Action {
    pub fn parse(action_data: &Map<String, Value>) -> Action {
        let action_name = action_data
            .get("type")
            .unwrap_or(&Value::Null)
            .as_str()
            .unwrap_or("null");
        Action {
            comment: action_data
                .get("comment")
                .unwrap_or(&Value::Null)
                .as_str()
                .map(|val| val.to_string()),
            ran_on_client: action_data
                .get("runOnClient")
                .unwrap_or(&Value::Null)
                .as_bool()
                .unwrap_or(false),
            disabled: action_data
                .get("disabled")
                .unwrap_or(&Value::Null)
                .as_bool()
                .unwrap_or(false),
            args: align_arguments_with_pymodd_structure_parameters(
                parse_arguments_of_object_data(action_data),
                &ACTIONS_TO_PYMODD_STRUCTURE
                    .get(action_name)
                    .unwrap_or(&PymoddStructure::default())
                    .parameters,
            ),
            name: action_name.to_string(),
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
        pub fn new(
            name: &str,
            args: Vec<Argument>,
            comment: Option<&str>,
            ran_on_client: bool,
            disabled: bool,
        ) -> Action {
            Action {
                name: name.to_string(),
                args,
                comment: { comment.map(|comment| comment.to_string()) },
                ran_on_client,
                disabled,
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
                        "runOnClient": true,
                        "disabled": true,
                        "vars": []
                    }
                ])
                .as_array()
                .unwrap()
            )
            .as_slice(),
            [Action::new(
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
                ],
                Some("opens a shop!"),
                true,
                true,
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
                            ],
                            None,
                            false,
                            false
                        ),])
                    ),
                    Argument::new("else", Actions(vec![])),
                ],
                None,
                false,
                false,
            ),]
        );
    }
}
