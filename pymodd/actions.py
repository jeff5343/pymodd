from __future__ import annotations
import functools

from .functions import Condition, Number, String
from .script import Base, to_dict


def action(func):
    @functools.wraps(func)
    def wrapper_action(args, **kwargs):
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
def set_player_variable(variable_type, player, value, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerVariable',
        'player': to_dict(player),
        'variable': to_dict(variable_type),
        'value': to_dict(value)
    }


@action
def set_entity_variable(variable_type, entity, value, comment=None, disabled=False, run_on_client=False):
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
def rotate_entity_instantly_to_face_position(entity, position, comment=None, disabled=False, run_on_client=False):
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
def set_depth_of_entity(value: Number, entity, comment=None, disabled=False, run_on_client=False):
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
def send_chat_message_to_everyone(message: String, comment=None, disabled=False, run_on_client=False):
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
def apply_force_on_entity_at_angle(force: Number, entity, angle: Number, comment=None, disabled=False, run_on_client=False):
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
def set_lifespan_of_entity(lifespan: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityLifeSpan',
        'entity': to_dict(entity),
        'lifeSpan': to_dict(lifespan),
    }


@action
def hide_name_label_of_entity_from_hostile_players(entity, comment=None, disabled=False, run_on_client=False):
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
def create_unit_for_player_at_position_with_rotation(unit_type, player, position, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createUnitAtPosition',
        'unitType': to_dict(unit_type),
        'entity': to_dict(player),
        'position': to_dict(position),
        'angle': to_dict(angle),
    }


@action
def hide_ui_target_for_everyone(target, comment=None, disabled=False, run_on_client=False):
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
def transform_dimensions_of_region(x: Number, y: Number, width: Number, height: Number, region, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'transformRegionDimensions',
        'region': to_dict(region),
        'x': to_dict(x),
        'y': to_dict(y),
        'width': to_dict(width),
        'height': to_dict(height),
    }


@action
def make_entity_invisible_to_friendly_players(entity, comment=None, disabled=False, run_on_client=False):
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
def show_invite_friends_modal_to_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showInviteFriendsModal',
        'player': to_dict(player),
    }


@action
def show_custom_modal_to_player(html_content, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showCustomModalToPlayer',
        'htmlContent': to_dict(html_content),
        'player': to_dict(player),
    }


@action
def show_ui_target_for_everyone(target, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUiTextForEveryone',
        'target': to_dict(target),
    }


@action
def move_debris_to_position(entity, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'moveDebris',
        'entity': to_dict(entity),
        'position': to_dict(position),
    }


@action
def for_all_items_in(item_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllItems',
        'itemGroup': to_dict(item_group),
        'actions': actions,
    }


@action
def remove_player_from_player_group(player, player_group, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removePlayerFromPlayerGroup',
        'player': to_dict(player),
        'playerGroup': to_dict(player_group),
    }


@action
def set_owner_of_unit(player, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setUnitOwner',
        'unit': to_dict(unit),
        'player': to_dict(player),
    }


@action
def update_quantity_of_item(quantity: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateItemQuantity',
        'entity': to_dict(entity),
        'quantity': to_dict(quantity),
    }


@action
def apply_loss_tolerant_force_on_entity_at_angle(force: Number, entity, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityAngleLT',
        'force': to_dict(force),
        'entity': to_dict(entity),
        'angle': to_dict(angle),
    }


@action
def set_state_of_entity(state, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setEntityState',
        'entity': to_dict(entity),
        'state': to_dict(state),
    }


@action
def hide_unit_in_minimap_for_player(unit, player, comment=None, disabled=False, run_on_client=False):
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
def run_script(script_name, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'runScript',
        'scriptName': to_dict(script_name),
    }


@action
def set_camera_zoom_of_player(zoom: Number, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playerCameraSetZoom',
        'player': to_dict(player),
        'zoom': to_dict(zoom),
    }


@action
def set_name_label_of_unit(name_label: String, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setUnitNameLabel',
        'unit': to_dict(unit),
        'name': to_dict(name_label),
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
def make_camera_of_player_track_unit(player, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playerCameraTrackUnit',
        'player': to_dict(player),
        'unit': to_dict(unit),
    }


@action
def make_unit_cast_ability_once(entity, ability_name, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'castAbility',
        'entity': to_dict(entity),
        'abilityName': to_dict(ability_name),
    }


@action
def play_animation_for_entity(animation, entity, comment=None, disabled=False, run_on_client=False):
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
def show_unit_with_color_in_minimap_of_player(unit, color: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUnitInPlayerMinimap',
        'unit': to_dict(unit),
        'color': to_dict(color),
        'player': to_dict(player),
    }


@action
def save_data_of_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'savePlayerData',
        'player': to_dict(player),
    }


@action
def hide_name_label_of_unit_from_player(entity, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUnitNameLabelFromPlayer',
        'entity': to_dict(entity),
        'player': to_dict(player),
    }


@action
def set_player_attribute(attribute, player, value: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttribute',
        'attribute': to_dict(attribute),
        'entity': to_dict(player),
        'value': to_dict(value),
    }


@action
def update_ui_target_for_player(target, value: String, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateUiTextForPlayer',
        'target': to_dict(target),
        'value': to_dict(value),
        'entity': to_dict(entity),
    }


@action
def show_name_label_of_unit_to_hostile_players(entity, comment=None, disabled=False, run_on_client=False):
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
def attach_debris_to_unit(debris, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'attachDebrisToUnit',
        'entity': to_dict(debris),
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
def stop_music_for_everyone(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopMusic',
    }


@action
def emit_particle_once_at_position(particle_type, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'emitParticleOnceAtPosition',
        'particleType': to_dict(particle_type),
        'position': to_dict(position),
    }


@action
def set_velocity_of_entity(velocity_x: Number, velocity_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setVelocityOfEntityXY',
        'velocity': {
            'x': to_dict(velocity_x),
            'y': to_dict(velocity_y),
        },
        'entity': to_dict(entity),
    }


@action
def show_name_label_of_unit_to_player(unit, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUnitNameLabelToPlayer',
        'entity': to_dict(unit),
        'player': to_dict(player),
    }


@action
def create_item_at_position(item_type, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'spawnItem',
        'itemType': to_dict(item_type),
        'position': to_dict(position),
    }


@action
def create_item_with_max_quantity_at_position(item_type, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createItemWithMaxQuantityAtPosition',
        'itemType': to_dict(item_type),
        'position': to_dict(position),
    }


@action
def show_menu_to_player(player, comment=None, disabled=False, run_on_client=False):
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
def for_all_entities_in(entity_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllEntities',
        'entityGroup': to_dict(entity_group),
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
def for_all_item_types_in(item_type_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllItemTypes',
        'itemTypeGroup': to_dict(item_type_group),
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
def for_all_units_in(unit_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllUnits',
        'unitGroup': to_dict(unit_group),
        'actions': actions,
    }


@action
def for_all_projectiles_in(projectile_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllProjectiles',
        'projectileGroup': to_dict(projectile_group),
        'actions': actions,
    }


@action
def stop_music_for_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopMusicForPlayer',
        'player': to_dict(player),
    }


@action
def make_camera_of_player_look_at_position(player, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'positionCamera',
        'player': to_dict(player),
        'position': to_dict(position),
    }


@action
def create_projectile_at_position_and_apply_force_with_angle(projectile_type, position, force: Number, angle: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'createProjectileAtPosition',
        'projectileType': to_dict(projectile_type),
        'position': to_dict(position),
        'force': to_dict(force),
        'angle': to_dict(angle),
    }


@action
def show_menu_to_player_and_select_current_server(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showMenuAndSelectCurrentServer',
        'player': to_dict(player),
    }


@action
def set_fading_text_of_unit(text: String, unit, color: String, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setFadingTextOfUnit',
        'unit': to_dict(unit),
        'text': to_dict(text),
        'color': to_dict(color),
    }


@action
def change_scale_of_entity_body(scale: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeScaleOfEntityBody',
        'entity': to_dict(entity),
        'scale': to_dict(scale),
    }


@action
def for_all_regions_in(region_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllRegions',
        'regionGroup': to_dict(region_group),
        'actions': actions,
    }


@action
def rotate_entity_loss_tolerant_to_radians(entity, radians: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'rotateEntityToRadiansLT',
        'entity': to_dict(entity),
        'radians': to_dict(radians),
    }


@action
def set_player_attribute_max(attribute_type, player, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttributeMax',
        'attributeType': to_dict(attribute_type),
        'player': to_dict(player),
        'number': to_dict(number),
    }


@action
def set_player_attribute_regeneration_rate(attribute_type, player, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttributeRegenerationRate',
        'attributeType': to_dict(attribute_type),
        'player': to_dict(player),
        'number': to_dict(number),
    }


@action
def for_all_unit_types_in(unit_type_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllUnitTypes',
        'unitTypeGroup': to_dict(unit_type_group),
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
def for_all_players_in(player_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllPlayers',
        'playerGroup': to_dict(player_group),
        'actions': actions,
    }


@action
def remove_unit_from_unit_group(unit, unit_group, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removeUnitFromUnitGroup',
        'unit': to_dict(unit),
        'unitGroup': to_dict(unit_group),
    }


@action
def flip_sprite_of_entity(flip, entity, comment=None, disabled=False, run_on_client=False):
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
def save_data_of_unit(unit, comment=None, disabled=False, run_on_client=False):
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
def give_new_item_to_unit(item_type, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'giveNewItemToUnit',
        'itemType': to_dict(item_type),
        'unit': to_dict(unit),
    }


@action
def use_item_continuously_until_stopped(item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'startUsingItem',
        'entity': to_dict(item),
        'hasFixedCSP': None,
    }


@action
def move_entity_to_position(entity, position, comment=None, disabled=False, run_on_client=False):
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
def show_menu_to_player_and_select_best_server(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showMenuAndSelectBestServer',
        'player': to_dict(player),
    }


@action
def apply_force_on_entity_relative_to_facing_angle(force_x: Number, force_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityXYRelative',
        'force': {
            'x': to_dict(force_x),
            'y': to_dict(force_y),
        },
        'entity': to_dict(entity),
    }


@action
def apply_force_loss_tolerant_on_entity(force_x: Number, force_y: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'applyForceOnEntityXYLT',
        'force': {
            'x': to_dict(force_x),
            'y': to_dict(force_y),
        },
        'entity': to_dict(entity),
    }


@action
def attach_entity_to_entity(entity, targeting_entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'attachEntityToEntity',
        'entity': to_dict(entity),
        'targetingEntity': to_dict(targeting_entity),
    }


@action
def ban_player_from_chat(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'banPlayerFromChat',
        'player': to_dict(player),
    }


@action
def change_unit_type_of_entity(unit_type, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeUnitType',
        'entity': to_dict(entity),
        'unitType': to_dict(unit_type),
    }


@action
def for_all_debris_in(debris_group, actions=[], comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'forAllDebris',
        'debrisGroup': to_dict(debris_group),
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
def stop_using_item(item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'stopUsingItem',
        'entity': to_dict(item),
        'hasFixedCSP': None,
    }


@action
def make_unit_visible_to_hostile_players(entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitVisible',
        'entity': to_dict(entity),
    }


@action
def make_unit_invisible_to_hostile_players(entity, comment=None, disabled=False, run_on_client=False):
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
def change_scale_of_sprite_for_entity(scale: Number, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeScaleOfEntitySprite',
        'entity': to_dict(entity),
        'scale': to_dict(scale),
    }


@ action
def set_name_of_player(name: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerName',
        'player': to_dict(player),
        'name': to_dict(name),
    }


@ action
def make_unit_pickup_item_at_inventory_slot(unit, item, slotIndex: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makeUnitPickupItemAtSlot',
        'unit': to_dict(unit),
        'item': to_dict(item),
        'slotIndex': to_dict(slotIndex),
    }


@ action
def make_unit_drop_item_at_inventory_slot(unit, slotIndex: Number, comment=None, disabled=False, run_on_client=False):
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
def change_description_of_item(string: String, item, comment=None, disabled=False, run_on_client=False):
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


@action
def add_words_to_chat_filter(words, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'addChatFilter',
        'words': to_dict(words),
    }


@ action
def play_ad_for_everyone(comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playAdForEveryone',
    }


@action
def send_coins_to_player_with_player_paying_fee(coins, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'sendCoinsToPlayer',
        'coins': to_dict(coins),
        'player': to_dict(player),
    }


@action
def send_coins_to_player_with_owner_paying_fee(coins, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'sendCoinsToPlayer2',
        'coins': to_dict(coins),
        'player': to_dict(player),
    }


@ action
def hide_ui_target_for_player(target, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'hideUiTextForPlayer',
        'target': to_dict(target),
        'entity': to_dict(entity),
    }


@ action
def show_ui_target_for_player(target, entity, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showUiTextForPlayer',
        'target': to_dict(target),
        'entity': to_dict(entity),
    }


@ action
def reset_position_of_debris(debris, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'resetDebrisPosition',
        'entity': to_dict(debris),
    }


@ action
def play_music_for_everyone(music, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'playMusic',
        'music': to_dict(music),
    }


@ action
def assign_player_to_player_type(entity, player_type, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'assignPlayerType',
        'entity': to_dict(entity),
        'playerType': to_dict(player_type),
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
def give_new_item_with_quantity_to_unit(item_type, number: Number, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'giveNewItemWithQuantityToUnit',
        'itemType': to_dict(item_type),
        'number': to_dict(number),
        'unit': to_dict(unit),
    }


@ action
def make_unit_drop_all_items(entity, comment=None, disabled=False, run_on_client=False):
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
def set_entity_velocity_with_speed_at_angle(entity, speed: Number, angle: Number, comment=None, disabled=False, run_on_client=False):
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
def set_player_attribute_min(attribute_type, player, number: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setPlayerAttributeMin',
        'attributeType': to_dict(attribute_type),
        'player': to_dict(player),
        'number': to_dict(number),
    }


@ action
def make_player_trade_with_player(player_a, player_b, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'makePlayerTradeWithPlayer',
        'playerA': to_dict(player_a),
        'playerB': to_dict(player_b),
    }


@ action
def update_ui_target_for_player_for_miliseconds(target, value: String, player, time: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'updateUiTextForTimeForPlayer',
        'target': to_dict(target),
        'value': to_dict(value),
        'player': to_dict(player),
        'time': to_dict(time),
    }


@ action
def command_ai_unit_to_move_to_position(unit, position, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'aiMoveToPosition',
        'unit': to_dict(unit),
        'position': to_dict(position),
    }


@ action
def command_ai_to_attack_unit(unit, target_unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'aiAttackUnit',
        'unit': to_dict(unit),
        'targetUnit': to_dict(target_unit),
    }


@ action
def change_radius_of_sensor(radius: Number, sensor, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeSensorRadius',
        'sensor': to_dict(sensor),
        'radius': to_dict(radius),
    }


@ action
def load_player_data_and_apply_it_to(player, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'loadPlayerDataAndApplyIt',
        'player': to_dict(player),
        'unit': to_dict(unit),
    }


@ action
def create_floating_text_at_position_with_color(text: String, position, color: String, comment=None, disabled=False, run_on_client=False):
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
def set_fire_rate_of_item(number: Number, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setItemFireRate',
        'number': to_dict(number),
        'item': to_dict(item),
    }


@ action
def apply_impulse_on_entity(impulse_x: Number, impulse_y: Number, entity, comment=None, disabled=False, run_on_client=False):
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
def show_dismissible_input_modal_asking_question_to_player(question: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'showDismissibleInputModalToPlayer',
        'player': to_dict(player),
        'inputLabel': to_dict(question),
    }


@ action
def set_name_of_item(name: String, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setItemName',
        'name': to_dict(name),
        'item': to_dict(item),
    }


@ action
def set_inventory_image_of_item(url: String, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeItemInventoryImage',
        'url': to_dict(url),
        'item': to_dict(item),
    }


@ action
def give_attribute_buff_to_entity_for_milliseconds(attribute, value: Number, entity, time: Number, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'addAttributeBuffToUnit',
        'entity': to_dict(entity),
        'value': to_dict(value),
        'attribute': to_dict(attribute),
        'time': to_dict(time),
    }


@ action
def give_percentage_attribute_buff_to_entity_for_milliseconds(value: Number, attribute, entity, time: Number, comment=None, disabled=False, run_on_client=False):
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
def mute_microphone_of_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'mutePlayerMicrophone',
        'player': to_dict(player),
    }


@ action
def unmute_microphone_of_player(player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'unmutePlayerMicrophone',
        'player': to_dict(player),
    }


@ action
def send_post_request_and_save_response_in_variable(url: String, value: String, var, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'sendPostRequest',
        'string': to_dict(value),
        'url': to_dict(url),
        'varName': to_dict(var),
    }


@ action
def load_data_from_string_and_apply_to_unit(string: String, unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'loadUnitDataFromString',
        'string': to_dict(string),
        'unit': to_dict(unit),
    }


@ action
def load_data_from_string_and_apply_to_player(string: String, player, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'loadPlayerDataFromString',
        'string': to_dict(string),
        'player': to_dict(player),
    }


@ action
def remove_all_attribute_buffs_from_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'removeAllAttributeBuffs',
        'unit': to_dict(unit),
    }


@ action
def change_color_of_inventory_slot_for_item(color: String, item, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'changeInventorySlotColor',
        'item': to_dict(item),
        'string': to_dict(color),
    }


@ action
def set_owner_unit_of_projectile(unit, projectile, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'setOwnerUnitOfProjectile',
        'unit': to_dict(unit),
        'projectile': to_dict(projectile),
    }


@ action
def enable_ai_for_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'enableAI',
        'unit': to_dict(unit),
    }


@ action
def disable_ai_for_unit(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'disableAI',
        'unit': to_dict(unit),
    }


@ action
def command_ai_to_idle(unit, comment=None, disabled=False, run_on_client=False):
    return {
        'type': 'aiGoIdle',
        'unit': to_dict(unit),
    }
