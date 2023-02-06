use heck::ToPascalCase;
use serde_json::{map::Values, Map, Value};

use crate::generator::utils::is_valid_class_name;

use super::actions::{self, Action};

static UNDEFINED_STRING: &str = "UNDEFINED";

#[derive(Debug, PartialEq, Eq)]
pub enum GameItem {
    Dir(Directory),
    Script(Script),
    DirectoryEnd,
}

fn parse_key_of_item_to_string(key: &str, item_data: &Value) -> String {
    item_data
        .get(key)
        .unwrap_or(&Value::Null)
        .as_str()
        .unwrap_or(UNDEFINED_STRING)
        .to_string()
}

impl GameItem {
    fn parse(item_data: &Value) -> GameItem {
        match item_data.get("actions") {
            Some(actions) => GameItem::Script(Script {
                name: parse_key_of_item_to_string("name", &item_data),
                key: parse_key_of_item_to_string("key", &item_data),
                triggers: item_data
                    .get("triggers")
                    .unwrap_or(&Value::Null)
                    .as_array()
                    .unwrap_or(&Vec::new())
                    .into_iter()
                    .map(|trigger| parse_key_of_item_to_string("type", &trigger))
                    .collect(),
                actions: actions::parse_actions(actions.as_array().unwrap_or(&Vec::new())),
            }),
            None => GameItem::Dir(Directory {
                children: Vec::new(),
                name: parse_key_of_item_to_string("folderName", &item_data),
                key: parse_key_of_item_to_string("key", &item_data),
            }),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct Directory {
    pub children: Vec<GameItem>,
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

    fn new(name: &str, key: &str, children: Vec<GameItem>) -> Directory {
        Directory {
            name: name.to_string(),
            key: key.to_string(),
            children,
        }
    }
}

fn root_children_from_scripts_data(scripts: &Value) -> Vec<GameItem> {
    let empty_map = Map::new();
    let mut items: Vec<&Value> =
        sort_based_on_order(scripts.as_object().unwrap_or(&empty_map).values());

    // filter out root level scripts and directories
    let mut children = filter_out_children_of_parent(&mut items, None);

    let mut stack: Vec<&mut GameItem> = children.iter_mut().collect();
    while stack.len() > 0 {
        if let GameItem::Dir(directory) = stack.pop().unwrap() {
            directory.children.extend(filter_out_children_of_parent(
                &mut items,
                Some(&directory.key),
            ));

            stack.extend(
                directory
                    .children
                    .iter_mut()
                    .collect::<Vec<&mut GameItem>>(),
            );
        }
    }
    children
}

fn sort_based_on_order(items: Values) -> Vec<&Value> {
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

/// `parent_name: None` represents the root
fn filter_out_children_of_parent(
    items: &mut Vec<&Value>,
    parent_key: Option<&str>,
) -> Vec<GameItem> {
    let mut children = Vec::new();
    items.retain(|item| {
        let item_parent = item.get("parent").unwrap_or(&Value::Null).as_str();
        if item_parent == parent_key {
            children.push(GameItem::parse(&item));
            return false;
        }
        true
    });
    children
}

impl<'a> IntoIterator for &'a Directory {
    type Item = &'a GameItem;
    type IntoIter = DirectoryIterator<'a>;

    fn into_iter(self) -> Self::IntoIter {
        DirectoryIterator::new(&self)
    }
}

pub struct DirectoryIterator<'a> {
    stack: Vec<&'a GameItem>,
}

impl<'a> DirectoryIterator<'a> {
    fn new(directory: &'a Directory) -> DirectoryIterator<'a> {
        DirectoryIterator {
            stack: directory.children.iter().collect(),
        }
    }
}

impl<'a> Iterator for DirectoryIterator<'a> {
    type Item = &'a GameItem;

    /// `GameItem::Directory` signifies the start of a directory
    /// `GameItem::DirectoryEnd` signifies the end of a directory
    fn next(&mut self) -> Option<Self::Item> {
        if self.stack.len() == 0 {
            return None;
        }
        let item = self.stack.remove(0);
        match item {
            GameItem::Dir(directory) => {
                self.stack.splice(
                    ..0,
                    directory
                        .children
                        .iter()
                        .chain([GameItem::DirectoryEnd].iter()),
                );
            }
            _ => {}
        }
        Some(&item)
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct Script {
    pub name: String,
    pub key: String,
    pub triggers: Vec<String>,
    pub actions: Vec<Action>,
}

impl Script {
    pub fn class_name(&self) -> String {
        let class_name = self.name.to_pascal_case().to_string();
        if !is_valid_class_name(&class_name) {
            return format!("q{class_name}");
        }
        class_name
    }

    pub fn triggers_to_objects(&self) -> Vec<String> {
        self.triggers
            .iter()
            .map(|trigger| format!("Trigger.{}", enum_name_of_trigger(trigger)))
            .collect()
    }

    pub fn new(name: &str, key: &str, triggers: Vec<&str>, actions: Vec<Action>) -> Script {
        Script {
            name: name.to_string(),
            key: key.to_string(),
            triggers: triggers
                .into_iter()
                .map(|string| string.to_string())
                .collect(),
            actions,
        }
    }
}

fn enum_name_of_trigger(trigger: &str) -> &str {
    trigger
}

#[cfg(test)]
mod tests {
    use serde_json::{json, Value};

    use crate::game_data::directory::{
        root_children_from_scripts_data, Directory, GameItem, Script, UNDEFINED_STRING,
    };

    use super::filter_out_children_of_parent;

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
                GameItem::Script(Script::new("initialize", "WI31HDK", vec!["gameStart"], Vec::new())),
                GameItem::Dir(Directory::new(
                    "utils",
                    "31IAD2B",
                    vec![
                        GameItem::Script(Script::new(
                            "change_state",
                            "SDUW31W",
                            vec![],
                            Vec::new()
                        )),
                        GameItem::Script(Script::new(
                            "check_players",
                            UNDEFINED_STRING,
                            vec!["secondTick"],
                            Vec::new()
                        )),
                        GameItem::Dir(Directory::new(
                            "other",
                            "HWI31WQ",
                            vec![GameItem::Script(Script::new(
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
            filter_out_children_of_parent(&mut items, Some("31IAD2B")).as_slice(),
            [
                GameItem::Script(Script::new(
                    "change_state",
                    "SDUW31W",
                    vec![],
                    Vec::new()
                )),
                GameItem::Script(Script::new(
                    "check_players",
                    "FWJ31WD",
                    vec![],
                    Vec::new()
                )),
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
