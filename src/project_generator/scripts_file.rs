use std::ops::Add;

use serde_json::Value;

use crate::game_data::{
    actions::Action,
    directory::{Directory, Script},
    variable_categories::{pymodd_class_name_of_category, CategoriesToVariables},
    GameData,
};

use super::utils::{
    iterators::{
        argument_values_iterator::ArgumentValueIterItem, directory_iterator::DirectoryIterItem,
    },
    surround_string_with_quotes,
    to_pymodd_maps::CONSTANTS_TO_PYMODD_ENUM,
};

pub struct ScriptsFile {}

impl ScriptsFile {
    pub fn build_content(game_data: &GameData) -> String {
        let content = format!(
            "from pymodd.actions import *\n\
            from pymodd.functions import *\n\
            from pymodd.script import Script, Trigger, UiTarget, Flip\n\n\
            from game_variables import *\n\n\n"
        );
        content.add(&build_all_scripts_content_of_directory(
            &game_data.root_directory,
            &ScriptsClassContentBuilder::new(&game_data.categories_to_variables),
        ))
    }
}

pub fn build_all_scripts_content_of_directory(
    directory: &Directory,
    scripts_class_content_builder: &ScriptsClassContentBuilder,
) -> String {
    directory
        .iter_flattened()
        .map(|game_item| match game_item {
            DirectoryIterItem::StartOfDirectory(directory) => format!(
                "# ╭\n\
                 # {}\n\
                 # |\n\n",
                directory.name.to_uppercase()
            ),
            DirectoryIterItem::Script(script) => scripts_class_content_builder
                .build_class_content_of(&script)
                .add("\n\n"),
            DirectoryIterItem::DirectoryEnd => String::from(
                "# |\n\
                 # ╰\n\n",
            ),
        })
        .collect::<String>()
        .trim_end()
        .to_string()
}

pub struct ScriptsClassContentBuilder<'a> {
    // may need to add Directory for script keys later on
    categories_to_variables: &'a CategoriesToVariables,
}

impl<'a> ScriptsClassContentBuilder<'a> {
    pub fn new(
        categories_to_variables: &'a CategoriesToVariables,
    ) -> ScriptsClassContentBuilder<'a> {
        ScriptsClassContentBuilder {
            categories_to_variables,
        }
    }

    pub fn build_class_content_of(&self, script: &Script) -> String {
        let (class_name, script_key): (String, &str) =
            (script.pymodd_class_name(), script.key.as_ref());
        format!(
            "class {class_name}(Script):\n\
            \tdef _build(self):\n\
                \t\tself.key = '{script_key}'\n\
                \t\tself.triggers = [{}]\n\
                \t\tself.actions = [\n\
                {}\
                \t\t\t\n\
                \t\t]\n",
            script.triggers_into_pymodd_enums().join(", "),
            self.build_content_of_actions(&script.actions)
                .lines()
                .map(|action| format!("{}{action}\n", "\t".repeat(3)))
                .collect::<String>(),
        )
    }

    fn build_content_of_actions(&self, actions: &Vec<Action>) -> String {
        actions
            .iter()
            .map(|action| {
                match action.name.as_str() {
                    // Pull out comment field for Comment action argument
                    "comment" => {
                        format!(
                            "{}({}),\n",
                            action.pymodd_class_name(),
                            surround_string_with_quotes(
                                action.comment.as_ref().unwrap_or(&String::from("None"))
                            )
                        )
                    }
                    _ => {
                        action
                            .iter_flattened_argument_values()
                            .fold(
                                format!("{}(", action.pymodd_class_name()),
                                |pymodd_action, argument| {
                                    let is_first_argument = pymodd_action.ends_with("(");
                                    pymodd_action.add(&format!(
                                        "{}{}",
                                        // add seperator only if the argument is not the first argument
                                        // of a action/function and is not the end of a function
                                        if !is_first_argument
                                            && argument != ArgumentValueIterItem::FunctionEnd
                                        {
                                            String::from(", ")
                                        } else {
                                            String::new()
                                        },
                                        &self.build_content_of_argument(argument)
                                    ))
                                },
                            )
                            .add("),\n")
                    }
                }
            })
            .collect::<String>()
    }

    fn build_content_of_argument(&self, arg: ArgumentValueIterItem) -> String {
        match arg {
            ArgumentValueIterItem::StartOfFunction(function) => {
                format!("{}(", function.pymodd_class_name())
            }
            ArgumentValueIterItem::Actions(actions) => {
                format!(
                    "[\n{}\t\n]",
                    self.build_content_of_actions(actions)
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
                Value::Bool(boolean) => String::from(match boolean {
                    true => "True",
                    false => "False",
                }),
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

    use super::ScriptsClassContentBuilder;

    #[test]
    fn script_content() {
        assert_eq!(
            ScriptsClassContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_class_content_of(&Script::new(
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
                        \t\t\t\n\
                        \t\t]\n",
            ))
        );
    }

    #[test]
    fn parse_action_with_variable_into_pymodd() {
        assert_eq!(
            ScriptsClassContentBuilder::new(&CategoriesToVariables::new(HashMap::from([(
                "shops",
                vec![Variable::new("OJbEQyc7is", "WEAPONS", None)]
            )])))
            .build_content_of_actions(&parse_actions(
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
            "open_shop_for_player(Shops.WEAPONS, OwnerOfEntity(LastCastingUnit())),\n"
        )
    }

    #[test]
    fn parse_action_with_constant_into_pymodd() {
        assert_eq!(
            ScriptsClassContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_content_of_actions(&parse_actions(
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
            "update_ui_text_for_everyone(UiTarget.TOP, 'Hello!'),\n"
        )
    }

    #[test]
    fn parse_comment_action_into_pymodd() {
        assert_eq!(
            ScriptsClassContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_content_of_actions(&parse_actions(
                    &json!([
                        {
                            "type": "comment",
                            "comment": "hey there",
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "comment('hey there'),\n"
        );
    }

    #[test]
    fn parse_nested_if_statements_into_pymodd() {
        assert_eq!(
            ScriptsClassContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_content_of_actions(&parse_actions(
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
            "if_else(Condition(True, '==', True), [\n\
                \tif_else(Condition(True, '==', True), [\n\
    		        \t\tif_else(Condition(True, '==', True), [\n\
		                \t\t\t\n\
		            \t\t], [\n\
		                \t\t\t\n\
		            \t\t]),\n\
                    \t\t\n\
                \t], [\n\
                    \t\t\n\
                \t]),\n\
                \t\n\
            ], [\n\
                \t\n\
            ]),\n"
        )
    }
}
