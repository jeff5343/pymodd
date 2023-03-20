// holds maps of modd.io object names to their corresponding pymodd class names

use std::collections::HashMap;

use lazy_static::lazy_static;

// pymodd files
const PYMODD_SCRIPT_FILE_CONTENT: &str = include_str!("../../../pymodd/script.py");
const PYMODD_ACTIONS_FILE_CONTENT: &str = include_str!("../../../pymodd/actions.py");
const PYMODD_FUNCTIONS_FILE_CONTENT: &str = include_str!("../../../pymodd/functions.py");

lazy_static! {
    // enum maps
    pub static ref TRIGGERS_TO_PYMODD_ENUM: HashMap<String, String> = generate_to_pymodd_enums_map_for_type("Trigger", PYMODD_SCRIPT_FILE_CONTENT);
    pub static ref UI_TARGET_CONSTANTS_TO_PYMODD_ENUM:HashMap<String, String> = generate_to_pymodd_enums_map_for_type("UiTarget", PYMODD_SCRIPT_FILE_CONTENT);
    pub static ref FLIP_CONSTANTS_TO_PYMODD_ENUM:HashMap<String, String> = generate_to_pymodd_enums_map_for_type("Flip", PYMODD_SCRIPT_FILE_CONTENT);

    // action/function maps
    pub static ref ACTIONS_TO_PYMODD_STRUCTURE: HashMap<String, PymoddStructure> = generate_actions_to_pymodd_structure_map();
    pub static ref FUNCTIONS_TO_PYMODD_STRUCTURE: HashMap<String, PymoddStructure> = generate_functions_to_pymodd_structure_map();
}

#[derive(Debug, PartialEq, Eq)]
pub struct PymoddStructure {
    pub name: String,
    pub parameters: Vec<String>,
}

impl PymoddStructure {
    pub fn new(name: &str, args: Vec<&str>) -> PymoddStructure {
        PymoddStructure {
            name: name.to_string(),
            parameters: args.into_iter().map(|arg| arg.to_string()).collect(),
        }
    }
}

impl Default for PymoddStructure {
    fn default() -> Self {
        PymoddStructure::new("None", Vec::new())
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
fn generate_actions_to_pymodd_structure_map() -> HashMap<String, PymoddStructure> {
    let mut actions_to_structure: HashMap<String, PymoddStructure> = HashMap::new();
    let action_functions: Vec<&str> = PYMODD_ACTIONS_FILE_CONTENT
        .split("\n\n\n")
        .skip(3)
        .collect();
    action_functions.into_iter().for_each(|function_content| {
        actions_to_structure.insert(
            parse_action_name_of_pymodd_action_function(&function_content),
            parse_pymodd_structure_of_pymodd_action_function(&function_content),
        );
    });
    actions_to_structure
}

fn parse_action_name_of_pymodd_action_function(action_function_content: &str) -> String {
    strip_quotes(
        &action_function_content
            .lines()
            .find(|line| line.contains("'type': "))
            .expect("action's type could not be found")
            .split("'type': ")
            .last()
            .unwrap()
            .trim()
            .strip_suffix(",")
            .expect("action's type does not trail with a comma"),
    )
}

fn parse_pymodd_structure_of_pymodd_action_function(
    action_function_content: &str,
) -> PymoddStructure {
    let parameters = action_function_content
        .lines()
        .find(|line| line.contains("def "))
        .expect("function not defined for action")
        .trim()
        .strip_suffix("):")
        .unwrap()
        .split(['(', ','])
        .skip(1)
        .take_while(|arg| !arg.contains("comment=None"))
        .map(|parameter| parameter.trim().to_string())
        .collect();
    PymoddStructure {
        name: parse_function_name(action_function_content),
        parameters,
    }
}

// FUNCTIONS
fn generate_functions_to_pymodd_structure_map() -> HashMap<String, PymoddStructure> {
    let mut functions_to_structure: HashMap<String, PymoddStructure> = HashMap::new();

    // Condition class is formatted differently from the other classes
    functions_to_structure.insert(
        String::from("condition"),
        PymoddStructure::new("Condition", vec!["item_a", "operator", "item_b"]),
    );

    let function_classes: Vec<&str> = PYMODD_FUNCTIONS_FILE_CONTENT
        .split("\n\n\n")
        .skip(5)
        .collect();
    function_classes.into_iter().for_each(|class_content| {
        // skip over invalid classes
        if class_content.contains("self.options = ") {
            functions_to_structure.insert(
                parse_function_type_of_pymodd_function_class(&class_content),
                parse_pymodd_structure_of_pymodd_function_class(&class_content),
            );
        }
    });
    functions_to_structure
}

fn parse_function_type_of_pymodd_function_class(function_class_content: &str) -> String {
    strip_quotes(
        &function_class_content
            .lines()
            .find(|line| line.contains("self.function = "))
            .expect("function's type could not be found")
            .split(" = ")
            .last()
            .unwrap(),
    )
}

fn parse_pymodd_structure_of_pymodd_function_class(
    function_class_content: &str,
) -> PymoddStructure {
    let parameters = function_class_content
        .lines()
        .find(|line| line.contains("def __init__("))
        .unwrap_or("")
        .trim()
        .replace("):", "")
        .split(['(', ','])
        .skip(2)
        .map(|parameter| parameter.trim().to_string())
        .collect();
    PymoddStructure {
        name: parse_class_name(function_class_content),
        parameters,
    }
}

// HELPER FUNCTIONS
fn parse_function_name(function_content: &str) -> String {
    function_content
        .lines()
        .find(|line| line.starts_with("def "))
        .expect("function name line could not be found")
        .strip_prefix("def ")
        .unwrap()
        .split("(")
        .next()
        .expect("function name could not be parsed")
        .to_string()
}

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

fn strip_quotes(string: &str) -> String {
    let string = string.trim();
    let left_quote_removed = string.strip_prefix(['\'', '"']).unwrap_or(string);
    left_quote_removed
        .strip_suffix(['\'', '"'])
        .unwrap_or(left_quote_removed)
        .to_string()
}

#[cfg(test)]
mod tests {
    use crate::project_generator::utils::to_pymodd_maps::{
        parse_pymodd_structure_of_pymodd_action_function,
        parse_pymodd_structure_of_pymodd_function_class, PymoddStructure,
    };

    #[test]
    fn parse_action_class() {
        assert_eq!(
            parse_pymodd_structure_of_pymodd_action_function(
                "@action\n\
                def set_player_variable(player, variable_type, value, comment=None, disabled=False, run_on_client=False):\n\
                    \treturn {\n\
                        \t\t'type': 'setPlayerVariable',\n\
                        \t\t'player': to_dict(player),\n\
                        \t\t'variable': to_dict(variable_type),\n\
                        \t\t'value': to_dict(value)\n\
                    \t}"
            ),
            PymoddStructure::new(
                "set_player_variable",
                vec!["player", "variable_type", "value"]
            ));
        assert_eq!(
            parse_pymodd_structure_of_pymodd_action_function(
                "@action\n\
                def end_game(comment=None, disabled=False, run_on_client=False):\n\
                    \treturn {\n\
                        \t\t'type': 'endGame',\n\
                    \t}"
            ),
            PymoddStructure::new("end_game", vec![])
        );
    }

    #[test]
    fn parse_function_class() {
        assert_eq!(
            parse_pymodd_structure_of_pymodd_function_class(
                "class PlayerFromId(Player):\n\
                    \tdef __init__(self, string):\n\
                    \t\tself.function = 'getPlayerFromId'\n\
                    \t\tself.options = {\n\
                        \t\t\t'string': to_dict(string),\n\
                    \t\t}"
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
