from __future__ import annotations

from .functions import Condition, Number, String
from .script import Base, to_dict


class Action(Base):
    def __init__(self):
        self.action = None
        self.options = {}

    def to_dict(self):
        data = {
            'type': self.action
        }
        data.update(self.options) if self.options is not None else None
        return data


class IfStatement(Action):
    def __init__(self, condition: Condition, then_actions=[], else_actions=[]):
        self.action = 'condition'
        self.condition = condition
        self.thenActions = [to_dict(action) for action in then_actions]
        self.elseActions = [to_dict(action) for action in else_actions]

    def to_dict(self):
        return {
            'type': 'condition',
            'conditions': to_dict(self.condition),
            'then': self.thenActions,
            'else': self.elseActions
        }


class SetPlayerVariable(Action):
    def __init__(self, player, variable_type, value):
        self.action = 'setPlayerVariable'
        self.options = {
            'player': to_dict(player),
            'variable': to_dict(variable_type),
            'value': to_dict(value),
        }


class SetEntityVariable(Action):
    def __init__(self, entity, variable_type, value):
        self.action = 'setEntityVariable'
        self.options = {
            'entity': to_dict(entity),
            'variable': to_dict(variable_type),
            'value': to_dict(value),
        }


class PlayAdForPlayer(Action):
    def __init__(self, entity):
        self.action = 'playAdForPlayer'
        self.options = {
            'entity': to_dict(entity),
        }


class SetTimeOut(Action):
    def __init__(self, duration: Number, actions=[]):
        self.action = 'setTimeOut'
        self.options = {
            'duration': to_dict(duration),
            'actions': [to_dict(action) for action in actions],
        }


class RotateEntityToFacePosition(Action):
    def __init__(self, entity, position):
        self.action = 'rotateEntityToFacePosition'
        self.options = {
            'entity': to_dict(entity),
            'position': to_dict(position),
        }


class DestroyEntity(Action):
    def __init__(self, entity):
        self.action = 'destroyEntity'
        self.options = {
            'entity': to_dict(entity),
        }


class SetEntityDepth(Action):
    def __init__(self, entity, value: Number):
        self.action = 'setEntityDepth'
        self.options = {
            'entity': to_dict(entity),
            'value': to_dict(value),
        }


class HideUnitFromPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'hideUnitFromPlayer'
        self.options = {
            'entity': to_dict(entity),
            'player': to_dict(player),
        }


class ShowUnitToPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'showUnitToPlayer'
        self.options = {
            'entity': to_dict(entity),
            'player': to_dict(player),
        }


class SendChatMessage(Action):
    def __init__(self, message: String):
        self.action = 'sendChatMessage'
        self.options = {
            'message': to_dict(message),
        }


class PlaySoundAtPosition(Action):
    def __init__(self, sound, position):
        self.action = 'playSoundAtPosition'
        self.options = {
            'sound': to_dict(sound),
            'position': to_dict(position),
        }


class DropItemAtPosition(Action):
    def __init__(self, item, position):
        self.action = 'dropItemAtPosition'
        self.options = {
            'item': to_dict(item),
            'position': to_dict(position),
        }


class ApplyForceOnEntityAngle(Action):
    def __init__(self, force: Number, entity, angle: Number):
        self.action = 'applyForceOnEntityAngle'
        self.options = {
            'force': to_dict(force),
            'entity': to_dict(entity),
            'angle': to_dict(angle),
        }


class ShowInputModalToPlayer(Action):
    def __init__(self, player, inputLabel: String):
        self.action = 'showInputModalToPlayer'
        self.options = {
            'player': to_dict(player),
            'inputLabel': to_dict(inputLabel),
        }


class OpenDialogueForPlayer(Action):
    def __init__(self, dialogue, player):
        self.action = 'openDialogueForPlayer'
        self.options = {
            'dialogue': to_dict(dialogue),
            'player': to_dict(player),
        }


class Continue(Action):
    def __init__(self):
        self.action = 'continue'
        self.options = {}


class OpenWebsiteForPlayer(Action):
    def __init__(self, string: String, player):
        self.action = 'openWebsiteForPlayer'
        self.options = {
            'string': to_dict(string),
            'player': to_dict(player),
        }


class SetEntityLifeSpan(Action):
    def __init__(self, entity, lifeSpan: Number):
        self.action = 'setEntityLifeSpan'
        self.options = {
            'entity': to_dict(entity),
            'lifeSpan': to_dict(lifeSpan),
        }


class HideUnitNameLabel(Action):
    def __init__(self, entity):
        self.action = 'hideUnitNameLabel'
        self.options = {
            'entity': to_dict(entity),
        }


class SetTriggeringUnit(Action):
    def __init__(self, entity):
        self.action = 'setTriggeringUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class CreateUnitForPlayerAtPosition(Action):
    def __init__(self, unitType, player, position, angle: Number):
        self.action = 'createUnitAtPosition'
        self.options = {
            'unitType': to_dict(unitType),
            'entity': to_dict(player),
            'position': to_dict(position),
            'angle': to_dict(angle),
        }


class HideUiTextForEveryone(Action):
    def __init__(self, target):
        self.action = 'hideUiTextForEveryone'
        self.options = {
            'target': to_dict(target),
        }


class HideGameSuggestionsForPlayer(Action):
    def __init__(self, player):
        self.action = 'hideGameSuggestionsForPlayer'
        self.options = {
            'player': to_dict(player),
        }


class TransformRegionDimensions(Action):
    def __init__(self, region, x: Number, y: Number, width: Number, height: Number):
        self.action = 'transformRegionDimensions'
        self.options = {
            'region': to_dict(region),
            'x': to_dict(x),
            'y': to_dict(y),
            'width': to_dict(width),
            'height': to_dict(height),
        }


class MakeUnitInvisibleToFriendlyPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitInvisibleToFriendlyPlayers'
        self.options = {
            'entity': to_dict(entity),
        }


class SetEntityAttributeMin(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttributeMin'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
            'value': to_dict(value),
        }


class ShowInviteFriendsModal(Action):
    def __init__(self, player):
        self.action = 'showInviteFriendsModal'
        self.options = {
            'player': to_dict(player),
        }


class ShowCustomModalToPlayer(Action):
    def __init__(self, htmlContent, player):
        self.action = 'showCustomModalToPlayer'
        self.options = {
            'htmlContent': to_dict(htmlContent),
            'player': to_dict(player),
        }


class ShowUiTextForEveryone(Action):
    def __init__(self, target):
        self.action = 'showUiTextForEveryone'
        self.options = {
            'target': to_dict(target),
        }


class MoveDebris(Action):
    def __init__(self, entity, position):
        self.action = 'moveDebris'
        self.options = {
            'entity': to_dict(entity),
            'position': to_dict(position),
        }


class ForAllItems(Action):
    def __init__(self, itemGroup, actions=[]):
        self.action = 'forAllItems'
        self.options = {
            'itemGroup': to_dict(itemGroup),
            'actions': [to_dict(action) for action in actions],
        }


class RemovePlayerFromPlayerGroup(Action):
    def __init__(self, player, playerGroup):
        self.action = 'removePlayerFromPlayerGroup'
        self.options = {
            'player': to_dict(player),
            'playerGroup': to_dict(playerGroup),
        }


class SetUnitOwner(Action):
    def __init__(self, unit, player):
        self.action = 'setUnitOwner'
        self.options = {
            'unit': to_dict(unit),
            'player': to_dict(player),
        }


class UpdateItemQuantity(Action):
    def __init__(self, entity, quantity: Number):
        self.action = 'updateItemQuantity'
        self.options = {
            'entity': to_dict(entity),
            'quantity': to_dict(quantity),
        }


class ApplyForceOnEntityAngleLT(Action):
    def __init__(self, force: Number, entity, angle: Number):
        self.action = 'applyForceOnEntityAngleLT'
        self.options = {
            'force': to_dict(force),
            'entity': to_dict(entity),
            'angle': to_dict(angle),
        }


class SetEntityState(Action):
    def __init__(self, entity, state):
        self.action = 'setEntityState'
        self.options = {
            'entity': to_dict(entity),
            'state': to_dict(state),
        }


class HideUnitInPlayerMinimap(Action):
    def __init__(self, unit, player):
        self.action = 'hideUnitInPlayerMinimap'
        self.options = {
            'unit': to_dict(unit),
            'player': to_dict(player),
        }


class Return(Action):
    def __init__(self):
        self.action = 'return'
        self.options = {}


class RunScript(Action):
    def __init__(self, scriptName):
        self.action = 'runScript'
        self.options = {
            'scriptName': to_dict(scriptName),
        }


class PlayerCameraSetZoom(Action):
    def __init__(self, player, zoom: Number):
        self.action = 'playerCameraSetZoom'
        self.options = {
            'player': to_dict(player),
            'zoom': to_dict(zoom),
        }


class SetUnitNameLabel(Action):
    def __init__(self, unit, name: String):
        self.action = 'setUnitNameLabel'
        self.options = {
            'unit': to_dict(unit),
            'name': to_dict(name),
        }


class OpenShopForPlayer(Action):
    def __init__(self, shop, player):
        self.action = 'openShopForPlayer'
        self.options = {
            'shop': to_dict(shop),
            'player': to_dict(player),
        }


class CloseDialogueForPlayer(Action):
    def __init__(self, player):
        self.action = 'closeDialogueForPlayer'
        self.options = {
            'player': to_dict(player),
        }


class Comment(Action):
    def __init__(self, comment):
        self.action = 'comment'
        self.options = {
            'comment': to_dict(comment)
        }


class CreateEntityAtPositionWithDimensions(Action):
    def __init__(self, entity, position, height: Number, width: Number, angle: Number):
        self.action = 'createEntityAtPositionWithDimensions'
        self.options = {
            'entity': to_dict(entity),
            'position': to_dict(position),
            'height': to_dict(height),
            'width': to_dict(width),
            'angle': to_dict(angle),
        }


class SetVariable(Action):
    def __init__(self, variable, value):
        self.action = 'setVariable'
        self.options = {
            'variableName': variable.name,
            'value': to_dict(value),
        }


class IncreaseVariableByNumber(Action):
    def __init__(self, variable, number: Number):
        self.action = 'increaseVariableByNumber'
        self.options = {
            'variable': to_dict(variable),
            'number': to_dict(number),
        }


class PlayerCameraTrackUnit(Action):
    def __init__(self, player, unit):
        self.action = 'playerCameraTrackUnit'
        self.options = {
            'player': to_dict(player),
            'unit': to_dict(unit),
        }


class CastAbility(Action):
    def __init__(self, entity, abilityName):
        self.action = 'castAbility'
        self.options = {
            'entity': to_dict(entity),
            'abilityName': to_dict(abilityName),
        }


class PlayEntityAnimation(Action):
    def __init__(self, entity, animation):
        self.action = 'playEntityAnimation'
        self.options = {
            'entity': to_dict(entity),
            'animation': to_dict(animation),
        }


class While(Action):
    def __init__(self, conditions, actions=[]):
        self.action = 'while'
        self.options = {
            'conditions': to_dict(conditions),
            'actions': [to_dict(action) for action in actions],
        }


class ApplyForceOnEntityXY(Action):
    def __init__(self, force_x: Number, force_y: Number, entity):
        self.action = 'applyForceOnEntityXY'
        self.options = {
            'force': {
                'x': to_dict(force_x),
                'y':to_dict(force_y),
            },
            'entity': to_dict(entity),
        }


class ShowUnitInPlayerMinimap(Action):
    def __init__(self, unit, color: String, player):
        self.action = 'showUnitInPlayerMinimap'
        self.options = {
            'unit': to_dict(unit),
            'color': to_dict(color),
            'player': to_dict(player),
        }


class SavePlayerData(Action):
    def __init__(self, player):
        self.action = 'savePlayerData'
        self.options = {
            'player': to_dict(player),
        }


class HideUnitNameLabelFromPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'hideUnitNameLabelFromPlayer'
        self.options = {
            'entity': to_dict(entity),
            'player': to_dict(player),
        }


class SetPlayerAttribute(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setPlayerAttribute'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
            'value': to_dict(value),
        }


class UpdateUiTextForPlayer(Action):
    def __init__(self, target, value: String, entity):
        self.action = 'updateUiTextForPlayer'
        self.options = {
            'target': to_dict(target),
            'value': to_dict(value),
            'entity': to_dict(entity),
        }


class ShowUnitNameLabel(Action):
    def __init__(self, entity):
        self.action = 'showUnitNameLabel'
        self.options = {
            'entity': to_dict(entity),
        }


class CloseShopForPlayer(Action):
    def __init__(self, player):
        self.action = 'closeShopForPlayer'
        self.options = {
            'player': to_dict(player),
        }


class AttachDebrisToUnit(Action):
    def __init__(self, entity, unit):
        self.action = 'attachDebrisToUnit'
        self.options = {
            'entity': to_dict(entity),
            'unit': to_dict(unit),
        }


class Repeat(Action):
    def __init__(self, count: Number, actions=[]):
        self.action = 'repeat'
        self.options = {
            'count': to_dict(count),
            'actions': [to_dict(action) for action in actions],
        }


class StopMusic(Action):
    def __init__(self):
        self.action = 'stopMusic'
        self.options = {}


class EmitParticleOnceAtPosition(Action):
    def __init__(self, particleType, position):
        self.action = 'emitParticleOnceAtPosition'
        self.options = {
            'particleType': to_dict(particleType),
            'position': to_dict(position),
        }


class SetVelocityOfEntityXY(Action):
    def __init__(self, velocity_x: Number, velocity_y: Number, entity):
        self.action = 'setVelocityOfEntityXY'
        self.options = {
            'velocity': {
                'x': to_dict(velocity_x),
                'y':to_dict(velocity_y),
            },
            'entity': to_dict(entity),
        }


class ShowUnitNameLabelToPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'showUnitNameLabelToPlayer'
        self.options = {
            'entity': to_dict(entity),
            'player': to_dict(player),
        }


class SpawnItem(Action):
    def __init__(self, itemType, position):
        self.action = 'spawnItem'
        self.options = {
            'itemType': to_dict(itemType),
            'position': to_dict(position),
        }


class CreateItemWithMaxQuantityAtPosition(Action):
    def __init__(self, itemType, position):
        self.action = 'createItemWithMaxQuantityAtPosition'
        self.options = {
            'itemType': to_dict(itemType),
            'position': to_dict(position),
        }


class ShowMenu(Action):
    def __init__(self, player):
        self.action = 'showMenu'
        self.options = {
            'player': to_dict(player),
        }


class StartAcceptingPlayers(Action):
    def __init__(self):
        self.action = 'startAcceptingPlayers'
        self.options = {}


class ForAllEntities(Action):
    def __init__(self, entityGroup, actions=[]):
        self.action = 'forAllEntities'
        self.options = {
            'entityGroup': to_dict(entityGroup),
            'actions': [to_dict(action) for action in actions],
        }


class MakePlayerSelectUnit(Action):
    def __init__(self, player, unit):
        self.action = 'makePlayerSelectUnit'
        self.options = {
            'player': to_dict(player),
            'unit': to_dict(unit),
        }


class SetEntityAttribute(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttribute'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
            'value': to_dict(value),
        }


class ForAllItemTypes(Action):
    def __init__(self, itemTypeGroup, actions=[]):
        self.action = 'forAllItemTypes'
        self.options = {
            'itemTypeGroup': to_dict(itemTypeGroup),
            'actions': [to_dict(action) for action in actions],
        }


class CreateEntityForPlayerAtPositionWithDimensions(Action):
    def __init__(self, entity, player, position, height: Number, width: Number, angle: Number):
        self.action = 'createEntityForPlayerAtPositionWithDimensions'
        self.options = {
            'entity': to_dict(entity),
            'player': to_dict(player),
            'position': to_dict(position),
            'height': to_dict(height),
            'width': to_dict(width),
            'angle': to_dict(angle),
        }


class EndGame(Action):
    def __init__(self):
        self.action = 'endGame'
        self.options = {}


class UpdateUiTextForEveryone(Action):
    def __init__(self, target, value: String):
        self.action = 'updateUiTextForEveryone'
        self.options = {
            'target': to_dict(target),
            'value': to_dict(value),
        }


class ForAllUnits(Action):
    def __init__(self, unitGroup, actions=[]):
        self.action = 'forAllUnits'
        self.options = {
            'unitGroup': to_dict(unitGroup),
            'actions': [to_dict(action) for action in actions],
        }


class ForAllProjectiles(Action):
    def __init__(self, projectileGroup, actions=[]):
        self.action = 'forAllProjectiles'
        self.options = {
            'projectileGroup': to_dict(projectileGroup),
            'actions': [to_dict(action) for action in actions],
        }


class StopMusicForPlayer(Action):
    def __init__(self, player):
        self.action = 'stopMusicForPlayer'
        self.options = {
            'player': to_dict(player),
        }


class PositionCamera(Action):
    def __init__(self, player, position):
        self.action = 'positionCamera'
        self.options = {
            'player': to_dict(player),
            'position': to_dict(position),
        }


class CreateProjectileAtPosition(Action):
    def __init__(self, projectileType, position, force: Number, angle: Number):
        self.action = 'createProjectileAtPosition'
        self.options = {
            'projectileType': to_dict(projectileType),
            'position': to_dict(position),
            'force': to_dict(force),
            'angle': to_dict(angle),
        }


class ShowMenuAndSelectCurrentServer(Action):
    def __init__(self, player):
        self.action = 'showMenuAndSelectCurrentServer'
        self.options = {
            'player': to_dict(player),
        }


class SetFadingTextOfUnit(Action):
    def __init__(self, unit, text: String, color: String):
        self.action = 'setFadingTextOfUnit'
        self.options = {
            'unit': to_dict(unit),
            'text': to_dict(text),
            'color': to_dict(color),
        }


class ChangeScaleOfEntityBody(Action):
    def __init__(self, entity, scale: Number):
        self.action = 'changeScaleOfEntityBody'
        self.options = {
            'entity': to_dict(entity),
            'scale': to_dict(scale),
        }


class ForAllRegions(Action):
    def __init__(self, regionGroup, actions=[]):
        self.action = 'forAllRegions'
        self.options = {
            'regionGroup': to_dict(regionGroup),
            'actions': [to_dict(action) for action in actions],
        }


class RotateEntityToRadiansLT(Action):
    def __init__(self, entity, radians: Number):
        self.action = 'rotateEntityToRadiansLT'
        self.options = {
            'entity': to_dict(entity),
            'radians': to_dict(radians),
        }


class SetPlayerAttributeMax(Action):
    def __init__(self, attributeType, player, number: Number):
        self.action = 'setPlayerAttributeMax'
        self.options = {
            'attributeType': to_dict(attributeType),
            'player': to_dict(player),
            'number': to_dict(number),
        }


class SetPlayerAttributeRegenerationRate(Action):
    def __init__(self, attributeType, player, number: Number):
        self.action = 'setPlayerAttributeRegenerationRate'
        self.options = {
            'attributeType': to_dict(attributeType),
            'player': to_dict(player),
            'number': to_dict(number),
        }


class ForAllUnitTypes(Action):
    def __init__(self, unitTypeGroup, actions=[]):
        self.action = 'forAllUnitTypes'
        self.options = {
            'unitTypeGroup': to_dict(unitTypeGroup),
            'actions': [to_dict(action) for action in actions],
        }


class DecreaseVariableByNumber(Action):
    def __init__(self, variable, number: Number):
        self.action = 'decreaseVariableByNumber'
        self.options = {
            'variable': to_dict(variable),
            'number': to_dict(number),
        }


class KickPlayer(Action):
    def __init__(self, entity):
        self.action = 'kickPlayer'
        self.options = {
            'entity': to_dict(entity),
        }


class ForAllPlayers(Action):
    def __init__(self, playerGroup, actions=[]):
        self.action = 'forAllPlayers'
        self.options = {
            'playerGroup': to_dict(playerGroup),
            'actions': [to_dict(action) for action in actions],
        }


class RemoveUnitFromUnitGroup(Action):
    def __init__(self, unit, unitGroup):
        self.action = 'removeUnitFromUnitGroup'
        self.options = {
            'unit': to_dict(unit),
            'unitGroup': to_dict(unitGroup),
        }


class FlipEntitySprite(Action):
    def __init__(self, entity, flip):
        """Flip entity sprite

        Args:
            entity (Entity): the entity who's sprite will be flipped
            flip (Flip): the flip direction, corresponding class is the Flip enum
        """
        self.action = 'flipEntitySprite'
        self.options = {
            'entity': to_dict(entity),
            'flip': to_dict(flip),
        }


class MakeUnitInvisibleToNeutralPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitInvisibleToNeutralPlayers'
        self.options = {
            'entity': to_dict(entity),
        }


class SaveUnitData(Action):
    def __init__(self, unit):
        self.action = 'saveUnitData'
        self.options = {
            'unit': to_dict(unit),
        }


class ApplyTorqueOnEntity(Action):
    def __init__(self, torque: Number, entity):
        self.action = 'applyTorqueOnEntity'
        self.options = {
            'torque': to_dict(torque),
            'entity': to_dict(entity),
        }


class GiveNewItemToUnit(Action):
    def __init__(self, itemType, unit):
        self.action = 'giveNewItemToUnit'
        self.options = {
            'itemType': to_dict(itemType),
            'unit': to_dict(unit),
        }


class StartUsingItem(Action):
    def __init__(self, entity):
        self.action = 'startUsingItem'
        self.options = {
            'entity': to_dict(entity),
            'hasFixedCSP': None,
        }


class MoveEntity(Action):
    def __init__(self, entity, position):
        self.action = 'moveEntity'
        self.options = {
            'entity': to_dict(entity),
            'position': to_dict(position),
        }


class For(Action):
    def __init__(self, variable, start: Number, stop: Number, actions=[]):
        self.action = 'for'
        self.options = {
            'variableName': variable.name,
            'start': to_dict(start),
            'stop': to_dict(stop),
            'actions': [to_dict(action) for action in actions],
        }


class ShowMenuAndSelectBestServer(Action):
    def __init__(self, player):
        self.action = 'showMenuAndSelectBestServer'
        self.options = {
            'player': to_dict(player),
        }


class ApplyForceOnEntityXYRelative(Action):
    def __init__(self, force_x: Number, force_y: Number, entity):
        self.action = 'applyForceOnEntityXYRelative'
        self.options = {
            'force': {
                'x': to_dict(force_x),
                'y':to_dict(force_y),
            },
            'entity': to_dict(entity),
        }


class ApplyForceOnEntityXYLT(Action):
    def __init__(self, force_x: Number, force_y: Number, entity):
        self.action = 'applyForceOnEntityXYLT'
        self.options = {
            'force': {
                'x': to_dict(force_x),
                'y':to_dict(force_y),
            },
            'entity': to_dict(entity),
        }


class AttachEntityToEntity(Action):
    def __init__(self, entity, targetingEntity):
        self.action = 'attachEntityToEntity'
        self.options = {
            'entity': to_dict(entity),
            'targetingEntity': to_dict(targetingEntity),
        }


class BanPlayerFromChat(Action):
    def __init__(self, player):
        self.action = 'banPlayerFromChat'
        self.options = {
            'player': to_dict(player),
        }


class ChangeUnitType(Action):
    def __init__(self, entity, unitType):
        self.action = 'changeUnitType'
        self.options = {
            'entity': to_dict(entity),
            'unitType': to_dict(unitType),
        }


class ForAllDebris(Action):
    def __init__(self, debrisGroup, actions=[]):
        self.action = 'forAllDebris'
        self.options = {
            'debrisGroup': to_dict(debrisGroup),
            'actions': [to_dict(action) for action in actions],
        }


class PlayMusicForPlayerRepeatedly(Action):
    def __init__(self, music, player):
        self.action = 'playMusicForPlayerRepeatedly'
        self.options = {
            'music': to_dict(music),
            'player': to_dict(player),
        }


class ShowGameSuggestionsForPlayer(Action):
    def __init__(self, player):
        self.action = 'showGameSuggestionsForPlayer'
        self.options = {
            'player': to_dict(player),
        }


class SetEntityAttributeRegenerationRate(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttributeRegenerationRate'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
            'value': to_dict(value),
        }


class MakeUnitSelectItemAtSlot(Action):
    def __init__(self, unit, slotIndex: Number):
        self.action = 'makeUnitSelectItemAtSlot'
        self.options = {
            'unit': to_dict(unit),
            'slotIndex': to_dict(slotIndex),
        }


class StopUsingItem(Action):
    def __init__(self, entity):
        self.action = 'stopUsingItem'
        self.options = {
            'entity': to_dict(entity),
            'hasFixedCSP': None,
        }


class MakeUnitVisible(Action):
    def __init__(self, entity):
        self.action = 'makeUnitVisible'
        self.options = {
            'entity': to_dict(entity),
        }


class MakeUnitInvisible(Action):
    def __init__(self, entity):
        self.action = 'makeUnitInvisible'
        self.options = {
            'entity': to_dict(entity),
        }


class Break(Action):
    def __init__(self):
        self.action = 'break'
        self.options = {}


class ChangeScaleOfEntitySprite(Action):
    def __init__(self, entity, scale: Number):
        self.action = 'changeScaleOfEntitySprite'
        self.options = {
            'entity': to_dict(entity),
            'scale': to_dict(scale),
        }


class SetPlayerName(Action):
    def __init__(self, player, name: String):
        self.action = 'setPlayerName'
        self.options = {
            'player': to_dict(player),
            'name': to_dict(name),
        }


class MakeUnitPickupItemAtSlot(Action):
    def __init__(self, unit, item, slotIndex: Number):
        self.action = 'makeUnitPickupItemAtSlot'
        self.options = {
            'unit': to_dict(unit),
            'item': to_dict(item),
            'slotIndex': to_dict(slotIndex),
        }


class DropItemInInventorySlot(Action):
    def __init__(self, unit, slotIndex: Number):
        self.action = 'dropItemInInventorySlot'
        self.options = {
            'unit': to_dict(unit),
            'slotIndex': to_dict(slotIndex),
        }


class UnbanPlayerFromChat(Action):
    def __init__(self, player):
        self.action = 'unbanPlayerFromChat'
        self.options = {
            'player': to_dict(player),
        }


class ChangeDescriptionOfItem(Action):
    def __init__(self, item, string: String):
        self.action = 'changeDescriptionOfItem'
        self.options = {
            'item': to_dict(item),
            'string': to_dict(string),
        }


class SendChatMessageToPlayer(Action):
    def __init__(self, message: String, player):
        self.action = 'sendChatMessageToPlayer'
        self.options = {
            'message': to_dict(message),
            'player': to_dict(player),
        }


class PlayAdForEveryone(Action):
    def __init__(self):
        self.action = 'playAdForEveryone'
        self.options = {}


class HideUiTextForPlayer(Action):
    def __init__(self, target, entity):
        self.action = 'hideUiTextForPlayer'
        self.options = {
            'target': to_dict(target),
            'entity': to_dict(entity),
        }


class ShowUiTextForPlayer(Action):
    def __init__(self, target, entity):
        self.action = 'showUiTextForPlayer'
        self.options = {
            'target': to_dict(target),
            'entity': to_dict(entity),
        }


class ResetDebrisPosition(Action):
    def __init__(self, entity):
        self.action = 'resetDebrisPosition'
        self.options = {
            'entity': to_dict(entity),
        }


class PlayMusic(Action):
    def __init__(self, music):
        self.action = 'playMusic'
        self.options = {
            'music': to_dict(music),
        }


class AssignPlayerType(Action):
    def __init__(self, entity, playerType):
        self.action = 'assignPlayerType'
        self.options = {
            'entity': to_dict(entity),
            'playerType': to_dict(playerType),
        }


class PlayMusicForPlayer(Action):
    def __init__(self, music, player):
        self.action = 'playMusicForPlayer'
        self.options = {
            'music': to_dict(music),
            'player': to_dict(player),
        }


class MakeUnitVisibleToNeutralPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitVisibleToNeutralPlayers'
        self.options = {
            'entity': to_dict(entity),
        }


class MakeUnitVisibleToFriendlyPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitVisibleToFriendlyPlayers'
        self.options = {
            'entity': to_dict(entity),
        }


class MakeUnitPickupItem(Action):
    def __init__(self, unit, item):
        self.action = 'makeUnitPickupItem'
        self.options = {
            'unit': to_dict(unit),
            'item': to_dict(item),
        }


class GiveNewItemWithQuantityToUnit(Action):
    def __init__(self, itemType, number: Number, unit):
        self.action = 'giveNewItemWithQuantityToUnit'
        self.options = {
            'itemType': to_dict(itemType),
            'number': to_dict(number),
            'unit': to_dict(unit),
        }


class DropAllItems(Action):
    def __init__(self, entity):
        self.action = 'dropAllItems'
        self.options = {
            'entity': to_dict(entity),
        }


class UseItemOnce(Action):
    def __init__(self, item):
        self.action = 'useItemOnce'
        self.options = {
            'item': to_dict(item),
        }


class StopAcceptingPlayers(Action):
    def __init__(self):
        self.action = 'stopAcceptingPlayers'
        self.options = {}


class SetEntityVelocityAtAngle(Action):
    def __init__(self, entity, speed: Number, angle: Number):
        self.action = 'setEntityVelocityAtAngle'
        self.options = {
            'entity': to_dict(entity),
            'speed': to_dict(speed),
            'angle': to_dict(angle),
        }


class SetEntityAttributeMax(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttributeMax'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
            'value': to_dict(value),
        }


class SetPlayerAttributeMin(Action):
    def __init__(self, attributeType, player, number: Number):
        self.action = 'setPlayerAttributeMin'
        self.options = {
            'attributeType': to_dict(attributeType),
            'player': to_dict(player),
            'number': to_dict(number),
        }


class MakePlayerTradeWithPlayer(Action):
    def __init__(self, playerA, playerB):
        self.action = 'makePlayerTradeWithPlayer'
        self.options = {
            'playerA': to_dict(playerA),
            'playerB': to_dict(playerB),
        }


class UpdateUiTextForTimeForPlayer(Action):
    def __init__(self, target, value: String, player, time: Number):
        self.action = 'updateUiTextForTimeForPlayer'
        self.options = {
            'target': to_dict(target),
            'value': to_dict(value),
            'player': to_dict(player),
            'time': to_dict(time),
        }


class AiMoveToPosition(Action):
    def __init__(self, unit, position):
        self.action = 'aiMoveToPosition'
        self.options = {
            'unit': to_dict(unit),
            'position': to_dict(position),
        }


class AiAttackUnit(Action):
    def __init__(self, unit, targetUnit):
        self.action = 'aiAttackUnit'
        self.options = {
            'unit': to_dict(unit),
            'targetUnit': to_dict(targetUnit),
        }


class ChangeSensorRadius(Action):
    def __init__(self, sensor, radius: Number):
        self.action = 'changeSensorRadius'
        self.options = {
            'sensor': to_dict(sensor),
            'radius': to_dict(radius),
        }


class LoadPlayerDataAndApplyIt(Action):
    def __init__(self, player, unit):
        self.action = 'loadPlayerDataAndApplyIt'
        self.options = {
            'player': to_dict(player),
            'unit': to_dict(unit),
        }


class CreateFloatingText(Action):
    def __init__(self, text: String, position, color: String):
        self.action = 'createFloatingText'
        self.options = {
            'text': to_dict(text),
            'position': to_dict(position),
            'color': to_dict(color),
        }


class SetLastAttackedUnit(Action):
    def __init__(self, unit):
        self.action = 'setLastAttackedUnit'
        self.options = {
            'unit': to_dict(unit),
        }


class SetLastAttackingUnit(Action):
    def __init__(self, unit):
        self.action = 'setLastAttackingUnit'
        self.options = {
            'unit': to_dict(unit),
        }


class SetItemFireRate(Action):
    def __init__(self, number: Number, item):
        self.action = 'setItemFireRate'
        self.options = {
            'number': to_dict(number),
            'item': to_dict(item),
        }


class ApplyImpulseOnEntityXY(Action):
    def __init__(self, impulse_x: Number, impulse_y: Number, entity):
        self.action = 'applyImpulseOnEntityXY'
        self.options = {
            'impulse': {
                'x': to_dict(impulse_x),
                'y': to_dict(impulse_y),
            },
            'entity': to_dict(entity),
        }


class PlaySoundForPlayer(Action):
    def __init__(self, sound, player):
        self.action = 'playSoundForPlayer'
        self.options = {
            'sound': to_dict(sound),
            'player': to_dict(player),
        }


class StopSoundForPlayer(Action):
    def __init__(self, sound, player):
        self.action = 'stopSoundForPlayer'
        self.options = {
            'sound': to_dict(sound),
            'player': to_dict(player),
        }


class ShowDismissibleInputModalToPlayer(Action):
    def __init__(self, player, inputLabel: String):
        self.action = 'showDismissibleInputModalToPlayer'
        self.options = {
            'player': to_dict(player),
            'inputLabel': to_dict(inputLabel),
        }


class SetItemName(Action):
    def __init__(self, name: String, item):
        self.action = 'setItemName'
        self.options = {
            'name': to_dict(name),
            'item': to_dict(item),
        }


class ChangeItemInventoryImage(Action):
    def __init__(self, url: String, item):
        self.action = 'changeItemInventoryImage'
        self.options = {
            'url': to_dict(url),
            'item': to_dict(item),
        }


class AddAttributeBuffToUnit(Action):
    def __init__(self, entity, value: Number, attribute, time: Number):
        self.action = 'addAttributeBuffToUnit'
        self.options = {
            'entity': to_dict(entity),
            'value': to_dict(value),
            'attribute': to_dict(attribute),
            'time': to_dict(time),
        }


class AddPercentageAttributeBuffToUnit(Action):
    def __init__(self, entity, value: Number, attribute, time: Number):
        self.action = 'addPercentageAttributeBuffToUnit'
        self.options = {
            'entity': to_dict(entity),
            'value': to_dict(value),
            'attribute': to_dict(attribute),
            'time': to_dict(time),
        }


class StunUnit(Action):
    def __init__(self, unit):
        self.action = 'stunUnit'
        self.options = {
            'unit': to_dict(unit),
        }


class RemoveStunFromUnit(Action):
    def __init__(self, unit):
        self.action = 'removeStunFromUnit'
        self.options = {
            'unit': to_dict(unit),
        }


class SetLastAttackingItem(Action):
    def __init__(self, item):
        self.action = 'setLastAttackingItem'
        self.options = {
            'item': to_dict(item),
        }


class MutePlayerMicrophone(Action):
    def __init__(self, player):
        self.action = 'mutePlayerMicrophone'
        self.options = {
            'player': to_dict(player),
        }


class UnmutePlayerMicrophone(Action):
    def __init__(self, player):
        self.action = 'unmutePlayerMicrophone'
        self.options = {
            'player': to_dict(player),
        }


class SendPostRequest(Action):
    def __init__(self, string: String, url: String, varName):
        self.action = 'sendPostRequest'
        self.options = {
            'string': to_dict(string),
            'url': to_dict(url),
            'varName': to_dict(varName),
        }


class LoadUnitDataFromString(Action):
    def __init__(self, string: String, unit):
        self.action = 'loadUnitDataFromString'
        self.options = {
            'string': to_dict(string),
            'unit': to_dict(unit),
        }


class LoadPlayerDataFromString(Action):
    def __init__(self, string: String, player):
        self.action = 'loadPlayerDataFromString'
        self.options = {
            'string': to_dict(string),
            'player': to_dict(player),
        }


class RemoveAllAttributeBuffs(Action):
    def __init__(self, unit):
        self.action = 'removeAllAttributeBuffs'
        self.options = {
            'unit': to_dict(unit),
        }


class ChangeInventorySlotColor(Action):
    def __init__(self, item, string: String):
        self.action = 'changeInventorySlotColor'
        self.options = {
            'item': to_dict(item),
            'string': to_dict(string),
        }


class SetOwnerUnitOfProjectile(Action):
    def __init__(self, unit, projectile):
        self.action = 'setOwnerUnitOfProjectile'
        self.options = {
            'unit': to_dict(unit),
            'projectile': to_dict(projectile),
        }


class EnableAI(Action):
    def __init__(self, unit):
        self.action = 'enableAI'
        self.options = {
            'unit': to_dict(unit),
        }


class DisableAI(Action):
    def __init__(self, unit):
        self.action = 'disableAI'
        self.options = {
            'unit': to_dict(unit),
        }


class AiGoIdle(Action):
    def __init__(self, unit):
        self.action = 'aiGoIdle'
        self.options = {
            'unit': to_dict(unit),
        }
