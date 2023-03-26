//! find and log new actions and functions missing in pymodd

include!("../../src/project_generator/utils/to_pymodd_maps.rs");

use std::fs::File;
use std::io::Write;

use crossterm::style::Stylize;
use heck::ToShoutySnakeCase;
use pymodd_library_validator::{
    fetch_modd_io_functions_and_actions_data, fetch_modd_io_triggers_data,
    generate_action_function_from_object, generate_function_class_from_object, Object, ObjectType,
};
use serde_json::Value;

const EXCLUDED_ACTIONS: [&str; 2] = [
    // these actions do not work in modd.io as of (3/20/2023)
    "addUnitToUnitGroup",
    "addPlayerToPlayerGroup",
];

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("\nFetching modd.io editor data...");
    let mut triggers_data = fetch_modd_io_triggers_data()?;
    let mut functions_and_actions_data = fetch_modd_io_functions_and_actions_data()?;
    let mut modd_objects_data: Vec<Value> = triggers_data
        .as_array_mut()
        .expect("invalid triggers data: cannot parse as an array")
        .to_owned();
    modd_objects_data.append(
        functions_and_actions_data
            .as_array_mut()
            .expect("invalid functions and actions data: cannot parse as an array"),
    );

    println!("\nValidating pymodd library...");
    let (mut missing_triggers, mut missing_actions, mut missing_functions) =
        (Vec::new(), Vec::new(), Vec::new());

    // find missing triggers
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Trigger {
            let trigger_name = object_data
                .get("key")
                .unwrap_or(&Value::Null)
                .as_str()
                .unwrap_or("none");
            if TRIGGERS_TO_PYMODD_ENUM.get(trigger_name) == None {
                missing_triggers.push(trigger_name);
            }
        }
    });

    // find missing actions
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Action {
            let action_object = Object::from_object_data(object_data);
            if ACTIONS_TO_PYMODD_STRUCTURE.get(&action_object.name) == None {
                missing_actions.push(action_object);
            }
        }
    });

    // find missing functions
    modd_objects_data.iter().for_each(|object_data| {
        if ObjectType::from_object_data(object_data) == ObjectType::Function {
            let function_object = Object::from_object_data(object_data);
            if FUNCTIONS_TO_PYMODD_STRUCTURE.get(&function_object.name) == None {
                missing_functions.push(function_object);
            }
        }
    });

    // remove excluded actions from missing actions
    missing_actions = missing_actions
        .into_iter()
        .filter(|action| !EXCLUDED_ACTIONS.contains(&action.name.as_str()))
        .collect();

    // log number of missing triggers
    println!(
        "  missing triggers: {}",
        styled_array_length(missing_triggers.len())
    );
    if !missing_triggers.is_empty() {
        // generate missing trigger enums content in a file
        println!(
            "    {} generating {} content",
            "-".dark_green(),
            "new_triggers.py".on_grey()
        );
        write!(
            File::create("new_triggers.py")?,
            "# auto generated\n\n\n{}\n",
            missing_triggers
                .iter()
                .map(|trigger_name| format!("{} = '{}'\n", trigger_name.to_shouty_snake_case(), trigger_name))
                .collect::<String>()
                .trim_end()
        )?;
    }

    // log number of missing actions
    println!(
        "  missing actions: {}",
        styled_array_length(missing_actions.len())
    );
    if !missing_actions.is_empty() {
        // generate missing action functions content in a file
        println!(
            "    {} generating {} content",
            "-".dark_green(),
            "new_actions.py".on_grey()
        );
        write!(
            File::create("new_actions.py")?,
            "# auto generated\n\n\n{}",
            missing_actions
                .iter()
                .map(|action_object| {
                    format!(
                        "{}\n\n\n",
                        generate_action_function_from_object(action_object)
                    )
                })
                .collect::<String>()
                .trim_end()
        )?;
    }

    // log number of missing functions
    println!(
        "  missing functions: {}",
        styled_array_length(missing_functions.len())
    );
    if !missing_functions.is_empty() {
        // generate missing function classes content in a file
        println!(
            "    {} generating {} content",
            "-".dark_green(),
            "new_functions.py".on_grey()
        );
        write!(
            File::create("new_functions.py")?,
            "# auto generated\n\n\n{}",
            missing_functions
                .iter()
                .map(|function_object| {
                    format!(
                        "{}\n\n\n",
                        generate_function_class_from_object(function_object)
                    )
                })
                .collect::<String>()
                .trim_end()
        )?;
    }

    println!("\nvalidation {}\n", "compelete".dark_green());
    Ok(())
}

fn styled_array_length(length: usize) -> String {
    if length != 0 {
        length.to_string().red()
    } else {
        String::from("0").dark_green()
    }
    .to_string()
}
