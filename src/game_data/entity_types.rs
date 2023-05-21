use std::collections::HashMap;

use heck::ToPascalCase;
use serde_json::{Map, Value};

use crate::project_generator::utils::{enum_name_of, is_valid_class_name};

use super::Directory;

const ENTITY_TYPE_CATEGORIES: [&str; 3] = ["unitTypes", "projectileTypes", "itemTypes"];
const KEYS_OF_KEYBINDINGS_TO_IGNORE: [&str; 2] = ["lookWheel", "movementWheel"];

pub struct CategoriesToEntityTypes {
    categories_to_entity_types: HashMap<&'static str, Vec<EntityType>>,
}

impl CategoriesToEntityTypes {
    pub fn parse(game_data: &Value) -> CategoriesToEntityTypes {
        let mut category_to_entity_types = HashMap::new();

        ENTITY_TYPE_CATEGORIES.iter().for_each(|&category| {
            category_to_entity_types.insert(
                category,
                match game_data.get(category) {
                    Some(category_data) => entity_types_from_category_data(&category_data),
                    None => Vec::new(),
                },
            );
        });

        CategoriesToEntityTypes {
            categories_to_entity_types: category_to_entity_types,
        }
    }

    pub fn iter(&self) -> std::vec::IntoIter<(&&'static str, &Vec<EntityType>)> {
        let mut categories_of_entity_types = self
            .categories_to_entity_types
            .iter()
            .collect::<Vec<(&&'static str, &Vec<EntityType>)>>();
        categories_of_entity_types.sort_by_key(|(category, _variables)| {
            ["unitTypes", "itemTypes", "projectileTypes"]
                .iter()
                .position(|element| &element == category)
                .unwrap()
        });
        categories_of_entity_types.into_iter()
    }
}

fn entity_types_from_category_data(category_data: &Value) -> Vec<EntityType> {
    category_data
        .as_object()
        .unwrap_or(&Map::new())
        .iter()
        .map(|(_, entity_type)| EntityType {
            name: entity_type
                .get("name")
                .unwrap_or(&Value::String(String::from("Undefined")))
                .as_str()
                .unwrap()
                .to_string(),
            directory: Directory::parse(
                entity_type
                    .get("scripts")
                    .unwrap_or(&Value::Array(Vec::new())),
            ),
            keybindings: Keybinding::parse_keybindings_data(
                entity_type
                    .get("controls")
                    .unwrap_or(&Value::Null)
                    .get("abilities")
                    .unwrap_or(&Value::Null),
            ),
        })
        .collect()
}

pub struct EntityType {
    pub name: String,
    pub directory: Directory,
    pub keybindings: Vec<Keybinding>,
}

impl EntityType {
    pub fn pymodd_class_name(&self) -> String {
        let class_name = self.name.replace("'", "").to_pascal_case().to_string();
        if !is_valid_class_name(&class_name) {
            return format!("q{class_name}");
        }
        class_name
    }

    pub fn enum_name(&self) -> String {
        enum_name_of(&self.name)
    }
}

#[derive(Debug, Clone)]
pub struct Keybinding {
    pub key: String,
    pub key_down_script_key: Option<String>,
    pub is_key_down_script_entity_script: bool,
    pub key_up_script_key: Option<String>,
    pub is_key_up_script_entity_script: bool,
}

impl Keybinding {
    pub fn parse_keybindings_data(keybindings_data: &Value) -> Vec<Keybinding> {
        keybindings_data
            .as_object()
            .unwrap_or(&Map::new())
            .iter()
            .map(|(key, data)| {
                let empty_map = Map::new();
                let (key_down_data, key_up_data) = (
                    data.get("keyDown")
                        .unwrap_or(&Value::Null)
                        .as_object()
                        .unwrap_or(&empty_map),
                    data.get("keyUp")
                        .unwrap_or(&Value::Null)
                        .as_object()
                        .unwrap_or(&empty_map),
                );
                Keybinding {
                    key: key.to_string(),
                    key_down_script_key: get_script_key_of_key_behvaior_data(key_down_data),
                    is_key_down_script_entity_script: key_down_data
                        .get("isEntityScript")
                        .unwrap_or(&Value::Null)
                        .as_bool()
                        .unwrap_or(false),
                    key_up_script_key: get_script_key_of_key_behvaior_data(key_up_data),
                    is_key_up_script_entity_script: key_up_data
                        .get("isEntityScript")
                        .unwrap_or(&Value::Null)
                        .as_bool()
                        .unwrap_or(false),
                }
            })
            .filter(|keybinding| !KEYS_OF_KEYBINDINGS_TO_IGNORE.contains(&keybinding.key.as_str()))
            .collect()
    }
}

fn get_script_key_of_key_behvaior_data(key_behavior_data: &Map<String, Value>) -> Option<String> {
    match key_behavior_data
        .get("scriptName")
        .unwrap_or(&Value::Null)
        .as_str()
    {
        Some(str) => {
            if !str.is_empty() {
                Some(str.to_string())
            } else {
                None
            }
        }
        _ => None,
    }
}
