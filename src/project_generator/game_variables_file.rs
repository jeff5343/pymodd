use std::ops::Add;

use crate::game_data::{
    variable_categories::{
        pymodd_class_name_of_category, pymodd_class_type_of_category,
        Variable,
    },
    GameData,
};

use super::utils::to_pymodd_maps::VARIABLE_DATA_TYPES_TO_PYMODD_ENUM;

pub struct GameVariablesFile {}

impl GameVariablesFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut file_content = String::new();
        game_data
            .categories_to_variables
            .iter()
            .for_each(|(category, variables)| {
                file_content.push_str(
                    &build_class_content_of_category(&category, &variables).add("\n\n\n"),
                );
            });
        let classes_to_import = game_data
            .categories_to_variables
            .iter()
            .map(|(category, _variables)| pymodd_class_type_of_category(&category))
            .collect::<Vec<String>>();

        format!(
            "from pymodd.functions import {}, DataType\n\n\n{}",
            classes_to_import.join(", "),
            file_content,
        )
    }
}

fn build_class_content_of_category(category: &'static str, variables: &Vec<Variable>) -> String {
    let class_content = format!("class {}:", pymodd_class_name_of_category(&category));
    if variables.len() == 0 {
        return class_content.add("\n\tpass");
    }
    class_content.add(
        build_class_variables_of_category(&category, &variables)
            .into_iter()
            .map(|class_variable| String::from("\n\t").add(&class_variable))
            .collect::<String>()
            .as_str(),
    )
}

fn build_class_variables_of_category(
    category: &'static str,
    variables: &Vec<Variable>,
) -> Vec<String> {
    variables
        .iter()
        .map(|variable| {
            format!(
                "{} = {}(\"{}\"{})",
                variable.enum_name,
                pymodd_class_type_of_category(&category),
                variable.id,
                if variable_category_requires_data_type(&category) {
                    format!(
                        ", {}",
                        VARIABLE_DATA_TYPES_TO_PYMODD_ENUM
                            .get(variable.data_type.as_ref().unwrap_or(&String::new()))
                            .unwrap_or(&String::from("None"))
                    )
                } else {
                    String::new()
                }
            )
            .to_string()
        })
        .collect()
}

fn variable_category_requires_data_type(category: &'static str) -> bool {
    ["variables", "entityTypeVariables", "playerTypeVariables"].contains(&category)
}

#[cfg(test)]
mod tests {
    use crate::{
        game_data::variable_categories::Variable,
        project_generator::game_variables_file::build_class_content_of_category,
    };

    #[test]
    fn category_class_content_with_variables() {
        assert_eq!(
            build_class_content_of_category(
                "itemTypes",
                &vec![
                    Variable::new("FW3513W", "APPLE", None),
                    Variable::new("OE51DW2", "BANANA", None)
                ],
            ),
            String::from(
                "class ItemTypes:\
                    \n\tAPPLE = ItemType(\"FW3513W\")\
                    \n\tBANANA = ItemType(\"OE51DW2\")"
            )
        );
    }

    #[test]
    fn category_class_content_with_no_variables() {
        assert_eq!(
            build_class_content_of_category("itemTypes", &Vec::new(),),
            String::from(
                "class ItemTypes:\n\
                    \tpass"
            )
        );
    }
}
