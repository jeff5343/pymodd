from _ast import AnnAssign, Assign, AugAssign, Delete
import ast
import inspect
import json
import random
import string
import textwrap
from enum import Enum
from typing import Any

from caseconverter import camelcase, snakecase

import pymodd


class Base():
    def to_dict(self):
        raise NotImplementedError("to_dict method not implemented")


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
            unincluded_category_variable_ids = list(
                category_data.keys())
            for variable in variables:
                category_contains_variable = variable.id in category_data.keys()
                category_data[variable.id] = variable.updated_data_with_user_provided_values(
                    category_data[variable.id] if category_contains_variable else variable.get_template_data())
                if variable.id in unincluded_category_variable_ids:
                    unincluded_category_variable_ids.remove(variable.id)
            # remove variables no longer included
            for unincluded_variable_id in unincluded_category_variable_ids:
                category_data.pop(unincluded_variable_id)

    def _build():
        pass

    def to_dict(self):
        # replace game scripts with scripts defined in self.scripts
        self.data['data']['scripts'] = self.flatten_scripts_data(self.scripts)
        for script in self.entity_scripts:
            entity_type_category, entity_type_id = f'{camelcase(script.entity_type.__class__.__name__)}s', script.entity_type.id
            self.data['data'][entity_type_category][entity_type_id]['scripts'] = self.flatten_scripts_data(
                script.scripts)
        return self.data

    def flatten_scripts_data(self, scripts):
        """Takes all scripts out of folders, transforms them into json, and put them all into one dictionary with the rest of the game's scripts

        Returns:
            dict: keys are the script's key, values are the script's data
        """
        flattened_scripts = {}
        scripts_queue = scripts.copy()
        while len(scripts_queue) > 0:
            script = scripts_queue.pop(0)
            # add folder's scripts to the queue
            if isinstance(script, Folder):
                scripts_queue += script.scripts
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


class EntityScripts(Game):
    def __init__(self):
        self.entity_type = None
        self.scripts = []
        self._build()
        # set position of scripts inside entity_scripts
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)

    def to_dict(self):
        self.flatten_scripts_data(self.scripts)
        return self.data


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


class Script(File):
    _class_to_key = {}

    def __new__(cls, *args, **kwargs):
        if cls._class_to_key.get(cls, None) is None:
            cls._class_to_key[cls] = generate_random_key()
        return super(Script, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()
        self.name = snakecase(self.__class__.__name__).replace('_', ' ')
        self.key = Script._class_to_key[self.__class__]
        self.triggers = []
        self.actions = []
        self.build_func_source_code = None

    def _build(self):
        pass

    def to_dict(self, project_globals_data):
        return {
            'triggers': [{'type': trigger.value} for trigger in self.triggers],
            'conditions': [{'operator': '==', 'operandType': 'boolean'}, True, True],
            'actions': ScriptActionsCompiler(self, project_globals_data).actions_data,
            'name': self.name,
            'parent': self.parent,
            'key': self.key,
            'order': self.order
        }


def script(triggers=[], name=None):
    """
    Args:
        triggers (list, optional): triggers for the script. Defaults to [].
        name (str, optional): name to override the default name of the script. Defaults to the class name of the script.
    """
    def wrapper_script(cls):
        class NewScript(Script):
            def __init__(self):
                super().__init__()
                self.triggers = triggers
                if name is not None:
                    self.name = name
                else:
                    self.name = snakecase(cls.__name__).replace('_', ' ')
                self.build_func_source_code = inspect.getsource(cls._build)

            def _build(self):
                cls._build(self)

        return NewScript
    return wrapper_script


class ScriptActionsCompiler(ast.NodeVisitor):
    def __init__(self, script: Script, project_globals_data) -> None:
        self.project_globals_data = project_globals_data
        self.depth_to_locals_data = {0: {}}
        self.depth = 0
        self.actions_data = []
        tree = ast.parse(textwrap.dedent(script.build_func_source_code))
        self.visit(tree)

    def visit(self, node: ast.AST):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)

        if visitor == self.generic_visit or visitor in [self.visit_Assign, self.visit_AnnAssign, self.visit_Delete]:
            return visitor(node)

        if visitor in [self.visit_If, self.visit_While, self.visit_For]:
            self.depth += 1
            self.depth_to_locals_data[self.depth] = {}
            action_data = visitor(node)
            self.depth_to_locals_data.pop(self.depth)
            self.depth -= 1
        else:
            action_data = visitor(node)
        if self.depth == 0:
            self.actions_data.append(action_data)
        return action_data

    def visit_Expr(self, node: ast.Expr):
        action = self.eval_node(node.value)
        return action

    def visit_If(self, node: ast.If):
        then_actions_data = [self.visit(nde) for nde in node.body]
        else_actions_data = [self.visit(nde) for nde in node.orelse]
        if_action_data = pymodd.actions.if_else(
            self.eval_node(node.test), then_actions_data, else_actions_data)
        return if_action_data

    def visit_While(self, node: ast.While):
        actions_data = [self.visit(nde) for nde in node.body]
        return pymodd.actions.while_do(self.eval_node(node.test), actions_data)

    def visit_For(self, node: ast.For):
        # work on this tommorow
        if isinstance(node.target, ast.Name):
            self.add_local_var_to_curr_depth_locals_data(node.target.id, 5)

        actions_data = [self.visit(nde) for nde in node.body]
        return pymodd.actions.for_all_players_in(pymodd.functions.AllPlayers(), actions_data)

    def visit_Break(self, node: ast.Break):
        return pymodd.actions.break_loop()

    def visit_Continue(self, node: ast.Continue):
        return pymodd.actions.continue_loop()

    def visit_Return(self, node: ast.Return):
        return pymodd.actions.return_loop()

    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.add_local_var_to_curr_depth_locals_data(
                    target.id, self.eval_node(node.value))
            elif isinstance(target, ast.Tuple):
                for tuple_target in target.elts:
                    self.add_local_var_to_curr_depth_locals_data(
                        tuple_target.id, self.eval_node(node.value))

    def visit_AnnAssign(self, node: AnnAssign):
        if isinstance(node.target, ast.Name):
            self.add_local_var_to_curr_depth_locals_data(
                node.target.id, self.eval_node(node.value))

    # unsure how to do for now
    # def visit_AugAssign(self, node: AugAssign):
    #     if isinstance(node.target, ast.Name):
    #         self.depth_to_locals_data[self.depth][node.target.id] = self.eval_node(
    #             node.value)

    def visit_Delete(self, node: Delete):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.depth_to_locals_data[self.depth].pop(target.id)

    def get_current_locals_data(self):
        locals_data = {}
        for value in self.depth_to_locals_data.values():
            locals_data.update(value)
        return locals_data

    def add_local_var_to_curr_depth_locals_data(self, var_name, var_value):
        self.depth_to_locals_data[self.depth][var_name] = var_value

    def eval_node(self, node: ast.AST):
        return eval(compile(ast.Expression(body=node), filename='<ast>', mode='eval'), self.project_globals_data, self.get_current_locals_data())


def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def to_dict(obj):
    if isinstance(obj, Base):
        return obj.to_dict()
    if isinstance(obj, Enum):
        return obj.value
    return obj


# ---------------------------------------------------------------------------- #
#                                   Constants                                  #
# ---------------------------------------------------------------------------- #


class Trigger(Enum):
    GAME_START = 'gameStart'
    EVERY_FRAME = 'frameTick'
    EVERY_SECOND = 'secondTick'
    SERVER_SHUTTING_DOWN = 'serverShuttingDown'

    UNIT_TOUCHES_WALL = 'unitTouchesWall'
    UNIT_USES_ITEM = 'unitUsesItem'
    UNIT_ATTRIBUTE_BECOMES_ZERO = 'unitAttributeBecomesZero'
    UNIT_STARTS_USING_AN_ITEM = 'unitStartsUsingAnItem'
    UNIT_ATTRIBUTE_BECOMES_FULL = 'unitAttributeBecomesFull'
    UNIT_DROPPED_AN_ITEM = 'unitDroppedAnItem'
    UNIT_ENTERS_REGION = 'unitEntersRegion'
    UNIT_TOUCHES_ITEM = 'unitTouchesItem'
    UNIT_PICKED_AN_ITEM = 'unitPickedAnItem'
    UNIT_TOUCHES_UNIT = 'unitTouchesUnit'
    UNIT_TOUCHES_DEBRIS = 'unitTouchesDebris'
    UNIT_TOUCHES_PROJECTILE = 'unitTouchesProjectile'
    UNIT_STOPS_USING_AN_ITEM = 'unitStopsUsingAnItem'
    UNIT_ATTACKS_UNIT = 'unitAttacksUnit'
    UNIT_SELECTS_ITEM = 'unitSelectsItem'
    UNIT_SELECTS_INVENTORY_SLOT = 'unitSelectsInventorySlot'
    UNIT_ENTERS_SENSOR = 'unitEntersSensor'

    PROJECTILE_TOUCHES_ITEM = 'projectileTouchesItem'
    PROJECTILE_TOUCHES_DEBRIS = 'projectileTouchesDebris'
    PROJECTILE_ATTRIBUTE_BECOMES_ZERO = 'projectileAttributeBecomesZero'
    PROJECTILE_TOUCHES_WALL = 'projectileTouchesWall'
    PROJECTILE_ENTERS_SENSOR = 'projectileEntersSensor'

    PLAYER_CUSTOM_INPUT = 'playerCustomInput'
    PLAYER_ATTRIBUTE_BECOMES_FULL = 'playerAttributeBecomesFull'
    PLAYER_JOINS_GAME = 'playerJoinsGame'
    PLAYER_PURCHASES_UNIT = 'playerPurchasesUnit'
    PLAYER_LEAVES_GAME = 'playerLeavesGame'
    PLAYER_ATTRIBUTE_BECOMES_ZERO = 'playerAttributeBecomesZero'
    PLAYER_SENDS_CHAT_MESSAGE = 'playerSendsChatMessage'

    ITEM_ATTRIBUTE_BECOMES_FULL = 'itemAttributeBecomesFull'
    ITEM_ENTERS_REGION = 'itemEntersRegion'
    ITEM_TOUCHES_WALL = 'itemTouchesWall'
    ITEM_ATTRIBUTE_BECOMES_ZERO = 'itemAttributeBecomesZero'
    ITEM_IS_USED = 'itemIsUsed'
    ITEM_ENTERS_SENSOR = 'itemEntersSensor'
    RAYCAST_ITEM_FIRED = 'raycastItemFired'

    ENTITY_CREATED = 'entityCreated'
    ENTITY_TOUCHES_WALL = 'entityTouchesWall'
    ENTITY_TOUCHES_ITEM = 'entityTouchesItem'
    ENTITY_TOUCHES_UNIT = 'entityTouchesUnit'
    ENTITY_TOUCHES_PROJECTILE = 'entityTouchesProjectile'
    ENTITY_ATTRIBUTE_BECOMES_ZERO = 'entityAttributeBecomesZero'
    ENTITY_ATTRIBUTE_BECOMES_FULL = 'entityAttributeBecomesFull'
    ENTITY_ENTERS_REGION = 'entityEntersRegion'
    ENTITY_GETS_ATTACKED = 'entityGetsAttacked'

    DEBRIS_ENTERS_REGION = 'debrisEntersRegion'

    AD_PLAY_COMPLETED = 'adPlayCompleted'
    AD_PLAY_SKIPPED = 'adPlaySkipped'
    AD_PLAY_FAILED = 'adPlayFailed'
    AD_PLAY_BLOCKED = 'adPlayBlocked'

    SEND_COINS_SUCCESS = 'sendCoinsSuccess'
    COIN_SEND_FAILURE_DUE_TO_DAILY_LIMIT = 'coinSendFailureDueToDailyLimit'
    COIN_SEND_FAILURE_DUE_TO_INSUFFICIENT_COINS = 'coinSendFailureDueToInsufficientCoins'


class UiTarget(Enum):
    TOP = 'top'
    CENTER = 'center-lg'
    SCOREBOARD = 'scoreboard'


class Flip(Enum):
    NONE = 'none'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    BOTH = 'both'
