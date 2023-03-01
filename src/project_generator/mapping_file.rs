use std::ops::Add;

use heck::ToPascalCase;

use crate::game_data::{directory::Directory, entity_types::CategoriesToEntityTypes, GameData};

use super::{
    utils::{iterators::directory_iterator::DirectoryIterItem, surround_string_with_quotes},
    STORED_GAME_JSON_FILE_PATH,
};

pub struct MappingFile {}

impl MappingFile {
    pub fn build_content(game_data: &GameData) -> String {
        let game_class_name = game_data.name.to_pascal_case().to_string();
        let mut content = format!(
            "from pymodd.script import Game, Folder, write_game_to_output, write_to_output\n\n\
            from scripts import *\n\
            from entity_scripts import * \n\n\n\
            class {game_class_name}(Game):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_scripts = [{}]\n\
                    \t\tself.scripts = [\n",
            retrieve_clases_of_entity_scripts(&game_data.categories_to_entity_types).join(", ")
        );
        content.push_str(
            &build_directory_items_contents(&game_data.root_directory)
                .into_iter()
                .map(|element| format!("{}{element}\n", "\t".repeat(3)))
                .collect::<String>()
                .as_str(),
        );
        let project_directory = game_data.pymodd_project_name();
        content.add(
            &format!(
                "\t\t\t\n\
                \t\t]\n\n\
                # run `python {project_directory}/mapping.py` to generate this game's files\n\
                write_game_to_output({game_class_name}('{project_directory}/{STORED_GAME_JSON_FILE_PATH}'))\n\
                # uncomment the following to quickly generate the json file for a script\n\
                # write_to_output('output/', SCRIPT_OBJECT())"
            )
            .as_str(),
        )
    }
}

fn retrieve_clases_of_entity_scripts(
    entity_type_categories: &CategoriesToEntityTypes,
) -> Vec<String> {
    entity_type_categories
        .iter()
        .flat_map(|(_category, entity_types)| entity_types)
        .filter(|entity_type| !entity_type.directory.is_empty())
        .map(|entity_type| entity_type.pymodd_class_name().add("()"))
        .collect()
}

pub fn build_directory_items_contents(directory: &Directory) -> Vec<String> {
    let mut elements = Vec::new();
    let mut curr_depth = 0;
    directory.iter_flattened().for_each(|game_item| {
        elements.push(match game_item {
            DirectoryIterItem::StartOfDirectory(directory) => {
                curr_depth += 1;
                format!(
                    "{}Folder({}, [",
                    "\t".repeat(curr_depth - 1),
                    surround_string_with_quotes(&directory.name)
                )
            }
            DirectoryIterItem::Script(script) => {
                format!(
                    "{}{}(),",
                    "\t".repeat(curr_depth),
                    script.pymodd_class_name()
                )
            }
            DirectoryIterItem::DirectoryEnd => {
                curr_depth -= 1;
                format!("{}]),", "\t".repeat(curr_depth))
            }
        })
    });
    elements
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use crate::{
        game_data::{directory::Directory, GameData},
        project_generator::mapping_file::build_directory_items_contents,
    };

    use super::MappingFile;

    #[test]
    fn directory_content() {
        assert_eq!(
            build_directory_items_contents(&Directory::parse(&json!({
                "WI31HDK": { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": None::<&str>, "order": 1},
                "31IAD2B": { "folderName": "utils", "key": "31IAD2B", "parent": None::<&str>, "order": 2 },
                "SDUW31W": { "name": "change_state", "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 },
                "Q31E2RS": { "name": "check_players", "key": None::<&str>, "actions": [], "parent": "31IAD2B", "order": 2 },
                "HWI31WQ": { "folderName": "other", "key": "HWI31WQ", "parent": "31IAD2B", "order": 3 },
                "JK32Q03": { "name": "destroy_server", "key": "JK32Q03", "actions": [], "parent": "HWI31WQ", "order": 1},
            }))).into_iter().collect::<String>(),
            "Initialize(),\
            Folder('utils', [\
                \tChangeState(),\
                \tCheckPlayers(),\
                \tFolder('other', [\
                    \t\tDestroyServer(),\
                \t]),\
            ]),"
        );
    }

    #[test]
    fn simple_mapping_file_content() {
        assert_eq!(MappingFile::build_content(&GameData::parse(r#"{
            "title": "test_game",
            "data": {
                "scripts": {
                    "WI31HDK": { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": null, "order": 1},
                    "31IAD2B": { "folderName": "utils", "key": "31IAD2B", "parent": null, "order": 2 },
                    "SDUW31W": { "name": "change_state", "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 }
                },
                "unitTypes": {
                    "RW31QW2": { "name": "bob", "scripts": {
                        "DF31W32": { "name": "initialize", "key": "DF31W32", "actions": [], "parent": null, "order": 1 }
                    }},
                    "IO53IWD": { "name": "empty" }
                }
            }
        }"#.to_string()).unwrap()), 
        "from pymodd.script import Game, Folder, write_game_to_output, write_to_output\n\n\
        from scripts import *\n\
        from entity_scripts import * \n\n\n\
        class TestGame(Game):\n\
            \tdef _build(self):\n\
                \t\tself.entity_scripts = [Bob()]\n\
                \t\tself.scripts = [\n\
                    \t\t\tInitialize(),\n\
                    \t\t\tFolder('utils', [\n\
                        \t\t\t\tChangeState(),\n\
                    \t\t\t]),\n\
                    \t\t\t\n\
                \t\t]\n\n\
        # run `python test_game/mapping.py` to generate this game's files\n\
        write_game_to_output(TestGame('test_game/utils/game.json'))\n\
        # uncomment the following to quickly generate the json file for a script\n\
        # write_to_output('output/', SCRIPT_OBJECT())");
    }
}
