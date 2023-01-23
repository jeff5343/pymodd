mod entity_types;
mod game_items;
mod variables;

use serde_json::Value;

use self::{entity_types::EntityTypes, game_items::Directory, variables::Variables};

pub struct GameData {
    pub name: String,
    pub json: Value,
    pub variables: Variables,
    pub directory: Directory,
    pub entity_types: EntityTypes,
}

impl GameData {
    pub fn parse(game_data: String) -> GameData {
        let game_json: Value = serde_json::from_str(&game_data).expect("could not parse game json file");
        let game_data = &game_json["data"];
        GameData {
            name: game_json["title"].to_string(),
            variables: Variables::parse(&game_data),
            directory: Directory::parse(&game_data["scripts"]),
            entity_types: EntityTypes::parse(&game_data),
            json: game_json,
        }
    }
}
