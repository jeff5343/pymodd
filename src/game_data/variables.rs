use std::collections::{hash_map, HashMap};

use heck::AsShoutySnakeCase;
use serde_json::{Map, Value};

static VARIABLE_CATEGORIES: [&str; 13] = [
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
];

pub static VARIABLES_CATEGORY: &str = "variables";
// modd.io holds these categories in the "variables" category
pub static SEPERATED_VARIABLE_CATEGORIES: [&str; 3] =
    ["regions", "itemTypeGroups", "unitTypeGroups"];

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

        // seperate categories from "variables" category
        category_to_variables.extend(seperated_variables_categories(
            game_data.get(VARIABLES_CATEGORY).unwrap_or(&Value::Null),
        ));
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
            if !data_type.is_empty() {
                Some(data_type)
            } else {
                None
            }
        }
        _ => None,
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

fn seperated_variables_categories(
    variables_category_data: &Value,
) -> HashMap<&'static str, Vec<Variable>> {
    let mut seperated_category_to_variables: HashMap<&'static str, Vec<Variable>> = HashMap::new();
    // initalize vectors for each variable category
    SEPERATED_VARIABLE_CATEGORIES
        .iter()
        .chain(&[VARIABLES_CATEGORY])
        .for_each(|category| {
            seperated_category_to_variables.insert(category, Vec::new());
        });

    variables_from_category_data(&variables_category_data)
        .into_iter()
        .for_each(|variable| {
            let category_index = SEPERATED_VARIABLE_CATEGORIES.iter().position(|category| {
                category.eq(&format!(
                    "{}s",
                    &variable.data_type.as_ref().unwrap_or(&String::new())
                )
                .as_str())
            });

            seperated_category_to_variables
                .get_mut(&match category_index {
                    Some(i) => SEPERATED_VARIABLE_CATEGORIES.get(i).unwrap(),
                    None => VARIABLES_CATEGORY,
                })
                .unwrap()
                .push(variable);
        });
    seperated_category_to_variables
}

#[derive(Debug, PartialEq, Eq)]
pub struct Variable {
    pub id: String,
    pub enum_name: String,
    pub data_type: Option<String>,
}

impl Variable {
    pub fn new(id: &str, enum_name: &str, data_type: Option<&str>) -> Variable {
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
mod tests {
    use std::collections::HashMap;

    use serde_json::json;

    use crate::game_data::variables::seperated_variables_categories;

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

    #[test]
    fn seperate_variables_category_into_multiple() {
        assert_eq!(
            seperated_variables_categories(&json!({
                "FW3513W": { "name": "apple", "dataType": "itemTypeGroup" },
                "O23FJW2": { "name": "banana", "dataType": "unitTypeGroup" },
                "WDWI313": { "name": "water", "dataType": "region" },
            })),
            HashMap::from([
                (
                    "itemTypeGroups",
                    vec![Variable::new("FW3513W", "APPLE", Some("itemTypeGroup"))]
                ),
                (
                    "unitTypeGroups",
                    vec![Variable::new("O23FJW2", "BANANA", Some("unitTypeGroup"))]
                ),
                (
                    "regions",
                    vec![Variable::new("WDWI313", "WATER", Some("region"))]
                ),
                ("variables", vec![]),
            ])
        );
    }
}
