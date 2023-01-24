use std::collections::{hash_map, HashMap};

use heck::AsShoutySnakeCase;
use serde_json::{Map, Value};

static VARIABLE_CATEGORIES: [&str; 14] = [
    "animationTypes",
    "attributeTypes",
    "dialogues",
    "entityTypeVariables",
    "itemTypes",
    "music",
    "projectileTypes",
    "playerTypes",
    "playerTypeVariables",
    "shops",
    "sound",
    "states",
    "unitTypes",
    "variables",
]; // modd.io treats these categories the same as the "variables" category
static GENERAL_VARIABLE_CATEGORIES: [&str; 3] = ["regions", "itemTypeGroups", "unitTypeGroups"];

pub struct Variables {
    pub category_to_variables: HashMap<&'static str, Vec<Variable>>,
}

impl Variables {
    pub fn parse(game_data: &Value) -> Variables {
        let mut category_to_variables = HashMap::new();

        VARIABLE_CATEGORIES.iter().for_each(|&category| {
            category_to_variables.insert(
                category,
                match game_data.get(category) {
                    Some(category_data) => {
                        resolve_duplicate_enum_names(variables_from_category_data(&category_data))
                    }
                    None => Vec::new(),
                },
            );
        });

        let variables = category_to_variables.get_mut("variables").unwrap();
        GENERAL_VARIABLE_CATEGORIES.iter().for_each(|&category| {
            variables.extend(match game_data.get(category) {
                Some(category_data) => {
                    resolve_duplicate_enum_names(variables_from_category_data(category_data))
                }
                None => Vec::new(),
            })
        });
        Variables {
            category_to_variables: category_to_variables,
        }
    }

    pub fn iter(&self) -> hash_map::Iter<&'static str, Vec<Variable>> {
        self.category_to_variables.iter()
    }
}

fn variables_from_category_data(category_data: &Value) -> Vec<Variable> {
    category_data
        .as_object()
        .unwrap_or(&Map::new())
        .iter()
        .map(|(var_id, var)| Variable {
            id: var_id.clone(),
            enum_name: AsShoutySnakeCase(
                var.get("name")
                    .unwrap_or(&Value::String(var_id.clone()))
                    .as_str()
                    .unwrap(),
            )
            .to_string(),
            data_type: parse_data_type(var.get("dataType")),
        })
        .collect()
}

fn parse_data_type(data_type: Option<&Value>) -> Option<String> {
    match data_type {
        Some(data_type) => {
            let data_type = data_type.as_str().unwrap_or("").to_string();
            if data_type.is_empty() {
                None
            } else {
                Some(data_type)
            }
        }
        None => None,
    }
}

fn resolve_duplicate_enum_names(variables: Vec<Variable>) -> Vec<Variable> {
    let mut enum_names_count: HashMap<String, u32> = HashMap::new();

    variables
        .into_iter()
        .map(|mut var| {
            enum_names_count.insert(
                var.enum_name.clone(),
                enum_names_count.get(&var.enum_name).unwrap_or(&0) + 1,
            );

            if let Some(&count) = enum_names_count.get(&var.enum_name) {
                if count > 1 {
                    var.enum_name.push_str(format!("_{}", count - 1).as_str());
                }
            }
            var
        })
        .collect()
}

#[derive(Debug, PartialEq, Eq)]
pub struct Variable {
    pub id: String,
    pub enum_name: String,
    pub data_type: Option<String>,
}

impl Variable {
    fn new(id: &str, enum_name: &str, data_type: Option<&str>) -> Variable {
        let data_type = match data_type {
            Some(string) => Some(string.to_string()),
            _ => None,
        };
        Variable {
            id: id.to_string(),
            enum_name: enum_name.to_string(),
            data_type,
        }
    }
}

#[cfg(test)]
mod variables_tests {
    use serde_json::json;

    use super::{resolve_duplicate_enum_names, variables_from_category_data, Variable};

    #[test]
    fn parse_variables_from_category_data() {
        assert_eq!(
            variables_from_category_data(&json!({
                "FW3513W": { "name": "apple", "dataType": None::<&str> },
                "O23FJW2": { "name": "banana", "dataType": "" },
                "WDWI313": { "name": "water", "dataType": "region" },
            }))
            .as_slice(),
            [
                Variable::new("FW3513W", "APPLE", None),
                Variable::new("O23FJW2", "BANANA", None),
                Variable::new("WDWI313", "WATER", Some("region")),
            ]
        );
    }

    #[test]
    fn ensure_no_duplicated_enum_names() {
        assert_eq!(
            resolve_duplicate_enum_names(vec![
                Variable::new("FW3513W", "APPLE", None),
                Variable::new("O23FJW2", "APPLE", None),
                Variable::new("WDWI313", "APPLE", None),
            ])
            .as_slice(),
            [
                Variable::new("FW3513W", "APPLE", None),
                Variable::new("O23FJW2", "APPLE_1", None),
                Variable::new("WDWI313", "APPLE_2", None),
            ]
        );
    }
}
