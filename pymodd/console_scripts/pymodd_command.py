import os
import sys
import json
import runpy
from argparse import ArgumentParser

from pymodd import _pymodd_helper
from pymodd.game import Game
from pymodd.entity_script import EntityScripts


VARIABLE_TYPE_CLASS_NAMES = [
    'UnitTypes', 'PlayerTypes', 'ItemTypes', 'ProjectileTypes', 'Regions', 'Variables',
    'EntityVariables', 'PlayerVariables', 'AnimationTypes', 'AttributeTypes', 'ItemTypeGroups',
    'UnitTypeGroups', 'States', 'Shops', 'Dialogues', 'Musics', 'Sounds'
]


def generate_project(args):
    _pymodd_helper.generate_project_from_json_file_path(args.json_file_path)


def compile_project(_args):
    required_files = ['mapping.py']
    for file in required_files:
        if not os.path.isfile(file):
            _pymodd_helper.log_error(
                f'{file} file not found: is your current working directory a pymodd project?')
            return

    project_directory_name = os.getcwd().split(os.sep)[-1]
    _pymodd_helper.log_cli_start_message("Compiling", project_directory_name)

    sys.path.append(os.path.abspath(f'../{project_directory_name}/'))
    project_data = runpy.run_path('mapping.py')

    game_classes = find_game_classes_in_project_data(project_data)
    if len(game_classes) == 0:
        _pymodd_helper.log_error(
            'no class subclassing Game was found in mapping.py, one is required')
        return
    if len(game_classes) > 1:
        _pymodd_helper.log_error(
            'more than one class subclassing Game was found in mapping.py, only one is required')
        return

    variable_classes = find_variable_classes_in_project_data(
        project_data)
    game = game_classes[0]('utils/game.json', variable_classes, project_data)

    compiled_json_output_path = f'output/{game.name}.json'
    if not os.path.exists('output/'):
        os.makedirs('output/')
    with open(f'{compiled_json_output_path}', 'w') as file:
        file.write(json.dumps(game.to_dict(), indent=4))
    _pymodd_helper.log_success(f'{compiled_json_output_path} written')

    _pymodd_helper.log_cli_end_message("compilation", True)


def find_game_classes_in_project_data(project_data: dict):
    return list(filter(
        lambda object_data:
        # is a class
        type(object_data) == type and
        # subclasses the Game class
        issubclass(object_data, Game) and
        # is not the Game class
        object_data != Game and
        # does not subclass the EntityScripts class
        not issubclass(object_data, EntityScripts),
        project_data.values()))


def find_variable_classes_in_project_data(project_data: dict):
    def is_class_data_of_variable_type(pair):
        key, _value = pair
        return key in VARIABLE_TYPE_CLASS_NAMES
    return list(dict(filter(
        is_class_data_of_variable_type,
        project_data.items())).values())


def main_cli():
    parser = ArgumentParser(prog='pymodd')
    subparsers = parser.add_subparsers(
        title='subcommands', description='valid subcommands')

    parser_generate_project = subparsers.add_parser(
        'generate-project', description='Parse a modd.io json file into a pymodd project')
    parser_generate_project.add_argument(
        'json_file_path', type=str, help='the path of the modd.io json file')
    parser_generate_project.set_defaults(func=generate_project)

    parser_build = subparsers.add_parser(
        'compile', description='Compile a pymodd project into a modd.io json file')
    parser_build.set_defaults(func=compile_project)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main_cli()
