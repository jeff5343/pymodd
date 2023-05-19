use std::collections::HashMap;

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
    "itemTypes",
    "projectileTypes",
    "unitTypes",
    "playerTypes",
    "itemTypeGroups",
    "unitTypeGroups",
    "variables",
    "entityTypeVariables",
    "playerTypeVariables",
    "regions",
    "shops",
    "dialogues",
    "music",
    "sound",
    "states",
    "animationTypes",
    "attributeTypes",
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

#[derive(Debug, PartialEq, Eq)]
pub struct Variable {
    pub id: String,
    pub name: String,
    data: Map<String, Value>,
}

impl Variable {
    pub fn enum_name(&self) -> String {
        enum_name_of(&self.name)
    }

    pub fn data_type(&self) -> Option<String> {
        Some(
            self.get_key("dataType")?
                .as_str()
                .filter(|value| !value.is_empty())?
                .to_string(),
        )
    }

    pub fn get_key(&self, key: &str) -> Option<&Value> {
        self.data.get(key)
    }
}

fn variables_from_category_data(category_data: &Value) -> Vec<Variable> {
    category_data
        .as_object()
        .unwrap_or(&Map::new())
        .iter()
        .map(|(var_id, var)| {
            let var_name = var
                .get("name")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or(var_id);
            Variable {
                id: var_id.clone(),
                name: var_name.to_string(),
                data: var.as_object().unwrap_or(&Map::new()).clone(),
            }
        })
        .collect()
}

fn resolve_duplicate_variable_enum_names(variables: Vec<Variable>) -> Vec<Variable> {
    let mut enum_names_to_count: HashMap<String, u32> = HashMap::new();
    variables
        .into_iter()
        .map(|var| {
            enum_names_to_count.insert(
                var.enum_name(),
                enum_names_to_count.get(&var.enum_name()).unwrap_or(&0) + 1,
            );
            if let Some(&count) = enum_names_to_count.get(&var.enum_name()) {
                if count > 1 {
                    var.enum_name().push_str(format!("_{}", count - 1).as_str());
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
                        &variable.data_type().unwrap_or(String::new())
                    ))
                });

            seperated_category_to_variables
                .get_mut(seperated_category_of_variable.unwrap_or(&VARIABLES_CATEGORY_NAME))
                .unwrap()
                .push(variable);
        });
    seperated_category_to_variables
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use serde_json::{json, Map, Value};

    use crate::game_data::variable_categories::seperated_variables_categories;

    use super::{
        resolve_duplicate_variable_enum_names, variables_from_category_data, CategoriesToVariables,
        Variable,
    };

    impl Variable {
        pub fn new(id: &str, name: &str, additonal_data: Value) -> Variable {
            let mut data = additonal_data.as_object().unwrap_or(&Map::new()).clone();
            data.insert(String::from("name"), Value::String(name.to_string()));
            Variable {
                id: id.to_string(),
                name: name.to_string(),
                data,
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
                    vec![Variable::new(
                        "O23FJW2",
                        "banana",
                        json!({"dataType": "unitTypeGroup"})
                    )]
                ),
                (
                    "regions",
                    vec![Variable::new(
                        "WDWI313",
                        "water",
                        json!({"dataType": "region"})
                    )]
                ),
                ("variables", vec![]),
            ]))
            .find_categoried_variable_with_id("WDWI313")
            .unwrap(),
            (
                "regions",
                &Variable::new("WDWI313", "water", json!({"dataType": "region"}))
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
                Variable::new("FW3513W", "apple", json!({ "dataType": null })),
                Variable::new("O23FJW2", "banana", json!({"dataType": ""})),
                Variable::new("WDWI313", "water", json!({"dataType": "region"})),
            ]
        );
    }

    #[test]
    fn ensure_no_duplicated_enum_names() {
        assert_eq!(
            resolve_duplicate_variable_enum_names(vec![
                Variable::new("FW3513W", "apple", json!({})),
                Variable::new("O23FJW2", "apple", json!({})),
                Variable::new("WDWI313", "apple", json!({})),
            ])
            .as_slice(),
            [
                Variable::new("FW3513W", "apple", json!({})),
                Variable::new("O23FJW2", "apple", json!({})),
                Variable::new("WDWI313", "apple", json!({})),
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
                    vec![Variable::new(
                        "FW3513W",
                        "apple",
                        json!({"dataType": "itemTypeGroup"})
                    )]
                ),
                (
                    "unitTypeGroups",
                    vec![Variable::new(
                        "O23FJW2",
                        "banana",
                        json!({"dataType": "unitTypeGroup"})
                    )]
                ),
                (
                    "regions",
                    vec![Variable::new(
                        "WDWI313",
                        "water",
                        json!({"dataType": "region"})
                    )]
                ),
                ("variables", vec![]),
            ])
        );
    }
}
