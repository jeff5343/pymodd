use std::ops::Add;

use serde_json::Value;

use crate::game_data::{
    actions::Action,
    directory::Script,
    variable_categories::{pymodd_class_name_of_category, CategoriesToVariables},
    GameData,
};

use super::utils::{
    iterators::{
        argument_values_iterator::ArgumentValueIterItem, directory_iterator::DirectoryIterItem,
    },
    surround_string_with_quotes,
    to_pymodd::CONSTANTS_TO_PYMODD_ENUM,
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
        let scripts_content_builder =
            ScriptsContentBuilder::new(&game_data.categories_to_variables);
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
                    DirectoryIterItem::Script(script) => scripts_content_builder
                        .build_content_of(&script)
                        .add("\n\n"),
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

pub struct ScriptsContentBuilder<'a> {
    // may need to add Directory for script keys later on
    categories_to_variables: &'a CategoriesToVariables,
}

impl<'a> ScriptsContentBuilder<'a> {
    pub fn new(categories_to_variables: &'a CategoriesToVariables) -> ScriptsContentBuilder<'a> {
        ScriptsContentBuilder {
            categories_to_variables,
        }
    }

    pub fn build_content_of(&self, script: &Script) -> String {
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
            self.build_actions_content(&script.actions)
                .lines()
                .map(|action| format!("{}{action}\n", "\t".repeat(3)))
                .collect::<String>(),
        )
    }

    fn build_actions_content(&self, actions: &Vec<Action>) -> String {
        actions
            .iter()
            .map(|action| {
                action
                    .iter_flattened_argument_values()
                    .fold(
                        format!("{}(", action.pymodd_class_name()),
                        |accumulated_args, curr_arg| {
                            let is_first_argument_of_action_or_function =
                                accumulated_args.ends_with("(");
                            accumulated_args.add(
                                // insert seperator only if the argument is not the first argument and is not the end of a function
                                &(!is_first_argument_of_action_or_function
                                    && curr_arg != ArgumentValueIterItem::FunctionEnd)
                                    .then_some(String::from(", "))
                                    .unwrap_or(String::new())
                                    .add(&self.build_argument_content(curr_arg)),
                            )
                        },
                    )
                    .add("),\n")
            })
            .collect::<String>()
    }

    fn build_argument_content(&self, arg: ArgumentValueIterItem) -> String {
        match arg {
            ArgumentValueIterItem::StartOfFunction(function) => {
                format!("{}(", function.pymodd_class_name())
            }
            ArgumentValueIterItem::Actions(actions) => {
                format!(
                    "[\n{}\n]",
                    self.build_actions_content(actions)
                        .lines()
                        .map(|line| format!("\t{line}\n"))
                        .collect::<String>()
                )
            }
            ArgumentValueIterItem::Value(value) => match value {
                Value::String(string) => {
                    if let Some(constant) = CONSTANTS_TO_PYMODD_ENUM.get(string) {
                        constant.to_owned()
                    } else if let Some((category, variable)) = self
                        .categories_to_variables
                        .find_categoried_variable_with_id(string)
                    {
                        format!(
                            "{}.{}",
                            pymodd_class_name_of_category(category),
                            variable.enum_name
                        )
                    } else {
                        surround_string_with_quotes(string)
                    }
                }
                Value::Bool(boolean) => boolean.to_string(),
                Value::Number(number) => number.to_string(),
                _ => String::from("None"),
            },
            ArgumentValueIterItem::FunctionEnd => String::from(")"),
        }
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use serde_json::json;

    use crate::game_data::{
        actions::parse_actions,
        directory::Script,
        variable_categories::{CategoriesToVariables, Variable},
    };

    use super::ScriptsContentBuilder;

    #[test]
    fn script_content() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_content_of(&Script::new(
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
    fn parse_action_with_variable_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::from([(
                "shops",
                vec![Variable::new("OJbEQyc7is", "WEAPONS", None)]
            )])))
            .build_actions_content(&parse_actions(
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
            )),
            "OpenShopForPlayer(Shops.WEAPONS, OwnerOfEntity(LastCastingUnit())),\n"
        )
    }

    #[test]
    fn parse_action_with_constant_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
                    &json!([
                        {
                            "type": "updateUiTextForEveryone",
                            "target": "top",
                            "value": "Hello!"
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "UpdateUiTextForEveryone(UiTarget.TOP, 'Hello!'),\n"
        )
    }

    #[test]
    fn parse_nested_if_statements_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
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
