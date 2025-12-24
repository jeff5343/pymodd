from __future__ import annotations
import json
from typing import Any

from caseconverter import camelcase

from pymodd.core.script import Script
from pymodd.variable.variable_type import VariableType
from pymodd.core.base import Base
from pymodd.core.folder import Folder
from pymodd.core.file import File


class Game(Base):
    def __init__(
        self,
        json_file_path: str,
        game_variable_classes: list[type],
        project_globals_data: dict[str, Any],
    ):
        self.project_globals_data: dict[str, Any] = project_globals_data
        with open(json_file_path, "r") as file:
            data = json.load(file)
        self.name: str = data.get("title")
        self.data: Any = data
        # holds EntityScripts
        self.entity_scripts: list[Any] = []
        self.scripts: list[File] = []
        self._update_data_with_variable_classes(game_variable_classes)
        self._build()
        # set position of scripts inside game
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)

    def _update_data_with_variable_classes(self, variable_classes: list[type]):
        # pull variable objects out from each class and place them in categories
        variable_category_to_variables: dict[str, list[VariableType]] = {}
        for klass in variable_classes:
            variable_category = variable_category_name_from_variable_class_name(
                klass.__name__
            )
            _ = variable_category_to_variables.setdefault(variable_category, [])
            # get variables name from the class
            class_var_names: list[str] = [
                item
                for item in vars(klass)
                if not item.startswith("_") and not callable(item)
            ]
            # get the variable type instance assigned to that name
            for var_name in class_var_names:
                variable_category_to_variables[variable_category].append(
                    getattr(klass, var_name)
                )

        # update old game data (JSON) with new/modified variable objects
        for variable_category, variables in variable_category_to_variables.items():
            # skip categories that do not exist (TODO: check what to do about REGIONS)
            if variable_category not in self.data["data"].keys():
                continue
            # get game data JSON for this category
            old_category_data: dict[str, Any] = self.data["data"][variable_category]
            old_variable_ids = list(old_category_data.keys())
            for variable in variables:
                # check if variable already existed in the old data
                variable_exists = variable.id in old_category_data.keys()
                old_category_data[variable.id] = (
                    variable.updated_data_with_user_provided_values(
                        old_category_data[variable.id]
                        if variable_exists
                        else variable.get_template_data()
                    )
                )
                if variable.id in old_variable_ids:
                    old_variable_ids.remove(variable.id)
            # remove variables no longer included
            for unincluded_variable_id in old_variable_ids:
                old_category_data.pop(unincluded_variable_id)

    def _build(self) -> None:
        pass

    def to_dict(self) -> Any:
        # update global scripts
        self.data["data"]["scripts"] = self.flatten_scripts_data()

        # update data of each entity_type
        for entity_script in self.entity_scripts:
            entity_script.project_globals_data = self.project_globals_data
            entity_category, entity_id = (
                f"{camelcase(entity_script.entity_type.__class__.__name__)[:-4]}s",
                entity_script.entity_type.id,
            )
            entity_data = self.data["data"][entity_category][entity_id]

            entity_data["scripts"] = entity_script.flatten_scripts_data()

            if entity_category != "unitTypes":
                continue

            # get keybindings JSON for this entity
            old_keybindings_data = entity_data["controls"]["abilities"]
            old_keys = list(old_keybindings_data.keys())

            # update entity keybindings for unit types with scripts
            for key, scripts in entity_script.keybindings.items():
                old_keybindings_data[key.value] = scripts.to_dict(
                    old_keybindings_data.get(key.value)
                )
                if key.value in old_keys:
                    old_keys.remove(key.value)
            # remove keybindings no longer included
            for key in old_keys:
                if key in ["lookWheel", "movementWheel"]:
                    continue
                old_keybindings_data.pop(key)
        return self.data

    def flatten_scripts_data(self) -> dict[str, Any]:
        """Takes all scripts out of folders, transforms them into json, and returns one dictionary with all of the game's script
        Returns:
            dict(str, dict): keys are script keys, values are datas of scripts
        """
        flattened_scripts = {}
        scripts_queue = self.scripts.copy()
        while len(scripts_queue) > 0:
            script = scripts_queue.pop(0)  # pyright: ignore[reportAssignmentType]
            script_data = None
            # add folder's scripts to the queue
            if isinstance((folder := script), Folder):
                script_data = folder.to_dict()
                scripts_queue += folder.scripts
            elif isinstance((s := script), Script):
                script: Script
                script_data = script.to_dict(self.project_globals_data)
            else:
                script_data = {"key": None}
            flattened_scripts[script_data["key"]] = script_data
        return flattened_scripts

    def find_script(self, script_name: str) -> Script | None:
        scripts_queue = self.scripts.copy()
        while len(scripts_queue) > 0:
            script = scripts_queue.pop(0)  # pyright: ignore[reportAssignmentType]
            # add folder's scripts to the queue
            if isinstance((folder := script), Folder):
                scripts_queue += folder.scripts
                continue
            script: Script
            if script.name == script_name:
                return script
        return None


def variable_category_name_from_variable_class_name(variable_class_name: str) -> str:
    if variable_class_name == "EntityVariables":
        return "entityTypeVariables"
    elif variable_class_name == "PlayerVariables":
        return "playerTypeVariables"
    elif variable_class_name == "Musics":
        return "music"
    elif variable_class_name in ["Regions", "ItemTypeGroups", "UnitTypeGroups"]:
        return "variables"
    else:
        return camelcase(variable_class_name)
