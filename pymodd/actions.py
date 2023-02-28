from __future__ import annotations
import functools

from .functions import Condition, Number, String
from .script import Base, to_dict


def action(func):
    @functools.wraps(func)
    def wrapper_action(*args, **kwargs):
        action_dictionary = (func(*args))
        action_dictionary.update(
            parse_optional_arguments_into_dictionary(
                kwargs.get('comment', None),
                kwargs.get('disabled', False),
                kwargs.get('run_on_client', False)))
        return action_dictionary
    return wrapper_action


def parse_optional_arguments_into_dictionary(comment, disabled, run_on_client):
    dictionary = {}
    if comment is not None:
        dictionary['comment'] = comment
    if disabled:
        dictionary['disabled'] = True
    if run_on_client:
        dictionary['runOnClient'] = True
    return dictionary


@action
def if_else(condition: Condition, then_actions=[], else_actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'condition',
        'conditions': to_dict(condition),
        'then': then_actions,
        'else': else_actions,
    }


@action
def set_player_variable(player, variable_type, value, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerVariable',
        'player': to_dict(player),
        'variable': to_dict(variable_type),
        'value': to_dict(value)
    }


@action
def set_entity_variable(entity, variable_type, value, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityVariable',
        'entity': to_dict(entity),
        'variable': to_dict(variable_type),
        'value': to_dict(value),
    }


@action
def play_ad_for_player(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playAdForPlayer',
        'entity': to_dict(entity),
    }


@action
def set_time_out(duration: Number, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setTimeOut',
        'duration': to_dict(duration),
        'actions': actions,
    }


@action
def rotate_entity_to_face_position(entity, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'rotateEntityToFacePosition',
        'entity': to_dict(entity),
        'position': to_dict(position),
    }


@action
def destroy_entity(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'destroyEntity',
        'entity': to_dict(entity),
    }


@action
def set_entity_depth(entity, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityDepth',
        'entity': to_dict(entity),
        'value': to_dict(value),
    }


@action
def hide_unit_from_player(entity, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUnitFromPlayer',
        'entity': to_dict(entity),
        'player': to_dict(player),
    }


@action
def show_unit_to_player(entity, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUnitToPlayer',
        'entity': to_dict(entity),
        'player': to_dict(player),
    }


@action
def send_chat_message(message: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'sendChatMessage',
        'message': to_dict(message),
    }


@action
def play_sound_at_position(sound, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playSoundAtPosition',
        'sound': to_dict(sound),
        'position': to_dict(position),
    }


@action
def drop_item_at_position(item, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'dropItemAtPosition',
        'item': to_dict(item),
        'position': to_dict(position),
    }


@action
def apply_force_on_entity_angle(force: Number, entity, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityAngle',
        'force': to_dict(force),
        'entity': to_dict(entity),
        'angle': to_dict(angle),
    }


@action
def show_input_modal_to_player(player, inputLabel: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showInputModalToPlayer',
        'player': to_dict(player),
        'inputLabel': to_dict(inputLabel),
    }


@action
def open_dialogue_for_player(dialogue, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'openDialogueForPlayer',
        'dialogue': to_dict(dialogue),
        'player': to_dict(player),
    }


@action
def continue_loop(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'continue',
    }


@action
def open_website_for_player(string: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'openWebsiteForPlayer',
        'string': to_dict(string),
        'player': to_dict(player),
    }


@action
def set_entity_life_span(entity, lifeSpan: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityLifeSpan',
        'entity': to_dict(entity),
        'lifeSpan': to_dict(lifeSpan),
    }


@action
def hide_unit_name_label(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUnitNameLabel',
        'entity': to_dict(entity),
    }


@action
def set_triggering_unit(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setTriggeringUnit',
        'entity': to_dict(entity),
    }


@action
def create_unit_for_player_at_position(unitType, player, position, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createUnitAtPosition',
        'unitType': to_dict(unitType),
        'entity': to_dict(player),
        'position': to_dict(position),
        'angle': to_dict(angle),
    }


@action
def hide_ui_text_for_everyone(target, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUiTextForEveryone',
        'target': to_dict(target),
    }


@action
def hide_game_suggestions_for_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideGameSuggestionsForPlayer',
        'player': to_dict(player),
    }


@action
def transform_region_dimensions(region, x: Number, y: Number, width: Number, height: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'transformRegionDimensions',
        'region': to_dict(region),
        'x': to_dict(x),
        'y': to_dict(y),
        'width': to_dict(width),
        'height': to_dict(height),
    }


@action
def make_unit_invisible_to_friendly_players(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitInvisibleToFriendlyPlayers',
        'entity': to_dict(entity),
    }


@action
def set_entity_attribute_min(attribute, entity, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityAttributeMin',
        'attribute': to_dict(attribute),
        'entity': to_dict(entity),
        'value': to_dict(value),
    }


@action
def show_invite_friends_modal(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showInviteFriendsModal',
        'player': to_dict(player),
    }


@action
def show_custom_modal_to_player(htmlContent, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showCustomModalToPlayer',
        'htmlContent': to_dict(htmlContent),
        'player': to_dict(player),
    }


@action
def show_ui_text_for_everyone(target, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUiTextForEveryone',
        'target': to_dict(target),
    }


@action
def move_debris(entity, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'moveDebris',
        'entity': to_dict(entity),
        'position': to_dict(position),
    }


@action
def for_all_items(itemGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllItems',
        'itemGroup': to_dict(itemGroup),
        'actions': actions,
    }


@action
def remove_player_from_player_group(player, playerGroup, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removePlayerFromPlayerGroup',
        'player': to_dict(player),
        'playerGroup': to_dict(playerGroup),
    }


@action
def set_unit_owner(unit, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setUnitOwner',
        'unit': to_dict(unit),
        'player': to_dict(player),
    }


@action
def update_item_quantity(entity, quantity: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateItemQuantity',
        'entity': to_dict(entity),
        'quantity': to_dict(quantity),
    }


@action
def apply_force_on_entity_angle_lt(force: Number, entity, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityAngleLT',
        'force': to_dict(force),
        'entity': to_dict(entity),
        'angle': to_dict(angle),
    }


@action
def set_entity_state(entity, state, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityState',
        'entity': to_dict(entity),
        'state': to_dict(state),
    }


@action
def hide_unit_in_player_minimap(unit, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUnitInPlayerMinimap',
        'unit': to_dict(unit),
        'player': to_dict(player),
    }


@action
def return_loop(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'return',
    }


@action
def run_script(scriptName, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'runScript',
        'scriptName': to_dict(scriptName),
    }


@action
def player_camera_set_zoom(player, zoom: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playerCameraSetZoom',
        'player': to_dict(player),
        'zoom': to_dict(zoom),
    }


@action
def set_unit_name_label(unit, name: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setUnitNameLabel',
        'unit': to_dict(unit),
        'name': to_dict(name),
    }


@action
def open_shop_for_player(shop, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'openShopForPlayer',
        'shop': to_dict(shop),
        'player': to_dict(player),
    }


@action
def close_dialogue_for_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'closeDialogueForPlayer',
        'player': to_dict(player),
    }


@action
def comment(comment, disabled=False, run_on_client=False):
    return {
        'type': 'comment',
        'comment': to_dict(comment)
    }


@action
def create_entity_at_position_with_dimensions(entity, position, height: Number, width: Number, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createEntityAtPositionWithDimensions',
        'entity': to_dict(entity),
        'position': to_dict(position),
        'height': to_dict(height),
        'width': to_dict(width),
        'angle': to_dict(angle),
    }


@action
def set_variable(variable, value, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setVariable',
        'variableName': variable.name,
        'value': to_dict(value),
    }


@action
def increase_variable_by_number(variable, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'increaseVariableByNumber',
        'variable': to_dict(variable),
        'number': to_dict(number),
    }


@action
def player_camera_track_unit(player, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playerCameraTrackUnit',
        'player': to_dict(player),
        'unit': to_dict(unit),
    }


@action
def cast_ability(entity, abilityName, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'castAbility',
        'entity': to_dict(entity),
        'abilityName': to_dict(abilityName),
    }


@action
def play_entity_animation(entity, animation, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playEntityAnimation',
        'entity': to_dict(entity),
        'animation': to_dict(animation),
    }


@action
def while_do(conditions, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'while',
        'conditions': to_dict(conditions),
        'actions': actions,
    }


@action
def apply_force_on_entity_xy(force_x: Number, force_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityXY',
        'force': {
            'x': to_dict(force_x),
            'y': to_dict(force_y),
        },
        'entity': to_dict(entity),
    }


@action
def show_unit_in_player_minimap(unit, color: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUnitInPlayerMinimap',
        'unit': to_dict(unit),
        'color': to_dict(color),
        'player': to_dict(player),
    }


@action
def save_player_data(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'savePlayerData',
        'player': to_dict(player),
    }


@action
def hide_unit_name_label_from_player(entity, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUnitNameLabelFromPlayer',
        'entity': to_dict(entity),
        'player': to_dict(player),
    }


@action
def set_player_attribute(attribute, entity, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttribute',
        'attribute': to_dict(attribute),
        'entity': to_dict(entity),
        'value': to_dict(value),
    }


@action
def update_ui_text_for_player(target, value: String, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateUiTextForPlayer',
        'target': to_dict(target),
        'value': to_dict(value),
        'entity': to_dict(entity),
    }


@action
def show_unit_name_label(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUnitNameLabel',
        'entity': to_dict(entity),
    }


@action
def close_shop_for_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'closeShopForPlayer',
        'player': to_dict(player),
    }


@action
def attach_debris_to_unit(entity, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'attachDebrisToUnit',
        'entity': to_dict(entity),
        'unit': to_dict(unit),
    }


@action
def repeat(count: Number, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'repeat',
        'count': to_dict(count),
        'actions': actions,
    }


@action
def stop_music(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopMusic',
    }


@action
def emit_particle_once_at_position(particleType, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'emitParticleOnceAtPosition',
        'particleType': to_dict(particleType),
        'position': to_dict(position),
    }


@action
def set_velocity_of_entity_xy(velocity_x: Number, velocity_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setVelocityOfEntityXY',
        'velocity': {
            'x': to_dict(velocity_x),
            'y': to_dict(velocity_y),
        },
        'entity': to_dict(entity),
    }


@action
def show_unit_name_label_to_player(entity, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUnitNameLabelToPlayer',
        'entity': to_dict(entity),
        'player': to_dict(player),
    }


@action
def spawn_item(itemType, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'spawnItem',
        'itemType': to_dict(itemType),
        'position': to_dict(position),
    }


@action
def create_item_with_max_quantity_at_position(itemType, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createItemWithMaxQuantityAtPosition',
        'itemType': to_dict(itemType),
        'position': to_dict(position),
    }


@action
def show_menu(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showMenu',
        'player': to_dict(player),
    }


@action
def start_accepting_players(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'startAcceptingPlayers',
    }


@action
def for_all_entities(entityGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllEntities',
        'entityGroup': to_dict(entityGroup),
        'actions': actions,
    }


@action
def make_player_select_unit(player, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makePlayerSelectUnit',
        'player': to_dict(player),
        'unit': to_dict(unit),
    }


@action
def set_entity_attribute(attribute, entity, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityAttribute',
        'attribute': to_dict(attribute),
        'entity': to_dict(entity),
        'value': to_dict(value),
    }


@action
def for_all_item_types(itemTypeGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllItemTypes',
        'itemTypeGroup': to_dict(itemTypeGroup),
        'actions': actions,
    }


@action
def create_entity_for_player_at_position_with_dimensions(entity, player, position, height: Number, width: Number, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createEntityForPlayerAtPositionWithDimensions',
        'entity': to_dict(entity),
        'player': to_dict(player),
        'position': to_dict(position),
        'height': to_dict(height),
        'width': to_dict(width),
        'angle': to_dict(angle),
    }


@action
def end_game(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'endGame',
    }


@action
def update_ui_text_for_everyone(target, value: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateUiTextForEveryone',
        'target': to_dict(target),
        'value': to_dict(value),
    }


@action
def for_all_units(unitGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllUnits',
        'unitGroup': to_dict(unitGroup),
        'actions': actions,
    }


@action
def for_all_projectiles(projectileGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllProjectiles',
        'projectileGroup': to_dict(projectileGroup),
        'actions': actions,
    }


@action
def stop_music_for_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopMusicForPlayer',
        'player': to_dict(player),
    }


@action
def position_camera(player, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'positionCamera',
        'player': to_dict(player),
        'position': to_dict(position),
    }


@action
def create_projectile_at_position(projectileType, position, force: Number, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createProjectileAtPosition',
        'projectileType': to_dict(projectileType),
        'position': to_dict(position),
        'force': to_dict(force),
        'angle': to_dict(angle),
    }


@action
def show_menu_and_select_current_server(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showMenuAndSelectCurrentServer',
        'player': to_dict(player),
    }


@action
def set_fading_text_of_unit(unit, text: String, color: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setFadingTextOfUnit',
        'unit': to_dict(unit),
        'text': to_dict(text),
        'color': to_dict(color),
    }


@action
def change_scale_of_entity_body(entity, scale: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeScaleOfEntityBody',
        'entity': to_dict(entity),
        'scale': to_dict(scale),
    }


@action
def for_all_regions(regionGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllRegions',
        'regionGroup': to_dict(regionGroup),
        'actions': actions,
    }


@action
def rotate_entity_to_radians_lt(entity, radians: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'rotateEntityToRadiansLT',
        'entity': to_dict(entity),
        'radians': to_dict(radians),
    }


@action
def set_player_attribute_max(attributeType, player, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttributeMax',
        'attributeType': to_dict(attributeType),
        'player': to_dict(player),
        'number': to_dict(number),
    }


@action
def set_player_attribute_regeneration_rate(attributeType, player, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttributeRegenerationRate',
        'attributeType': to_dict(attributeType),
        'player': to_dict(player),
        'number': to_dict(number),
    }


@action
def for_all_unit_types(unitTypeGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllUnitTypes',
        'unitTypeGroup': to_dict(unitTypeGroup),
        'actions': actions,
    }


@action
def decrease_variable_by_number(variable, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'decreaseVariableByNumber',
        'variable': to_dict(variable),
        'number': to_dict(number),
    }


@action
def kick_player(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'kickPlayer',
        'entity': to_dict(entity),
    }


@action
def for_all_players(playerGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllPlayers',
        'playerGroup': to_dict(playerGroup),
        'actions': actions,
    }


@action
def remove_unit_from_unit_group(unit, unitGroup, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removeUnitFromUnitGroup',
        'unit': to_dict(unit),
        'unitGroup': to_dict(unitGroup),
    }


@action
def flip_entity_sprite(entity, flip, comment=None, disabled=False, run_on_client=False):
    '''Flip the sprite of an entity

    Args:
        entity (Entity): the entity that will be flipped
        flip (Flip): the flip direction from `Flip` enum class
    '''
    return {
        'type': 'flipEntitySprite',
        'entity': to_dict(entity),
        'flip': to_dict(flip),
    }


@action
def make_unit_invisible_to_neutral_players(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitInvisibleToNeutralPlayers',
        'entity': to_dict(entity),
    }


@action
def save_unit_data(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'saveUnitData',
        'unit': to_dict(unit),
    }


@action
def apply_torque_on_entity(torque: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyTorqueOnEntity',
        'torque': to_dict(torque),
        'entity': to_dict(entity),
    }


@action
def give_new_item_to_unit(itemType, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'giveNewItemToUnit',
        'itemType': to_dict(itemType),
        'unit': to_dict(unit),
    }


@action
def start_using_item(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'startUsingItem',
        'entity': to_dict(entity),
        'hasFixedCSP': None,
    }


@action
def move_entity(entity, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'moveEntity',
        'entity': to_dict(entity),
        'position': to_dict(position),
    }


@action
def for_range(variable, start: Number, stop: Number, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'for',
        'variableName': variable.name,
        'start': to_dict(start),
        'stop': to_dict(stop),
        'actions': actions,
    }


@action
def show_menu_and_select_best_server(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showMenuAndSelectBestServer',
        'player': to_dict(player),
    }


@action
def apply_force_on_entity_xyrelative(force_x: Number, force_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityXYRelative',
        'force': {
            'x': to_dict(force_x),
            'y': to_dict(force_y),
        },
        'entity': to_dict(entity),
    }


@action
def apply_force_on_entity_xylt(force_x: Number, force_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityXYLT',
        'force': {
            'x': to_dict(force_x),
            'y': to_dict(force_y),
        },
        'entity': to_dict(entity),
    }


@action
def attach_entity_to_entity(entity, targetingEntity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'attachEntityToEntity',
        'entity': to_dict(entity),
        'targetingEntity': to_dict(targetingEntity),
    }


@action
def ban_player_from_chat(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'banPlayerFromChat',
        'player': to_dict(player),
    }


@action
def change_unit_type(entity, unitType, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeUnitType',
        'entity': to_dict(entity),
        'unitType': to_dict(unitType),
    }


@action
def for_all_debris(debrisGroup, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllDebris',
        'debrisGroup': to_dict(debrisGroup),
        'actions': actions,
    }


@action
def play_music_for_player_repeatedly(music, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playMusicForPlayerRepeatedly',
        'music': to_dict(music),
        'player': to_dict(player),
    }


@action
def show_game_suggestions_for_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showGameSuggestionsForPlayer',
        'player': to_dict(player),
    }


@action
def set_entity_attribute_regeneration_rate(attribute, entity, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityAttributeRegenerationRate',
        'attribute': to_dict(attribute),
        'entity': to_dict(entity),
        'value': to_dict(value),
    }


@action
def make_unit_select_item_at_slot(unit, slotIndex: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitSelectItemAtSlot',
        'unit': to_dict(unit),
        'slotIndex': to_dict(slotIndex),
    }


@action
def stop_using_item(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopUsingItem',
        'entity': to_dict(entity),
        'hasFixedCSP': None,
    }


@action
def make_unit_visible(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitVisible',
        'entity': to_dict(entity),
    }


@action
def make_unit_invisible(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitInvisible',
        'entity': to_dict(entity),
    }


@action
def break_loop(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'break',
    }


@ action
def change_scale_of_entity_sprite(entity, scale: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeScaleOfEntitySprite',
        'entity': to_dict(entity),
        'scale': to_dict(scale),
    }


@ action
def set_player_name(player, name: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerName',
        'player': to_dict(player),
        'name': to_dict(name),
    }


@ action
def make_unit_pickup_item_at_slot(unit, item, slotIndex: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitPickupItemAtSlot',
        'unit': to_dict(unit),
        'item': to_dict(item),
        'slotIndex': to_dict(slotIndex),
    }


@ action
def drop_item_in_inventory_slot(unit, slotIndex: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'dropItemInInventorySlot',
        'unit': to_dict(unit),
        'slotIndex': to_dict(slotIndex),
    }


@ action
def unban_player_from_chat(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'unbanPlayerFromChat',
        'player': to_dict(player),
    }


@ action
def change_description_of_item(item, string: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeDescriptionOfItem',
        'item': to_dict(item),
        'string': to_dict(string),
    }


@ action
def send_chat_message_to_player(message: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'sendChatMessageToPlayer',
        'message': to_dict(message),
        'player': to_dict(player),
    }


@ action
def play_ad_for_everyone(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playAdForEveryone',
    }


@ action
def hide_ui_text_for_player(target, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUiTextForPlayer',
        'target': to_dict(target),
        'entity': to_dict(entity),
    }


@ action
def show_ui_text_for_player(target, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUiTextForPlayer',
        'target': to_dict(target),
        'entity': to_dict(entity),
    }


@ action
def reset_debris_position(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'resetDebrisPosition',
        'entity': to_dict(entity),
    }


@ action
def play_music(music, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playMusic',
        'music': to_dict(music),
    }


@ action
def assign_player_type(entity, playerType, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'assignPlayerType',
        'entity': to_dict(entity),
        'playerType': to_dict(playerType),
    }


@ action
def play_music_for_player(music, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playMusicForPlayer',
        'music': to_dict(music),
        'player': to_dict(player),
    }


@ action
def make_unit_visible_to_neutral_players(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitVisibleToNeutralPlayers',
        'entity': to_dict(entity),
    }


@ action
def make_unit_visible_to_friendly_players(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitVisibleToFriendlyPlayers',
        'entity': to_dict(entity),
    }


@ action
def make_unit_pickup_item(unit, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitPickupItem',
        'unit': to_dict(unit),
        'item': to_dict(item),
    }


@ action
def give_new_item_with_quantity_to_unit(itemType, number: Number, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'giveNewItemWithQuantityToUnit',
        'itemType': to_dict(itemType),
        'number': to_dict(number),
        'unit': to_dict(unit),
    }


@ action
def drop_all_items(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'dropAllItems',
        'entity': to_dict(entity),
    }


@ action
def use_item_once(item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'useItemOnce',
        'item': to_dict(item),
    }


@ action
def stop_accepting_players(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopAcceptingPlayers',
    }


@ action
def set_entity_velocity_at_angle(entity, speed: Number, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityVelocityAtAngle',
        'entity': to_dict(entity),
        'speed': to_dict(speed),
        'angle': to_dict(angle),
    }


@ action
def set_entity_attribute_max(attribute, entity, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityAttributeMax',
        'attribute': to_dict(attribute),
        'entity': to_dict(entity),
        'value': to_dict(value),
    }


@ action
def set_player_attribute_min(attributeType, player, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttributeMin',
        'attributeType': to_dict(attributeType),
        'player': to_dict(player),
        'number': to_dict(number),
    }


@ action
def make_player_trade_with_player(playerA, playerB, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makePlayerTradeWithPlayer',
        'playerA': to_dict(playerA),
        'playerB': to_dict(playerB),
    }


@ action
def update_ui_text_for_time_for_player(target, value: String, player, time: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateUiTextForTimeForPlayer',
        'target': to_dict(target),
        'value': to_dict(value),
        'player': to_dict(player),
        'time': to_dict(time),
    }


@ action
def ai_move_to_position(unit, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'aiMoveToPosition',
        'unit': to_dict(unit),
        'position': to_dict(position),
    }


@ action
def ai_attack_unit(unit, targetUnit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'aiAttackUnit',
        'unit': to_dict(unit),
        'targetUnit': to_dict(targetUnit),
    }


@ action
def change_sensor_radius(sensor, radius: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeSensorRadius',
        'sensor': to_dict(sensor),
        'radius': to_dict(radius),
    }


@ action
def load_player_data_and_apply_it(player, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'loadPlayerDataAndApplyIt',
        'player': to_dict(player),
        'unit': to_dict(unit),
    }


@ action
def create_floating_text(text: String, position, color: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createFloatingText',
        'text': to_dict(text),
        'position': to_dict(position),
        'color': to_dict(color),
    }


@ action
def set_last_attacked_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setLastAttackedUnit',
        'unit': to_dict(unit),
    }


@ action
def set_last_attacking_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setLastAttackingUnit',
        'unit': to_dict(unit),
    }


@ action
def set_item_fire_rate(number: Number, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setItemFireRate',
        'number': to_dict(number),
        'item': to_dict(item),
    }


@ action
def apply_impulse_on_entity_xy(impulse_x: Number, impulse_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyImpulseOnEntityXY',
        'impulse': {
            'x': to_dict(impulse_x),
            'y': to_dict(impulse_y),
        },
        'entity': to_dict(entity),
    }


@ action
def play_sound_for_player(sound, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playSoundForPlayer',
        'sound': to_dict(sound),
        'player': to_dict(player),
    }


@ action
def stop_sound_for_player(sound, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopSoundForPlayer',
        'sound': to_dict(sound),
        'player': to_dict(player),
    }


@ action
def show_dismissible_input_modal_to_player(player, inputLabel: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showDismissibleInputModalToPlayer',
        'player': to_dict(player),
        'inputLabel': to_dict(inputLabel),
    }


@ action
def set_item_name(name: String, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setItemName',
        'name': to_dict(name),
        'item': to_dict(item),
    }


@ action
def change_item_inventory_image(url: String, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeItemInventoryImage',
        'url': to_dict(url),
        'item': to_dict(item),
    }


@ action
def add_attribute_buff_to_unit(entity, value: Number, attribute, time: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'addAttributeBuffToUnit',
        'entity': to_dict(entity),
        'value': to_dict(value),
        'attribute': to_dict(attribute),
        'time': to_dict(time),
    }


@ action
def add_percentage_attribute_buff_to_unit(entity, value: Number, attribute, time: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'addPercentageAttributeBuffToUnit',
        'entity': to_dict(entity),
        'value': to_dict(value),
        'attribute': to_dict(attribute),
        'time': to_dict(time),
    }


@ action
def stun_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stunUnit',
        'unit': to_dict(unit),
    }


@ action
def remove_stun_from_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removeStunFromUnit',
        'unit': to_dict(unit),
    }


@ action
def set_last_attacking_item(item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setLastAttackingItem',
        'item': to_dict(item),
    }


@ action
def mute_player_microphone(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'mutePlayerMicrophone',
        'player': to_dict(player),
    }


@ action
def unmute_player_microphone(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'unmutePlayerMicrophone',
        'player': to_dict(player),
    }


@ action
def send_post_request(string: String, url: String, varName, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'sendPostRequest',
        'string': to_dict(string),
        'url': to_dict(url),
        'varName': to_dict(varName),
    }


@ action
def load_unit_data_from_string(string: String, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'loadUnitDataFromString',
        'string': to_dict(string),
        'unit': to_dict(unit),
    }


@ action
def load_player_data_from_string(string: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'loadPlayerDataFromString',
        'string': to_dict(string),
        'player': to_dict(player),
    }


@ action
def remove_all_attribute_buffs(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removeAllAttributeBuffs',
        'unit': to_dict(unit),
    }


@ action
def change_inventory_slot_color(item, string: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeInventorySlotColor',
        'item': to_dict(item),
        'string': to_dict(string),
    }


@ action
def set_owner_unit_of_projectile(unit, projectile, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setOwnerUnitOfProjectile',
        'unit': to_dict(unit),
        'projectile': to_dict(projectile),
    }


@ action
def enable_ai(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'enableAI',
        'unit': to_dict(unit),
    }


@ action
def disable_ai(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'disableAI',
        'unit': to_dict(unit),
    }


@ action
def ai_go_idle(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'aiGoIdle',
        'unit': to_dict(unit),
    }
