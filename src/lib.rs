mod game_data;
mod project_generator;

use game_data::GameData;
use project_generator::ProjectGenerator;
use pyo3::prelude::*;

#[pyfunction]
fn generate_project(game_data: String) {
    ProjectGenerator::generate(GameData::parse(game_data));
}

#[pymodule]
fn pymodd_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_project, m)?)?;
    Ok(())
}
