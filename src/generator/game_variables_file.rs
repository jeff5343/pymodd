use std::ops::Add;

use heck::ToPascalCase;

use crate::game_data::{
    variables::{Variable, SEPERATED_VARIABLE_CATEGORIES},
    GameData,
};

pub struct GameVariablesFile {}

impl GameVariablesFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut importing_clases: Vec<String> = Vec::new();
        let mut category_classes = String::new();
        game_data
            .variables
            .iter()
            .for_each(|(category, variables)| {
                category_classes
                    .push_str(&build_category_class_content(&category, &variables).add("\n\n\n"));
                if variables.len() > 0 {
                    importing_clases.push(class_type_from_category(&category));
                }
            });

        format!(
            "from pymodd.functions import {}\n\n{}",
            importing_clases.join(", "),
            category_classes,
        )
    }
}

fn build_category_class_content(category: &'static str, variables: &Vec<Variable>) -> String {
    let class_content = format!("class {}:", class_name_of_category(&category));
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
                class_type_from_category(&category),
                variable.id,
                if is_category_variable_type(&category) {
                    format!(
                        ", variable_type='{}'",
                        variable.data_type.as_ref().unwrap_or(&String::from("None"))
                    )
                } else {
                    String::new()
                }
            )
            .to_string()
        })
        .collect()
}

fn class_name_of_category(category: &'static str) -> String {
    let mut class_name = match category {
        "entityTypeVariables" => "entityVariables",
        "playerTypeVariables" => "playerVariables",
        _ => category,
    }
    .to_pascal_case()
    .to_string();
    if !class_name.ends_with("s") {
        class_name.push('s')
    }
    class_name
}

fn class_type_from_category(category: &'static str) -> String {
    // in order to match with classes defined in pymodd/functions.py
    if SEPERATED_VARIABLE_CATEGORIES.contains(&category) {
        return String::from("Variables");
    }
    class_name_of_category(&category)
        .strip_suffix('s')
        .unwrap()
        .to_string()
}

fn is_category_variable_type(category: &'static str) -> bool {
    category.to_lowercase().contains("variables")
        || SEPERATED_VARIABLE_CATEGORIES.contains(&category)
}

#[cfg(test)]
mod tests {
    use crate::{
        game_data::variables::Variable,
        generator::game_variables_file::build_category_class_content,
    };

    #[test]
    fn category_class_content_with_variables() {
        assert_eq!(
            build_category_class_content(
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
            build_category_class_content("itemTypes", &Vec::new(),),
            String::from(
                "class ItemTypes:\n\
                    \tpass"
            )
        );
    }
}
