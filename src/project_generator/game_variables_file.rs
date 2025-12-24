use std::ops::Add;

use heck::ToPascalCase;
use serde_json::Value;

use crate::{
    game_data::{variable_categories::Variable, GameData},
    project_generator::utils::{
        iterators::argument_values_iterator::ArgumentValueIterItem, surround_string_with_quotes,
    },
};

use super::{
    scripts_file::ScriptsContentBuilder,
    utils::{to_pymodd_maps::VARIABLE_DATA_TYPES_TO_PYMODD_ENUM, TAB_SIZE},
};

pub struct GameVariablesFile {}

impl GameVariablesFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut file_content = String::new();
        let scripts_content_builder = ScriptsContentBuilder::new(
            &game_data.categories_to_variables,
            &game_data.root_directory,
        );
        let category_class_content_builder =
            CategoryClassContentBuilder::new(&scripts_content_builder);
        game_data
            .categories_to_variables
            .iter()
            .for_each(|(category, variables)| {
                file_content.push_str(
                    &category_class_content_builder
                        .build_class_content(&category, &variables)
                        .add("\n\n\n"),
                );
            });
        let classes_to_import = {
            let mut classes = game_data
                .categories_to_variables
                .iter()
                .map(|(category, _variables)| pymodd_class_type_of_category(&category))
                .collect::<Vec<String>>();
            classes.sort();
            classes.dedup();
            classes
        };

        format!(
            "from pymodd.variable_types import {}\n\
            from pymodd.variable.data_type import DataType\n\n\n{}",
            classes_to_import.join(", "),
            file_content,
        )
        .replace("\t", &" ".repeat(TAB_SIZE))
    }
}

pub struct CategoryClassContentBuilder<'a> {
    // used for parsing default values of variables
    scripts_content_builder: &'a ScriptsContentBuilder<'a>,
}

impl<'a> CategoryClassContentBuilder<'a> {
    pub fn new(
        scripts_content_builder: &'a ScriptsContentBuilder,
    ) -> CategoryClassContentBuilder<'a> {
        CategoryClassContentBuilder {
            scripts_content_builder: &scripts_content_builder,
        }
    }

    fn build_class_content(&self, category: &'static str, variables: &Vec<Variable>) -> String {
        let class_content = format!("class {}:", pymodd_class_name_of_category(&category));
        if variables.len() == 0 {
            return class_content.add("\n\tpass");
        }
        class_content.add(
            self.build_class_variables_of_category(&category, &variables)
                .into_iter()
                .map(|class_variable| String::from("\n\t").add(&class_variable))
                .collect::<String>()
                .as_str(),
        )
    }

    fn build_class_variables_of_category(
        &self,
        category: &'static str,
        variables: &Vec<Variable>,
    ) -> Vec<String> {
        variables
            .iter()
            .map(|variable| {
                format!(
                    "{} = {}({}{})",
                    variable.enum_name(),
                    pymodd_class_type_of_category(&category),
                    surround_string_with_quotes(&variable.id),
                    if !is_category_of_variable_type(&category) {
                        format!(", name={}", surround_string_with_quotes(&variable.name))
                    } else {
                        let data_type = variable.data_type().unwrap_or(String::new());
                        format!(
                            ", {}{}",
                            VARIABLE_DATA_TYPES_TO_PYMODD_ENUM
                                .get(&data_type)
                                .unwrap_or(&String::from("None")),
                            match (
                                variable.get_key("default"),
                                ["entityTypeVariables", "playerTypeVariables"].contains(&category)
                                    || data_type == "region"
                            ) {
                                (Some(default_value), false) if data_type != "region" => format!(
                                    ", default_value={}",
                                    self.build_default_value_of_variable(default_value)
                                ),
                                _ => String::new(),
                            }
                        )
                    }
                )
                .to_string()
            })
            .collect()
    }

    fn build_default_value_of_variable(&self, default_value: &Value) -> String {
        match default_value {
            Value::Object(object) => format!(
                "[{}]",
                object
                    .keys()
                    .map(|val| {
                        self.scripts_content_builder.build_argument_content(
                            ArgumentValueIterItem::Value(&Value::String(val.to_string())),
                        )
                    })
                    .collect::<Vec<String>>()
                    .join(", ")
            ),
            _ => self
                .scripts_content_builder
                .build_argument_content(ArgumentValueIterItem::Value(default_value)),
        }
    }
}

pub fn pymodd_class_name_of_category(category: &'static str) -> String {
    let class_name = match category {
        "entityTypeVariables" => "EntityVariable",
        "playerTypeVariables" => "PlayerVariable",
        _ => category,
    }
    .to_pascal_case()
    .to_string();
    if class_name.ends_with("s") {
        return class_name.strip_suffix("s").unwrap().to_string();
    }
    class_name
}

fn pymodd_class_type_of_category(category: &'static str) -> String {
    match category {
        "itemTypeGroups" | "unitTypeGroups" | "regions" => String::from("Variable"),
        _ => pymodd_class_name_of_category(&category).to_string(),
    }
    .add("Base")
}

fn is_category_of_variable_type(category: &'static str) -> bool {
    [
        "variables",
        "entityTypeVariables",
        "playerTypeVariables",
        "itemTypeGroups",
        "unitTypeGroups",
        "regions",
    ]
    .contains(&category)
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use serde_json::json;

    use crate::{
        game_data::{
            directory::Directory,
            variable_categories::{CategoriesToVariables, Variable},
        },
        project_generator::{
            game_variables_file::CategoryClassContentBuilder, scripts_file::ScriptsContentBuilder,
        },
    };

    #[test]
    fn category_class_content_with_variables() {
        assert_eq!(
            CategoryClassContentBuilder::new(&ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            ))
            .build_class_content(
                "itemTypes",
                &vec![
                    Variable::new("FW3513W", "apple", json!({})),
                    Variable::new("OE51DW2", "banana", json!({}))
                ],
            ),
            String::from(
                "class ItemType:\
                    \n\tAPPLE = ItemTypeBase('FW3513W', name='apple')\
                    \n\tBANANA = ItemTypeBase('OE51DW2', name='banana')"
            )
        );
    }

    #[test]
    fn category_class_content_with_variables_starting_with_numbers() {
        assert_eq!(
            CategoryClassContentBuilder::new(&ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            ))
            .build_class_content(
                "itemTypes",
                &vec![
                    Variable::new("FW3513W", "1apple", json!({})),
                    Variable::new("OE51DW2", "2banana", json!({}))
                ],
            ),
            String::from(
                "class ItemType:\
                    \n\t_1APPLE = ItemTypeBase('FW3513W', name='1apple')\
                    \n\t_2BANANA = ItemTypeBase('OE51DW2', name='2banana')"
            )
        );
    }

    #[test]
    fn category_class_content_with_no_variables() {
        assert_eq!(
            CategoryClassContentBuilder::new(&ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            ))
            .build_class_content("itemTypes", &Vec::new(),),
            String::from(
                "class ItemType:\n\
                    \tpass"
            )
        );
    }

    #[test]
    fn variable_type_category_class_content_with_variables() {
        assert_eq!(
            CategoryClassContentBuilder::new(&ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::from([(
                    "itemTypes",
                    vec![
                        Variable::new("FW3513W", "sword", json![{}]), 
                        Variable::new("Ue25P1i", "stick", json![{}]), 
                        Variable::new("YfO9w81", "sand", json![{}])
                    ]
                )])),
                &Directory::new("root", "null", Vec::new())
            ))
            .build_class_content(
                "variables",
                &vec![
                    Variable::new(
                        "apple",
                        "apple",
                        json!({ "dataType": "number", "default": json!(5) })
                    ),
                    Variable::new(
                        "banana",
                        "banana",
                        json!({
                            "dataType": "itemTypeGroup",
                            "default": {
                                "FW3513W": { "probability": 20, "quantity": 1 },
                                "Ue25P1i": { "probability": 20, "quantity": 1 },
                                "YfO9w81": { "probability": 20, "quantity": 1 }
                            }
                        })
                    ),
                    Variable::new(
                        "peach",
                        "peach",
                        json!({
                            "dataType": "region", 
                            "default": {
                                "alpha": 100,
                                "height": 204,
                                "inside": "#000000",
                                "outside": "",
                                "videoChatEnabled": false,
                                "width": 389,
                                "x": 837,
                                "y": 781
                            }
                        })
                    ),
                ],
            ),
            String::from(
                "class Variable:\n\
                    \tAPPLE = VariableBase('apple', DataType.NUMBER, default_value=5)\n\
                    \tBANANA = VariableBase('banana', DataType.ITEM_TYPE_GROUP, default_value=[ItemType.SWORD, ItemType.STICK, ItemType.SAND])\n\
                    \tPEACH = VariableBase('peach', DataType.REGION)"
            )
        );
    }

    #[test]
    fn entity_variable_category_class_content() {
        assert_eq!(
            CategoryClassContentBuilder::new(&ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            ))
            .build_class_content(
                "entityTypeVariables",
                &vec![Variable::new(
                    "apple",
                    "apple",
                    json!({ "dataType": "number", "default": json!(5) })
                )],
            ),
            String::from(
                "class EntityVariable:\n\
                    \tAPPLE = EntityVariableBase('apple', DataType.NUMBER)"
            )
        );
    }

    #[test]
    fn player_variable_category_class_content() {
        assert_eq!(
            CategoryClassContentBuilder::new(&ScriptsContentBuilder::new(
                &CategoriesToVariables::new(HashMap::new()),
                &Directory::new("root", "null", Vec::new())
            ))
            .build_class_content(
                "playerTypeVariables",
                &vec![Variable::new(
                    "apple",
                    "apple",
                    json!({ "dataType": "number", "default": json!(5) })
                )],
            ),
            String::from(
                "class PlayerVariable:\n\
                    \tAPPLE = PlayerVariableBase('apple', DataType.NUMBER)"
            )
        );
    }
}
