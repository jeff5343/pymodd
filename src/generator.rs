mod entity_scripts_file;
mod game_json_file;
mod game_variables_file;
mod mapping_file;
mod scripts_file;
pub mod utils;

use std::{fs, io::Write, path::PathBuf};

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
                path: PathBuf::from("game_variables.py"),
                content: GameVariablesFile::build_content(&game_data),
            },
            File {
                path: PathBuf::from("mapping.py"),
                content: MappingFile::build_content(&game_data),
            },
            File {
                path: PathBuf::from("scripts.py"),
                content: ScriptsFile::build_content(&game_data),
            },
            File {
                path: PathBuf::from("entity_scripts.py"),
                content: EntityScriptsFile::build_content(&game_data),
            },
            File {
                path: PathBuf::from("utils/game.json"),
                content: GameJsonFile::build_content(&game_data),
            },
        ];

        files.into_iter().for_each(|mut file| {
            file.path = PathBuf::from(game_data.pymodd_project_name()).join(file.path);
            if let Some(parent) = file.path.parent() {
                fs::create_dir_all(parent).expect("could not create directories");
            }
            let mut file_output = fs::File::create(&file.path).expect("could not create file");
            write!(file_output, "{}", file.content).expect("could not write to file");
        });
    }
}

struct File {
    path: PathBuf,
    content: String,
}
