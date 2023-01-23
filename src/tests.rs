use crate::game_data::GameData;

#[test]
fn progress_check() {
    // ^ will delete
    let game_data = GameData::parse(
        std::fs::read_to_string("other/Crowdz.io (UNDERWORLD).json").expect("could not read file"),
    );
    println!("name: {}", game_data.name);
    game_data
        .variables
        .iter()
        .for_each(|(category, variables)| {
            println!("\n{category}");
            variables
                .iter()
                .for_each(|var| print!("{}, ", var.enum_name));
            print!("\n");
        });
}
