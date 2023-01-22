use std::collections::HashMap;

use serde_json::Value;

static VARIABLE_CATEGORIES: [&str; 14] = [
    "entityTypeVariables", "shops", "animationTypes", "states", "projectileTypes",
    "itemTypes", "music", "sound", "unitTypes", "variables", "attributeTypes", 
    "playerTypes", "playerTypeVariables", "dialogues" 
];
// categories to group into one category
static GENERAL_VARIABLE_TYPES: [&str; 3] = [
    "regions", "itemTypeGroups", "unitTypeGroups"
];

pub struct Variables {
    category_to_variables: HashMap<String, Vec<Variable>>,
}

impl Variables {
    pub fn parse(game_data: &Value) -> Variables {
        let category_to_variables = HashMap::new();
        Variables { 
            category_to_variables: category_to_variables
        }
    }

    pub fn from_category(&self, category: &str) -> Option<&Vec<Variable>> {
        self.category_to_variables.get(category)
    }
}

pub struct Variable {
    id: String,
    enum_name: String,
}


