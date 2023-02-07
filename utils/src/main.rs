//! generates maps of modd.io object names to their corresponding pymodd class names
//! generated maps are used by the pymodd project generator

use std::{
    fs::{self, File},
    io::{BufWriter, Write},
};

use phf_codegen::OrderedMap;

fn main() {
    let mut file = BufWriter::new(File::create("output.rs").unwrap());
    let mut content = String::new();
    content.push_str(
        format!(
            "static TRIGGERS: phf::OrderedMap<&'static str, &'static str> = {};\n",
            parse_triggers_map().build()
        )
        .as_str(),
    );
    write!(&mut file, "{}", content).unwrap();
}

// fn print_pythonified_map(map: &<String, String>) {
//     println!(
//         "{{\n{}}}",
//         map.iter()
//             .map(|(modd_name, enum_name)| format!("\t'{modd_name}': '{enum_name}',\n"))
//             .collect::<String>()
//     );
// }

fn parse_triggers_map() -> OrderedMap<String> {
    let mut trigger_to_enum = OrderedMap::new();
    parse_class_content_from_file("Trigger", &read_pymodd_file("script.py"))
        .lines()
        .for_each(|line| match line.split_once("=") {
            Some((enum_name, modd_name)) => {
                trigger_to_enum.entry(strip_quotes(modd_name), strip_quotes(enum_name).as_str());
            }
            None => {}
        });
    trigger_to_enum
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
    let path = format!("../pymodd/{path}");
    fs::read_to_string(path).expect("could not read file")
}

fn strip_quotes(string: &str) -> String {
    let string = string.trim();
    let left_quote_removed = string.strip_prefix(['\'', '"']).unwrap_or(string);
    left_quote_removed
        .strip_suffix(['\'', '"'])
        .unwrap_or(left_quote_removed)
        .to_string()
}
