import json
import random
import string

from caseconverter import camelcase


class Base():
    def to_dict(self):
        raise NotImplementedError('to_dict method not implemented')


class Game(Base):
    def __init__(self, json_file_path, game_variable_classes, project_globals_data):
        self.project_globals_data = project_globals_data
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        self.name = data.get('title')
        self.data = data
        self.entity_scripts = []
        self.scripts = []
        self._update_data_with_variable_classes(game_variable_classes)
        self._build()
        # set position of scripts inside game
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)

    def _update_data_with_variable_classes(self, variable_classes):
        # pull variable objects out from each class and place them in categories
        variable_category_to_variables = {}
        for klass in variable_classes:
            variable_category = variable_category_name_from_variable_class_name(
                klass.__name__)
            variable_category_to_variables.setdefault(variable_category, [])
            class_vars = [item for item in vars(klass)
                          if not item.startswith('_') and not callable(item)]
            for var in class_vars:
                variable_category_to_variables[variable_category].append(getattr(
                    klass, var))

        # update game data with modified variable objects
        for variable_category, variables in variable_category_to_variables.items():
            if variable_category not in self.data['data'].keys():
                continue
            category_data = self.data['data'][variable_category]
            unincluded_variable_ids = list(
                category_data.keys())
            for variable in variables:
                category_contains_variable = variable.id in category_data.keys()
                category_data[variable.id] = variable.updated_data_with_user_provided_values(
                    category_data[variable.id] if category_contains_variable else variable.get_template_data())
                if variable.id in unincluded_variable_ids:
                    unincluded_variable_ids.remove(variable.id)
            # remove variables no longer included
            for unincluded_variable_id in unincluded_variable_ids:
                category_data.pop(unincluded_variable_id)

    def _build():
        pass

    def to_dict(self):
        # update global scripts
        self.data['data']['scripts'] = self.flatten_scripts_data(self.scripts)

        # update data of each entity_type
        for entity_script in self.entity_scripts:
            entity_category, entity_id = f'{camelcase(entity_script.entity_type.__class__.__name__)[:-4]}s', entity_script.entity_type.id
            entity_data = self.data['data'][entity_category][entity_id]

            # update entity scripts
            entity_data['scripts'] = self.flatten_scripts_data(
                entity_script.scripts)

            if entity_category != "unitTypes":
                continue
            # update entity keybindings for unit types
            entity_keybindings_data = entity_data['controls']['abilities']
            unincluded_keys = list(entity_keybindings_data.keys())
            for (key, scripts) in entity_script.keybindings.items():
                entity_keybindings_data[key.value] = scripts.to_dict(
                    entity_keybindings_data.get(key.value))
                if key.value in unincluded_keys:
                    unincluded_keys.remove(key.value)
            # remove keybindings no longer included
            for unincluded_key in unincluded_keys:
                if unincluded_key in ['lookWheel', 'movementWheel']:
                    continue
                entity_keybindings_data.pop(unincluded_key)
        return self.data

    def flatten_scripts_data(self, scripts):
        '''Takes all scripts out of folders, transforms them into json, and returns one dictionary with all of the game's script

        Returns:
            dict(str, dict): keys are script keys, values are datas of scripts
        '''
        flattened_scripts = {}
        scripts_queue = scripts.copy()
        while len(scripts_queue) > 0:
            script = scripts_queue.pop(0)
            scripts_data = None
            # add folder's scripts to the queue
            if isinstance((folder := script), Folder):
                script_data = folder.to_dict()
                scripts_queue += folder.scripts
            else:
                script_data = script.to_dict(self.project_globals_data)
            flattened_scripts[script_data['key']] = script_data
        return flattened_scripts


def variable_category_name_from_variable_class_name(variable_class_name):
    if variable_class_name == 'EntityVariables':
        return 'entityTypeVariables'
    elif variable_class_name == 'PlayerVariables':
        return 'playerTypeVariables'
    elif variable_class_name == 'Musics':
        return 'music'
    elif variable_class_name in ['Regions', 'ItemTypeGroups', 'UnitTypeGroups']:
        return 'variables'
    else:
        return camelcase(variable_class_name)


class File(Base):
    def __init__(self):
        self.name = None
        self.key = None
        self.parent = None
        self.order = 0

    def set_position(self, order, parent):
        self.order = order
        self.parent = parent


class Folder(File):
    def __init__(self, name, scripts: list):
        super().__init__()
        self.name = name
        self.key = generate_random_key()
        self.scripts = scripts
        # set position of scripts inside the folder
        for i, script in enumerate(scripts):
            script.set_position(i, self.key)

    def to_dict(self):
        return {
            'key': self.key,
            'folderName': self.name,
            'parent': self.parent,
            'order': self.order,
            'expanded': True
        }


def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
