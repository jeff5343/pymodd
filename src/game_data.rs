pub mod actions;
pub mod argument;
pub mod directory;
pub mod entity_types;
pub mod variable_categories;

use heck::ToSnakeCase;
use serde_json::Value;

use self::{
    directory::Directory, entity_types::CategoriesToEntityTypes,
    variable_categories::CategoriesToVariables,
};

pub struct GameData {
    pub name: String,
    pub json: Value,
    pub categories_to_variables: CategoriesToVariables,
    pub root_directory: Directory,
    pub categories_to_entity_types: CategoriesToEntityTypes,
}

impl GameData {
    pub fn parse(game_json_file_content: String) -> Result<GameData, &'static str> {
        let game_json: Value = serde_json::from_str(&game_json_file_content)
            .map_err(|_| "error parsing modd.io json file!")?;
        let game_data = &game_json["data"];
        Ok(GameData {
            name: game_json
                .get("title")
                .ok_or("invalid modd.io json file! missing key: title")?
                .to_string(),
            categories_to_variables: CategoriesToVariables::parse(&game_data),
            root_directory: Directory::parse(
                &game_data
                    .get("scripts")
                    .ok_or("invalid modd.io json file! missing key: scripts")?
                    .to_owned(),
            ),
            categories_to_entity_types: CategoriesToEntityTypes::parse(&game_data),
            json: game_json,
        })
    }

    /// returns the name of the game's generating project directory
    pub fn pymodd_project_name(&self) -> String {
        self.name.to_snake_case()
    }
}
