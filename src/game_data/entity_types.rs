use std::collections::{hash_map, HashMap};

use heck::ToPascalCase;
use serde_json::{Map, Value};

use crate::project_generator::utils::is_valid_class_name;

use super::Directory;

const ENTITY_TYPE_CATEGORIES: [&str; 3] = ["unitTypes", "projectileTypes", "itemTypes"];

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

    pub fn iter(&self) -> hash_map::Iter<&'static str, Vec<EntityType>> {
        self.categories_to_entity_types.iter()
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
        })
        .collect()
}

pub struct EntityType {
    pub name: String,
    pub directory: Directory,
}

impl EntityType {
    pub fn pymodd_class_name(&self) -> String {
        let class_name = self.name.replace("'", "").to_pascal_case().to_string();
        if !is_valid_class_name(&class_name) {
            return format!("q{class_name}");
        }
        class_name
    }
}
