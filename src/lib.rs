mod game_data;
mod project_generator;

use crossterm::style::Stylize;
use game_data::GameData;
use project_generator::ProjectGenerator;
use pyo3::prelude::*;

#[pyfunction]
fn generate_project_from_json_file_content(json_file_content: String) {
    let game_data = match GameData::parse(json_file_content) {
        Err(err_msg) => {
            log_error(err_msg);
            return;
        }
        Ok(data) => data,
    };

    log_cli_start_message("Generating", &game_data.pymodd_project_name());
    match ProjectGenerator::generate(game_data, |file| {
        log_success(&format!("{} written", file.path.to_str().unwrap()))
    }) {
        Err(err_msg) => {
            log_error(err_msg);
            log_cli_end_message("generation", false);
        }
        Ok(_) => log_cli_end_message("generation", true),
    }
}

#[pyfunction]
pub fn log_success(message: &str) {
    println!(" {} {}", "-".dark_green(), message);
}

#[pyfunction]
pub fn log_error(message: &str) {
    println!(" {} {}", "x".dark_red(), message.red().underlined());
}

#[pyfunction]
pub fn log_cli_start_message(action: &str, pymodd_project_name: &str) {
    println!(
        "\n{action} pymodd project, {}...",
        pymodd_project_name.underlined()
    );
}

#[pyfunction]
pub fn log_cli_end_message(completed_action: &str, ended_successfully: bool) {
    println!(
        "\n{} completed {completed_action}!\n",
        match ended_successfully {
            true => "successfully",
            false => "unsuccessfully",
        }
        .dark_green()
    );
}

#[pymodule]
fn _pymodd_helper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(
        generate_project_from_json_file_content,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(log_success, m)?)?;
    m.add_function(wrap_pyfunction!(log_error, m)?)?;
    m.add_function(wrap_pyfunction!(log_cli_start_message, m)?)?;
    m.add_function(wrap_pyfunction!(log_cli_end_message, m)?)?;
    Ok(())
}
