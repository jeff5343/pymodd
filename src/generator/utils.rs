use heck::ToLowerCamelCase;

use crate::game_data::variables::{
    SEPERATED_VARIABLE_CATEGORIES, VARIABLES_CATEGORY, VARIABLE_CATEGORIES,
};

pub(crate) fn is_valid_class_name(class_name: &str) -> bool {
    !(class_name.is_empty()
        || string_starts_with_number(&class_name)
        || type_conflicts_with_class_name(&class_name))
}

fn string_starts_with_number(string: &str) -> bool {
    string.chars().next().unwrap().is_numeric()
}

fn type_conflicts_with_class_name(class_name: &str) -> bool {
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

#[cfg(test)]
mod tests {
    use crate::generator::utils::{is_valid_class_name, surrounding_quote_for_string};

    #[test]
    fn valid_class_name_for_seperated_variables_category_name() {
        assert!(!is_valid_class_name(&"Regions"));
    }

    #[test]
    fn valid_class_name_for_variables_category_name() {
        assert!(!is_valid_class_name(&"Dialogues"));
    }

    #[test]
    fn valid_class_name_for_string_starting_with_number() {
        assert!(!is_valid_class_name(&"2BananaSword"));
    }

    #[test]
    fn valid_class_name_for_regular_string() {
        assert!(is_valid_class_name(&"AppleGun"));
    }

    #[test]
    fn surrounding_quote_for_multiline_string() {
        assert_eq!(surrounding_quote_for_string("Hi\nthere"), "'''");
    }

    #[test]
    fn surrounding_quote_for_single_quote_string() {
        assert_eq!(
            surrounding_quote_for_string("bob's apples taste delicious"),
            "\""
        );
    }

    #[test]
    fn surrounding_quote_for_regular_string() {
        assert_eq!(surrounding_quote_for_string("my name is bob"), "'");
    }
}
