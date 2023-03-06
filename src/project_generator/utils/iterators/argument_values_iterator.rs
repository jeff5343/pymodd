use serde_json::Value;

use crate::game_data::{
    actions::Action,
    argument::{Argument, ArgumentValue, Function},
};

impl Action {
    pub fn iter_flattened_argument_values(&self) -> ArgumentValuesIterator {
        ArgumentValuesIterator::new(self)
    }
}

pub struct ArgumentValuesIterator<'a> {
    stack: Vec<ArgumentValueIterItem<'a>>,
}

impl<'a> ArgumentValuesIterator<'a> {
    fn new(action: &Action) -> ArgumentValuesIterator {
        ArgumentValuesIterator {
            stack: action
                .args
                .iter()
                .map(|arg| ArgumentValueIterItem::from(arg))
                .collect(),
        }
    }

    pub fn from_argument_iter_value(argument: ArgumentValueIterItem) -> ArgumentValuesIterator {
        ArgumentValuesIterator {
            stack: vec![argument],
        }
    }
}

/// Preforms a pre-order traversal on the action's argument values
impl<'a> Iterator for ArgumentValuesIterator<'a> {
    type Item = ArgumentValueIterItem<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.stack.len() == 0 {
            return None;
        }

        let item = self.stack.remove(0);
        if let ArgumentValueIterItem::StartOfFunction(function) = item {
            // chain FunctionEnd on to the end of the function's arguments
            self.stack.splice(
                ..0,
                function
                    .args
                    .iter()
                    .map(|arg| ArgumentValueIterItem::from(arg))
                    .chain([ArgumentValueIterItem::FunctionEnd]),
            );
        }
        Some(item)
    }
}

#[derive(Debug, Eq, PartialEq)]
pub enum ArgumentValueIterItem<'a> {
    StartOfFunction(&'a Function),
    Actions(&'a Vec<Action>),
    Value(&'a Value),
    Condition(&'a Function),
    FunctionEnd,
}

impl<'a> ArgumentValueIterItem<'a> {
    pub fn from(argument: &Argument) -> ArgumentValueIterItem {
        match &argument.value {
            ArgumentValue::Function(function) => match function.name.as_str() {
                "condition" => ArgumentValueIterItem::Condition(function),
                _ => ArgumentValueIterItem::StartOfFunction(&function),
            },
            ArgumentValue::Value(value) => ArgumentValueIterItem::Value(&value),
            ArgumentValue::Actions(actions) => ArgumentValueIterItem::Actions(&actions),
        }
    }
}

#[cfg(test)]
mod tests {
    use serde_json::Value;

    use crate::{
        game_data::{
            actions::Action,
            argument::{Argument, ArgumentValue, Function},
        },
        project_generator::utils::iterators::argument_values_iterator::ArgumentValueIterItem,
    };

    #[test]
    fn flatten_arguments_of_action() {
        assert_eq!(
            Action::new(
                "openShopForPlayer",
                vec![
                    Argument::new(
                        "shop",
                        ArgumentValue::Value(Value::String("OJbEQyc7is".to_string()))
                    ),
                    Argument::new(
                        "player",
                        ArgumentValue::Function(Function::new(
                            "getOwner",
                            vec![Argument::new(
                                "entity",
                                ArgumentValue::Function(Function::new(
                                    "getLastCastingUnit",
                                    Vec::new()
                                ))
                            )]
                        )),
                    ),
                ],
                Some("opens a shop!"),
                false,
                false,
            )
            .iter_flattened_argument_values()
            .collect::<Vec<ArgumentValueIterItem>>()
            .as_slice(),
            [
                ArgumentValueIterItem::Value(&Value::String("OJbEQyc7is".to_string())),
                ArgumentValueIterItem::StartOfFunction(&Function::new(
                    "getOwner",
                    vec![Argument::new(
                        "entity",
                        ArgumentValue::Function(Function::new("getLastCastingUnit", Vec::new()))
                    )]
                )),
                ArgumentValueIterItem::StartOfFunction(&Function::new(
                    "getLastCastingUnit",
                    Vec::new()
                )),
                ArgumentValueIterItem::FunctionEnd,
                ArgumentValueIterItem::FunctionEnd,
            ]
        );
    }

    #[test]
    fn parse_condition_argument() {
        assert_eq!(
            Action::new(
                "condition",
                vec![
                    Argument::new(
                        "conditions",
                        ArgumentValue::Function(Function::new(
                            "condition",
                            vec![
                                Argument::new("item_a", ArgumentValue::Value(Value::Bool(true))),
                                Argument::new(
                                    "operator",
                                    ArgumentValue::Value(Value::String("==".to_string()))
                                ),
                                Argument::new("item_b", ArgumentValue::Value(Value::Bool(true))),
                            ],
                        ))
                    ),
                    Argument::new("then", ArgumentValue::Actions(vec![])),
                    Argument::new("else", ArgumentValue::Actions(vec![])),
                ],
                None,
                false,
                false,
            )
            .iter_flattened_argument_values()
            .collect::<Vec<ArgumentValueIterItem>>()
            .as_slice(),
            [
                ArgumentValueIterItem::Condition(&Function::new(
                    "condition",
                    vec![
                        Argument::new("item_a", ArgumentValue::Value(Value::Bool(true))),
                        Argument::new(
                            "operator",
                            ArgumentValue::Value(Value::String("==".to_string()))
                        ),
                        Argument::new("item_b", ArgumentValue::Value(Value::Bool(true))),
                    ],
                )),
                ArgumentValueIterItem::Actions(&vec![]),
                ArgumentValueIterItem::Actions(&vec![]),
            ]
        );
    }
}
