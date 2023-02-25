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

const STORED_GAME_JSON_FILE_PATH: &str = "utils/game.json";

pub struct ProjectGenerator {}

impl ProjectGenerator {
    pub fn generate<F>(game_data: GameData, generation_logger: F) -> Result<(), &'static str>
    where
        F: Fn(File),
    {
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
                path: PathBuf::from(STORED_GAME_JSON_FILE_PATH),
                content: GameJsonFile::build_content(&game_data),
            },
        ];

        for file in files.into_iter().map(|file| File {
            // insert project directory as parent to all file paths
            path: PathBuf::from(game_data.pymodd_project_name()).join(file.path),
            content: file.content,
        }) {
            // unwrap is fine as all files have the project directory as parent
            let parent = file.path.parent().unwrap();
            if !parent.exists() {
                fs::create_dir_all(parent).map_err(|_| "error creating project directories!")?;
            }
            write!(
                fs::File::create(&file.path).map_err(|_| "error creating project file!")?,
                "{}",
                file.content
            )
            .map_err(|_| "error writing to project file!")?;
            generation_logger(file);
        }
        Ok(())
    }
}

pub struct File {
    pub path: PathBuf,
    content: String,
}
