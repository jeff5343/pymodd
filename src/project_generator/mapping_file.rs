use std::ops::Add;

use heck::ToPascalCase;

use crate::game_data::{directory::Directory, entity_types::CategoriesToEntityTypes, GameData};

use super::utils::{
    iterators::directory_iterator::DirectoryIterItem, surround_string_with_quotes, TAB_SIZE,
};

pub struct MappingFile {}

impl MappingFile {
    pub fn build_content(game_data: &GameData) -> String {
        let game_class_name = game_data.name.to_pascal_case().to_string();
        let mut content = format!(
            "from pymodd.game import Game\n\
            from pymodd.core.folder import Folder\n\n\
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
        content.add(
            &format!(
                "\t\t\t\n\
                \t\t]\n\n\n\
                # run `pymodd compile` within this project directory to generate this game's json files\n\
                # example:\n\
                \"\"\"\n\
                $ cd {}\n\
                $ pymodd compile\n\
                \"\"\"\n",
                game_data.pymodd_project_name()
            )
            .as_str(),
        ).replace("\t", &" ".repeat(TAB_SIZE))
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
                format!("{}{}(),", "\t".repeat(curr_depth), script.function_name)
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
        game_data::directory::Directory,
        project_generator::mapping_file::build_directory_items_contents,
    };

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
            "initialize(),\
            Folder('utils', [\
                \tchange_state(),\
                \tcheck_players(),\
                \tFolder('other', [\
                    \t\tdestroy_server(),\
                \t]),\
            ]),"
        );
    }
}
