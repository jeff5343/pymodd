mod game_data;
mod project_generator;

use std::fs;

use crossterm::style::Stylize;
use game_data::GameData;
use project_generator::ProjectGenerator;
use pyo3::prelude::*;

#[pyfunction]
fn generate_project_from_json_file_path(json_file_path: String) {
    let json_file_content = match fs::read_to_string(&json_file_path) {
        Err(_) => {
            log_error("invalid json file path!");
            return;
        }
        Ok(content) => content,
    };

    let game_data = match GameData::parse(json_file_content) {
        Err(err_msg) => {
            log_error(err_msg);
            return;
        }
        Ok(data) => data,
    };

    println!(
        "\nGenerating pymodd project, {}...",
        game_data.pymodd_project_name().underlined()
    );
    ProjectGenerator::generate(game_data, |file| {
        log_success(&format!("{} written", file.path.to_str().unwrap()))
    })
    .unwrap_or_else(|err_msg| log_error(err_msg));
    println!("\n{} completed generation!\n", "successfully".dark_green());
}

fn log_success(message: &str) {
    println!(" {} {}", "-".dark_green(), message);
}

fn log_error(message: &str) {
    println!(" {} {}", "x".dark_red(), message.red().underlined());
}

#[pymodule]
fn _pymodd_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_project_from_json_file_path, m)?)?;
    Ok(())
}
