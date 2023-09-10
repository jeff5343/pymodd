import ast
import inspect
import textwrap
from enum import Enum
from _ast import AnnAssign, Assign, Delete

from caseconverter import snakecase

import pymodd
from pymodd import _pymodd_helper
from pymodd.game import Base, File, generate_random_key


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
        self.build_actions_function = None

    def to_dict(self, project_globals_data):
        script_actions_compiler = ScriptActionsCompiler(project_globals_data)
        actions_data = None
        try:
            actions_data = script_actions_compiler.compile_script(self)
        except ScriptActionsCompileError as compile_error:
            script_source_file = inspect.getsourcefile(
                self.build_actions_function)
            script_source_starting_line_num = inspect.getsourcelines(
                self.build_actions_function)[1]

            print()
            _pymodd_helper.log_error('Compile error!\n')
            print(f''' File "{script_source_file}", line {script_source_starting_line_num + compile_error.error_line_num - 1}''',
                  f'   {compile_error.error_line_code}\n',
                  f'{type(compile_error.error).__name__}: {compile_error.error}\n',
                  sep='\n')
            import sys
            sys.exit(1)
        return {
            'triggers': [{'type': trigger.value} for trigger in self.triggers],
            'conditions': [{'operator': '==', 'operandType': 'boolean'}, True, True],
            'actions': actions_data,
            'name': self.name,
            'parent': self.parent,
            'key': self.key,
            'order': self.order
        }


def script(triggers=[], name=None):
    '''turn a function into a script

    Args:
        triggers (list, optional): triggers for the script. Defaults to [].

        name (str, optional): name to override the default name of the script. Defaults to the function name of the script.
    '''
    def wrapper_script(func):
        class NewScript(Script):
            def __init__(self):
                super().__init__()
                self.triggers = triggers
                if name is not None:
                    self.name = name
                else:
                    self.name = func.__name__.replace('_', ' ')
                self.build_actions_function = func

        return NewScript
    return wrapper_script


class ScriptActionsCompileError(Exception):
    '''Exception raised for errors while compiling script actions'''

    def __init__(self, error_line_num, error_line_code, error) -> None:
        self.error_line_num = error_line_num
        self.error_line_code = error_line_code
        self.error = error
        # handle recursive errors
        if isinstance(error, ScriptActionsCompileError):
            self.error_line_num = error.error_line_num
            self.error_line_code = error.error_line_code
            self.error = error.error


class ScriptActionsCompiler(ast.NodeVisitor):
    def __init__(self, project_globals_data):
        self.project_globals_data = project_globals_data

    def compile_script(self, script: Script):
        self.depth = 0
        self.depth_to_locals_data = {0: {}}
        self.actions_data = []
        tree = ast.parse(textwrap.dedent(
            inspect.getsource(script.build_actions_function)))
        self.visit(tree)
        return self.actions_data

    def visit(self, node: ast.AST):
        '''Visit a node.'''
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)

        try:
            if visitor == self.generic_visit or visitor in [self.visit_Assign, self.visit_AnnAssign, self.visit_Delete]:
                return visitor(node)

            if visitor in [self.visit_If, self.visit_While, self.visit_For, self.visit_With]:
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
        except Exception as error:
            raise ScriptActionsCompileError(
                node.lineno if 'lineno' in node._attributes else 1,
                ast.unparse(node).splitlines()[0],
                error
            )

    def visit_Expr(self, node: ast.Expr):
        action = self.eval_node(node.value)
        return action

    def visit_If(self, node: ast.If):
        then_actions_data = self.parse_actions_of_body(node.body)
        else_actions_data = self.parse_actions_of_body(node.orelse)
        if_action_data = pymodd.actions.if_else(
            self.eval_condition(node.test), then_actions_data, else_actions_data)
        return if_action_data

    def visit_While(self, node: ast.While):
        actions_data = self.parse_actions_of_body(node.body)
        return pymodd.actions.while_do(self.eval_condition(node.test), actions_data)

    def visit_For(self, node: ast.For):
        evaled_iter = self.eval_node(node.iter)
        # repeat action
        if isinstance((repeat_action_data := evaled_iter), dict) and repeat_action_data.get('type') == 'repeat':
            repeat_action_data['actions'] = self.parse_actions_of_body(
                node.body)
            return repeat_action_data
        # for loop action
        elif isinstance((loop_function_data := evaled_iter), dict) and repeat_action_data.get('type') == 'for':
            for_loop_var = self.eval_code(ast.unparse(node.target))
            if for_loop_var.data_type != pymodd.variable_types.DataType.NUMBER:
                raise TypeError(
                    f"DataType of '{ast.unparse(node.iter)}' must be DataType.NUMBER"
                )
            loop_function_data['variableName'] = for_loop_var.id
            loop_function_data['actions'] = self.parse_actions_of_body(
                node.body)
            return loop_function_data
        # for _ in group variable action
        elif isinstance((variable := evaled_iter), pymodd.variable_types.VariableBase):
            if variable.data_type not in [pymodd.variable_types.DataType.ITEM_GROUP, pymodd.variable_types.DataType.UNIT_GROUP,
                                          pymodd.variable_types.DataType.PLAYER_GROUP, pymodd.variable_types.DataType.ITEM_TYPE_GROUP,
                                          pymodd.variable_types.DataType.UNIT_TYPE_GROUP]:
                raise TypeError(
                    f"DataType of '{ast.unparse(node.iter)}' must be DataType.ITEM_GROUP, UNIT_GROUP, PLAYER_GROUP, ITEM_TYPE_GROUP, or UNIT_TYPE_GROUP"
                )
            if isinstance(node.target, ast.Name):
                self.add_local_var_to_curr_depth_locals_data(
                    node.target.id, variable._get_iteration_object())
            action = variable._get_iterating_action()
            return action(variable, self.parse_actions_of_body(node.body))
        # for _ in group function action
        elif isinstance((group_function := evaled_iter), pymodd.functions.Function):
            if not isinstance(group_function, pymodd.functions.Group):
                raise TypeError(
                    f"'{ast.unparse(node.iter)}' is not iterable"
                )
            if isinstance(node.target, ast.Name):
                self.add_local_var_to_curr_depth_locals_data(
                    node.target.id, group_function._get_iteration_object())
            action = group_function._get_iterating_action()
            return action(group_function, self.parse_actions_of_body(node.body))

    def visit_With(self, node: ast.With):
        evaled_item = self.eval_code(ast.unparse(node.items[0]))
        if isinstance((timeout_action_data := evaled_item), dict) and timeout_action_data.get('type') == 'setTimeOut':
            timeout_action_data['actions'] = self.parse_actions_of_body(
                node.body)
            return timeout_action_data
        raise ValueError(
            "'with' statement argument must be a 'after_timeout' action"
        )

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

    def visit_Delete(self, node: Delete):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.depth_to_locals_data[self.depth].pop(target.id)

    def parse_actions_of_body(self, node_body):
        actions_data = []
        for node in node_body:
            action_data = self.visit(node)
            if action_data is not None:
                actions_data.append(action_data)
        return actions_data

    def get_current_locals_data(self):
        locals_data = {}
        for value in self.depth_to_locals_data.values():
            locals_data.update(value)
        return locals_data

    def add_local_var_to_curr_depth_locals_data(self, var_name, var_value):
        self.depth_to_locals_data[self.depth][var_name] = var_value

    def eval_condition(self, condition_node: ast.AST):
        if isinstance(condition_node, ast.BoolOp):
            return pymodd.functions.Condition(
                self.eval_condition(condition_node.values[0]),
                'AND' if isinstance(condition_node.op, ast.And) else 'OR',
                self.eval_condition(condition_node.values[1]))

        if isinstance(condition_node, ast.Compare):
            ast_operator_to_string = {
                ast.Eq: '==', ast.NotEq: '!=',
                ast.Gt: '>', ast.Lt: '<',
                ast.GtE: '>=', ast.LtE: '<='
            }
            if len(condition_node.ops) == 0 or (operator := ast_operator_to_string.get(type(condition_node.ops[0]))) is None:
                raise ValueError(
                    f"Condition '{ast.unparse(condition_node)}' contains an invalid comparison operator"
                )
            return pymodd.functions.Condition(
                self.eval_node(condition_node.left),
                operator,
                self.eval_node(condition_node.comparators[0]))

        raise ValueError(
            f"Condition '{ast.unparse(condition_node)}' must include a comparison operator"
        )

    def eval_node(self, node: ast.AST):
        return self.eval_code(compile(ast.Expression(body=node), filename='<ast>', mode='eval'))

    def eval_code(self, code):
        return eval(code, self.project_globals_data, self.get_current_locals_data())


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
    UNIT_LEAVES_REGION = 'unitLeavesRegion'
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
    ITEM_LEAVES_REGION = 'itemLeavesRegion'
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
    ENTITY_LEAVES_REGION = 'entityLeavesRegion'
    ENTITY_GETS_ATTACKED = 'entityGetsAttacked'

    DEBRIS_ENTERS_REGION = 'debrisEntersRegion'

    AD_PLAY_COMPLETED = 'adPlayCompleted'
    AD_PLAY_SKIPPED = 'adPlaySkipped'
    AD_PLAY_FAILED = 'adPlayFailed'
    AD_PLAY_BLOCKED = 'adPlayBlocked'

    SEND_COINS_SUCCESS = 'sendCoinsSuccess'
    COIN_SEND_FAILURE_DUE_TO_DAILY_LIMIT = 'coinSendFailureDueToDailyLimit'
    COIN_SEND_FAILURE_DUE_TO_INSUFFICIENT_COINS = 'coinSendFailureDueToInsufficientCoins'

    ON_POST_RESPONSE = 'onPostResponse'


class UiTarget(Enum):
    TOP = 'top'
    CENTER = 'center-lg'
    SCOREBOARD = 'scoreboard'


class Flip(Enum):
    NONE = 'none'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    BOTH = 'both'
