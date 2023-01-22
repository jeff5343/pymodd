use serde_json::Value;

enum GameItem {
    Dir(Directory),
    Script(Script),
}

pub struct Directory {
    items: Vec<Box<GameItem>>,
    name: String,
    id: String,
}

impl Directory {
    pub fn parse(scripts: &Value) -> Directory {
        Directory {
            items: vec![],
            name: String::from(""),
            id: String::from(""),
        }
    }
}

struct Script {
    data: Value,
    name: String,
    id: String,
}
