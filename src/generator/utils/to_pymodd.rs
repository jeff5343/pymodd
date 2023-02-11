//! holds maps of modd.io object names to their corresponding pymodd class names

use std::{collections::HashMap, fs};

use lazy_static::lazy_static;

use super::strip_quotes;

lazy_static! {
    // enum maps
    static ref SCRIPTS_FILE_CONTENT: String = read_pymodd_file("script.py");
    pub static ref TRIGGERS_TO_PYMODD_ENUMS: HashMap<String, String> = generate_to_pymodd_enums_map_for_type("Trigger", &SCRIPTS_FILE_CONTENT);
    pub static ref CONSTANTS_TO_PYMODD_ENUMS: HashMap<String, String> = generate_to_pymodd_enums_map_for_type("UiTarget", &SCRIPTS_FILE_CONTENT)
        .into_iter()
        .chain(generate_to_pymodd_enums_map_for_type("Flip", &SCRIPTS_FILE_CONTENT))
        .collect();

    // action/function maps
    pub static ref ACTIONS_TO_PYMODD_STRUCTURES: HashMap<String, PymoddStructure> = generate_actions_to_pymodd_structures_map();
    pub static ref FUNCTIONS_TO_PYMODD_STRUCTURES: HashMap<String, PymoddStructure> = generate_functions_to_pymodd_structures_map();
}

#[derive(Debug, PartialEq, Eq)]
pub struct PymoddStructure {
    pub name: String,
    pub args: Vec<String>,
}

impl PymoddStructure {
    fn new(name: &str, args: Vec<&str>) -> PymoddStructure {
        PymoddStructure {
            name: name.to_string(),
            args: args.into_iter().map(|arg| arg.to_string()).collect(),
        }
    }
}

// CONSTANTS
fn generate_to_pymodd_enums_map_for_type(
    type_name: &str,
    file_content: &str,
) -> HashMap<String, String> {
    let mut modd_names_to_pymodd_enums: HashMap<String, String> = HashMap::new();
    parse_class_content_from_file(type_name, file_content)
        .lines()
        .for_each(|line| match line.split_once("=") {
            Some((enum_name, modd_name)) => {
                modd_names_to_pymodd_enums.insert(
                    strip_quotes(modd_name),
                    strip_quotes(&format!("{type_name}.{}", enum_name.trim())),
                );
            }
            None => {}
        });
    modd_names_to_pymodd_enums
}

// ACTIONS
fn generate_actions_to_pymodd_structures_map() -> HashMap<String, PymoddStructure> {
    let mut actions_to_structures: HashMap<String, PymoddStructure> = HashMap::new();
    // IfStatement class is formatted differently from the other classes
    actions_to_structures.insert(
        String::from("condition"),
        PymoddStructure::new("IfStatement", vec!["conditions", "then", "else"]),
    );

    let actions_file = read_pymodd_file("actions.py");
    let action_classes: Vec<&str> = actions_file.split("\n\n\n").skip(3).collect();
    action_classes.into_iter().for_each(|class_content| {
        actions_to_structures.insert(
            parse_action_type_of_pymodd_action_class(&class_content),
            parse_pymodd_structure_of_pymodd_action_class(&class_content),
        );
    });

    actions_to_structures
}

fn parse_action_type_of_pymodd_action_class(action_class_content: &str) -> String {
    strip_quotes(
        &action_class_content
            .lines()
            .find(|line| line.contains("self.action = "))
            .expect("action's type could not be found")
            .split(" = ")
            .last()
            .unwrap(),
    )
}

fn parse_pymodd_structure_of_pymodd_action_class(action_class_content: &str) -> PymoddStructure {
    let args = action_class_content
        .lines()
        .filter(|line| line.contains("': ")) // find dictionary entries
        .map(|line| strip_quotes(&line.split(":").next().unwrap()))
        .collect();
    PymoddStructure {
        name: parse_class_name(action_class_content),
        args,
    }
}

// FUNCTIONS
fn generate_functions_to_pymodd_structures_map() -> HashMap<String, PymoddStructure> {
    let mut functions_to_structures: HashMap<String, PymoddStructure> = HashMap::new();

    let functions_file = read_pymodd_file("functions.py");
    let function_classes: Vec<&str> = functions_file.split("\n\n\n").skip(3).collect();
    function_classes.into_iter().for_each(|class_content| {
        // skip over empty classes
        if class_content.contains("self.options = ") {
            functions_to_structures.insert(
                parse_function_type_of_pymodd_function_class(&class_content),
                parse_pymodd_structure_of_pymodd_function_class(&class_content),
            );
        }
    });
    functions_to_structures
}

fn parse_function_type_of_pymodd_function_class(function_class_content: &str) -> String {
    strip_quotes(
        &function_class_content
            .lines()
            .find(|line| line.contains("self.function = "))
            .expect("action's type could not be found")
            .split(" = ")
            .last()
            .unwrap(),
    )
}

fn parse_pymodd_structure_of_pymodd_function_class(function_class_content: &str) -> PymoddStructure {
    let args = function_class_content
        .lines()
        .skip_while(|line| !line.contains("self.options"))
        .filter(|line| line.contains("': ")) // find dictionary entries
        .map(|line| strip_quotes(&line.split(":").next().unwrap()))
        .collect();
    PymoddStructure {
        name: parse_class_name(function_class_content),
        args,
    }
}

// HELPER FUNCTIONS
fn parse_class_name(class_content: &str) -> String {
    class_content
        .lines()
        .find(|line| line.starts_with("class "))
        .expect("class line could not be found")
        .split([' ', '('])
        .nth(1)
        .expect("class name could not be parsed")
        .to_string()
}

fn parse_class_content_from_file(class_name: &str, file_content: &str) -> String {
    file_content
        .lines()
        .skip_while(|line| !line.starts_with(&format!("class {class_name}")))
        .skip(1)
        .take_while(|line| !line.starts_with("class"))
        .map(|line| format!("{line}\n"))
        .collect::<String>()
}

fn read_pymodd_file(path: &str) -> String {
    let path = format!("pymodd/{path}");
    fs::read_to_string(path).expect("could not read file")
}

#[cfg(test)]
mod tests {
    use crate::generator::utils::to_pymodd::{
        parse_pymodd_structure_of_pymodd_function_class, parse_pymodd_structure_of_pymodd_action_class,
        PymoddStructure,
    };

    #[test]
    fn parse_action_class() {
        assert_eq!(
            parse_pymodd_structure_of_pymodd_action_class(
                "class SetPlayerVariable(Action):\n\
                    \tdef __init__(self, player, variable_type, value):\n\
                        \t\tself.action = 'setPlayerVariable'\n\
                        \t\tself.options = {\n\
                            \t\t\t'player': to_dict(player),\n\
                            \t\t\t'variable': to_dict(variable_type),\n\
                            \t\t\t'value': to_dict(value),\n\
                        }"
            ),
            PymoddStructure::new("SetPlayerVariable", vec!["player", "variable", "value"])
        );
        assert_eq!(
            parse_pymodd_structure_of_pymodd_action_class(
                "class EndGame(Action):\n\
                    \tdef __init__(self):\n\
                        \t\tself.action = 'endGame'\n\
                        \t\tself.options = {}"
            ),
            PymoddStructure::new("EndGame", vec![])
        );
    }

    #[test]
    fn parse_function_class() {
        assert_eq!(
            parse_pymodd_structure_of_pymodd_function_class(
                "class PlayerFromId(Player):\n\
                    \tself.function = 'getPlayerFromId'\n\
                    \tself.options = {\n\
                        \t\t'string': to_dict(string),\n\
                    \t}"
            ),
            PymoddStructure::new("PlayerFromId", vec!["string"])
        );
        assert_eq!(
            parse_pymodd_structure_of_pymodd_function_class(
                "class Undefined(Function):\n\
                    \tdef __init__(self):\n\
                        \t\tself.function = 'undefinedValue'\n\
                        \t\tself.options = {}"
            ),
            PymoddStructure::new("Undefined", vec![])
        );
    }
}
