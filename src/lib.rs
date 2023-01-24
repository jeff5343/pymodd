mod game_data;

use pyo3::prelude::*;
use game_data::GameData;

#[pyfunction]
fn generate_project(game_data: String) {
    let game_data = GameData::parse(game_data);
}

#[pymodule]
fn pymodd_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_project, m)?)?;
    Ok(())
}
