use std::collections::HashMap;

use heck::ToPascalCase;
use serde_json::{Map, Value};

use crate::project_generator::utils::enum_name_of;

pub const VARIABLE_CATEGORIES: [&str; 13] = [
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

pub const VARIABLES_CATEGORY_NAME: &str = "variables";
// modd.io holds these categories in the "variables" category
pub const SEPERATED_VARIABLE_CATEGORIES: [&str; 3] =
    ["regions", "itemTypeGroups", "unitTypeGroups"];

const VARIABLE_CATEGORIES_ITERATION_ORDER: [&str; 17] = [
    "unitTypes",
    "playerTypes",
    "itemTypes",
    "projectileTypes",
    "regions",
    "variables",
    "entityTypeVariables",
    "playerTypeVariables",
    "animationTypes",
    "attributeTypes",
    "itemTypeGroups",
    "unitTypeGroups",
    "states",
    "shops",
    "dialogues",
    "music",
    "sound",
];

pub struct CategoriesToVariables {
    pub categories_to_variables: HashMap<&'static str, Vec<Variable>>,
}

impl CategoriesToVariables {
    pub fn parse(game_data: &Value) -> CategoriesToVariables {
        let mut category_to_variables = HashMap::new();

        VARIABLE_CATEGORIES.iter().for_each(|&category| {
            category_to_variables.insert(
                category,
                match game_data.get(category) {
                    Some(category_data) => resolve_duplicate_variable_enum_names(
                        variables_from_category_data(&category_data),
                    ),
                    None => Vec::new(),
                },
            );
        });

        // seperate categories from "variables" category
        category_to_variables.extend(seperated_variables_categories(
            game_data
                .get(VARIABLES_CATEGORY_NAME)
                .unwrap_or(&Value::Null),
        ));
        CategoriesToVariables {
            categories_to_variables: category_to_variables,
        }
    }

    /// Returns (category, &variable)
    pub fn find_categoried_variable_with_id(
        &self,
        variable_id: &str,
    ) -> Option<(&'static str, &Variable)> {
        for (category, variables) in self.categories_to_variables.iter() {
            if let Some(var) = variables.iter().find(|variable| variable.id == variable_id) {
                return Some((category, &var));
            }
        }
        None
    }

    pub fn iter(&self) -> std::vec::IntoIter<(&&'static str, &Vec<Variable>)> {
        let mut categories_of_variables = self
            .categories_to_variables
            .iter()
            .collect::<Vec<(&&'static str, &Vec<Variable>)>>();
        categories_of_variables.sort_by_key(|(category, _variables)| {
            VARIABLE_CATEGORIES_ITERATION_ORDER
                .iter()
                .position(|element| &element == category)
                .unwrap()
        });
        categories_of_variables.into_iter()
    }
}

fn variables_from_category_data(category_data: &Value) -> Vec<Variable> {
    category_data
        .as_object()
        .unwrap_or(&Map::new())
        .iter()
        .map(|(var_id, var)| Variable {
            id: var_id.clone(),
            enum_name: enum_name_of(
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
    Some(
        data_type?
            .as_str()
            .filter(|value| !value.is_empty())?
            .to_string(),
    )
}

fn resolve_duplicate_variable_enum_names(variables: Vec<Variable>) -> Vec<Variable> {
    let mut enum_names_to_count: HashMap<String, u32> = HashMap::new();
    variables
        .into_iter()
        .map(|mut var| {
            enum_names_to_count.insert(
                var.enum_name.clone(),
                enum_names_to_count.get(&var.enum_name).unwrap_or(&0) + 1,
            );
            if let Some(&count) = enum_names_to_count.get(&var.enum_name) {
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
        .chain(&[VARIABLES_CATEGORY_NAME])
        .for_each(|category| {
            seperated_category_to_variables.insert(category, Vec::new());
        });

    variables_from_category_data(&variables_category_data)
        .into_iter()
        .for_each(|variable| {
            let seperated_category_of_variable =
                SEPERATED_VARIABLE_CATEGORIES.iter().find(|&category| {
                    category.eq(&format!(
                        "{}s",
                        &variable.data_type.as_ref().unwrap_or(&String::new())
                    ))
                });

            seperated_category_to_variables
                .get_mut(seperated_category_of_variable.unwrap_or(&VARIABLES_CATEGORY_NAME))
                .unwrap()
                .push(variable);
        });
    seperated_category_to_variables
}

pub fn pymodd_class_name_of_category(category: &'static str) -> String {
    let mut class_name = match category {
        "entityTypeVariables" => "EntityVariables",
        "playerTypeVariables" => "PlayerVariables",
        _ => category,
    }
    .to_pascal_case()
    .to_string();
    if !class_name.ends_with("s") {
        class_name.push('s')
    }
    class_name
}

pub fn pymodd_class_type_of_category(category: &'static str) -> String {
    // in order to match with classes defined in pymodd/functions.py
    if VARIABLES_CATEGORY_NAME == category || SEPERATED_VARIABLE_CATEGORIES.contains(&category) {
        return String::from("Variable");
    }
    pymodd_class_name_of_category(&category)
        .strip_suffix('s')
        .unwrap()
        .to_string()
}

pub fn is_category_of_variable_type(category: &'static str) -> bool {
    category.to_lowercase().contains("variables")
        || SEPERATED_VARIABLE_CATEGORIES.contains(&category)
}

#[derive(Debug, PartialEq, Eq)]
pub struct Variable {
    pub id: String,
    pub enum_name: String,
    pub data_type: Option<String>,
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use serde_json::json;

    use crate::game_data::variable_categories::seperated_variables_categories;

    use super::{
        resolve_duplicate_variable_enum_names, variables_from_category_data, CategoriesToVariables,
        Variable,
    };

    impl Variable {
        pub fn new(id: &str, enum_name: &str, data_type: Option<&str>) -> Variable {
            Variable {
                id: id.to_string(),
                enum_name: enum_name.to_string(),
                data_type: data_type.map(|val| val.to_string()),
            }
        }
    }

    impl CategoriesToVariables {
        pub fn new(map: HashMap<&'static str, Vec<Variable>>) -> CategoriesToVariables {
            CategoriesToVariables {
                categories_to_variables: map,
            }
        }
    }

    #[test]
    fn find_variable_with_key() {
        assert_eq!(
            CategoriesToVariables::new(HashMap::from([
                (
                    "unitTypeGroups",
                    vec![Variable::new("O23FJW2", "BANANA", Some("unitTypeGroup"))]
                ),
                (
                    "regions",
                    vec![Variable::new("WDWI313", "WATER", Some("region"))]
                ),
                ("variables", vec![]),
            ]))
            .find_categoried_variable_with_id("WDWI313")
            .unwrap(),
            (
                "regions",
                &Variable::new("WDWI313", "WATER", Some("region"))
            )
        );
    }

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
            resolve_duplicate_variable_enum_names(vec![
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
