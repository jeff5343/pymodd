import sys
import json
import runpy
from pathlib import Path
from argparse import ArgumentParser
from typing import Any, Type, TypeVar

from pymodd import _pymodd_helper
from pymodd.game import Game
from pymodd.entity_script import EntityScripts


# make sure game_variables.py contain classes with these names
VARIABLE_TYPE_CLASS_NAMES = [
    "UnitType",
    "PlayerType",
    "ItemType",
    "ProjectileType",
    "Region",
    "Variable",
    "EntityVariable",
    "PlayerVariable",
    "AnimationType",
    "AttributeType",
    "ItemTypeGroup",
    "UnitTypeGroup",
    "ParticleType",
    "Abilities",
    "State",
    "Shop",
    "Dialogue",
    "Music",
    "Sound",
]


def generate_project(args):
    json_file = Path(args.json_file_path)
    if args.json_file_path == "default-template":
        json_file = Path(__file__).parent.parent.joinpath("utils", "Default Game.json")
    if not Path.exists(json_file):
        _pymodd_helper.log_error("invalid json file path!")
        return

    _pymodd_helper.generate_project_from_json_file_content(json_file.read_text())


def compile_project(args):
    required_files = [Path("mapping.py")]
    for file in required_files:
        if not Path.exists(file):
            _pymodd_helper.log_error(
                f"{file.name} file not found: is your current working directory a pymodd project?"
            )
            return

    sys.path.append(str(Path.cwd().absolute()))
    project_data = runpy.run_path("mapping.py")

    game_classes = find_game_classes_in_project_data(project_data)
    if len(game_classes) == 0:
        _pymodd_helper.log_error(
            "no class subclassing Game was found in mapping.py, one is required"
        )
        return
    if len(game_classes) > 1:
        _pymodd_helper.log_error(
            "more than one class subclassing Game was found in mapping.py, only one is required"
        )
        return

    variable_classes = find_variable_classes_in_project_data(project_data)
    game = game_classes[0]("utils/game.json", variable_classes, project_data)

    # create output directory
    Path("output/").mkdir(parents=True, exist_ok=True)

    project_directory_name = Path.cwd().name
    is_successful = True

    if args.only_scripts is None or len(args.only_scripts) == 0:
        # compile project if no scripts are given
        _pymodd_helper.log_cli_start_message("Compiling", project_directory_name)
        compiled_json_file = Path(f"output/{game.name}.json")
        compiled_json_file.write_text(json.dumps(game.to_dict(), indent=4))
        _pymodd_helper.log_success(f"{compiled_json_file} written")
    else:
        # compile scripts individually if they are provided
        _pymodd_helper.log_cli_start_message(
            "Compiling scripts for", project_directory_name
        )

        for script_info in args.only_scripts:
            script_info = script_info.split("/")

            if len(script_info) not in range(2, 4):
                is_successful = False
                _pymodd_helper.log_error(
                    "script must be provided in the format: `folder_id/script_function_name` or `entity_id/folder_id/script_function_name"
                )
                continue

            script_data = None
            output_file_name = None
            if len(script_info) == 2:
                # global scripts
                [script_parent_id, script_function_name] = script_info
                script_data = game.find_script(script_function_name.replace("_", " "))
                output_file_name = script_function_name
            else:
                # entity scripts
                [entity_id, script_parent_id, script_function_name] = script_info
                for entity_script in game.entity_scripts:
                    if entity_id != entity_script.entity_type.id:
                        continue
                    script_data = entity_script.find_script(
                        script_function_name.replace("_", " ")
                    )
                    break
                output_file_name = f"{entity_id}-{script_function_name}"

            if script_data is None:
                _pymodd_helper.log_error(
                    f"{script_function_name} script does not exist"
                )
                is_successful = False
                continue

            script_data = script_data.to_dict(
                project_globals_data=game.project_globals_data
            )
            script_data["parent"] = script_parent_id

            # write data
            compiled_script_json_file = Path(f"output/{output_file_name}.json")
            _ = compiled_script_json_file.write_text(json.dumps(script_data))
            _pymodd_helper.log_success(f"{compiled_script_json_file} written")

    _pymodd_helper.log_cli_end_message("compilation", is_successful)


def find_game_classes_in_project_data(project_data: dict[str, Any]) -> list[Type[Game]]:
    return list(
        filter(
            lambda object_data:
            # is a class
            type(object_data) == type and
            # subclasses the Game class
            issubclass(object_data, Game) and
            # is not the Game class
            object_data != Game and
            # does not subclass the EntityScripts class
            not issubclass(object_data, EntityScripts),
            project_data.values(),
        )
    )


def find_variable_classes_in_project_data(project_data: dict[str, Any]) -> list[type]:
    def is_class_data_of_variable_type(pair: tuple[str, Any]) -> bool:
        key, _value = pair
        return key in VARIABLE_TYPE_CLASS_NAMES

    return list(
        dict(filter(is_class_data_of_variable_type, project_data.items())).values()
    )


def main_cli():
    parser = ArgumentParser(prog="pymodd")
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="generate-project, compile",
        metavar="",
        required=True,
    )

    parser_generate_project = subparsers.add_parser(
        "generate-project",
        description="Generate a pymodd project from a modd.io json file",
    )
    parser_generate_project.add_argument(
        "json_file_path",
        type=str,
        help="the path of the modd.io json file. to generate a default project, fill in `default-template` instead",
    )
    parser_generate_project.set_defaults(func=generate_project)

    parser_compile = subparsers.add_parser(
        "compile", description="Compile a pymodd project into a modd.io json file"
    )
    parser_compile.add_argument(
        "--only-scripts",
        nargs="*",
        help="""
            information of the scripts to compile.
            for global scripts provide the script_folder_id/script_function_name: `W90gBX/game_over`.
            for entity scripts provide the entity_id/script_folder_id/script_function_name: `2Di32W/K3Gd92/drop_item`.
            will NOT compile the entire game""",
    )
    parser_compile.set_defaults(func=compile_project)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
