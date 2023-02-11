pub mod actions;
pub mod directory;
pub mod entity_types;
pub mod variables;

use heck::ToSnakeCase;
use serde_json::Value;

use self::{directory::Directory, entity_types::CategoryToEntityTypes, variables::Variables};

pub struct GameData {
    pub name: String,
    pub json: Value,
    pub variables: Variables,
    pub root_directory: Directory,
    pub entity_type_categories: CategoryToEntityTypes,
}

impl GameData {
    pub fn parse(game_data: String) -> GameData {
        let game_json: Value =
            serde_json::from_str(&game_data).expect("could not parse game json file");
        let game_data = &game_json["data"];
        GameData {
            name: game_json
                .get("title")
                .expect("could not find key: title")
                .to_string(),
            variables: Variables::parse(&game_data),
            root_directory: Directory::parse(
                &game_data
                    .get("scripts")
                    .expect("could not find key: scripts"),
            ),
            entity_type_categories: CategoryToEntityTypes::parse(&game_data),
            json: game_json,
        }
    }

    /// returns the name of the game's generated project directory
    pub fn project_directory_name(&self) -> String {
        self.name.to_snake_case()
    }
}
