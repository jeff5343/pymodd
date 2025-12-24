use std::ops::Add;

use heck::{ToSnakeCase, ToUpperCamelCase};
use serde_json::Value;

use crate::game_data::{
    actions::Action,
    directory::{Directory, Script},
    variable_categories::CategoriesToVariables,
    GameData,
};

use super::{
    game_variables_file::pymodd_class_name_of_category,
    utils::{
        iterators::{
            argument_values_iterator::{ArgumentValueIterItem, ArgumentValuesIterator, Operation},
            directory_iterator::DirectoryIterItem,
        },
        surround_string_with_quotes, TAB_SIZE,
    },
};

pub struct ScriptsFile {}

impl ScriptsFile {
    pub fn build_content(game_data: &GameData) -> String {
        format!(
            "from pymodd.actions import *\n\
            from pymodd.functions import *\n\
            from pymodd.script import Trigger, UiTarget, Flip, script\n\n\
            from game_variables import *\n\n\n\
            {}\n\n",
            &build_directory_content(
                &game_data.root_directory,
                &ScriptsContentBuilder::new(
                    &game_data.categories_to_variables,
                    &game_data.root_directory,
                ),
            )
        )
        .replace("\t", &" ".repeat(TAB_SIZE))
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
    root_directory: &'a Directory,
}

impl<'a> ScriptsContentBuilder<'a> {
    pub fn new(
        categories_to_variables: &'a CategoriesToVariables,
        root_directory: &'a Directory,
    ) -> ScriptsContentBuilder<'a> {
        ScriptsContentBuilder {
            categories_to_variables,
            root_directory,
        }
    }

    pub fn build_script_content(&self, script: &Script) -> String {
        let function_name = &script.function_name;
        format!(
            "@script(triggers=[{}]{})\n\
            def {function_name}():\n\
                {}",
            script.triggers_into_pymodd_enums().join(", "),
            if script.name.is_ascii() {
                String::new()
            } else {
                format!(", name={}", surround_string_with_quotes(&script.name))
            },
            if script.actions.len() > 0 {
                let content = self
                    .build_actions_content(&script.actions)
                    .lines()
                    .map(|action| format!("{}{action}\n", "\t"))
                    .collect::<String>();
                // generate pass statements for functions with commented bodies
                if self.is_body_commented_out(&format!("def func:\n{content}")) {
                    content.to_string().add("\tpass\n")
                } else {
                    content
                }
            } else {
                String::from("\tpass\n")
            }
        )
    }

    fn build_actions_content(&self, actions: &Vec<Action>) -> String {
        actions
            .iter()
            .map(|action| self.build_action_content(&action))
            .collect::<String>()
    }

    fn build_action_content(&self, action: &Action) -> String {
        // for use while converting arguments of special actions
        let (none, pass) = (String::from("None"), String::from("\t\tpass\n"));

        // convert actions into python statements
        let statement_content = match action.name.as_str() {
            // convert condition actions into if statements
            "condition" => {
                let args = self.build_arguments_of_action_individually(action);
                let (condition, then_actions, else_actions) = (
                    args.get(0).unwrap_or(&none),
                    args.get(1).unwrap_or(&pass),
                    args.get(2).unwrap_or(&pass),
                );
                Some(format!(
                    "if {condition}:{}{}",
                    then_actions.strip_suffix("\n").unwrap(),
                    if else_actions != "\n\tpass\n" {
                        format!("\nelse:{else_actions}")
                    } else {
                        String::from("\n")
                    }
                ))
            }

            // convert variable for loop actions into for loops
            "for" => {
                let args = self.build_arguments_of_action_individually(action);
                let (start, stop, variable, actions) = (
                    args.get(0).unwrap_or(&none),
                    args.get(1).unwrap_or(&none),
                    args.get(2).unwrap_or(&none),
                    args.get(3).unwrap_or(&pass),
                );
                Some(format!(
                    "for {variable} in range({start}, {stop}):{actions}"
                ))
            }

            // convert for each type in function/variable actions into for loops
            "forAllEntities" | "forAllProjectiles" | "forAllItems" | "forAllUnits"
            | "forAllPlayers" | "forAllItemTypes" | "forAllUnitTypes" | "forAllRegions"
            | "forAllDebris" => {
                let args = self.build_arguments_of_action_individually(action);
                let (group, actions) = (args.get(0).unwrap_or(&none), args.get(1).unwrap_or(&pass));
                let group_type = match action
                    .name
                    .strip_prefix("forAll")
                    .unwrap()
                    .to_snake_case()
                    .strip_suffix("s")
                    .unwrap()
                {
                    "entitie" => "entity",
                    "debri" => "debris",
                    group_type => group_type,
                }
                .to_string();
                // use the variable provided by the for loop instead of functions
                let actions = actions.replace(
                    &format!("Selected{}()", group_type.to_upper_camel_case()),
                    &group_type,
                );
                Some(format!("for {group_type} in {group}:{actions}"))
            }

            // convert repeat actions into for loops
            "repeat" => {
                let args = self.build_arguments_of_action_individually(action);
                let (count, actions) = (args.get(0).unwrap_or(&none), args.get(1).expect(&pass));
                Some(format!("for _ in repeat({count}):{actions}"))
            }

            // convert while actions into while loops
            "while" => {
                let args = self.build_arguments_of_action_individually(action);
                let (condition, actions) =
                    (args.get(0).unwrap_or(&none), args.get(1).unwrap_or(&pass));
                Some(format!("while {condition}:{actions}"))
            }

            // convert set timeout actions into with loops
            "setTimeOut" => {
                let args = self.build_arguments_of_action_individually(action);
                let (duration, actions) =
                    (args.get(0).unwrap_or(&none), args.get(1).unwrap_or(&pass));
                Some(format!("with after_timeout({duration}):{actions}"))
            }

            _ => None,
        };
        if let Some(statement_content) = statement_content {
            return match action.disabled {
                true => self.comment_out_statement_content(statement_content),
                false => {
                    self.append_pass_keyword_to_commented_bodies_of_statement(statement_content)
                }
            };
        }

        match action.name.as_str() {
            // convert break, continue, and return actions into python keywords
            "break" | "continue" | "return" => {
                format!(
                    "{}{}\n",
                    if action.disabled { "# " } else { "" },
                    &action.name
                )
            }

            "comment" => {
                format!(
                    "{}({}{})\n",
                    action.pymodd_class_name(),
                    // set argument manually for comments
                    surround_string_with_quotes(
                        action.comment.as_ref().unwrap_or(&String::from("None"))
                    ),
                    self.build_optional_arguments_contents(&action)
                        .into_iter()
                        .skip(1) // skip over optional comment argument
                        .map(|arg| String::from(", ") + &arg)
                        .collect::<String>(),
                )
            }

            _ => format!(
                "{}({}{})\n",
                action.pymodd_class_name(),
                self.build_arguments_content(action.iter_flattened_argument_values()),
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
            ),
        }
    }

    fn comment_out_statement_content(&self, statement_content: String) -> String {
        statement_content
            .lines()
            .map(|line| {
                if line.trim().starts_with("# ") {
                    format!("# \t{}", line.trim().strip_prefix("# ").unwrap())
                } else {
                    format!("# {line}")
                }
                .add("\n")
            })
            .collect()
    }

    fn append_pass_keyword_to_commented_bodies_of_statement(
        &self,
        statement_content: String,
    ) -> String {
        let bodies: Vec<&str> = statement_content.trim().split("\nelse:").collect();
        let (mut then_body, mut else_body) = (
            bodies.get(0).unwrap_or(&"").to_string(),
            format!("else:{}", bodies.get(1).unwrap_or(&"").to_string()),
        );
        if self.is_body_commented_out(&then_body) {
            then_body = then_body.add("\n\tpass")
        }
        if self.is_body_commented_out(&else_body) {
            else_body = else_body.add("\n\tpass")
        }
        format!(
            "{then_body}{}\n",
            // add else body if it is not empty
            if else_body != String::from("else:") {
                format!("\n{else_body}")
            } else {
                String::new()
            }
        )
    }

    fn is_body_commented_out(&self, body_content: &String) -> bool {
        let body_lines = body_content.lines();
        if body_lines.collect::<Vec<&str>>().len() == 1 {
            return false;
        }
        !body_content
            .lines()
            .skip(1)
            .any(|line| line.starts_with("\t") & !line.starts_with("\t# "))
    }

    /// used while parsing if statements, for loops, and while loops
    fn build_arguments_of_action_individually(&self, action: &Action) -> Vec<String> {
        action
            .args
            .iter()
            .map(|arg| {
                self.build_arguments_content(ArgumentValuesIterator::new(&vec![arg.clone()]))
            })
            .collect::<Vec<String>>()
    }

    fn build_arguments_content(&self, args_iter: ArgumentValuesIterator) -> String {
        args_iter
            .fold(String::from("("), |pymodd_args, arg| {
                let include_seperator =
                    !pymodd_args.ends_with("(") && arg != ArgumentValueIterItem::FunctionEnd;
                pymodd_args
                    .add(if include_seperator { ", " } else { "" })
                    .add(&{
                        // remove parentheses surrounding the outermost layer of conditions
                        if let ArgumentValueIterItem::Condition(_) = arg {
                            let condition_content = self.build_argument_content(arg);
                            if condition_content.starts_with("(")
                                && condition_content.ends_with(")")
                            {
                                condition_content
                                    .strip_prefix("(")
                                    .unwrap()
                                    .strip_suffix(")")
                                    .unwrap()
                                    .to_string()
                            } else {
                                condition_content
                            }
                        } else {
                            self.build_argument_content(arg)
                        }
                    })
            })
            .strip_prefix("(")
            .unwrap()
            .to_string()
    }

    pub(crate) fn build_argument_content(&self, arg: ArgumentValueIterItem) -> String {
        match arg {
            ArgumentValueIterItem::StartOfFunction(function) => {
                format!("{}(", function.pymodd_class_name())
            }
            ArgumentValueIterItem::Actions(actions) => {
                format!(
                    "\n{}",
                    if actions.len() > 0 {
                        self.build_actions_content(actions)
                            .lines()
                            .map(|line| format!("\t{line}\n"))
                            .collect::<String>()
                    } else {
                        String::from("\tpass\n")
                    }
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
                            variable.enum_name()
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
            ArgumentValueIterItem::ScriptKey(key) => {
                let item_with_key = self.root_directory.find_item_with_key(&key);
                if item_with_key.is_some() {
                    if let DirectoryIterItem::Script(script) = item_with_key.unwrap() {
                        // run_script action accepts Script objects, not keys
                        return format!("{}()", script.function_name);
                    }
                }
                String::from("None")
            }
            ArgumentValueIterItem::None => String::from("None"),
            ArgumentValueIterItem::FunctionEnd => String::from(")"),
        }
    }

    fn build_operation_content(&self, operator: &Operation) -> String {
        let (item_a, operator, item_b) = (
            ArgumentValueIterItem::from_argument(&operator.item_a),
            ArgumentValueIterItem::from_argument(&operator.operator),
            ArgumentValueIterItem::from_argument(&operator.item_b),
        );

        let operator = if let ArgumentValueIterItem::Value(operator_val) = operator {
            into_operator(operator_val.as_str().unwrap_or("")).unwrap_or("")
        } else {
            ""
        };

        let content = format!(
            "{} {} {}",
            self.build_operation_item_content(item_a),
            operator,
            self.build_operation_item_content(item_b)
        );
        // surround `and` and `or` conditions with parentheses
        if ["and", "or"].contains(&operator) {
            format!("({content})")
        } else {
            content
        }
    }

    fn build_operation_item_content(&self, operation_item: ArgumentValueIterItem) -> String {
        match operation_item {
            // surround calculations with parentheses
            ArgumentValueIterItem::Calculation(_) => {
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
    if [
        "==", "!=", "<=", "<", ">", ">=", "+", "-", "/", "*", "%", "**",
    ]
    .contains(&string)
    {
        return Some(string);
    }
    match string.to_lowercase().as_str() {
        "and" => Some("and"),
        "or" => Some("or"),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use serde_json::json;

    use crate::game_data::{
        actions::{parse_actions, Action},
        directory::{Directory, DirectoryItem, Script},
        variable_categories::{CategoriesToVariables, Variable},
    };

    use super::ScriptsContentBuilder;

    #[test]
    fn script_content() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_script_content(&Script::qnew(
                "initialize",
                "WI31HDK",
                vec!["gameStart"],
                Vec::new()
            )),
            String::from(format!(
                "@script(triggers=[Trigger.GAME_START])\n\
                def initialize():\n\
                    \tpass\n",
            ))
        );
    }

    #[test]
    fn script_with_non_ascii_name_content() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_script_content(&Script::qnew(
                "【 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚎 イ】",
                "WI31HDK",
                vec!["gameStart"],
                Vec::new()
            )),
            String::from(format!(
                "@script(triggers=[Trigger.GAME_START], name='【 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚎 イ】')\n\
                def wi31hdk():\n\
                    \tpass\n",
            ))
        );
    }

    #[test]
    fn script_with_no_name() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_script_content(&Script::qnew("", "WI31HDK", vec![], Vec::new())),
            String::from(format!(
                "@script(triggers=[])\n\
                def wi31hdk():\n\
                    \tpass\n",
            ))
        );
    }

    #[test]
    fn script_content_with_commented_body() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_script_content(&Script::qnew(
                "initialize",
                "WI31HDK",
                vec!["gameStart"],
                vec![Action::new("break", vec![], None, false, true)]
            )),
            String::from(format!(
                "@script(triggers=[Trigger.GAME_START])\n\
                def initialize():\n\
                    \t# break\n\
                    \tpass\n",
            ))
        );
    }

    #[test]
    fn parse_action_with_variable_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::from([(
                    "shops",
                    vec![Variable::new("OJbEQyc7is", "weapons", json!({}))]
                )])),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    {
                        "type": "openShopForPlayer",
                            "player": {
                                "function": "getOwner",
                                "entity": { "function": "getLastCastingUnit", "vars": [] },
                                "vars": []
                            },
                        "shop": "OJbEQyc7is",
                        "vars": []
                    }
                ])
                .as_array()
                .unwrap()
            )),
            "open_shop_for_player(Shop.WEAPONS, OwnerOfEntity(LastCastingUnit()))\n"
        )
    }

    #[test]
    fn parse_action_with_optional_arguments_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    {
                        "type": "startUsingItem",
                        "entity": { "function": "getTriggeringItem" },
                        "comment": "hi!",
                        "runOnClient": true,
                        "disabled": true,
                    }
                ])
                .as_array()
                .unwrap()
            )),
            "use_item_continuously_until_stopped(LastTriggeringItem(), comment='hi!', disabled=True, run_on_client=True)\n"
        )
    }

    #[test]
    fn parse_action_with_only_optional_arguments_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    { "type": "stopMusic", "comment": "hi!", "runOnClient": true, "disabled": false, }
                ])
                .as_array()
                .unwrap()
            )),
            "stop_music_for_everyone(comment='hi!', run_on_client=True)\n"
        )
    }

    #[test]
    fn parse_action_with_constant_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    { "type": "updateUiTextForEveryone", "target": "top", "value": "Hello!" }
                ])
                .as_array()
                .unwrap()
            )),
            "update_ui_text_for_everyone(UiTarget.TOP, 'Hello!')\n"
        )
    }

    #[test]
    fn parse_action_with_null_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    { "type": "updateUiTextForEveryone", "target": "top", "value": null }
                ])
                .as_array()
                .unwrap()
            )),
            "update_ui_text_for_everyone(UiTarget.TOP, None)\n"
        )
    }

    #[test]
    fn parse_action_with_undefined_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([{
                  "type": "updateUiTextForTimeForPlayer",
                  "player": { "function": "undefinedValue", "vars": [] },
                  "target": "center-lg",
                  "time": 5000,
                  "value": "BOSS SPAWNED",
                  "vars": []
                }])
                .as_array()
                .unwrap()
            )),
            "update_ui_target_for_player_for_miliseconds(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000)\n"
        )
    }

    #[test]
    fn parse_comment_action_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    { "type": "comment", "comment": "hey there", }
                ])
                .as_array()
                .unwrap()
            )),
            "comment('hey there')\n"
        );
    }

    #[test]
    fn parse_keyword_actions_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([ { "type": "break" }, { "type": "continue" }, { "type": "return" } ])
                    .as_array()
                    .unwrap()
            )),
            "break\n\
            continue\n\
            return\n"
        );
    }

    #[test]
    fn parse_disabled_keyword_actions_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                &json!([
                    { "type": "break", "disabled": true },
                    { "type": "continue", "disabled": true },
                    { "type": "return", "disabled": true }
                ])
                .as_array()
                .unwrap()
            )),
            "# break\n\
            # continue\n\
            # return\n"
        );
    }

    #[test]
    fn parse_nested_calculations_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
                .build_actions_content(&parse_actions(
                    &json!([
                        {
                            "type": "increaseVariableByNumber",
                            "variable": null,
                            "number": {
                                "function": "calculate", 
                                "items": [
                                    { "operator": "%" }, 10, { "function": "calculate", "items": [
                                            { "operator": "+" }, 5, { "function": "calculate", "items": [
                                                    { "operator": "-" }, 3, { "function": "calculate", "items": [ 
                                                            { "operator": "*" }, 3, { "function": "calculate", "items": [ 
                                                                    { "operator": "/" }, 2,
                                                                    { "function": "getExponent", "base": 5, "power": 2 }
                                                            ] }
                                                        ] }
                                                ] }
                                        ] }
                                ]
                            }
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "increase_variable_by_number(None, 10 % (5 + (3 - (3 * (2 / (5 ** 2))))))\n"
        );
    }

    #[test]
    fn parse_nested_concatenations_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
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
                                        "player": { "function": "getTriggeringPlayer" }
                                    },
                                    "textB": " player!"
                                }
                            }
                        }
                    ])
                    .as_array()
                    .unwrap()
                )),
            "send_chat_message_to_everyone('hi ' + IdOfPlayer(LastTriggeringPlayer()) + ' player!')\n"
        );
    }

    #[test]
    fn parse_nested_if_statements_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                     {
                        "type": "condition",
                        "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                        "then": [
                            {
                                "type": "condition",
                                "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                                "then": [
                                    {
                                        "type": "condition",
                                        "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                                        "then": [ { "type": "sendChatMessage", "message": "hi" } ],
                                        "else": [ { "type": "sendChatMessage", "message": "hi" } ]
                                    }
                                ],
                                "else": [ { "type": "sendChatMessage", "message": "hi" } ]
                            }
                        ],
                        "else": [ { "type": "sendChatMessage", "message": "hi" } ]
                     }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "if True == True:\n\
                \tif True == True:\n\
    		        \t\tif True == True:\n\
		                \t\t\tsend_chat_message_to_everyone('hi')\n\
                    \t\telse:\n\
		                \t\t\tsend_chat_message_to_everyone('hi')\n\
                \telse:\n\
		            \t\tsend_chat_message_to_everyone('hi')\n\
            else:\n\
                \tsend_chat_message_to_everyone('hi')\n"
        )
    }

    #[test]
    fn parse_nested_conditions_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    {
                        "type": "condition",
                        "conditions": [
                              { "operandType": "and", "operator": "AND" },
                              [ { "operandType": "boolean", "operator": "==" }, true, true ],
                              [
                                   { "operandType": "or", "operator": "OR" },
                                   [ { "operandType": "boolean", "operator": "==" }, true, true ],
                                   [ { "operandType": "boolean", "operator": "==" }, true, true ]
                              ]
                         ],
                         "then": [],
                         "else": []
                }])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "if True == True and (True == True or True == True):\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_variable_for_loop_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::from([(
                    "variables",
                    vec![Variable::new("i", "i", json!({"dataType": "number"}))]
                )])),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    { "type": "for", "variableName": "i", "start": 0, "stop": 5, "actions": [] }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "for Variable.I in range(0, 5):\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_for_each_type_in_function_action_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    { "type": "forAllEntities", "entityGroup": { "function": "allEntities" }, "actions": [
                        { "type": "destroyEntity", "entity": { "function": "getSelectedEntity" } }
                    ] }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "for entity in AllEntitiesInTheGame():\n\
                \tdestroy_entity(entity)\n"
        );
    }

    #[test]
    fn parse_for_each_type_in_variable_action_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::from([(
                    "itemTypeGroups",
                    vec![Variable::new("specialItemTypes", "specialItemTypes", json![{}])]
                )])),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    {
                        "type": "forAllItemTypes",
                        "itemTypeGroup": { "function": "getVariable", "variableName": "specialItemTypes" },
                        "actions": []
                     }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "for item_type in ItemTypeGroup.SPECIAL_ITEM_TYPES:\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_for_each_type_in_multi_arg_function_action_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    {
                        "type": "forAllUnits",
                        "unitGroup": { "function": "allUnitsInRegion", "region": {
                                "function": "dynamicRegion",
                                "x": 0, "y": 0, "width": 5, "height": 5 }
                        },
                        "actions": []
                    }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "for unit in AllUnitsInRegion(DynamicRegion(0, 0, 5, 5)):\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_repeat_action_into_python() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    { "type": "repeat", "count": 5, "actions": [] }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "for _ in repeat(5):\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_while_action_into_python() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    {
                        "type": "while",
                        "conditions": [
                            { "operandType": "boolean", "operator": "==" },
                            { "function": "entityExists", "entity": { "function": "getTriggeringUnit" } },
                            true
                        ],
                        "actions": []
                    }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "while EntityExists(LastTriggeringUnit()) == True:\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_set_timeout_action_into_python() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    { "type": "setTimeOut", "duration": 1000, "actions": [ { "type": "stopMusic" } ] } 
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "with after_timeout(1000):\n\
                \tstop_music_for_everyone()\n"
        );
    }

    #[test]
    fn parse_disabled_while_action_into_python() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    {
                        "type": "while", "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ], "actions": [],
                        "disabled": true
                    }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "# while True == True:\n\
                # \tpass\n"
        );
    }

    #[test]
    fn parse_while_action_with_disabled_actions_into_python() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                    {
                        "type": "while", 
                        "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ], 
                        "actions": [
                            {
                                "type": "while", "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ], "actions": [],
                                "disabled": true
                            }
                        ],
                    }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "while True == True:\n\
                \t# while True == True:\n\
                \t# \tpass\n\
                \tpass\n"
        );
    }

    #[test]
    fn parse_nested_disabled_if_statements_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            )
            .build_actions_content(&parse_actions(
                json!([
                     {
                        "type": "condition", "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                        "then": [ {
                                "type": "condition", "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                                "then": [ {
                                        "type": "condition", "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                                        "then": [ { "type": "sendChatMessage", "message": "hi" } ],
                                        "else": [ { "type": "sendChatMessage", "message": "hi" } ],
                                        "disabled": true
                                    } ],
                                "else": [ { "type": "sendChatMessage", "message": "hi" } ],
                                "disabled": true
                            } ],
                        "else": [ {
                                "type": "condition", "conditions": [ { "operandType": "boolean", "operator": "==" }, true, true ],
                                "then": [ { "type": "sendChatMessage", "message": "hi" } ],
                                "else": [ { "type": "sendChatMessage", "message": "hi" } ],
                                "disabled": true
                            } ]
                     }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "if True == True:\n\
                \t# if True == True:\n\
    		        \t# \tif True == True:\n\
		                \t# \t\tsend_chat_message_to_everyone('hi')\n\
                    \t# \telse:\n\
		                \t# \t\tsend_chat_message_to_everyone('hi')\n\
                \t# else:\n\
		            \t# \tsend_chat_message_to_everyone('hi')\n\
                \tpass\n\
            else:\n\
                \t# if True == True:\n\
                    \t# \tsend_chat_message_to_everyone('hi')\n\
                \t# else:\n\
                    \t# \tsend_chat_message_to_everyone('hi')\n\
                \tpass\n"
        )
    }

    #[test]
    fn parse_run_script_action_into_pymodd() {
        assert_eq!(
            ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new(
                    "root",
                    "null",
                    vec![DirectoryItem::Directory(Directory::new(
                        "utils",
                        "n3DhW3",
                        vec![DirectoryItem::Script(Script::qnew(
                            "spawn boss",
                            "If2aW3B",
                            Vec::new(),
                            Vec::new()
                        ))]
                    ))]
                )
            )
            .build_actions_content(&parse_actions(
                json!([
                     { "type": "runScript", "scriptName": "If2aW3B" }
                ])
                .as_array()
                .unwrap(),
            ))
            .as_str(),
            "run_script(spawn_boss())\n"
        )
    }
}
