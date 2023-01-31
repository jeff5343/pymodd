use heck::ToPascalCase;

use crate::game_data::{GameData, variables::Variable};

pub struct GameVariablesFile {}

// work in progress
impl GameVariablesFile {
    pub fn build_content(game_data: &GameData) -> String {
        let importing_clases: Vec<String> = Vec::new();

        let variable_classes = String::new();
        game_data.variables.iter().for_each(|(category, variables)| {
                       
        });

        let content = format!(
            "from pymodd.functions import {}\n",
            importing_clases.join(", ")
        );

        content
    }
}

fn build_category_class_content(category: &'static str, variables: Vec<Variable>) -> String {
    let class_variables: Vec<String> = variables.iter().map(|var| {
        format!("{} = {}", class_name_from_category(category), "")
    }).collect();

    String::from("")
}

fn class_name_from_category(category: &'static str) -> String {
    match category {
         "entityTypeVariables" => "entityVariables",
         "playerTypeVariables" => "playerVariables",
         _ => category
    }.strip_suffix("s").unwrap_or(category).to_pascal_case().to_string()
}
