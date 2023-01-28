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


