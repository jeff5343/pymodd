use serde_json::{map::Values, Map, Value};

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
    let mut children: Vec<GameItem> = Vec::new();

    let empty_map = Map::new();
    let mut items: Vec<&Value> =
        sort_based_on_order(scripts.as_object().unwrap_or(&empty_map).values());

    children.extend(filter_out_children(&mut items, None));

    let mut stack: Vec<&mut GameItem> = children.iter_mut().collect();
    while stack.len() > 0 {
        if let GameItem::Dir(directory) = stack.pop().unwrap() {
            directory
                .children
                .extend(filter_out_children(&mut items, Some(&directory.key)));

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
            .get_or_null("order")
            .as_i64()
            .unwrap_or(-1)
            .cmp(&item_b.get_or_null("order").as_i64().unwrap_or(-1))
    });
    items
}

// `parent_name: None` represents the root
fn filter_out_children(items: &mut Vec<&Value>, parent_key: Option<&str>) -> Vec<GameItem> {
    let mut children = Vec::new();
    items.retain(|item| {
        let item_parent = item.get_or_null("parent").as_str();
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
    actions: Vec<Value>,
    name: String,
    key: String,
}

impl Script {
    fn new(name: &str, key: &str, actions: Vec<Value>) -> Script {
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
                actions: actions.as_array().unwrap_or(&Vec::new()).clone(),
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
        .get_or_null(key)
        .as_str()
        .unwrap_or("UNDEFINED")
        .to_string()
}

trait GetOrNull {
    fn get_or_null(&self, key: &str) -> &Value;
}

impl GetOrNull for Value {
    fn get_or_null(&self, key: &str) -> &Value {
        self.get(key).unwrap_or(&Value::Null)
    }
}

#[cfg(test)]
mod directory_tests {
    use serde_json::json;

    use crate::game_data::directory::{
        root_children_from_scripts_data, Directory, GameItem, Script,
    };

    #[test]
    fn parse_directory() {
        assert_eq!(
            root_children_from_scripts_data(&json!({
                "31IAD2B": { "folderName": "utils", "key": "31IAD2B", "parent": None::<&str> },
                "Q31E2RS": { "name": "check_players", "key": "Q31E2RS", "actions": [], "parent": "31IAD2B" },
                "SDUW31W": { "name": "change_state", "key": "SDUW31W", "actions": [], "parent": "31IAD2B" },
                "WI31HDK": { "name": "initialize", "key": "WI31HDK", "actions": [], "parent": None::<&str>},
            })).as_slice(),
            [
                GameItem::Dir(Directory::new("utils", "31IAD2B", vec![
                               GameItem::Script(Script::new("check_players", "Q31E2RS", Vec::new())),
                               GameItem::Script(Script::new("change_state", "SDUW31W", Vec::new()))
                ])),
                GameItem::Script(Script::new("initialize", "WI31HDK", Vec::new())),
            ]
        );
    }
}
