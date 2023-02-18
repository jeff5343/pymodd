use crate::game_data::{
    entity_types::EntityType, variable_categories::pymodd_class_name_of_category, GameData,
};

use super::{
    mapping_file::build_directory_elements,
    scripts_file::{build_scripts_of_directory, ScriptsClassContentBuilder},
    utils::enum_name_of,
};

pub struct EntityScriptsFile {}

impl EntityScriptsFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut content = format!(
            "from pymodd.actions import *\n\
            from pymodd.functions import *\n\
            from pymodd.script import EntityScripts, Folder, Script, Trigger, UiTarget, Flip\n\n\
            from game_variables import *\n\n"
        );

        let scripts_class_content_builder =
            ScriptsClassContentBuilder::new(&game_data.categories_to_variables);
        game_data
            .categories_to_entity_types
            .iter()
            .for_each(|(category, entity_types)| {
                entity_types
                    .iter()
                    .filter(|entity_type| !entity_type.directory.is_empty())
                    .for_each(|entity_type| {
                        content.push_str(&format!(
                            "{}\n{}",
                            build_class_content_of_entity_type_in_category(&entity_type, category),
                            build_scripts_of_directory(
                                &entity_type.directory,
                                &scripts_class_content_builder
                            )
                            .lines()
                            .map(|line| format!("{}{line}\n", "\t"))
                            .collect::<String>()
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
                {}\n\
                \t\t]\n",
        enum_name_of(&entity_type.name),
        build_directory_elements(&entity_type.directory)
            .into_iter()
            .map(|element| format!("{}{element}\n", "\t".repeat(3)))
            .collect::<String>()
    )
}

#[cfg(test)]
mod tests {
    use crate::{game_data::GameData, generator::entity_scripts_file::EntityScriptsFile};

    #[test]
    fn simple_entity_scripts_file_content() {
        assert_eq!(
            EntityScriptsFile::build_content(&GameData::parse(
                r#"{
                "title": "test_game",
                "data": {
                    "scripts": {
                    },
                    "unitTypes": {
                        "RW31QW2": { "name": "bob", "scripts": {
                            "DF31W32": { "name": "initialize", "key": "DF31W32", "actions": [
                            {
                                "type": null
                            }
                            ], "parent": null, "order": 1 }
                        }}
                    }
                }
            }"#
                .to_string()
            ))
            .as_str(),
            "from pymodd.actions import *\n\
            from pymodd.functions import *\n\
            from pymodd.script import EntityScripts, Folder, Script, Trigger, UiTarget, Flip\n\
            \n\
            from game_variables import *\n\
            \n\
            class Bob(EntityScripts):\n\
            	\tdef _build(self):\n\
            		\t\tself.entity_type = UnitTypes.BOB\n\
            		\t\tself.scripts = [\n\
            			\t\t\tInitialize(),\n\n\
                    \t\t]\n\
            \n\
            	\tclass Initialize(Script):\n\
            		\t\tdef _build(self):\n\
            			\t\t\tself.key = 'DF31W32'\n\
            			\t\t\tself.triggers = []\n\
            			\t\t\tself.actions = [\n\
            				\t\t\t\tNone(),\n\
            	            \t\n\
            			\t\t\t]\n"
        );
    }
}
