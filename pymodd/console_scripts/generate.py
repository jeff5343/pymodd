import os
import json
from argparse import ArgumentParser
from caseconverter import pascalcase, snakecase, camelcase

from ..utils.class_dicts import trigger_to_enum, function_to_class, action_to_class

GENERATION_TYPE_CATEGORIES = [
    'entityTypeVariables', 'shops', 'animationTypes', 'states', 'projectileTypes', 'itemTypes', 'music',
    'sound', 'unitTypes', 'variables', 'attributeTypes', 'playerTypes', 'playerTypeVariables'
]

# to put inside f-strings
NEW_LINE = '\n'
TAB = '\t'

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
        self.variable_name_to_class = {}

    def generate_project(self):
        print(f'\nGenerating project, {self.game_name}...')

        if not os.path.isdir(f'{self.game_name}/'):
            os.mkdir(f'{self.game_name}/')

        self.write_project_file('game.py', self.create_gamepy_content())
        print(f' - game.py successfuly created/updated')
        write_scripts = (input(f'   Do you want to overwrite {self.game_name}/scripts.py? (Y/n): ').strip() in (
            'Y', 'y')) if os.path.isfile(f'{self.game_name}/scripts.py') else True
        if write_scripts:
            self.write_project_file(
                'scripts.py', self.create_scriptspy_content())
            print(f' - scripts.py successfuly written')

        self.create_scriptspy_content()

        print('\nGame created/updated successfully\n')

    def create_gamepy_content(self):
        content = ''
        import_classes = []

        # for converting variables into classes
        self.variable_name_to_class = {}

        for category in GENERATION_TYPE_CATEGORIES:
            self.variable_name_to_class[category] = {}

            is_variable_type = 'variable' in category.lower()
            current_dict = self.game_dict.get(category)
            var_ids = self.game_dict.get(category, {}).keys()

            content += f'\n\nclass {Generator.class_from_category_name(category)}():\n'
            if len(var_ids) == 0:
                content += '\tpass\n'
                continue

            # for more consistent names
            type_name = pascalcase(category).removesuffix(
                's') if not category == 'variables' else 'Variable'
            if 'TypeVariables' in category:
                type_name = 'EntityVariable' if category == 'entityTypeVariables' else 'PlayerVariable'

            # include imports
            if type_name not in import_classes:
                import_classes.append(type_name)

            # add variables
            for var_id in var_ids:
                var_name = current_dict.get(var_id).get('name')
                data_type = current_dict.get(var_id).get('dataType')
                enum_name = snakecase(
                    var_id if var_name is None else var_name).upper()
                content += ''.join(
                    [f"""\t{enum_name} = {type_name}('{var_id}'{'' if not is_variable_type else f", variable_type='{data_type}'"})\n"""])

                if var_name is not None:
                    keys_of_category = list(
                        self.variable_name_to_class[category].keys())
                    if var_name in keys_of_category:
                        var_name += f'_{keys_of_category.count(var_name)}'
                    self.variable_name_to_class[category][var_name] = enum_name
                self.variable_name_to_class[category][var_id] = enum_name
        # add only used imports
        content = (
            f"from pymodd.functions import {', '.join([class_name for class_name in import_classes])}\n"
            f'{content}'
        )
        return content

    def create_scriptspy_content(self):
        scripts_dict = self.game_dict.get('scripts')
        content = "from pymodd.actions import *\nfrom pymodd.functions import *\nfrom pymodd.script import Script, Trigger, write_to_output\n\nfrom game import *"
        for script in scripts_dict.values():
            script_name = script.get('name')
            script_triggers = [
                f"Trigger.{trigger_to_enum[trigger.get('type')]}" for trigger in script.get('triggers')]
            script_order = script.get('order')
            actions = JsonActionsConverter(script.get('actions'), self.variable_name_to_class, 0).convert_to_python()

            content += (
                f'\n\n\nclass {pascalcase(script_name)}(Script):\n'
                f'\tdef __init__(self):\n'
                f"\t\tself.triggers = [{', '.join(script_triggers)}]\n"
                f'\t\tself.actions = [\n'
                f"{''.join([f'{TAB * 3}{action},{NEW_LINE}' for action in actions])}\n"
                f'\t\t]\n'
                f'\t\tself.order = {script_order}'
            )
        print(content)
        # print(self.variable_name_to_class)
        return content

    def write_project_file(self, file_name, content):
        with open(f'{self.game_name}/{file_name}', 'w') as game_file:
            game_file.write(content)

    @staticmethod
    def class_from_category_name(category_name):
        return f"{pascalcase(category_name)}{'s' if category_name[-1] != 's' else ''}"


class JsonActionsConverter():
    def __init__(self, actions, variable_name_to_class, level):
        self.actions = actions
        self.variable_name_to_class = variable_name_to_class
        self.level = level

    def convert_to_python(self):
        py_actions = []
        for action in self.actions:
            action_class = action_to_class.get(action.get('type'))
            argument_values = self.match_arguments_to_class(
                self.arguments_from_action(action), action_class)
            py_actions.append(
                f"{action_class.get('className')}({', '.join(argument_values)})")
        return py_actions

    def arguments_from_action(self, action):
        args = []
        for arg, value in action.items():
            if arg in ('type', 'vars', 'function'):
                continue
            args.append(
                {'name': arg, 'value': self.python_from_function(arg, value)})
        return args

    def python_from_function(self, name, value):

        # maybe delete array if empty? for then and if statements?

        # handle actions
        if type(value) is list:
            if len(value) > 0 and (operator := value[0].get('operator')):
                return f"Condition({self.python_from_function('itemA', value[1])}, '{operator}', {self.python_from_function('itemB', value[2])})"
            # for actions
            return (
                f'[\n'
                f"{''.join([f'{TAB * (4 + self.level)}{action},{NEW_LINE}' for action in JsonActionsConverter(value, self.variable_name_to_class, self.level + 1).convert_to_python()])}"
                f'{TAB * (3 + self.level)}]'
            )

        # for variables and primitives
        if type(value) is dict and (var_name := (value.get('variableName') or value.get('variable', {}).get('key'))):
            name, value = 'variableName', var_name
        if not type(value) is dict:
            return f"{(self.variable_from_value(name, value) or self.primitive_from_value(value)) or 'Null()'}"

        function_class = function_to_class.get(value.get('function'))
        if not function_class:
            return 'Null()'

        # if function has no arguments
        if len(function_class.get('arguments')) == 0:
            return f"{function_class['className']}()"

        # different structured actions (maybe put in a function later):
        if function_class['className'] == 'Calculate':
            value = value.get('items')
            return f"{function_class['className']}({self.python_from_function('itemA', value[1])}, '{value[0].get('operator')}', {self.python_from_function('itemB', value[2])})"

        # add arguments to function (recursive)
        args = []
        for argument, func in value.items():
            if argument in ('type', 'vars', 'function'):
                continue
            args.append(
                {'name': argument, 'value': self.python_from_function(argument, func)})
        python_args = self.match_arguments_to_class(args, function_class)
        return f"{function_class['className']}({', '.join(python_args)})"

    def variable_from_value(self, name, value):
        category = name.removesuffix('Name')
        categories = [
            f"{category}{'s' if name[-1] != 's' and category not in ('music', 'sound') else ''}"]

        # entity variables, player variables, and regular variables are all accessed the same way in modd.io
        if 'variables' in categories:
            categories.extend(['entityTypeVariables', 'playerTypeVariables'])

        for category in categories:
            if (category_dict := self.variable_name_to_class.get(category)) and (variable_name := category_dict.get(value)):
                return f'{Generator.class_from_category_name(category)}.{variable_name}'
        return None

    def primitive_from_value(self, value):
        primitive_map = {
            int: 'Number',
            bool: 'Boolean',
            str: 'String',
        }
        primitive_type = primitive_map.get(type(value))
        value = f"'{value}'" if primitive_type == 'String' else value
        return f"{primitive_type}({value})" if primitive_type is not None else None

    def match_arguments_to_class(self, args_dict, class_dict):
        class_arguments = class_dict.get('arguments', []).copy()
        args, unused_args = [''] * len(class_arguments), []

        for item in args_dict:
            if (name := item.get('name')) and camelcase(name) in class_arguments:
                class_arguments[(index := class_arguments.index(
                    camelcase(name)))] = None
                args[index] = item.get('value')
                continue
            unused_args.append(item)
        for i, arg in enumerate(args):
            if len(unused_args) == 0:
                break
            if arg == '':
                args[i] = unused_args.pop(0).get('value')
        return args


def main():
    args = parser.parse_args()
    Generator(args.json_file).generate_project()


if __name__ == '__main__':
    main()
