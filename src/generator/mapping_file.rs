use std::ops::Add;

use heck::ToPascalCase;

use crate::game_data::{
    directory::{Directory, GameItem},
    entity_types::CategoryToEntityTypes,
    GameData,
};

use super::utils::surround_string_with_quotes;

pub struct MappingFile {}

impl MappingFile {
    pub fn build_content(game_data: &GameData) -> String {
        let game_class_name = game_data.name.to_pascal_case().to_string();
        let content = format!(
            "from pymodd.script import Game, Folder, write_game_to_output, write_to_output\n\n\
            from scripts import *\n\
            from entity_scripts import * \n\n\
            class {game_class_name}(Game):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_scripts = [{}]\n\
                    \t\tself.scripts = [",
            retrieve_clases_of_entity_scripts(&game_data.entity_type_categories).join(", ")
        );
        content.add("work on adding rest of the file")
    }
}

fn retrieve_clases_of_entity_scripts(
    entity_type_categories: &CategoryToEntityTypes,
) -> Vec<String> {
    entity_type_categories
        .iter()
        .flat_map(|(_category, entity_types)| entity_types)
        .filter(|entity_type| !entity_type.directory.is_empty())
        .map(|entity_type| entity_type.class_name().add("()"))
        .collect()
}

fn build_directory_content(directory: &Directory) -> String {
    let mut content = String::new();
    let mut curr_depth = 0;
    directory
        .into_iter()
        .for_each(|item| println!("{:?}\n", item));
    directory.into_iter().for_each(|game_item| {
        content.push_str(
            match game_item {
                GameItem::Dir(directory) => {
                    curr_depth += 1;
                    format!(
                        "{}Folder({}, [",
                        "\t".repeat(curr_depth - 1),
                        surround_string_with_quotes(&directory.name)
                    )
                }
                GameItem::Script(script) => {
                    format!("{}{}(),", "\t".repeat(curr_depth), script.class_name())
                }
                GameItem::DirectoryEnd => {
                    curr_depth -= 1;
                    format!("{}]),", "\t".repeat(curr_depth))
                }
            }
            .add("\n")
            .as_str(),
        )
    });
    content
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use crate::{
        game_data::directory::Directory, generator::mapping_file::build_directory_content,
    };

    #[test]
    fn directory_content() {
        assert_eq!(
            build_directory_content(&Directory::parse(&json!({
                "WI31HDK": { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": None::<&str>, "order": 1},
                "31IAD2B": { "folderName": "utils", "key": "31IAD2B", "parent": None::<&str>, "order": 2 },
                "SDUW31W": { "name": "change_state", "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 },
                "Q31E2RS": { "name": "check_players", "key": None::<&str>, "actions": [], "parent": "31IAD2B", "order": 2 },
                "HWI31WQ": { "folderName": "other", "key": "HWI31WQ", "parent": "31IAD2B", "order": 3 },
                "JK32Q03": { "name": "destroy_server", "key": "JK32Q03", "actions": [], "parent": "HWI31WQ", "order": 1},
            }))),
            String::from(
                "Initialize(),\n\
                Folder('utils', [\n\
                    \tChangeState(),\n\
                    \tCheckPlayers(),\n\
                    \tFolder('other', [\n\
                        \t\tDestroyServer(),\n\
                    \t]),\n\
                ]),\n"
            )
        );
    }
}
