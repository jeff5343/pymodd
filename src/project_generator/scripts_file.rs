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
        content.add(&build_directory_content(
            &game_data.root_directory,
            &ScriptsContentBuilder::new(&game_data.categories_to_variables),
        ))
    }
}

pub fn build_directory_content(
    directory: &Directory,
    scripts_class_content_builder: &ScriptsContentBuilder,
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
                .build_script_content(&script)
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

pub struct ScriptsContentBuilder<'a> {
    categories_to_variables: &'a CategoriesToVariables,
}

impl<'a> ScriptsContentBuilder<'a> {
    pub fn new(
        categories_to_variables: &'a CategoriesToVariables,
    ) -> ScriptsContentBuilder<'a> {
        ScriptsContentBuilder {
            categories_to_variables,
        }
    }

    pub fn build_script_content(&self, script: &Script) -> String {
        let (class_name, script_key): (String, &str) =
            (script.pymodd_class_name(), &script.key);
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
            self.build_script_actions_content(&script.actions)
                .lines()
                .map(|action| format!("{}{action}\n", "\t".repeat(3)))
                .collect::<String>(),
        )
    }

    fn build_script_actions_content(&self, actions: &Vec<Action>) -> String {
        actions
            .iter()
            .map(|action| {
                match action.name.as_str() {
                    "comment" => {
                        // Pull out comment field for Comment action argument
                        format!(
                            "{}({}{}),\n",
                            action.pymodd_class_name(),
                            surround_string_with_quotes(
                                action.comment.as_ref().unwrap_or(&String::from("None"))
                            ),
                            self.build_optional_arguments_content(&action)
                                .into_iter()
                                .skip(1)
                                .map(|arg| String::from(", ") + &arg)
                                .collect::<String>(),
                        )
                    }
                    _ => self.build_action_content(&action),
                }
            })
            .collect::<String>()
    }

    fn build_action_content(&self, action: &Action) -> String {
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
                        if !is_first_argument && argument != ArgumentValueIterItem::FunctionEnd {
                            String::from(", ")
                        } else {
                            String::new()
                        },
                        &self.build_argument_content(argument)
                    ))
                },
            )
            .add(
                &self
                    .build_optional_arguments_content(&action)
                    .into_iter()
                    .enumerate()
                    .map(|(i, arg)| {
                        if action.args.is_empty() && i == 0 {
                            arg
                        } else {
                            String::from(", ") + &arg
                        }
                    })
                    .collect::<String>(),
            )
            .add("),\n")
    }

    fn build_argument_content(&self, arg: ArgumentValueIterItem) -> String {
        match arg {
            ArgumentValueIterItem::StartOfFunction(function) => {
                format!("{}(", function.pymodd_class_name())
            }
            ArgumentValueIterItem::Actions(actions) => {
                format!(
                    "[\n{}\t\n]",
                    self.build_script_actions_content(actions)
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

    fn build_optional_arguments_content(&self, action: &Action) -> Vec<String> {
        let mut optional_arguments: Vec<String> = Vec::new();
        if let Some(comment) = &action.comment {
            if !comment.is_empty() {
                optional_arguments
                    .push(format!("comment={}", surround_string_with_quotes(comment)));
            }
        }
        if action.disabled {
            optional_arguments.push(String::from("disabled=True"));
        }
        if action.ran_on_client {
            optional_arguments.push(String::from("run_on_client=True"));
        }
        optional_arguments
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
                .build_script_content(&Script::new(
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
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::from([(
                "shops",
                vec![Variable::new("OJbEQyc7is", "WEAPONS", None)]
            )])))
            .build_script_actions_content(&parse_actions(
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
    fn parse_action_with_optional_arguments_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_script_actions_content(&parse_actions(
                    &json!([
                        {
                            "type": "runScript",
                            "scriptName": "fjw24WdJ",
                            "comment": "hi!",
                            "runOnClient": true,
                            "disabled": true,
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "run_script('fjw24WdJ', comment='hi!', disabled=True, run_on_client=True),\n"
        )
    }

    #[test]
    fn parse_action_with_only_optional_arguments_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_script_actions_content(&parse_actions(
                    &json!([
                        {
                            "type": "return",
                            "comment": "hi!",
                            "runOnClient": true,
                            "disabled": false,
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "return_loop(comment='hi!', run_on_client=True),\n"
        )
    }

    #[test]
    fn parse_action_with_constant_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_script_actions_content(&parse_actions(
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
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_script_actions_content(&parse_actions(
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
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_script_actions_content(&parse_actions(
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
