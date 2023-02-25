use std::ops::Add;

use crate::game_data::{
    variable_categories::{
        is_category_of_variable_type, pymodd_class_name_of_category, pymodd_class_type_of_category,
        Variable,
    },
    GameData,
};

pub struct GameVariablesFile {}

impl GameVariablesFile {
    pub fn build_content(game_data: &GameData) -> String {
        let mut importing_classes: Vec<String> = Vec::new();
        let mut file_content = String::new();
        game_data
            .categories_to_variables
            .iter()
            .for_each(|(category, variables)| {
                let importing_class_for_category = pymodd_class_type_of_category(&category);
                if variables.len() > 0 && !importing_classes.contains(&importing_class_for_category)
                {
                    importing_classes.push(importing_class_for_category);
                }
                file_content.push_str(
                    &build_class_content_of_category(&category, &variables).add("\n\n\n"),
                );
            });

        format!(
            "from pymodd.functions import {}\n\n\n{}",
            importing_classes.join(", "),
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
                if is_category_of_variable_type(&category) {
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
