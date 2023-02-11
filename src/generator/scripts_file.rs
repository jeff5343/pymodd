use std::ops::Add;

use crate::game_data::{actions::Action, directory::Script, GameData};

use super::utils::iterators::directory_iterator::DirectoryIterItem;

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
            .into_iter()
            .map(|action| format!("{}{action}\n", "\t".repeat(3)))
            .collect::<String>(),
    )
}

fn build_actions(actions: &Vec<Action>) -> Vec<String> {
    let elements = Vec::new();

    // work on this

    elements
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
    fn actions_content() {
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
            )),
            vec!["OpenShopForPlayer(GetOwnerOf(GetLastCastingUnit()), 'OjbEQyc7is)"]
        )
    }
}
