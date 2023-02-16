pub mod iterators;
pub mod to_pymodd;

use heck::ToLowerCamelCase;

use crate::game_data::variable_categories::{
    SEPERATED_VARIABLE_CATEGORIES, VARIABLES_CATEGORY, VARIABLE_CATEGORIES,
};

pub(crate) fn is_valid_class_name(class_name: &str) -> bool {
    !(class_name.is_empty()
        || string_starts_with_a_number(&class_name)
        || type_conflicts_with_a_category_class_name(&class_name))
}

fn string_starts_with_a_number(string: &str) -> bool {
    string.chars().next().unwrap().is_numeric()
}

fn type_conflicts_with_a_category_class_name(class_name: &str) -> bool {
    SEPERATED_VARIABLE_CATEGORIES
        .into_iter()
        .chain([VARIABLES_CATEGORY])
        .collect::<Vec<&str>>()
        .contains(&class_name.to_lower_camel_case().as_str())
        || VARIABLE_CATEGORIES.contains(&class_name.to_lower_camel_case().as_str())
}

pub(crate) fn surround_string_with_quotes(string: &str) -> String {
    let quote = surrounding_quote_for_string(string);
    format!("{quote}{string}{quote}")
}

fn surrounding_quote_for_string(string: &str) -> &str {
    if string.contains(['"', '`', '\n']) {
        return "'''";
    } else if string.contains('\'') {
        return "\"";
    }
    "'"
}

pub(crate) fn strip_quotes(string: &str) -> String {
    let string = string.trim();
    let left_quote_removed = string.strip_prefix(['\'', '"']).unwrap_or(string);
    left_quote_removed
        .strip_suffix(['\'', '"'])
        .unwrap_or(left_quote_removed)
        .to_string()
}

#[cfg(test)]
mod tests {
    use crate::generator::utils::{is_valid_class_name, surrounding_quote_for_string};

    #[test]
    fn valid_class_name() {
        assert!(is_valid_class_name(&"AppleGun"));
        // seperated variables category name
        assert!(!is_valid_class_name(&"Regions"));
        // variables category name
        assert!(!is_valid_class_name(&"Dialogues"));
        // string starting with number
        assert!(!is_valid_class_name(&"2BananaSword"));
    }

    #[test]
    fn string_surrounding_quotes() {
        // string with no special characters
        assert_eq!(surrounding_quote_for_string("my name is bob"), "'");
        // multiline string
        assert_eq!(surrounding_quote_for_string("Hi\nthere"), "'''");
        // string with single quote
        assert_eq!(
            surrounding_quote_for_string("bob's apples taste delicious"),
            "\""
        );
    }
}