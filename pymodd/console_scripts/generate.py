import os
import json
from argparse import ArgumentParser
from caseconverter import pascalcase, snakecase, camelcase

from ..utils.class_dicts import TRIGGER_TO_ENUM, FUNCTION_TO_CLASS, ACTION_TO_CLASS

GENERATION_TYPE_CATEGORIES = [
    'entityTypeVariables', 'shops', 'animationTypes', 'states', 'projectileTypes', 'itemTypes', 'music',
    'sound', 'unitTypes', 'variables', 'attributeTypes', 'playerTypes', 'playerTypeVariables', 'dialogues',
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

        for category in GENERATION_TYPE_CATEGORIES:
            is_variable_type = 'variable' in category.lower()
            current_dict = self.game_dict.get(category)
            var_ids = self.game_dict.get(category, {}).keys()

            content += f'\n\nclass {(category_class_name := Generator.class_from_category_name(category))}():\n'
            if len(var_ids) == 0:
                content += '\tpass\n'
                continue

            # to match with the classes defined in functions.py
            type_name = category_class_name.removesuffix('s')
            if 'TypeVariables' in category:
                type_name = 'EntityVariable' if category == 'entityTypeVariables' else 'PlayerVariable'

            # include imports
            if type_name not in import_classes:
                import_classes.append(type_name)

            # add variables
            for var_id in var_ids:
                var_name, data_type = current_dict[var_id].get('name'), current_dict[var_id].get('dataType')
                enum_name = snakecase(
                    var_id if var_name is None else var_name).upper()
                content += ''.join(
                    [f"""\t{enum_name} = {type_name}('{var_id}'{'' if not is_variable_type else f", variable_type='{data_type}'"})\n"""])

                VariableNameToClass.add_variable_to_category(
                    category, var_id, var_name, enum_name)
        # add only used imports
        content = (
            f"from pymodd.functions import {', '.join([class_name for class_name in import_classes])}\n"
            f'{content}'
        )
        return content

    def create_scriptspy_content(self):
        content = "from pymodd.actions import *\nfrom pymodd.functions import *\nfrom pymodd.script import Script, Trigger, write_to_output\n\nfrom game import *"
        scripts_dict = self.game_dict.get('scripts')
        for script in scripts_dict.values():
            if script.get('triggers') is None:
                continue
            script_name = script.get('name')
            script_triggers = [f"Trigger.{TRIGGER_TO_ENUM[trigger.get('type')]}" for trigger in script.get('triggers')]
            script_order = script.get('order')
            actions = JsonActionsConverter(script.get('actions'), 0).convert_to_python()

            content += (
                f'\n\n\nclass {pascalcase(script_name)}(Script):\n'
                f'\tdef __init__(self):\n'
                f"\t\tself.triggers = [{', '.join(script_triggers)}]\n"
                f'\t\tself.actions = [\n'
                f"{''.join([f'{TAB * 3}{action},{NEW_LINE}' for action in actions])}\n"
                f'\t\t]\n'
                f'\t\tself.order = {script_order}'
            )
        return content

    def write_project_file(self, file_name, content):
        with open(f'{self.game_name}/{file_name}', 'w') as game_file:
            game_file.write(content)

    @staticmethod
    def class_from_category_name(category_name):
        category_name_to_class = {
            'entityTypeVariables': 'entityVariables',
            'playerTypeVariables': 'playerVariables'
        }
        category_name = pascalcase(category_name_to_class.get(category_name, category_name))
        return f"{category_name}{'s' if category_name[-1] != 's' else ''}"


class JsonActionsConverter():
    def __init__(self, actions, level):
        self.actions = actions
        self.level = level

    def convert_to_python(self):
        py_actions = []
        for action in self.actions:
            action_class = ACTION_TO_CLASS.get(action.get('type'))
            py_actions.append(
                f"{action_class.get('className')}({', '.join(self.arguments_from_action(action, action_class))})")
        return py_actions

    def arguments_from_action(self, action, action_class):
        args = []
        for arg, value in action.items():
            if arg in ('type', 'vars', 'function'):
                continue
            if (peculiar_args := self.handle_weird_arguments(arg, value)) is not None:
                args.extend(peculiar_args)
                continue
            args.append({'name': arg, 'value': self.python_from_function(arg, value)})

        return self.align_arguments_with_class(args, action_class)

    def handle_weird_arguments(self, argument, value):
        if type(value) is not dict:
            return None
        # xy force is returned as one argument by modd, but in actions.py there are two arguemnts for force_x and force_y
        if argument == 'force' and (x := value.get('x')) is not None:
            return [
                {'name': 'force_x', 'value': self.python_from_function('force_x', x)},
                {'name': 'force_y', 'value': self.python_from_function('force_y', value.get('y'))}
            ]

    def python_from_function(self, name, value):
        # handle weird list formats
        if type(value) is list:
            return self.handle_list_function(value)

        # for variables and primitives
        if type(value) is dict and (var_name := (value.get('variableName') or value.get('variable', {}).get('key'))):
            name, value = 'variableName', var_name
        if not type(value) is dict:
            if (variable := self.variable_from_function(name, value)) is not None:
                return variable
            if (primitive := self.primitive_from_function(value)) is not None:
                return primitive
            return 'Null()'

        # if the function does not exist
        function_class = FUNCTION_TO_CLASS.get(value.get('function'))
        if not function_class:
            return 'Null()'

        # if function has no arguments
        if len(function_class.get('arguments')) == 0:
            return f"{function_class['className']}()"

        # handle calculate function
        if function_class['className'] == 'Calculate':
            value = value.get('items')
            return f"{function_class['className']}({self.python_from_function('number', value[1])}, '{value[0].get('operator')}', {self.python_from_function('number', value[2])})"

        # add arguments to function (recursive)
        args = []
        for argument, func in value.items():
            if argument in ('type', 'vars', 'function'):
                continue
            args.append(
                {'name': argument, 'value': self.python_from_function(argument, func)})
        python_args = self.align_arguments_with_class(args, function_class)
        return f"{function_class['className']}({', '.join(python_args)})"

    def handle_list_function(self, function):
        if len(function) > 0 and (operator := function[0].get('operator')):
            operandType = function[0].get('operandType')
            return f"Condition({self.python_from_function(operandType, function[1])}, '{operator}', {self.python_from_function(operandType, function[2])})"
        # for actions
        return (
            f'[\n'
            f"{''.join([f'{TAB * (4 + self.level)}{action},{NEW_LINE}' for action in JsonActionsConverter(function, self.level + 1).convert_to_python()])}"
            f'{TAB * (3 + self.level)}]'
        )

    def variable_from_function(self, name, value):
        # some types are accessed the same way or different ways in modd.io
        category_to_categories = {
            'variables': ['variables', 'entityTypeVariables', 'playerTypeVariables'],
            'attributes': ['attributeTypes'],
        }

        category = name.removesuffix('Name')
        category = f"{category}{'s' if category[-1] != 's' and category not in ('music', 'sound') else ''}"
        categories = category_to_categories.get(category, [category])

        for category in categories:
            if (category_dict := VariableNameToClass.get_category(category)) and (variable_name := category_dict.get(value)):
                return f'{Generator.class_from_category_name(category)}.{variable_name}'
        return None

    def primitive_from_function(self, value):
        primitives = [int, str, bool]
        if type(value) not in primitives:
            return None
        if type(value) == str:
            quote = self.surrounding_quote_for_string(value)
            value = f"{quote}{value}{quote}"
        return f"{value}"

    def surrounding_quote_for_string(self, string):
        if "'" in string:
            return '''"'''
        if '''"''' in string:
            return """'''"""
        return "'"

    def align_arguments_with_class(self, args_dict, class_dict):
        """Aligns arguments from modd.io functions with classes in pymodd.
        For example, `Func(itemB, itemA)` should be `Func(itemA, itemB)`

        Args:
            args_dict (dict): MUST be in format `{'name': argument_name, 'value': argument_value}`
            class_dict (dict): from `ACTION_TO_CLASS` dict

        Returns:
            list: aligned arguments
        """
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


class VariableNameToClass():

    categories = {}

    @staticmethod
    def get_category(category, default=None):
        return VariableNameToClass.categories.get(category, default)

    @staticmethod
    def create_category(category_name):
        VariableNameToClass.categories[category_name] = {}

    @staticmethod
    def add_variable_to_category(category_name, variable_id, variable_name, enum_name):
        if category_name not in VariableNameToClass.categories.keys():
            VariableNameToClass.create_category(category_name)

        if variable_name is not None:
            VariableNameToClass.categories[category_name][variable_name] = enum_name
        VariableNameToClass.categories[category_name][variable_id] = enum_name


def main():
    args = parser.parse_args()
    Generator(args.json_file).generate_project()


if __name__ == '__main__':
    main()
