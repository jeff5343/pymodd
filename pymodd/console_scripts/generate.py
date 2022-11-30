import json
import os
from copy import deepcopy
from argparse import ArgumentParser

from caseconverter import camelcase, pascalcase, snakecase

from ..utils.class_dicts import ACTION_TO_CLASS, CONSTANTS_TO_ENUM, FUNCTION_TO_CLASS, TRIGGER_TO_ENUM

# to put inside f-strings
NEW_LINE = '\n'
TAB = '\t'

parser = ArgumentParser(
    description='Turn a modd.io game json file into python')
parser.add_argument('json_file', help='The exported game json file')


class GameGenerator():
    def __init__(self, json_file):
        if not json_file or not json_file.endswith('.json'):
            parser.error(f'{json_file} is not a json file')

        with open(json_file, 'rt') as game_file:
            game_json = json.loads(game_file.read())
            if game_json is None or game_json.get('data') is None:
                parser.error(f'{json_file} contains invalid content')

        self.game_data = GameData(game_json)
        self.game_name = snakecase(self.game_data.game_name)
        self.json_file_path = '/utils/game.json'

    def generate_project(self):
        files_to_generate = [
            GameVariablesPy(self.game_data.category_to_variables),
            MappingPy(self.game_name, self.game_data.game_items,
                      self.json_file_path),
            ScriptsPy(self.game_data.game_items),
            GameJson(self.json_file_path, self.game_data.game_json),
        ]

        print(f'\nGenerating project, {self.game_name}...')
        if not os.path.isdir(f'{self.game_name}/'):
            os.mkdir(f'{self.game_name}/')

        for file in files_to_generate:
            if file.ask_to_write and not self.can_write_project_file(file.file_path):
                continue
            self.write_project_file(file.file_path, file.generate_content())
            print(f' - {file.file_path} successfuly written')

        print('\nGame created/updated successfully\n')

    def can_write_project_file(self, file):
        # ask for input if file already exists
        if os.path.isfile(f'{self.game_name}/{file}'):
            response = input(
                f'   Do you want to overwrite {self.game_name}/{file}? (Y/n): ').strip()
            return response.strip() in ('Y', 'y')
        return True

    def write_project_file(self, file_path, content):
        file_base_path = f"{self.game_name}/{file_path[:file_path.rfind('/')]}"
        if '/' in file_path and not os.path.exists(f'{file_base_path}/'):
            os.makedirs(f'{file_base_path}/')
        with open(f'{self.game_name}/{file_path}', 'w') as game_file:
            game_file.write(content)


class GameData:
    # what variable types to generate
    GENERATION_CATEGORIES = [
        'entityTypeVariables', 'shops', 'animationTypes', 'states', 'projectileTypes', 'itemTypes', 'music',
        'sound', 'unitTypes', 'variables', 'attributeTypes', 'playerTypes', 'playerTypeVariables', 'dialogues',
    ]

    # variable types to seperate from the regular variables category
    SEPERATED_CATEGORIES = [
        'regions', 'itemTypeGroups', 'unitTypeGroups'
    ]

    def __init__(self, game_json):
        self.game_json = game_json
        self.game_name = game_json.get('title')
        self.game_data = game_json.get('data')
        self.game_items = self.retrieve_ordered_game_items()
        self.category_to_variables = self.retrieve_category_to_variables()

    def retrieve_ordered_game_items(self):
        game_items = self.game_data.get('scripts')
        folder_to_items = self.order_game_items_to_folder_key(game_items)
        root_game_items = self.merge_ordered_items(
            self.insert_items_into_folders(folder_to_items).get(None))
        return root_game_items

    def order_game_items_to_folder_key(self, game_items):
        # game root folder key is None
        folder_key_to_ordered_items = {}
        for item in game_items.values():
            order, parent_key = item.get('order'), item.get('parent')
            folder_dict = folder_key_to_ordered_items.setdefault(
                parent_key, {})
            # there can be scripts with the same order number, so store them in a list
            folder_dict.setdefault(order, []).append(item)
        # sort items based on their order numbers in each folder
        folder_key_to_ordered_items = self.sort_based_on_order_key(
            folder_key_to_ordered_items)
        return folder_key_to_ordered_items

    def sort_based_on_order_key(self, folder_to_items):
        sorted_folder_to_items = {}
        for folder_key in folder_to_items.keys():
            folder_dict = folder_to_items[folder_key]
            sorted_folder_to_items[folder_key] = sort_dictionary_based_on_keys(
                folder_dict)
        return sorted_folder_to_items

    def insert_items_into_folders(self, folder_to_items):
        """fill folders in the root game directory, and then folders inside those, up with their corresponding items"""
        inserted_folder_to_items = deepcopy(folder_to_items)
        item_queue = self.merge_ordered_items(
            inserted_folder_to_items.get(None, {}))
        while len(item_queue) > 0:
            item = item_queue.pop(0)
            if not is_game_item_folder(item):
                continue
            if (nested_items := inserted_folder_to_items.get(item.get('key'))) is None:
                continue
            item['children'] = self.merge_ordered_items(nested_items)
            item_queue += item['children']
        return inserted_folder_to_items

    def merge_ordered_items(self, ordered_items):
        merged_items = []
        for level in ordered_items.values():
            for item in level:
                merged_items.append(item)
        return merged_items

    def retrieve_category_to_variables(self):
        category_to_variables = {}
        for category in GameData.GENERATION_CATEGORIES:
            for variable_id, variable in self.game_data.get(category).items():
                variable_category = self.seperated_category_of_variable(variable) or category
                updated_variable = deepcopy(variable)
                updated_variable['id'] = variable_id
                category_to_variables.setdefault(variable_category, []).append(updated_variable)
        return category_to_variables

    def seperated_category_of_variable(self, variable):
        if (seperated_category := f"{variable.get('dataType')}s") in GameData.SEPERATED_CATEGORIES:
            return seperated_category
        return None


class GenerationFile:
    def __init__(self, file_path, ask_to_write):
        self.file_path = file_path
        self.ask_to_write = ask_to_write

    def generate_content(self):
        pass


class GameVariablesPy(GenerationFile):
    def __init__(self, category_to_variables):
        super().__init__('game_variables.py', False)
        self.category_to_variables = category_to_variables

    def generate_content(self):
        content = ''
        import_classes = []

        for category, variables in self.category_to_variables.items():
            variables = self.information_from_variables(variables)

            content += f'\n\nclass {class_name_from_category_name(category)}():\n'
            if len(variables) == 0:
                content += '\tpass\n'
                continue

            type_name = self.type_name_from_category(category)
            import_classes.append(type_name)
            # add variables
            for variable in variables:
                variable_type = None
                if self.is_category_variable_type(category):
                    variable_type = variable['data_type']
                content += f"""\t{variable['enum_name']} = {type_name}('{variable['id']}'{'' if not variable_type else f", variable_type='{variable_type}'"})\n"""
                # store variable information for generating scripts
                VariableCategories.add_variable_to_category(
                    category, variable['id'], variable['name'], variable['enum_name'])
        # add only used imports
        content = (
            f"from pymodd.functions import {', '.join([class_name for class_name in import_classes])}\n"
            f'{content}'
        )
        return content

    def information_from_variables(self, variables):
        information = []

        for variable in variables:
            variable_id = variable.get('id')
            variable_name = variable.get('name')
            data_type = variable.get('dataType')
            enum_name = snakecase(
                variable_name if variable_name is not None else variable_id).upper()

            variable = {'id': variable_id, 'name': variable_name,
                        'data_type': data_type, 'enum_name': enum_name}
            information.append(variable)
        return information

    def type_name_from_category(self, category):
        # to match with the classes defined in functions.py
        if category in GameData.SEPERATED_CATEGORIES:
            return 'Variable'
        return class_name_from_category_name(category).removesuffix('s')

    def is_category_variable_type(self, category):
        return 'variable' in category.lower() or category in GameData.SEPERATED_CATEGORIES


class ScriptsPy(GenerationFile):
    def __init__(self, game_items):
        super().__init__('scripts.py', True)
        self.game_items = game_items

    def generate_content(self):
        content = (
            'from pymodd.actions import *\n'
            'from pymodd.functions import *\n'
            'from pymodd.script import Script, Trigger, UiTarget, Flip\n\n'
            'from game_variables import *\n'
        )
        game_items_queue = self.game_items.copy()
        while len(game_items_queue) > 0:
            game_item = game_items_queue.pop(0)
            if is_game_item_folder(game_item):
                content += f"\n\n#\n# {game_item.get('folderName').upper()}\n#"
                game_items_queue[:0] = game_item.get('children')
                continue
            content += self.generate_script_class_content(game_item)
        return content

    def generate_script_class_content(self, script):
        script_triggers = [
            f"Trigger.{TRIGGER_TO_ENUM[trigger.get('type')]}" for trigger in script.get('triggers')]
        script_key = script.get('key')
        actions = JsonActions(script.get('actions')).convert_to_python()

        return (
            f'\n\nclass {class_name_from_script_data(script)}(Script):\n'
            f'\tdef _build(self):\n'
            f"\t\tself.key = '{script_key}'\n"
            f"\t\tself.triggers = [{', '.join(script_triggers)}]\n"
            f'\t\tself.actions = [\n'
            f"{''.join([f'{TAB * 3}{action},{NEW_LINE}' for action in actions])}\n"
            f'\t\t]\n'
        )


# work in progress:
class EntityScriptsPy(GenerationFile):
    def __init__(self, unit_types):
        super().__init__('entity_scripts.py', False)
        self.unit_types = unit_types

    def generate_content(self):
        content = ''


class MappingPy(GenerationFile):
    def __init__(self, game_name, game_items, game_json_file_path):
        super().__init__('mapping.py', False)
        self.game_name = game_name
        self.game_items = game_items
        self.game_json_file_path = game_json_file_path

    def generate_content(self):
        game_class_name = pascalcase(self.game_name)
        content = (
            'from pymodd.script import Game, Folder, write_game_to_output, write_to_output\n\n'
            'from scripts import *\n\n'
            f'class {game_class_name}(Game):\n'
            '\tdef _build(self):\n'
            '\t\tself.scripts = [\n'
        )

        for item in self.game_items:
            content += self.game_item_to_string(item, depth=3)

        content += (
            '\n\t\t]\n\n'
            f'# run this file to generate the all json files for this game `python {self.game_name}/mapping.py`\n'
            f"write_game_to_output({game_class_name}(json_file='{self.game_name}{self.game_json_file_path}'))\n\n"
            f'# uncomment the following to quickly generate the json file for a script\n'
            f"# write_to_output('output/', SCRIPT_OBJECT())\n"
        )
        return content

    def game_item_to_string(self, game_item, depth):
        if not is_game_item_folder(game_item):
            script_name = class_name_from_script_data(game_item)
            return f"{TAB * depth}{script_name}(),\n"
        folder_name = game_item.get('folderName')
        stringified_children = []
        for child in game_item.get('children'):
            stringified_children.append(
                self.game_item_to_string(child, depth + 1))
        surrounding_quote = surrounding_quote_for_string(folder_name)
        return (
            f'''{TAB * depth}Folder({surrounding_quote}{folder_name}{surrounding_quote}, [\n'''
            f"{''.join(stringified_children)}"
            f"{TAB * depth}]),\n"
        )


class GameJson(GenerationFile):
    def __init__(self, game_json_path, entire_game_json):
        super().__init__(game_json_path, False)
        self.entire_game_json = entire_game_json

    def generate_content(self):
        return json.dumps(self.entire_game_json)


class JsonActions:
    def __init__(self, json_actions, depth=3):
        self.actions = json_actions
        # how many tabs away the actions are from the left (3 is the minimum)
        self.depth = max(depth, 3)

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
            if arg in ('type', 'vars', 'function', 'comment', 'disabled'):
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
        # xy force is returned as one argument by modd, but in actions.py there are two arguemnts for x and y
        if argument in ('force', 'velocity', 'impulse') and (x := value.get('x')) is not None:
            return [
                {'name': 'x',
                 'value': self.python_from_function(f'{argument}_x', x)},
                {'name': 'y',
                 'value': self.python_from_function(f'{argument}_y', value.get('y'))}
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
            f"{''.join([f'{TAB * (self.depth + 1)}{action},{NEW_LINE}' for action in JsonActions(function, self.depth + 1).convert_to_python()])}"
            f'{TAB * self.depth}]'
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
            if (category_dict := VariableCategories.get_category(category)) and (variable_name := category_dict.get(value)):
                return f'{class_name_from_category_name(category)}.{variable_name}'
        return None

    def primitive_from_function(self, value):
        primitives = [int, float, str, bool]
        if type(value) not in primitives:
            return None
        # surround strings with quotes
        if type(value) == str:
            quote = surrounding_quote_for_string(value)
            value = f"{quote}{self.insert_tabs_into_multiline_string(value)}{quote}"
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

    def insert_tabs_into_multiline_string(self, string):
        if '\n' in string:
            tabs = f"\n{TAB * (self.depth + 1)}"
            return tabs + tabs.join(string.splitlines())
        return string

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
        args, unused_args = [None] * len(class_arguments), []

        for arg in args_dict:
            arg_name = arg.get('name')
            if (index := self.index_of_arg_in_class_args(arg_name, class_arguments)) != -1:
                class_arguments[index] = None
                args[index] = arg.get('value')
                continue
            unused_args.append(arg)
        for i, arg in enumerate(args):
            if arg is not None:
                continue
            value = 'Null()'
            if len(unused_args) > 0:
                value = unused_args.pop(0).get('value')
            args[i] = value
        return args

    def index_of_arg_in_class_args(self, arg_name, class_args):
        possible_args = (arg_name, camelcase(arg_name), snakecase(arg_name))
        for i, class_arg in enumerate(class_args):
            if class_arg is None:
                continue
            if class_arg in possible_args or any(arg in class_arg for arg in possible_args):
                return i
        return -1


class VariableCategories():
    # used for finding the enum names of variables while generating scripts
    categories = {}

    @staticmethod
    def get_category(category, default=None):
        return VariableCategories.categories.get(category, default)

    @staticmethod
    def create_category(category_name):
        VariableCategories.categories[category_name] = {}

    @staticmethod
    def add_variable_to_category(category_name, variable_id, variable_name, enum_name):
        if category_name not in VariableCategories.categories.keys():
            VariableCategories.create_category(category_name)

        if variable_name is not None:
            VariableCategories.categories[category_name][variable_name] = enum_name
        VariableCategories.categories[category_name][variable_id] = enum_name


def class_name_from_script_data(script_data):
    script_name = script_data.get('name') or script_data.get('key')
    class_name = pascalcase(script_name).strip()
    if len(script_name) == 0 or not class_name[0].isalpha() or camelcase(script_name) in GameData.GENERATION_CATEGORIES + GameData.SEPERATED_CATEGORIES:
        class_name = f"q{class_name}"
    return class_name


def class_name_from_category_name(category_name):
    category_name_to_class = {
        'entityTypeVariables': 'entityVariables',
        'playerTypeVariables': 'playerVariables',
    }
    category_name = pascalcase(
        category_name_to_class.get(category_name, category_name))
    return f"{category_name}{'s' if category_name[-1] != 's' else ''}"


def surrounding_quote_for_string(string):
    if "'" in string:
        return '''"'''
    if any(char in string for char in ['''"''', '`', '\n']):
        return """'''"""
    return "'"


def is_game_item_folder(game_item):
    return game_item.get('actions') is None


def sort_dictionary_based_on_keys(dictionary):
    return dict(sorted(dictionary.items()))


def main():
    args = parser.parse_args()
    GameGenerator(args.json_file).generate_project()


if __name__ == '__main__':
    main()
