import os
import runpy
from argparse import ArgumentParser

from pymodd import _pymodd_helper


def generate_project(args):
    _pymodd_helper.generate_project_from_json_file_path(args.json_file_path)


def build(_args):
    if not os.path.isfile('mapping.py'):
        print(
            'mapping.py file could not be found\nis the current working directory a pymodd project?')
        return
    print(f'{os.getcwd().split(os.sep)[-1]}.mapping')
    runpy.run_module(mod_name=f'{os.getcwd().split(os.sep)[-1]}.mapping')


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
        'build', description='Generate a modd.io game json file from a pymodd project in an output folder')
    parser_build.set_defaults(func=build)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main_cli()
