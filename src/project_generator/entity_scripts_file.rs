use crate::game_data::{
    entity_types::EntityType, variable_categories::pymodd_class_name_of_category, GameData,
};

use super::{
    mapping_file::build_directory_items_contents,
    scripts_file::{build_directory_content, ScriptsContentBuilder},
    utils::enum_name_of,
};

pub struct EntityScriptsFile {}

impl EntityScriptsFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut content = format!(
            "from pymodd.actions import *\n\
            from pymodd.functions import *\n\
            from pymodd.script import EntityScripts, Folder, Script, Trigger, UiTarget, Flip\n\n\
            from game_variables import *\n\n\n"
        );
        let scripts_class_content_builder =
            ScriptsContentBuilder::new(&game_data.categories_to_variables);

        game_data
            .categories_to_entity_types
            .iter()
            .for_each(|(category, entity_types)| {
                entity_types
                    .iter()
                    .filter(|entity_type| !entity_type.directory.is_empty())
                    .for_each(|entity_type| {
                        content.push_str(&format!(
                            "{}\n{}\n\n",
                            build_class_content_of_entity_type_in_category(&entity_type, category),
                            build_directory_content(
                                &entity_type.directory,
                                &scripts_class_content_builder
                            )
                            .lines()
                            .map(|line| { format!("\t{line}\n") })
                            .collect::<String>()
                            // remove one line in between the scripts of the entity_type
                            .replace("\t\n\t\n", "\n")
                        ));
                    });
            });
        content
    }
}

fn build_class_content_of_entity_type_in_category(
    entity_type: &EntityType,
    category: &'static str,
) -> String {
    let (entity_type_class_name, category_class_name) = (
        entity_type.pymodd_class_name(),
        pymodd_class_name_of_category(category),
    );
    format!(
        "class {entity_type_class_name}(EntityScripts):\n\
            \tdef _build(self):\n\
                \t\tself.entity_type = {category_class_name}.{}\n\
                \t\tself.scripts = [\n\
                {}\
                \t\t\t\n\
                \t\t]\n",
        enum_name_of(&entity_type.name),
        build_directory_elements_for_entity_type(&entity_type)
            .into_iter()
            .map(|element| format!("{}{element}\n", "\t".repeat(3)))
            .collect::<String>()
    )
}

fn build_directory_elements_for_entity_type(entity_type: &EntityType) -> Vec<String> {
    build_directory_items_contents(&entity_type.directory)
        .into_iter()
        .map(|mut element| {
            if !element.trim_start().starts_with("Folder") && !element.trim_start().starts_with("]")
            {
                element.insert_str(element.find(char::is_alphabetic).unwrap_or(0), "self.")
            }
            element
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use crate::{
        game_data::{directory::Directory, entity_types::EntityType},
        project_generator::entity_scripts_file::build_class_content_of_entity_type_in_category,
    };

    #[test]
    fn simple_entity_scripts_class_content() {
        assert_eq!(
            build_class_content_of_entity_type_in_category(
                &EntityType {
                    name: "bob".to_string(),
                    directory: Directory::parse(&json!({
                        "DF31W32": { "name": "initialize", "key": "DF31W32", "actions": [{
                            "type": null
                        }], "parent": null, "order": 1 },
                        "31IAD2B": { "triggers": [], "folderName": "utils",
                            "key": "31IAD2B", "parent": null, "order": 2 },
                        "SDUW31W": { "triggers": [], "name": "change_state",
                            "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 }
                    }))
                },
                "unitTypes"
            )
            .as_str(),
            "class Bob(EntityScripts):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_type = UnitTypes.BOB\n\
                    \t\tself.scripts = [\n\
                        \t\t\tself.Initialize(),\n\
                        \t\t\tFolder('utils', [\n\
                            \t\t\t\tself.ChangeState(),\n\
                        \t\t\t]),\n\
                        \t\t\t\n\
                    \t\t]\n"
        );
    }
}
