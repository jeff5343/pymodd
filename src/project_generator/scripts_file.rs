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
        argument_values_iterator::{ArgumentValueIterItem, ArgumentValuesIterator, Operation},
        directory_iterator::DirectoryIterItem,
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
    pub fn new(categories_to_variables: &'a CategoriesToVariables) -> ScriptsContentBuilder<'a> {
        ScriptsContentBuilder {
            categories_to_variables,
        }
    }

    pub fn build_script_content(&self, script: &Script) -> String {
        let (class_name, script_key): (String, &str) = (script.pymodd_class_name(), &script.key);
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
                match action.name.as_str() {
                    "comment" => {
                        // pull out comment field for Comment action
                        format!(
                            "{}({}{}),\n",
                            action.pymodd_class_name(),
                            surround_string_with_quotes(
                                action.comment.as_ref().unwrap_or(&String::from("None"))
                            ),
                            self.build_optional_arguments_contents(&action)
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
        format!(
            "{}({}",
            action.pymodd_class_name(),
            self.build_arguments_content(action.iter_flattened_argument_values())
        )
        .add(
            &self
                .build_optional_arguments_contents(&action)
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

    fn build_arguments_content(&self, args_iter: ArgumentValuesIterator) -> String {
        args_iter
            .fold(String::from("("), |pymodd_args, arg| {
                let include_seperator =
                    !pymodd_args.ends_with("(") && arg != ArgumentValueIterItem::FunctionEnd;
                pymodd_args
                    + &format!(
                        "{}{}",
                        String::from(if include_seperator { ", " } else { "" }),
                        match arg {
                            // surround entire condition with parenthesis
                            ArgumentValueIterItem::Condition(_) =>
                                format!("({})", self.build_argument_content(arg)),
                            _ => self.build_argument_content(arg),
                        }
                    )
            })
            .strip_prefix("(")
            .unwrap()
            .to_string()
    }

    fn build_argument_content(&self, arg: ArgumentValueIterItem) -> String {
        match arg {
            ArgumentValueIterItem::StartOfFunction(function) => {
                format!("{}(", function.pymodd_class_name())
            }
            ArgumentValueIterItem::Actions(actions) => {
                format!(
                    "[\n{}\t\n]",
                    self.build_actions_content(actions)
                        .lines()
                        .map(|line| format!("\t{line}\n"))
                        .collect::<String>()
                )
            }
            ArgumentValueIterItem::Value(value) => match value {
                Value::String(string) => {
                    match self
                        .categories_to_variables
                        .find_categoried_variable_with_id(string)
                    {
                        Some((category, variable)) => format!(
                            "{}.{}",
                            pymodd_class_name_of_category(category),
                            variable.enum_name
                        ),
                        _ => surround_string_with_quotes(string),
                    }
                }
                Value::Bool(boolean) => String::from(match boolean {
                    true => "True",
                    false => "False",
                }),
                Value::Number(number) => number.to_string(),
                _ => String::from("None"),
            },
            ArgumentValueIterItem::Constant(constant) => constant.to_owned(),
            ArgumentValueIterItem::Condition(operation)
            | ArgumentValueIterItem::Concatenation(operation)
            | ArgumentValueIterItem::Calculation(operation) => {
                self.build_operation_content(&operation)
            }
            ArgumentValueIterItem::FunctionEnd => String::from(")"),
        }
    }

    fn build_operation_content(&self, operator: &Operation) -> String {
        let (item_a, operator, item_b) = (
            ArgumentValueIterItem::from_argument(&operator.item_a),
            ArgumentValueIterItem::from_argument(&operator.operator),
            ArgumentValueIterItem::from_argument(&operator.item_b),
        );

        format!(
            "{} {} {}",
            self.build_operation_item_content(item_a),
            if let ArgumentValueIterItem::Value(operator_value) = operator {
                into_operator(operator_value.as_str().unwrap_or("")).unwrap_or("")
            } else {
                ""
            },
            self.build_operation_item_content(item_b)
        )
    }

    fn build_operation_item_content(&self, operation_item: ArgumentValueIterItem) -> String {
        match operation_item {
            // only surround conditions and calculations with parenthesis
            ArgumentValueIterItem::Condition(_) | ArgumentValueIterItem::Calculation(_) => {
                format!("({})", self.build_argument_content(operation_item))
            }
            ArgumentValueIterItem::StartOfFunction(_) => self.build_arguments_content(
                ArgumentValuesIterator::from_argument_iter_value(operation_item),
            ),
            _ => self.build_argument_content(operation_item),
        }
    }

    fn build_optional_arguments_contents(&self, action: &Action) -> Vec<String> {
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

fn into_operator(string: &str) -> Option<&str> {
    if ["==", "!=", "<=", "<", ">", ">=", "+", "-", "/", "*", "**"].contains(&string) {
        return Some(string);
    }
    match string.to_lowercase().as_str() {
        "and" => Some("&"),
        "or" => Some("|"),
        _ => None,
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
            "open_shop_for_player(Shops.WEAPONS, OwnerOfEntity(LastCastingUnit())),\n"
        )
    }

    #[test]
    fn parse_action_with_optional_arguments_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
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
                .build_actions_content(&parse_actions(
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
            "update_ui_text_for_everyone(UiTarget.TOP, 'Hello!'),\n"
        )
    }

    #[test]
    fn parse_comment_action_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
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
    fn parse_nested_calculations_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
                    &json!([
                        {
                            "type": "increaseVariableByNumber",
                            "variable": null,
                            "number": {
                                "function": "calculate",
                                "items": [
                                    { "operator": "*" },
                                    { "function": "getRandomNumberBetween", "min": 0, "max": 5 },
                                    { "function": "calculate", "items": [
                                            { "operator": "+" },
                                            { "function": "getExponent", "base": { "function": "currentTimeStamp" }, "power": 2 },
                                            3
                                       ]
                                    }
                                ]
                            }
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "increase_variable_by_number(None, RandomNumberBetween(0, 5) * ((CurrentUnixTimeStamp() ** 2) + 3)),\n"
        );
    }

    #[test]
    fn parse_nested_concatenations_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
                    &json!([
                        {
                            "type": "sendChatMessage",
                            "message": {
                                "function": "concat",
                                "textA": "hi ",
                                "textB": {
                                    "function": "concat",
                                    "textA": {
                                        "function": "getPlayerId",
                                        "player": {
                                            "function": "getTriggeringPlayer"
                                        }
                                    },
                                    "textB": " player!"
                                }
                            }
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "send_chat_message_to_everyone('hi ' + IdOfPlayer(LastTriggeringPlayer()) + ' player!'),\n"
        );
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
                                { "operandType": "boolean", "operator": "==" },
                                true,
                                true
                            ],
                            "then": [
                                {
                                    "type": "condition",
                                    "conditions": [
                                        { "operandType": "boolean", "operator": "==" },
                                        true,
                                        true
                                    ],
                                    "then": [
                                        {
                                            "type": "condition",
                                            "conditions": [
                                                { "operandType": "boolean", "operator": "==" },
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
            "if_else((True == True), [\n\
                \tif_else((True == True), [\n\
    		        \t\tif_else((True == True), [\n\
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

    #[test]
    fn parse_nested_conditions_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(&CategoriesToVariables::new(HashMap::new()))
                .build_actions_content(&parse_actions(
                    json!([
                         {
                            "type": "condition",
                            "conditions": [
                                { "operandType": "and", "operator": "AND" },
                                [
                                    { "operandType": "boolean", "operator": "==" },
                                    { "function": "getNumberOfUnitsOfUnitType", "unitType": "oTDQ3jlcMa" },
                                    5
                                ],
                                [
                                    { "operandType": "boolean", "operator": "==" },
                                    true,
                                    true
                                ]
                            ],
                            "then": [],
                            "else": []
                         }
                    ])
                    .as_array()
                    .unwrap(),
                ))
                .as_str(),
            "if_else(((NumberOfUnitsOfUnitType('oTDQ3jlcMa') == 5) & (True == True)), [\n\
                \t\n\
            ], [\n\
                \t\n\
            ]),\n"
        );
    }
}
