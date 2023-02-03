mod entity_scripts_file;
mod game_json_file;
mod game_variables_file;
mod mapping_file;
mod scripts_file;
pub mod utils;

use std::{fs, io::Write};

use crate::game_data::GameData;

use self::{
    entity_scripts_file::EntityScriptsFile, game_json_file::GameJsonFile,
    game_variables_file::GameVariablesFile, mapping_file::MappingFile, scripts_file::ScriptsFile,
};

pub struct Generator {}

impl Generator {
    pub fn generate(game_data: GameData) {
        let files: [File; 5] = [
            File {
                path: "game_variables.py",
                content: GameVariablesFile::build_content(&game_data),
            },
            File {
                path: "mapping.py",
                content: MappingFile::build_content(&game_data),
            },
            File {
                path: "scripts.py",
                content: ScriptsFile::build_content(&game_data),
            },
            File {
                path: "entity_scripts.py",
                content: EntityScriptsFile::build_content(&game_data),
            },
            File {
                path: "/utils/game.json",
                content: GameJsonFile::build_content(&game_data),
            },
        ];

        files.iter().for_each(|file| {
            let mut file_output = fs::File::create(file.path).expect("could not create file");
            write!(file_output, "{}", file.content).expect("could not write to file");
        });
    }
}

struct File {
    path: &'static str,
    content: String,
}
