use crate::{
    game_data::{directory::Directory, entity_types::EntityType, GameData},
    project_generator::{
        game_variables_file::pymodd_class_name_of_category,
        utils::to_pymodd_maps::KEYS_TO_PYMODD_ENUM,
    },
};

use super::{
    mapping_file::build_directory_items_contents,
    scripts_file::{build_directory_content, ScriptsContentBuilder},
    utils::{iterators::directory_iterator::DirectoryIterItem, TAB_SIZE},
};

pub struct EntityScriptsFile {}

impl EntityScriptsFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut content = format!(
            "from pymodd.core.folder import Folder\n\
            from pymodd.entity_script import EntityScripts, Key, KeyBehavior\n\n\
            from scripts import *\n\n\n"
        );
        let scripts_class_content_builder = ScriptsContentBuilder::new(
            &game_data.categories_to_variables,
            &game_data.root_directory,
        );

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
                            build_class_content_of_entity_type_in_category(
                                &entity_type,
                                category,
                                &game_data.root_directory,
                            ),
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
        content.replace("\t", &" ".repeat(TAB_SIZE))
    }
}

fn build_class_content_of_entity_type_in_category(
    entity_type: &EntityType,
    category: &'static str,
    game_directory: &Directory,
) -> String {
    let (entity_type_class_name, category_class_name) = (
        entity_type.pymodd_class_name(),
        pymodd_class_name_of_category(category),
    );
    format!(
        "class {entity_type_class_name}(EntityScripts):\n\
            \tdef _build(self):\n\
                \t\tself.entity_type = {category_class_name}.{}\n\
                    {}\
                \t\tself.scripts = [\n\
                    {}\
                \t\t\t\n\
                \t\t]\n",
        entity_type.enum_name(),
        if category == "unitTypes" {
            format!(
                "\t\tself.keybindings = {{\n\
                    {}\
                \t\t\t\n\
                \t\t}}\n",
                build_keybindings_dictionary_elements_for_entity_type(&entity_type, game_directory)
                    .into_iter()
                    .map(|element| format!("{}{element},\n", "\t".repeat(3)))
                    .collect::<String>()
            )
        } else {
            String::new()
        },
        build_directory_elements_for_entity_type(&entity_type)
            .into_iter()
            .map(|element| format!("{}{element}\n", "\t".repeat(3)))
            .collect::<String>()
    )
}

fn build_keybindings_dictionary_elements_for_entity_type(
    entity_type: &EntityType,
    game_directory: &Directory,
) -> Vec<String> {
    let mut keybindings = entity_type.keybindings.clone();
    keybindings.sort_by(|a, b| {
        if a.key.len() <= 1 && b.key.len() <= 1 {
            // sort by the first character
            a.key
                .chars()
                .next()
                .unwrap_or(' ')
                .to_digit(10)
                .cmp(&b.key.chars().next().unwrap_or(' ').to_digit(10))
        } else {
            // sort by length
            a.key.len().cmp(&b.key.len()).reverse()
        }
    });
    keybindings
        .iter()
        .map(|keybinding| {
            format!(
                "{}: KeyBehavior({}, {})",
                KEYS_TO_PYMODD_ENUM
                    .get(&keybinding.key)
                    .unwrap_or(&String::from("None")),
                build_content_of_script_with_key(
                    &keybinding.key_down_script_key,
                    keybinding.is_key_down_script_entity_script,
                    game_directory,
                    &entity_type.directory
                ),
                build_content_of_script_with_key(
                    &keybinding.key_up_script_key,
                    keybinding.is_key_up_script_entity_script,
                    game_directory,
                    &entity_type.directory
                )
            )
        })
        .collect()
}

fn build_content_of_script_with_key(
    key: &Option<String>,
    is_entity_type_script: bool,
    game_directory: &Directory,
    entity_type_directory: &Directory,
) -> String {
    if let Some(key) = key {
        if is_entity_type_script {
            if let DirectoryIterItem::Script(script) = entity_type_directory
                .find_item_with_key(&key)
                .unwrap_or(DirectoryIterItem::DirectoryEnd)
            {
                return format!("self.{}()", script.function_name);
            };
        } else {
            if let DirectoryIterItem::Script(script) = game_directory
                .find_item_with_key(&key)
                .unwrap_or(DirectoryIterItem::DirectoryEnd)
            {
                return format!("{}()", script.function_name);
            };
        };
    }
    String::from("None")
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
        game_data::{
            directory::{Directory, DirectoryItem, Script},
            entity_types::{EntityType, Keybinding},
        },
        project_generator::entity_scripts_file::build_class_content_of_entity_type_in_category,
    };

    impl Keybinding {
        fn new(
            key: &str,
            key_down_script_key: Option<&str>,
            is_key_down_script_entity_script: bool,
            key_up_script_key: Option<&str>,
            is_key_up_script_entity_script: bool,
        ) -> Keybinding {
            Keybinding {
                key: key.to_string(),
                key_down_script_key: key_down_script_key.map(|s| s.to_string()),
                is_key_down_script_entity_script,
                key_up_script_key: key_up_script_key.map(|s| s.to_string()),
                is_key_up_script_entity_script,
            }
        }
    }

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
                    })),
                    keybindings: Vec::new()
                },
                "unitTypes",
                &Directory::new("root", "null", Vec::new()),
            )
            .as_str(),
            "class Bob(EntityScripts):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_type = UnitType.BOB\n\
                    \t\tself.keybindings = {\n\
                        \t\t\t\n\
                    \t\t}\n\
                    \t\tself.scripts = [\n\
                        \t\t\tself.initialize(),\n\
                        \t\t\tFolder('utils', [\n\
                            \t\t\t\tself.change_state(),\n\
                        \t\t\t]),\n\
                        \t\t\t\n\
                    \t\t]\n"
        );
    }

    #[test]
    fn keybindings_field_of_entity_scripts_class() {
        assert_eq!(
            build_class_content_of_entity_type_in_category(
                &EntityType {
                    name: "bob".to_string(),
                    directory: Directory::parse(&json!({
                        "DF31W32": { "triggers": [], "name": "use item",
                            "key": "DF31W32", "actions": [], "parent": null, "order": 1 },
                        "SDUW31W": { "triggers": [], "name": "stop using item",
                            "key": "SDUW31W", "actions": [], "parent": null, "order": 2 }
                    })),
                    keybindings: vec![
                        Keybinding::new("q", Some("DF31W32"), true, Some("3FJ31WD"), false),
                        Keybinding::new("r", Some("3FJ31WD"), false, None, false),
                        Keybinding::new("button1", Some("DF31W32"), true, Some("SDUW31W"), true),
                        Keybinding::new("z", None, false, None, false)
                    ]
                },
                "unitTypes",
                &Directory::new(
                    "root",
                    "null",
                    vec![DirectoryItem::Script(Script::qnew(
                        "EndGame",
                        "3FJ31WD",
                        Vec::new(),
                        Vec::new(),
                    ))]
                )
            )
            .as_str(),
            "class Bob(EntityScripts):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_type = UnitType.BOB\n\
                    \t\tself.keybindings = {\n\
                        \t\t\tKey.LEFT_CLICK: KeyBehavior(self.use_item(), self.stop_using_item()),\n\
                        \t\t\tKey.Q: KeyBehavior(self.use_item(), end_game()),\n\
                        \t\t\tKey.R: KeyBehavior(end_game(), None),\n\
                        \t\t\tKey.Z: KeyBehavior(None, None),\n\
                        \t\t\t\n\
                    \t\t}\n\
                    \t\tself.scripts = [\n\
                        \t\t\tself.use_item(),\n\
                        \t\t\tself.stop_using_item(),\n\
                        \t\t\t\n\
                    \t\t]\n"
        );
    }

    #[test]
    fn item_type_entity_scripts_class() {
        assert_eq!(
            build_class_content_of_entity_type_in_category(
                &EntityType {
                    name: "sword".to_string(),
                    directory: Directory::parse(&json!({})),
                    keybindings: vec![]
                },
                "itemTypes",
                &Directory::new("root", "null", vec![])
            )
            .as_str(),
            "class Sword(EntityScripts):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_type = ItemType.SWORD\n\
                    \t\tself.scripts = [\n\
                        \t\t\t\n\
                    \t\t]\n"
        );
    }

    #[test]
    fn projectile_type_entity_scripts_class() {
        assert_eq!(
            build_class_content_of_entity_type_in_category(
                &EntityType {
                    name: "bullet".to_string(),
                    directory: Directory::parse(&json!({})),
                    keybindings: vec![]
                },
                "projectileTypes",
                &Directory::new("root", "null", vec![])
            )
            .as_str(),
            "class Bullet(EntityScripts):\n\
                \tdef _build(self):\n\
                    \t\tself.entity_type = ProjectileType.BULLET\n\
                    \t\tself.scripts = [\n\
                        \t\t\t\n\
                    \t\t]\n"
        );
    }
}
