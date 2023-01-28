use serde_json::{map::Values, Map, Value};

use super::actions::{Action, self};

static UNDEFINED_STRING: &str = "UNDEFINED";

#[derive(Debug, PartialEq, Eq)]
pub struct Directory {
    children: Vec<GameItem>,
    name: String,
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

// `parent_name: None` represents the root
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

#[derive(Debug, PartialEq, Eq)]
pub struct Script {
    actions: Vec<Action>,
    name: String,
    key: String,
}

impl Script {
    fn new(name: &str, key: &str, actions: Vec<Action>) -> Script {
        Script {
            name: name.to_string(),
            key: key.to_string(),
            actions,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
enum GameItem {
    Dir(Directory),
    Script(Script),
}

impl GameItem {
    fn parse(item_data: &Value) -> GameItem {
        match item_data.get("actions") {
            Some(actions) => GameItem::Script(Script {
                actions: actions::parse_actions(actions.as_array().unwrap_or(&Vec::new())),
                name: parse_item_key_to_string(&item_data, "name"),
                key: parse_item_key_to_string(&item_data, "key"),
            }),
            None => GameItem::Dir(Directory {
                children: Vec::new(),
                name: parse_item_key_to_string(&item_data, "folderName"),
                key: parse_item_key_to_string(&item_data, "key"),
            }),
        }
    }
}

fn parse_item_key_to_string(item_data: &Value, key: &str) -> String {
    item_data
        .get(key)
        .unwrap_or(&Value::Null)
        .as_str()
        .unwrap_or(UNDEFINED_STRING)
        .to_string()
}

#[cfg(test)]
mod directory_tests {
    use serde_json::{json, Value};

    use crate::game_data::directory::{
        root_children_from_scripts_data, Directory, GameItem, Script, UNDEFINED_STRING,
    };

    use super::filter_out_children_of_parent;

    #[test]
    fn parse_directory() {
        assert_eq!(
            root_children_from_scripts_data(&json!({
                "31IAD2B": { "folderName": "utils", "key": "31IAD2B", "parent": None::<&str>, "order": 2 },
                "Q31E2RS": { "name": "check_players", "key": None::<&str>, "actions": [], "parent": "31IAD2B", "order": 2 },
                "SDUW31W": { "name": "change_state", "key": "SDUW31W", "actions": [], "parent": "31IAD2B", "order": 1 },
                "HWI31WQ": { "folderName": "other", "key": "HWI31WQ", "parent": "31IAD2B", "order": 3 },
                "JK32Q03": { "name": "destroy_server", "key": "JK32Q03", "actions": [], "parent": "HWI31WQ", "order": 1},
                "WI31HDK": { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": None::<&str>, "order": 1},
            })).as_slice(),
            [
                GameItem::Script(Script::new("initialize", "WI31HDK", Vec::new())),
                GameItem::Dir(Directory::new("utils", "31IAD2B", vec![
                    GameItem::Script(Script::new("change_state", "SDUW31W", Vec::new())),
                    GameItem::Script(Script::new("check_players", UNDEFINED_STRING, Vec::new())),
                    GameItem::Dir(Directory::new("other", "HWI31WQ", vec![
                        GameItem::Script(Script::new("destroy_server", "JK32Q03", Vec::new())),
                    ])),
                ])),
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
                GameItem::Script(Script::new("change_state", "SDUW31W", Vec::new())),
                GameItem::Script(Script::new("check_players", "FWJ31WD", Vec::new())),
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
