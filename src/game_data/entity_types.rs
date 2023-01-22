use std::collections::HashMap;

use serde_json::Value;

use super::Directory;

static ENTITY_TYPE_CATEGORIES: [&str; 3] = ["unitTypes", "projectileTypes", "itemTypes"];

pub struct EntityTypes {
    category_to_entity_types: HashMap<String, Vec<EntityType>>,
}

impl EntityTypes {
    pub fn parse(game_data: &Value) -> EntityTypes {
        let category_to_entity_types = HashMap::new();
        EntityTypes {
            category_to_entity_types: category_to_entity_types
        }
    }

    pub fn from_category(&self, category: &str) -> Option<&Vec<EntityType>> {
        self.category_to_entity_types.get(category)
    }
}

pub struct EntityType {
    name: String,
    scripts: Directory,
}
