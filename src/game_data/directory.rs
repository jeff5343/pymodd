use heck::ToSnakeCase;
use serde_json::{map::Values, Map, Value};

use crate::project_generator::utils::{
    is_valid_class_name, iterators::directory_iterator::DirectoryIterItem,
    to_pymodd_maps::TRIGGERS_TO_PYMODD_ENUM,
};

use super::actions::{self, Action};

const UNDEFINED_STRING: &str = "UNDEFINED";

#[derive(Debug, PartialEq, Eq)]
pub struct Directory {
    pub children: Vec<DirectoryItem>,
    pub name: String,
    key: String,
}

impl Directory {
    pub fn parse(scripts: &Value) -> Directory {
        Directory {
            children: root_children_from_scripts_data(scripts),
            name: String::from("/"),
            key: String::from("root"),
        }
    }

    pub fn is_empty(&self) -> bool {
        self.children.is_empty()
    }

    pub fn find_item_with_key(&self, key: &str) -> Option<DirectoryIterItem> {
        self.iter_flattened().find(|item| match item {
            DirectoryIterItem::StartOfDirectory(dir) => dir.key == key,
            DirectoryIterItem::Script(script) => script.key == key,
            _ => false,
        })
    }
}

fn root_children_from_scripts_data(scripts: &Value) -> Vec<DirectoryItem> {
    let empty_map = Map::new();
    let mut items: Vec<&Value> =
        sort_items_by_order(scripts.as_object().unwrap_or(&empty_map).values());

    // remove root level scripts and directories
    let mut children: Vec<DirectoryItem> = remove_children_of_parent_in_items(None, &mut items)
        .into_iter()
        .map(|val| DirectoryItem::parse(val))
        .collect();

    let mut stack: Vec<&mut DirectoryItem> = children.iter_mut().collect();
    while stack.len() > 0 {
        if let DirectoryItem::Directory(directory) = stack.pop().unwrap() {
            directory.children.extend(
                remove_children_of_parent_in_items(Some(&directory.key), &mut items)
                    .into_iter()
                    .map(|val| DirectoryItem::parse(val)),
            );

            stack.extend(
                directory
                    .children
                    .iter_mut()
                    .collect::<Vec<&mut DirectoryItem>>(),
            );
        }
    }
    // before returning the children, apply some kinda function to find duplicate pymodd script
    // names and change them. or do this in scripts_file.rs on the root directory before parsing
    // scripts? idk this sounds stupid. i like the first idea better.
    children
}

fn sort_items_by_order(items: Values) -> Vec<&Value> {
    let mut items: Vec<&Value> = items.collect();
    items.sort_by(|item_a, item_b| {
        item_a
            .get("order")
            .unwrap_or(&Value::Null)
            .as_i64()
            .unwrap_or(-1)
            .cmp(
                &item_b
                    .get("order")
                    .unwrap_or(&Value::Null)
                    .as_i64()
                    .unwrap_or(-1),
            )
    });
    items
}

/// The key of the root directory is `None`
///
/// Returns the removed children
fn remove_children_of_parent_in_items<'a>(
    parent_key: Option<&str>,
    items: &mut Vec<&'a Value>,
) -> Vec<&'a Value> {
    let mut children = Vec::new();
    items.retain(|&item| {
        let item_parent = item.get("parent").unwrap_or(&Value::Null).as_str();
        if item_parent == parent_key {
            children.push(item);
            return false;
        }
        true
    });
    children
}

#[derive(Debug, PartialEq, Eq)]
pub enum DirectoryItem {
    Directory(Directory),
    Script(Script),
}

fn parse_key_of_item_to_string(key: &str, item_data: &Value) -> String {
    item_data
        .get(key)
        .unwrap_or(&Value::Null)
        .as_str()
        .unwrap_or(UNDEFINED_STRING)
        .to_string()
}

impl DirectoryItem {
    fn parse(item_data: &Value) -> DirectoryItem {
        match item_data.get("actions") {
            Some(actions) => DirectoryItem::Script({
                Script::new(
                    parse_key_of_item_to_string("name", &item_data),
                    parse_key_of_item_to_string("key", &item_data),
                    item_data
                        .get("triggers")
                        .unwrap_or(&Value::Null)
                        .as_array()
                        .unwrap_or(&Vec::new())
                        .into_iter()
                        .map(|trigger| parse_key_of_item_to_string("type", &trigger))
                        .collect(),
                    actions::parse_actions(actions.as_array().unwrap_or(&Vec::new())),
                )
            }),
            None => DirectoryItem::Directory(Directory {
                children: Vec::new(),
                name: parse_key_of_item_to_string("folderName", &item_data),
                key: parse_key_of_item_to_string("key", &item_data),
            }),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct Script {
    pub name: String,
    pub function_name: String,
    pub key: String,
    pub triggers: Vec<String>,
    pub actions: Vec<Action>,
}

impl Script {
    fn new(name: String, key: String, triggers: Vec<String>, actions: Vec<Action>) -> Script {
        Script {
            function_name: Script::function_name_of(&name).unwrap_or(key.to_lowercase()),
            name,
            key,
            triggers,
            actions,
        }
    }

    fn function_name_of(name: &str) -> Option<String> {
        let function_name = name
            .replace(
                |c: char| !(c.is_alphabetic() || c.is_digit(10) || [' ', '_'].contains(&c)),
                "",
            )
            .to_snake_case();
        if function_name.is_empty() {
            return None;
        }
        if !is_valid_class_name(&function_name) {
            Some(format!("_{function_name}"))
        } else {
            Some(function_name)
        }
    }

    pub fn triggers_into_pymodd_enums(&self) -> Vec<String> {
        self.triggers
            .iter()
            .map(|trigger| {
                TRIGGERS_TO_PYMODD_ENUM
                    .get(trigger)
                    .unwrap_or(&String::from("None"))
                    .clone()
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use serde_json::{json, Value};

    use crate::game_data::{
        actions::Action,
        directory::{
            root_children_from_scripts_data, Directory, DirectoryItem, Script, UNDEFINED_STRING,
        },
    };

    use super::remove_children_of_parent_in_items;

    impl Directory {
        pub fn new(name: &str, key: &str, children: Vec<DirectoryItem>) -> Directory {
            Directory {
                name: name.to_string(),
                key: key.to_string(),
                children,
            }
        }
    }

    impl Script {
        /// q (quick) new function
        pub fn qnew(name: &str, key: &str, triggers: Vec<&str>, actions: Vec<Action>) -> Script {
            Script::new(
                name.to_string(),
                key.to_string(),
                triggers
                    .into_iter()
                    .map(|string| string.to_string())
                    .collect(),
                actions,
            )
        }
    }

    #[test]
    fn parse_directory() {
        assert_eq!(
            root_children_from_scripts_data(&json!({
                "31IAD2B": { "triggers": [], "folderName": "utils",
                                "key": "31IAD2B", "parent": None::<&str>, "order": 2 },
                "Q31E2RS": { "triggers": [ { "type": "secondTick" } ], "name": "check_players",
                                "key": None::<&str>, "actions": [], "parent": "31IAD2B", "order": 2 },
                "SDUW31W": { "triggers": [], "name": "change_state",
                                "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 },
                "HWI31WQ": { "triggers": [], "folderName": "other",
                                "key": "HWI31WQ", "parent": "31IAD2B", "order": 3 },
                "JK32Q03": { "triggers": [], "name": "destroy_server",
                                "key": "JK32Q03", "actions": [], "parent": "HWI31WQ", "order": 1},
                "WI31HDK": { "triggers": [ { "type": "gameStart"} ], "name": "initialize",
                                "key": "WI31HDK", "actions": [], "parent": None::<&str>, "order": 1},
            }))
            .as_slice(),
            [
                DirectoryItem::Script(Script::qnew("initialize", "WI31HDK", vec!["gameStart"], Vec::new())),
                DirectoryItem::Directory(Directory::new(
                    "utils",
                    "31IAD2B",
                    vec![
                        DirectoryItem::Script(Script::qnew(
                            "change_state",
                            "SDUW31W",
                            vec![],
                            Vec::new()
                        )),
                        DirectoryItem::Script(Script::qnew(
                            "check_players",
                            UNDEFINED_STRING,
                            vec!["secondTick"],
                            Vec::new()
                        )),
                        DirectoryItem::Directory(Directory::new(
                            "other",
                            "HWI31WQ",
                            vec![DirectoryItem::Script(Script::qnew(
                                "destroy_server",
                                "JK32Q03",
                                vec![],
                                Vec::new()
                            )),]
                        )),
                    ]
                )),
            ]
        );
    }

    #[test]
    fn filter_out_children_of_parent_from_items() {
        let data = &mut json!([
           { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": None::<&str>, "order": 1},
           { "name": "change_state", "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 },
           { "name": "check_players", "key": "FWJ31WD", "actions": [], "parent": "31IAD2B", "order": 2 },
        ]);
        let mut items: Vec<&Value> = data.as_array().unwrap().iter().collect();

        assert_eq!(
            remove_children_of_parent_in_items(Some("31IAD2B"), &mut items)
                .into_iter()
                .map(|val| DirectoryItem::parse(val))
                .collect::<Vec<DirectoryItem>>()
                .as_slice(),
            [
                DirectoryItem::Script(Script::qnew("change_state", "SDUW31W", vec![], Vec::new())),
                DirectoryItem::Script(Script::qnew("check_players", "FWJ31WD", vec![], Vec::new())),
            ]
        );
        assert_eq!(
            items.as_slice(),
            json!([
               { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": None::<&str>, "order": 1},
            ]).as_array().unwrap().iter().collect::<Vec<&Value>>().as_slice(),
        );
    }
}
