use crate::game_data::GameData;

pub struct GameJsonFile {}

impl GameJsonFile {
    pub fn build_content(game_data: &GameData) -> String {
        game_data.json.as_str().unwrap_or("{}").to_string()
    }
}
