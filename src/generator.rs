mod entity_scripts_file;
mod game_json_file;
mod game_variables_file;
mod mapping_file;
mod scripts_file;

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
            File::new(
                "game_variables.py",
                GameVariablesFile::build_content(&game_data),
            ),
            File::new("mapping.py", MappingFile::build_content(&game_data)),
            File::new("scripts.py", ScriptsFile::build_content(&game_data)),
            File::new(
                "entity_scripts.py",
                EntityScriptsFile::build_content(&game_data),
            ),
            File::new("/utils/game.json", GameJsonFile::build_content(&game_data)),
        ];

        files.iter().for_each(|file| {
            let mut file_output = fs::File::create(file.path).expect("could not create file");
            write!(file_output, "{}", file.content).expect("could not write to file");
        });
    }
}

struct File {
    content: String,
    path: &'static str,
}

impl File {
    fn new(path: &'static str, content: String) -> File {
        File { content, path }
    }
}
