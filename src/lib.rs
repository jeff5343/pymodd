mod game_data;
mod generator;

use game_data::GameData;
use generator::Generator;
use pyo3::prelude::*;

#[pyfunction]
fn generate_project(game_data: String) {
    Generator::generate(GameData::parse(game_data));
}

#[pymodule]
fn pymodd_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_project, m)?)?;
    Ok(())
}
