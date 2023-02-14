use std::ops::Add;

use serde_json::Value;

use crate::game_data::{actions::Action, directory::Script, GameData};

use super::utils::{
    iterators::{
        argument_values_iterator::ArgumentValueIterItem, directory_iterator::DirectoryIterItem,
    },
    surround_string_with_quotes,
};

pub struct ScriptsFile {}

impl ScriptsFile {
    pub fn build_content(game_data: &GameData) -> String {
        let content = format!(
            "from pymodd.actions import *\n\
            from pymodd.functions import *\n\
            from pymodd.script import Script, Trigger, UiTarget, Flip\n\n\
            from game_variables import *\n\n"
        );
        content.add(
            game_data
                .root_directory
                .iter_flattened()
                .map(|game_item| match game_item {
                    DirectoryIterItem::StartOfDirectory(directory) => format!(
                        "# ╭\n\
                         # {}\n\
                         # |\n\n",
                        directory.name.to_uppercase()
                    ),
                    DirectoryIterItem::Script(script) => build_script_content(&script).add("\n\n"),
                    DirectoryIterItem::DirectoryEnd => String::from(
                        "# |\n\
                         # ╰\n\n",
                    ),
                })
                .collect::<String>()
                .as_str(),
        )
    }
}

fn build_script_content(script: &Script) -> String {
    let (class_name, script_key): (String, &str) = (script.class_name(), script.key.as_ref());
    format!(
        "class {class_name}(Script):\n\
            \tdef _build(self):\n\
                \t\tself.key = '{script_key}'\n\
                \t\tself.triggers = [{}]\n\
                \t\tself.actions = [\n\
                {}\n\
                \t\t]\n",
        script.triggers_into_pymodd_enums().join(", "),
        build_actions(&script.actions)
            .lines()
            .map(|action| format!("{}{action}\n", "\t".repeat(3)))
            .collect::<String>(),
    )
}

fn build_actions(actions: &Vec<Action>) -> String {
    actions
        .iter()
        .map(|action| {
            action
                .iter_flattened_argument_values()
                .fold(
                    format!("{}(", action.pymodd_class_name()),
                    |accumulated_args, curr_arg| {
                        let is_first_argument = accumulated_args.ends_with("(");
                        accumulated_args.add(
                            // insert seperator only if the argument is after the first argument and is not the end of a function
                            &if !is_first_argument && curr_arg != ArgumentValueIterItem::FunctionEnd {
                                String::from(", ")
                            } else {
                                String::new()
                            }
                            .add(&build_argument(curr_arg)),
                        )
                    },
                )
                .add("),\n")
        })
        .collect::<String>()
}

fn build_argument(arg: ArgumentValueIterItem) -> String {
    match arg {
        ArgumentValueIterItem::StartOfFunction(function) => {
            format!("{}(", function.pymodd_class_name())
        }
        ArgumentValueIterItem::Actions(actions) => {
            format!(
                "[\n{}\n]",
                build_actions(actions)
                    .lines()
                    .map(|line| format!("\t{line}\n"))
                    .collect::<String>()
            )
        }
        ArgumentValueIterItem::Value(value) => {
            format!(
                "{}",
                match value {
                    Value::Bool(boolean) => boolean.to_string(),
                    Value::Number(number) => number.to_string(),
                    Value::String(string) => surround_string_with_quotes(string),
                    _ => String::from("Null"),
                }
            )
        }
        ArgumentValueIterItem::FunctionEnd => String::from(")"),
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use crate::game_data::{actions::parse_actions, directory::Script};

    use super::{build_actions, build_script_content};

    #[test]
    fn script_content() {
        assert_eq!(
            build_script_content(&Script::new(
                "initialize",
                "WI31HDK",
                vec!["gameStart"],
                Vec::new()
            )),
            String::from(format!(
                "class Initialize(Script):\n\
                    \tdef _build(self):\n\
                        \t\tself.key = 'WI31HDK'\n\
                        \t\tself.triggers = [Trigger.GAME_START]\n\
                        \t\tself.actions = [\n\
                        \n\
                        \t\t]\n",
            ))
        );
    }

    #[test]
    fn parse_single_action_into_pymodd() {
        assert_eq!(
            build_actions(&parse_actions(
                &json!([
                    {
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
            ))
            .as_str(),
            "OpenShopForPlayer('OJbEQyc7is', OwnerOfEntity(LastCastingUnit())),\n"
        )
    }

    #[test]
    fn parse_nested_if_statements_into_pymodd() {
        assert_eq!(
            build_actions(&parse_actions(
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
                          ],
                          "else": []
                     }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "IfStatement(Condition(true, '==', true), [\n\
                \tIfStatement(Condition(true, '==', true), [\n\
    		        \t\tIfStatement(Condition(true, '==', true), [\n\
		            \t\t\n\
		            \t\t], [\n\
		            \t\t\n\
		            \t\t]),\n\
                \t\n\
                \t], [\n\
                \t\n\
                \t]),\n\
            \n\
            ], [\n\
            \n\
            ]),\n"
        )
    }
}
