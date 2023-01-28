use std::collections::{HashMap, hash_map};

use heck::AsUpperCamelCase;
use serde_json::{Map, Value};

use super::Directory;

static ENTITY_TYPE_CATEGORIES: [&str; 3] = ["unitTypes", "projectileTypes", "itemTypes"];

pub struct EntityTypes {
    category_to_entity_types: HashMap<&'static str, Vec<EntityType>>,
}

impl EntityTypes {
    pub fn parse(game_data: &Value) -> EntityTypes {
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

        EntityTypes {
            category_to_entity_types: category_to_entity_types,
        }
    }

    pub fn iter(&self) -> hash_map::Iter<&'static str, Vec<EntityType>> {
        self.category_to_entity_types.iter()
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
            scripts: Directory::parse(
                entity_type
                    .get("scripts")
                    .unwrap_or(&Value::Array(Vec::new())),
            ),
        })
        .collect()
}

pub struct EntityType {
    name: String,
    scripts: Directory,
}

impl EntityType {
    fn class_name(&self) -> String {
        AsUpperCamelCase(self.name.clone()).to_string()
    }
}
