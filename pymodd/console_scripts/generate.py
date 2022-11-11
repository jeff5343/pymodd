import os
import json
from argparse import ArgumentParser
from caseconverter import pascalcase, snakecase

from ..utils.class_dicts import trigger_to_enum, function_to_class, action_to_class

GENERATION_TYPE_CATEGORIES = [
    'entityTypeVariables', 'shops', 'animationTypes', 'states', 'projectileTypes', 'itemTypes', 'music',
    'sound', 'unitTypes', 'variables', 'attributeTypes', 'playerTypes', 'playerTypeVariables'
]

parser = ArgumentParser(
    description='Turn a modd.io game json file into python')
parser.add_argument('json_file', help='The exported game json file')


class Generator():
    def __init__(self, json_file):
        if not json_file or not json_file.endswith('.json'):
            parser.error(f'{json_file} is not a json file')
        
        game_dict = None
        with open(json_file, 'rt') as game_file:
            game_dict = json.loads(game_file.read())
            if game_dict is None or game_dict.get('data') is None:
                parser.error(f'{json_file} contains invalid content')
        self.game_name = snakecase(game_dict.get('title'))
        self.game_dict = game_dict.get('data')
    
    def generate_project(self):
        print(f'\nGenerating project, {self.game_name}...')

        if not os.path.isdir(f'{self.game_name}/'):
            os.mkdir(f'{self.game_name}/')

        self.write_project_file('game.py', self.create_gamepy_content())
        print(f' - game.py successfuly created/updated')
        write_scripts = (input(f'   Do you want to overwrite {self.game_name}/scripts.py? (Y/n): ') in ('Y', 'y')) if os.path.isfile(f'{self.game_name}/scripts.py') else True
        if write_scripts:
            self.write_project_file('scripts.py', self.create_scriptspy_content())
            print(f' - scripts.py successfuly written')

        self.create_scriptspy_content()

        print('\nGame created/updated successfully\n')
    
    def create_gamepy_content(self):
        content = ''
        import_classes = []
        for category in GENERATION_TYPE_CATEGORIES:
            current_dict = self.game_dict.get(category)
            is_variable_type = 'variable' in category.lower()
            class_name = f"{pascalcase(category)}{'s' if category[-1] != 's' else ''}"
            content += f'\n\nclass {class_name}():\n'
            obj_ids = self.game_dict.get(category, {}).keys()
            if len(obj_ids) == 0:
                content += '\tpass\n'
                continue
            type_name = pascalcase(category).removesuffix('s') if not category == 'variables' else 'Variable'
            # for more consistent names
            if 'TypeVariables' in category:
                type_name = 'EntityVariable' if category == 'entityTypeVariables' else 'PlayerVariable'
            # add import
            if type_name not in import_classes:
                import_classes.append(type_name)
            for obj_id in obj_ids:
                obj_name = current_dict.get(obj_id).get('name')
                data_type = current_dict.get(obj_id).get('dataType')
                obj_name = obj_name if obj_name is not None else obj_id
                content += ''.join(
                    [f"""\t{snakecase(obj_name).upper()} = {type_name}('{obj_id}'{'' if not is_variable_type else f", variable_type='{data_type}'"}) \n"""])
        # add only used imports
        content = (
            f"from pymodd.functions import {', '.join([class_name for class_name in import_classes])}\n"
            f'{content}'
        )
        return content

    def create_scriptspy_content(self):
        scripts_dict = self.game_dict.get('scripts')
        content = "from pymodd.actions import *\nfrom pymodd.functions import *\nfrom pymodd.script import Script, Trigger, write_to_output\n\nfrom game import *"
        for script_key, script in scripts_dict.items():
            script_name = script.get('name')
            script_triggers = [f"Trigger.{trigger_to_enum[trigger.get('type')]}" for trigger in script.get('triggers')]
            script_order = script.get('order')
            actions = ''

            content += (
                f'\n\n\nclass {pascalcase(script_name)}(Script):\n' \
                f'\tdef __init__(self):\n' \
                f"\t\tself.triggers = [{', '.join(script_triggers)}]\n" \
                f'\t\tself.actions = [\n' \
                f'\t\t\tPUT ACTIONS HERE (somehow)\n' \
                f'\t\t]\n'
                f'\t\tself.order = {script_order}'
            )
        # dont forget write_to_output()
        print(content)
        return content

    def write_project_file(self, file_name, content):
        with open(f'{self.game_name}/{file_name}', 'w') as game_file:
            game_file.write(content)


def main():
    args = parser.parse_args()
    Generator(args.json_file).generate_project()


if __name__ == '__main__':
    main()
