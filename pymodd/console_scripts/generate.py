import os
import json
from argparse import ArgumentParser
from caseconverter import pascalcase, snakecase, camelcase

from ..utils.class_dicts import TRIGGER_TO_ENUM, CONSTANTS_TO_ENUM, FUNCTION_TO_CLASS, ACTION_TO_CLASS

# what variable types to generate
GENERATION_CATEGORIES = [
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
        self.game_data = game_dict
        self.game_dict = game_dict.get('data')
        self.json_file_path = f'utils/game.json'

    def generate_project(self):
        print(f'\nGenerating project, {self.game_name}...')

        if not os.path.isdir(f'{self.game_name}/'):
            os.mkdir(f'{self.game_name}/')

        self.write_project_file('game_variables.py',
                                self.create_game_variablespy_content())
        print(f' - game_variables.py successfuly created/updated')

        self.write_project_file('mapping.py', self.create_mappingpy_content())
        print(f' - mapping.py successfuly written')

        if self.can_write_project_file('scripts.py'):
            self.write_project_file(
                'scripts.py', self.create_scriptspy_content())
            print(f' - scripts.py successfuly written')
        
        if not os.path.isdir(f'{self.game_name}/utils/'):
            os.mkdir(f'{self.game_name}/utils/')

        self.write_project_file(self.json_file_path, json.dumps(self.game_data))
        print(f' - {self.json_file_path} successfuly written')

        print('\nGame created/updated successfully\n')

    def can_write_project_file(self, file):
        # ask for input if file already exists
        if os.path.isfile(f'{self.game_name}/{file}'):
            response = input(
                f'   Do you want to overwrite {self.game_name}/{file}? (Y/n): ').strip()
            return response.strip() in ('Y', 'y')
        return True

    def create_game_variablespy_content(self):
        content = ''
        import_classes = []

        # to seperate different variables from regular variables
        seperated_datatype_variables = {
            'regions': [],
            'itemTypeGroups': [],
            'unitTypeGroups': [],
        }

        for category in GENERATION_CATEGORIES + list(seperated_datatype_variables.keys()):
            variables = self.variables_from_category(
                category, seperated_datatype_variables)
            # use the variables stored in seperated_datatype_variables
            if (seperated_variables := seperated_datatype_variables.get(category)):
                variables = seperated_variables

            content += f'\n\nclass {(category_class_name := Generator.class_from_category_name(category))}():\n'
            if len(variables) == 0:
                content += '\tpass\n'
                continue
            # to match with the classes defined in functions.py
            type_name = category_class_name.removesuffix('s')
            if seperated_variables:
                type_name = 'Variable'
            import_classes.append(type_name)
            # add variables
            for variable in variables:
                content += f"""\t{variable['enum_name']} = {type_name}('{variable['id']}'{'' if not (data_type := variable['data_type']) else f", variable_type='{data_type}'"})\n"""

                VariableNameToEnum.add_variable_to_category(category, variable['id'], variable['name'], variable['enum_name'])
        # add only used imports
        content = (
            f"from pymodd.functions import {', '.join([class_name for class_name in import_classes])}\n"
            f'{content}'
        )
        return content

    def variables_from_category(self, category, seperated_datatype_variables):
        category_dict = self.game_dict.get(category)
        variable_ids = self.game_dict.get(category, {}).keys()
        variables = []

        for variable_id in variable_ids:
            variable_name, data_type = category_dict[variable_id].get(
                'name'), category_dict[variable_id].get('dataType')
            # only include data type if its a global variable
            if 'variable' not in category.lower():
                data_type = None
            enum_name = snakecase(
                variable_name if variable_name is not None else variable_id).upper()

            variable = {'id': variable_id, 'name': variable_name,
                        'data_type': data_type, 'enum_name': enum_name}
            # seperate variables
            if (datatype_variables := seperated_datatype_variables.get(f'{data_type}s')) is not None:
                datatype_variables.append(variable)
                continue
            variables.append(variable)
        return variables

    def create_scriptspy_content(self):
        content = (
            'from pymodd.actions import *\n'
            'from pymodd.functions import *\n'
            'from pymodd.script import Script, Trigger, UiTarget, Flip, write_to_output\n\n'
            'from game_variables import *\n'
        )
        scripts_dict = self.game_dict.get('scripts')
        for script in scripts_dict.values():
            if script.get('triggers') is None:
                continue
            script_name = script.get('name')
            script_triggers = [
                f"Trigger.{TRIGGER_TO_ENUM[trigger.get('type')]}" for trigger in script.get('triggers')]
            script_key = script.get('key')
            actions = JsonActionsConverter(script.get('actions')).convert_to_python()

            content += (
                f'\n\nclass {self.class_name_from_script_name(script_name)}(Script):\n'
                f'\tdef build(self):\n'
                f"\t\tself.key = '{script_key}'\n"
                f"\t\tself.triggers = [{', '.join(script_triggers)}]\n"
                f'\t\tself.actions = [\n'
                f"{''.join([f'{TAB * 3}{action},{NEW_LINE}' for action in actions])}\n"
                f'\t\t]\n'
            )
        return content

    def create_mappingpy_content(self):
        game_class_name = pascalcase(self.game_name)
        content = (
            'from pymodd.script import Game, Folder, write_game_to_output, write_to_output\n\n'
            'from scripts import *\n\n'
            f'class {game_class_name}(Game):\n'
            '\tdef build(self):\n'
            '\t\tself.scripts = [\n'
        )
        game_directory = self.sorted_game_directory_from_game_items(self.game_dict.get('scripts').values())
        for level in game_directory.values():
            for game_item in level:
                content += self.game_item_to_string(game_item, depth=3)
        content += (
            '\n\t\t]\n\n'
            f'# run this file to generate the all json files for this game `python {self.game_name}/mapping.py`\n'
            f"write_game_to_output({game_class_name}(json_file='{self.game_name}/{self.json_file_path}'))\n\n"
            f'# uncomment the following to quickly generate the json file for a script\n'
            f"# write_to_output('output/', SCRIPT_OBJECT())\n"
        )
        return content

    def game_item_to_string(self, game_item, depth):
        if game_item.get('type') == 'script':
            return f"{TAB * depth}{game_item.get('name')}(),\n"
        stringified_children = []
        for level in game_item.get('children').values():
            for child in level:
                stringified_children.append(self.game_item_to_string(child, depth + 1))
        return (
            f'''{TAB * depth}Folder("{game_item.get('name')}", [\n'''
            f"{''.join(stringified_children)}"
            f"{TAB * depth}]),\n"
        )

    def sorted_game_directory_from_game_items(self, items):
        # retrieve root game items and items in folders and store them
        root_game_items = {}
        folder_key_to_nested_items = {}
        for item in items:
            order = item.get('order')
            # store in the root directory of the game
            scope = root_game_items
            # if parent is present, store in parent directory
            if (parent := item.get('parent')) is not None:
                if folder_key_to_nested_items.get(parent) is None:
                    folder_key_to_nested_items[parent] = {}
                scope = folder_key_to_nested_items[parent]
            # since there can be scripts with the same order
            if scope.get(order) is None:
                scope[order] = []
            scope[order].append(self.dictionary_from_game_item(item))

        # sort game items by their order number and insert nested items into each folder
        sorted_root_game_items = sort_dictionary(root_game_items)
        items_queue = list(sorted_root_game_items.values())
        while len(items_queue) > 0:
            items = items_queue.pop(0)
            for item in items:
                if not item.get('type') == 'folder':
                    continue
                if (nested_items := folder_key_to_nested_items.get(item.get('key'))) is None:
                    continue
                item['children'] = sort_dictionary(nested_items)
                items_queue += list(item['children'].values())
        return sorted_root_game_items

    def dictionary_from_game_item(self, game_item):
        # if its a folder
        if game_item.get('triggers') is None:
            return {'type': 'folder', 'name': game_item.get('folderName'), 'key': game_item.get('key'), 'children': []}
        return {'type': 'script', 'name': self.class_name_from_script_name(game_item.get('name'))}

    def write_project_file(self, file_name, content):
        with open(f'{self.game_name}/{file_name}', 'w') as game_file:
            game_file.write(content)

    def class_name_from_script_name(self, script_name):
        return pascalcase(script_name)

    @staticmethod
    def class_from_category_name(category_name):
        category_name_to_class = {
            'entityTypeVariables': 'entityVariables',
            'playerTypeVariables': 'playerVariables',
        }
        category_name = pascalcase(
            category_name_to_class.get(category_name, category_name))
        return f"{category_name}{'s' if category_name[-1] != 's' else ''}"


class JsonActionsConverter():
    def __init__(self, actions, level=0):
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
            if (weird_args := self.handle_weird_arguments(arg, value)) is not None:
                args.extend(weird_args)
                continue
            args.append(
                {'name': arg, 'value': self.python_from_function(arg, value)})

        return self.align_arguments_with_class(args, action_class)

    def handle_weird_arguments(self, argument, value):
        if type(value) is not dict:
            return None
        # xy force is returned as one argument by modd, but in actions.py there are two arguemnts for force_x and force_y
        if argument == 'force' and (x := value.get('x')) is not None:
            return [
                {'name': 'force_x',
                    'value': self.python_from_function('force_x', x)},
                {'name': 'force_y', 'value': self.python_from_function(
                    'force_y', value.get('y'))}
            ]

    def python_from_function(self, argument, value):
        # handle weird list formats
        if type(value) is list:
            return self.handle_list_function(value)

        # for variables, constants, and primitives
        if type(value) is dict and (var_name := (value.get('variableName') or value.get('variable', {}).get('key'))):
            argument, value = 'variableName', var_name
        if type(value) is not dict:
            if (variable := self.variable_from_function(argument, value)) is not None:
                return variable
            if (constant := self.constant_from_function(argument, value)) is not None:
                return constant
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

    def variable_from_function(self, argument, value):
        # some types are accessed the same way or different ways in modd.io
        category_to_categories = {
            'variables': ['variables', 'entityTypeVariables', 'playerTypeVariables', 'regions', 'itemTypeGroups', 'unitTypeGroups'],
            'attributes': ['attributeTypes'],
        }

        category = argument.removesuffix('Name')
        category = f"{category}{'s' if category[-1] != 's' and category not in ('music', 'sound') else ''}"
        categories = category_to_categories.get(category, [category])

        for category in categories:
            if (category_dict := VariableNameToEnum.get_category(category)) and (variable_name := category_dict.get(value)):
                return f'{Generator.class_from_category_name(category)}.{variable_name}'
        return None

    def primitive_from_function(self, value):
        primitives = [int, float, str, bool]
        if type(value) not in primitives:
            return None
        # surround strings with quotes
        if type(value) == str:
            quote = self.surrounding_quote_for_string(value)
            value = f"{quote}{value}{quote}"
        return f"{value}"

    def constant_from_function(self, argument, value):
        argument_to_constant = {
            'target': {'class_name': 'UiTarget', 'dictionary': CONSTANTS_TO_ENUM['ui_target_to_enum']},
            'flip': {'class_name': 'Flip', 'dictionary': CONSTANTS_TO_ENUM['flip_direction_to_enum']}
        }
        constant_data = argument_to_constant.get(argument)
        if constant_data is None:
            return None
        return f"{constant_data['class_name']}.{constant_data['dictionary'].get(value)}"

    def surrounding_quote_for_string(self, string):
        if "'" in string:
            return '''"'''
        if '''"''' in string:
            return """'''"""
        return "'"

    def align_arguments_with_class(self, args_dict, class_dict):
        """Aligns arguments from modd.io functions with classes in pymodd.
        For example, `Func(itemB, itemA)` would be converted into `Func(itemA, itemB)`

        Args:
            args_dict (dict): MUST be in format `{'name': argument_name, 'value': argument_value}`
            class_dict (dict): from `ACTION_TO_CLASS` dict

        Returns:
            list: aligned arguments
        """
        class_arguments = class_dict.get('arguments', []).copy()
        args, unused_args = [''] * len(class_arguments), []

        for arg in args_dict:
            if (name := camelcase(arg.get('name'))) in class_arguments:
                class_arguments[(index := class_arguments.index(
                    camelcase(name)))] = None
                args[index] = arg.get('value')
                continue
            unused_args.append(arg)
        for i, arg in enumerate(args):
            if len(unused_args) == 0:
                break
            if arg == '':
                args[i] = unused_args.pop(0).get('value')
        return args


class VariableNameToEnum():
    # used for finding the enum names of variables created in game_variabless.py while generating scripts.py
    categories = {}

    @staticmethod
    def get_category(category, default=None):
        return VariableNameToEnum.categories.get(category, default)

    @staticmethod
    def create_category(category_name):
        VariableNameToEnum.categories[category_name] = {}

    @staticmethod
    def add_variable_to_category(category_name, variable_id, variable_name, enum_name):
        if category_name not in VariableNameToEnum.categories.keys():
            VariableNameToEnum.create_category(category_name)

        if variable_name is not None:
            VariableNameToEnum.categories[category_name][variable_name] = enum_name
        VariableNameToEnum.categories[category_name][variable_id] = enum_name


def sort_dictionary(dictionary):
    return dict(sorted(dictionary.items()))


def main():
    args = parser.parse_args()
    Generator(args.json_file).generate_project()


if __name__ == '__main__':
    main()
