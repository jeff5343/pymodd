from __future__ import annotations
from copy import deepcopy

from .script import Base
from .utils.data_templates import CONDITION_DATA_TEMPLATE
from .functions import Number, String


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


class Condition(Base):
    def __init__(self, item_a: Base, operator: str, item_b: Base):
        """The comparison type of the condition is determined based on the type of item_a

        Args:
            item_a (Base): any object
            operator (str): can be regular comparisons (==, !=, >=, ...) or 'AND' and 'OR'
            item_b (Base): any object
        """

        type_class = None
        if operator.lower() == 'and' or operator.lower() == 'or':
            type_class = operator.lower()
        else:
            base_classes = item_a.__class__.mro()
            for i, base_class in enumerate(base_classes):
                if base_class.__name__ == 'Function':
                    type_class = base_classes[i-1].__name__.lower()
                    break
        self.comparison = type_class
        self.item_a = item_a
        self.operator = operator.upper()
        self.item_b = item_b

    def to_dict(self):
        data = deepcopy(CONDITION_DATA_TEMPLATE)
        data[0]['operandType'] = self.comparison
        data[0]['operator'] = self.operator
        data[1] = self.item_a.to_dict()
        data[2] = self.item_b.to_dict()
        return data


class IfStatement(Action):
    def __init__(self, condition: Condition, then_actions=[], else_actions=[]):
        self.condition = condition
        self.thenActions = [action.to_dict() for action in then_actions]
        self.elseActions = [action.to_dict() for action in else_actions]

    def to_dict(self):
        return {
            'type': 'condition',
            'conditions': self.condition.to_dict(),
            'then': self.thenActions,
            'else': self.elseActions
        }



class PlayAdForPlayer(Action):
    def __init__(self, entity):
        self.action = 'playAdForPlayer'
        self.options = {
            'entity': entity.to_dict(),
        }


class SetTimeOut(Action):
    def __init__(self, duration: Number, actions=[]):
        self.action = 'setTimeOut'
        self.options = {
            'duration': duration.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class RotateEntityToFacePosition(Action):
    def __init__(self, entity, position):
        self.action = 'rotateEntityToFacePosition'
        self.options = {
            'entity': entity.to_dict(),
            'position': position.to_dict(),
        }


class DestroyEntity(Action):
    def __init__(self, entity):
        self.action = 'destroyEntity'
        self.options = {
            'entity': entity.to_dict(),
        }


class SetEntityDepth(Action):
    def __init__(self, entity, value: Number):
        self.action = 'setEntityDepth'
        self.options = {
            'entity': entity.to_dict(),
            'value': value.to_dict(),
        }


class HideUnitFromPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'hideUnitFromPlayer'
        self.options = {
            'entity': entity.to_dict(),
            'player': player.to_dict(),
        }


class ShowUnitToPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'showUnitToPlayer'
        self.options = {
            'entity': entity.to_dict(),
            'player': player.to_dict(),
        }


class SendChatMessage(Action):
    def __init__(self, message: String):
        self.action = 'sendChatMessage'
        self.options = {
            'message': message.to_dict(),
        }


class PlaySoundAtPosition(Action):
    def __init__(self, sound, position):
        self.action = 'playSoundAtPosition'
        self.options = {
            'sound': sound.to_dict(),
            'position': position.to_dict(),
        }


class DropItemAtPosition(Action):
    def __init__(self, item, position):
        self.action = 'dropItemAtPosition'
        self.options = {
            'item': item.to_dict(),
            'position': position.to_dict(),
        }


class ApplyForceOnEntityAngle(Action):
    def __init__(self, force: Number, entity, angle: Number):
        self.action = 'applyForceOnEntityAngle'
        self.options = {
            'force': force.to_dict(),
            'entity': entity.to_dict(),
            'angle': angle.to_dict(),
        }


class ShowInputModalToPlayer(Action):
    def __init__(self, player, inputLabel: String):
        self.action = 'showInputModalToPlayer'
        self.options = {
            'player': player.to_dict(),
            'inputLabel': inputLabel.to_dict(),
        }


class OpenDialogueForPlayer(Action):
    def __init__(self, dialogue, player):
        self.action = 'openDialogueForPlayer'
        self.options = {
            'dialogue': dialogue.to_dict(),
            'player': player.to_dict(),
        }


class Continue(Action):
    def __init__(self):
        self.action = 'continue'
        self.options = {}


class OpenWebsiteForPlayer(Action):
    def __init__(self, string: String, player):
        self.action = 'openWebsiteForPlayer'
        self.options = {
            'string': string.to_dict(),
            'player': player.to_dict(),
        }


class SetEntityLifeSpan(Action):
    def __init__(self, entity, lifeSpan: Number):
        self.action = 'setEntityLifeSpan'
        self.options = {
            'entity': entity.to_dict(),
            'lifeSpan': lifeSpan.to_dict(),
        }


class HideUnitNameLabel(Action):
    def __init__(self, entity):
        self.action = 'hideUnitNameLabel'
        self.options = {
            'entity': entity.to_dict(),
        }


class SetTriggeringUnit(Action):
    def __init__(self, entity):
        self.action = 'setTriggeringUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class CreateUnitForPlayerAtPosition(Action):
    def __init__(self, unitType, player, position, angle: Number):
        self.action = 'createUnitAtPosition'
        self.options = {
            'unitType': unitType.to_dict(),
            'entity': player.to_dict(),
            'position': position.to_dict(),
            'angle': angle.to_dict(),
        }


class HideUiTextForEveryone(Action):
    def __init__(self, target):
        self.action = 'hideUiTextForEveryone'
        self.options = {
            'target': target.to_dict(),
        }


class HideGameSuggestionsForPlayer(Action):
    def __init__(self, player):
        self.action = 'hideGameSuggestionsForPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class TransformRegionDimensions(Action):
    def __init__(self, region, x: Number, y: Number, width: Number, height: Number):
        self.action = 'transformRegionDimensions'
        self.options = {
            'region': region.to_dict(),
            'x': x.to_dict(),
            'y': y.to_dict(),
            'width': width.to_dict(),
            'height': height.to_dict(),
        }


class MakeUnitInvisibleToFriendlyPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitInvisibleToFriendlyPlayers'
        self.options = {
            'entity': entity.to_dict(),
        }


class SetEntityAttributeMin(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttributeMin'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
            'value': value.to_dict(),
        }


class ShowInviteFriendsModal(Action):
    def __init__(self, player):
        self.action = 'showInviteFriendsModal'
        self.options = {
            'player': player.to_dict(),
        }


class ShowCustomModalToPlayer(Action):
    def __init__(self, htmlContent, player):
        self.action = 'showCustomModalToPlayer'
        self.options = {
            'htmlContent': htmlContent.to_dict(),
            'player': player.to_dict(),
        }


class ShowUiTextForEveryone(Action):
    def __init__(self, target):
        self.action = 'showUiTextForEveryone'
        self.options = {
            'target': target.to_dict(),
        }


class MoveDebris(Action):
    def __init__(self, entity, position):
        self.action = 'moveDebris'
        self.options = {
            'entity': entity.to_dict(),
            'position': position.to_dict(),
        }


class ForAllItems(Action):
    def __init__(self, itemGroup, actions=[]):
        self.action = 'forAllItems'
        self.options = {
            'itemGroup': itemGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class RemovePlayerFromPlayerGroup(Action):
    def __init__(self, player, playerGroup):
        self.action = 'removePlayerFromPlayerGroup'
        self.options = {
            'player': player.to_dict(),
            'playerGroup': playerGroup.to_dict(),
        }


class SetUnitOwner(Action):
    def __init__(self, unit, player):
        self.action = 'setUnitOwner'
        self.options = {
            'unit': unit.to_dict(),
            'player': player.to_dict(),
        }


class UpdateItemQuantity(Action):
    def __init__(self, entity, quantity: Number):
        self.action = 'updateItemQuantity'
        self.options = {
            'entity': entity.to_dict(),
            'quantity': quantity.to_dict(),
        }


class ApplyForceOnEntityAngleLT(Action):
    def __init__(self, force: Number, entity, angle: Number):
        self.action = 'applyForceOnEntityAngleLT'
        self.options = {
            'force': force.to_dict(),
            'entity': entity.to_dict(),
            'angle': angle.to_dict(),
        }


class SetEntityState(Action):
    def __init__(self, entity, state):
        self.action = 'setEntityState'
        self.options = {
            'entity': entity.to_dict(),
            'state': state.to_dict(),
        }


class HideUnitInPlayerMinimap(Action):
    def __init__(self, unit, player):
        self.action = 'hideUnitInPlayerMinimap'
        self.options = {
            'unit': unit.to_dict(),
            'player': player.to_dict(),
        }


class Return(Action):
    def __init__(self):
        self.action = 'return'
        self.options = {}


class RunScript(Action):
    def __init__(self, scriptName):
        self.action = 'runScript'
        self.options = {
            'scriptName': scriptName.to_dict(),
        }


class PlayerCameraSetZoom(Action):
    def __init__(self, player, zoom: Number):
        self.action = 'playerCameraSetZoom'
        self.options = {
            'player': player.to_dict(),
            'zoom': zoom.to_dict(),
        }


class SetUnitNameLabel(Action):
    def __init__(self, unit, name: String):
        self.action = 'setUnitNameLabel'
        self.options = {
            'unit': unit.to_dict(),
            'name': name.to_dict(),
        }


class OpenShopForPlayer(Action):
    def __init__(self, shop, player):
        self.action = 'openShopForPlayer'
        self.options = {
            'shop': shop.to_dict(),
            'player': player.to_dict(),
        }


class CloseDialogueForPlayer(Action):
    def __init__(self, player):
        self.action = 'closeDialogueForPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class Comment(Action):
    def __init__(self):
        self.action = 'comment'
        self.options = {}


class CreateEntityAtPositionWithDimensions(Action):
    def __init__(self, entity, position, height: Number, width: Number, angle: Number):
        self.action = 'createEntityAtPositionWithDimensions'
        self.options = {
            'entity': entity.to_dict(),
            'position': position.to_dict(),
            'height': height.to_dict(),
            'width': width.to_dict(),
            'angle': angle.to_dict(),
        }


class SetVariable(Action):
    def __init__(self, variable, value):
        self.action = 'setVariable'
        self.options = {
            'variableName': variable.name,
            'value': value.to_dict(),
        }


class IncreaseVariableByNumber(Action):
    def __init__(self, variable, number: Number):
        self.action = 'increaseVariableByNumber'
        self.options = {
            'variable': variable.to_dict(),
            'number': number.to_dict(),
        }


class PlayerCameraTrackUnit(Action):
    def __init__(self, player, unit):
        self.action = 'playerCameraTrackUnit'
        self.options = {
            'player': player.to_dict(),
            'unit': unit.to_dict(),
        }


class CastAbility(Action):
    def __init__(self, entity, abilityName):
        self.action = 'castAbility'
        self.options = {
            'entity': entity.to_dict(),
            'abilityName': abilityName.to_dict(),
        }


class PlayEntityAnimation(Action):
    def __init__(self, entity, animation):
        self.action = 'playEntityAnimation'
        self.options = {
            'entity': entity.to_dict(),
            'animation': animation.to_dict(),
        }


class While(Action):
    def __init__(self, conditions, actions=[]):
        self.action = 'while'
        self.options = {
            'conditions': conditions.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class ApplyForceOnEntityXY(Action):
    def __init__(self, force_x: Number, force_y: Number, entity):
        self.action = 'applyForceOnEntityXY'
        self.options = {
            'force.x': force_x.to_dict(),
            'force.y': force_y.to_dict(),
            'entity': entity.to_dict(),
        }


class ShowUnitInPlayerMinimap(Action):
    def __init__(self, unit, color: String, player):
        self.action = 'showUnitInPlayerMinimap'
        self.options = {
            'unit': unit.to_dict(),
            'color': color.to_dict(),
            'player': player.to_dict(),
        }


class SavePlayerData(Action):
    def __init__(self, player):
        self.action = 'savePlayerData'
        self.options = {
            'player': player.to_dict(),
        }


class HideUnitNameLabelFromPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'hideUnitNameLabelFromPlayer'
        self.options = {
            'entity': entity.to_dict(),
            'player': player.to_dict(),
        }


class SetPlayerAttribute(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setPlayerAttribute'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
            'value': value.to_dict(),
        }


class UpdateUiTextForPlayer(Action):
    def __init__(self, target, value: String, entity):
        self.action = 'updateUiTextForPlayer'
        self.options = {
            'target': target.to_dict(),
            'value': value.to_dict(),
            'entity': entity.to_dict(),
        }


class ShowUnitNameLabel(Action):
    def __init__(self, entity):
        self.action = 'showUnitNameLabel'
        self.options = {
            'entity': entity.to_dict(),
        }


class CloseShopForPlayer(Action):
    def __init__(self, player):
        self.action = 'closeShopForPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class AttachDebrisToUnit(Action):
    def __init__(self, entity, unit):
        self.action = 'attachDebrisToUnit'
        self.options = {
            'entity': entity.to_dict(),
            'unit': unit.to_dict(),
        }


class Repeat(Action):
    def __init__(self, count: Number, actions=[]):
        self.action = 'repeat'
        self.options = {
            'count': count.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class StopMusic(Action):
    def __init__(self):
        self.action = 'stopMusic'
        self.options = {}


class EmitParticleOnceAtPosition(Action):
    def __init__(self, particleType, position):
        self.action = 'emitParticleOnceAtPosition'
        self.options = {
            'particleType': particleType.to_dict(),
            'position': position.to_dict(),
        }


class SetVelocityOfEntityXY(Action):
    def __init__(self, velocity_x: Number, velocity_y: Number, entity):
        self.action = 'setVelocityOfEntityXY'
        self.options = {
            'velocity.x': velocity_x.to_dict(),
            'velocity.y': velocity_y.to_dict(),
            'entity': entity.to_dict(),
        }


class ShowUnitNameLabelToPlayer(Action):
    def __init__(self, entity, player):
        self.action = 'showUnitNameLabelToPlayer'
        self.options = {
            'entity': entity.to_dict(),
            'player': player.to_dict(),
        }


class SpawnItem(Action):
    def __init__(self, itemType, position):
        self.action = 'spawnItem'
        self.options = {
            'itemType': itemType.to_dict(),
            'position': position.to_dict(),
        }


class CreateItemWithMaxQuantityAtPosition(Action):
    def __init__(self, itemType, position):
        self.action = 'createItemWithMaxQuantityAtPosition'
        self.options = {
            'itemType': itemType.to_dict(),
            'position': position.to_dict(),
        }


class ShowMenu(Action):
    def __init__(self, player):
        self.action = 'showMenu'
        self.options = {
            'player': player.to_dict(),
        }


class StartAcceptingPlayers(Action):
    def __init__(self):
        self.action = 'startAcceptingPlayers'
        self.options = {}


class ForAllEntities(Action):
    def __init__(self, entityGroup, actions=[]):
        self.action = 'forAllEntities'
        self.options = {
            'entityGroup': entityGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class MakePlayerSelectUnit(Action):
    def __init__(self, player, unit):
        self.action = 'makePlayerSelectUnit'
        self.options = {
            'player': player.to_dict(),
            'unit': unit.to_dict(),
        }


class SetEntityAttribute(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttribute'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
            'value': value.to_dict(),
        }


class ForAllItemTypes(Action):
    def __init__(self, itemTypeGroup, actions=[]):
        self.action = 'forAllItemTypes'
        self.options = {
            'itemTypeGroup': itemTypeGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class CreateEntityForPlayerAtPositionWithDimensions(Action):
    def __init__(self, entity, player, position, height: Number, width: Number, angle: Number):
        self.action = 'createEntityForPlayerAtPositionWithDimensions'
        self.options = {
            'entity': entity.to_dict(),
            'player': player.to_dict(),
            'position': position.to_dict(),
            'height': height.to_dict(),
            'width': width.to_dict(),
            'angle': angle.to_dict(),
        }


class EndGame(Action):
    def __init__(self):
        self.action = 'endGame'
        self.options = {}


class UpdateUiTextForEveryone(Action):
    def __init__(self, target, value: String):
        self.action = 'updateUiTextForEveryone'
        self.options = {
            'target': target.to_dict(),
            'value': value.to_dict(),
        }


class ForAllUnits(Action):
    def __init__(self, unitGroup, actions=[]):
        self.action = 'forAllUnits'
        self.options = {
            'unitGroup': unitGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class ForAllProjectiles(Action):
    def __init__(self, projectileGroup, actions=[]):
        self.action = 'forAllProjectiles'
        self.options = {
            'projectileGroup': projectileGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class StopMusicForPlayer(Action):
    def __init__(self, player):
        self.action = 'stopMusicForPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class PositionCamera(Action):
    def __init__(self, player, position):
        self.action = 'positionCamera'
        self.options = {
            'player': player.to_dict(),
            'position': position.to_dict(),
        }


class CreateProjectileAtPosition(Action):
    def __init__(self, projectileType, position, force: Number, angle: Number):
        self.action = 'createProjectileAtPosition'
        self.options = {
            'projectileType': projectileType.to_dict(),
            'position': position.to_dict(),
            'force': force.to_dict(),
            'angle': angle.to_dict(),
        }


class ShowMenuAndSelectCurrentServer(Action):
    def __init__(self, player):
        self.action = 'showMenuAndSelectCurrentServer'
        self.options = {
            'player': player.to_dict(),
        }


class SetFadingTextOfUnit(Action):
    def __init__(self, unit, text: String, color: String):
        self.action = 'setFadingTextOfUnit'
        self.options = {
            'unit': unit.to_dict(),
            'text': text.to_dict(),
            'color': color.to_dict(),
        }


class ChangeScaleOfEntityBody(Action):
    def __init__(self, entity, scale: Number):
        self.action = 'changeScaleOfEntityBody'
        self.options = {
            'entity': entity.to_dict(),
            'scale': scale.to_dict(),
        }


class ForAllRegions(Action):
    def __init__(self, regionGroup, actions=[]):
        self.action = 'forAllRegions'
        self.options = {
            'regionGroup': regionGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class RotateEntityToRadiansLT(Action):
    def __init__(self, entity, radians: Number):
        self.action = 'rotateEntityToRadiansLT'
        self.options = {
            'entity': entity.to_dict(),
            'radians': radians.to_dict(),
        }


class SetPlayerAttributeMax(Action):
    def __init__(self, attributeType, player, number: Number):
        self.action = 'setPlayerAttributeMax'
        self.options = {
            'attributeType': attributeType.to_dict(),
            'player': player.to_dict(),
            'number': number.to_dict(),
        }


class SetPlayerAttributeRegenerationRate(Action):
    def __init__(self, attributeType, player, number: Number):
        self.action = 'setPlayerAttributeRegenerationRate'
        self.options = {
            'attributeType': attributeType.to_dict(),
            'player': player.to_dict(),
            'number': number.to_dict(),
        }


class ForAllUnitTypes(Action):
    def __init__(self, unitTypeGroup, actions=[]):
        self.action = 'forAllUnitTypes'
        self.options = {
            'unitTypeGroup': unitTypeGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class DecreaseVariableByNumber(Action):
    def __init__(self, variable, number: Number):
        self.action = 'decreaseVariableByNumber'
        self.options = {
            'variable': variable.to_dict(),
            'number': number.to_dict(),
        }


class KickPlayer(Action):
    def __init__(self, entity):
        self.action = 'kickPlayer'
        self.options = {
            'entity': entity.to_dict(),
        }


class ForAllPlayers(Action):
    def __init__(self, playerGroup, actions=[]):
        self.action = 'forAllPlayers'
        self.options = {
            'playerGroup': playerGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class RemoveUnitFromUnitGroup(Action):
    def __init__(self, unit, unitGroup):
        self.action = 'removeUnitFromUnitGroup'
        self.options = {
            'unit': unit.to_dict(),
            'unitGroup': unitGroup.to_dict(),
        }


class FlipEntitySprite(Action):
    def __init__(self, entity, flip):
        self.action = 'flipEntitySprite'
        self.options = {
            'entity': entity.to_dict(),
            'flip': flip.to_dict(),
        }


class MakeUnitInvisibleToNeutralPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitInvisibleToNeutralPlayers'
        self.options = {
            'entity': entity.to_dict(),
        }


class SaveUnitData(Action):
    def __init__(self, unit):
        self.action = 'saveUnitData'
        self.options = {
            'unit': unit.to_dict(),
        }


class ApplyTorqueOnEntity(Action):
    def __init__(self, torque: Number, entity):
        self.action = 'applyTorqueOnEntity'
        self.options = {
            'torque': torque.to_dict(),
            'entity': entity.to_dict(),
        }


class GiveNewItemToUnit(Action):
    def __init__(self, itemType, unit):
        self.action = 'giveNewItemToUnit'
        self.options = {
            'itemType': itemType.to_dict(),
            'unit': unit.to_dict(),
        }


class StartUsingItem(Action):
    def __init__(self, entity, hasFixedCSP):
        self.action = 'startUsingItem'
        self.options = {
            'entity': entity.to_dict(),
            'hasFixedCSP': hasFixedCSP.to_dict(),
        }


class MoveEntity(Action):
    def __init__(self, entity, position):
        self.action = 'moveEntity'
        self.options = {
            'entity': entity.to_dict(),
            'position': position.to_dict(),
        }


class For(Action):
    def __init__(self, variable, start: Number, stop: Number, actions=[]):
        self.action = 'for'
        self.options = {
            'variableName': variable.name,
            'start': start.to_dict(),
            'stop': stop.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class ShowMenuAndSelectBestServer(Action):
    def __init__(self, player):
        self.action = 'showMenuAndSelectBestServer'
        self.options = {
            'player': player.to_dict(),
        }


class ApplyForceOnEntityXYRelative(Action):
    def __init__(self, force_x: Number, force_y: Number, entity):
        self.action = 'applyForceOnEntityXYRelative'
        self.options = {
            'force.x': force_x.to_dict(),
            'force.y': force_y.to_dict(),
            'entity': entity.to_dict(),
        }


class ApplyForceOnEntityXYLT(Action):
    def __init__(self, force_x: Number, force_y: Number, entity):
        self.action = 'applyForceOnEntityXYLT'
        self.options = {
            'force.x': force_x.to_dict(),
            'force.y': force_y.to_dict(),
            'entity': entity.to_dict(),
        }


class AttachEntityToEntity(Action):
    def __init__(self, entity, targetingEntity):
        self.action = 'attachEntityToEntity'
        self.options = {
            'entity': entity.to_dict(),
            'targetingEntity': targetingEntity.to_dict(),
        }


class BanPlayerFromChat(Action):
    def __init__(self, player):
        self.action = 'banPlayerFromChat'
        self.options = {
            'player': player.to_dict(),
        }


class ChangeUnitType(Action):
    def __init__(self, entity, unitType):
        self.action = 'changeUnitType'
        self.options = {
            'entity': entity.to_dict(),
            'unitType': unitType.to_dict(),
        }


class ForAllDebris(Action):
    def __init__(self, debrisGroup, actions=[]):
        self.action = 'forAllDebris'
        self.options = {
            'debrisGroup': debrisGroup.to_dict(),
            'actions': [action.to_dict() for action in actions],
        }


class PlayMusicForPlayerRepeatedly(Action):
    def __init__(self, music, player):
        self.action = 'playMusicForPlayerRepeatedly'
        self.options = {
            'music': music.to_dict(),
            'player': player.to_dict(),
        }


class ShowGameSuggestionsForPlayer(Action):
    def __init__(self, player):
        self.action = 'showGameSuggestionsForPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class SetEntityAttributeRegenerationRate(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttributeRegenerationRate'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
            'value': value.to_dict(),
        }


class MakeUnitSelectItemAtSlot(Action):
    def __init__(self, unit, slotIndex: Number):
        self.action = 'makeUnitSelectItemAtSlot'
        self.options = {
            'unit': unit.to_dict(),
            'slotIndex': slotIndex.to_dict(),
        }


class StopUsingItem(Action):
    def __init__(self, entity, hasFixedCSP):
        self.action = 'stopUsingItem'
        self.options = {
            'entity': entity.to_dict(),
            'hasFixedCSP': hasFixedCSP.to_dict(),
        }


class MakeUnitVisible(Action):
    def __init__(self, entity):
        self.action = 'makeUnitVisible'
        self.options = {
            'entity': entity.to_dict(),
        }


class MakeUnitInvisible(Action):
    def __init__(self, entity):
        self.action = 'makeUnitInvisible'
        self.options = {
            'entity': entity.to_dict(),
        }


class Break(Action):
    def __init__(self):
        self.action = 'break'
        self.options = {}


class ChangeScaleOfEntitySprite(Action):
    def __init__(self, entity, scale: Number):
        self.action = 'changeScaleOfEntitySprite'
        self.options = {
            'entity': entity.to_dict(),
            'scale': scale.to_dict(),
        }


class SetPlayerName(Action):
    def __init__(self, player, name: String):
        self.action = 'setPlayerName'
        self.options = {
            'player': player.to_dict(),
            'name': name.to_dict(),
        }


class MakeUnitPickupItemAtSlot(Action):
    def __init__(self, unit, item, slotIndex: Number):
        self.action = 'makeUnitPickupItemAtSlot'
        self.options = {
            'unit': unit.to_dict(),
            'item': item.to_dict(),
            'slotIndex': slotIndex.to_dict(),
        }


class DropItemInInventorySlot(Action):
    def __init__(self, unit, slotIndex: Number):
        self.action = 'dropItemInInventorySlot'
        self.options = {
            'unit': unit.to_dict(),
            'slotIndex': slotIndex.to_dict(),
        }


class UnbanPlayerFromChat(Action):
    def __init__(self, player):
        self.action = 'unbanPlayerFromChat'
        self.options = {
            'player': player.to_dict(),
        }


class ChangeDescriptionOfItem(Action):
    def __init__(self, item, string: String):
        self.action = 'changeDescriptionOfItem'
        self.options = {
            'item': item.to_dict(),
            'string': string.to_dict(),
        }


class SendChatMessageToPlayer(Action):
    def __init__(self, message: String, player):
        self.action = 'sendChatMessageToPlayer'
        self.options = {
            'message': message.to_dict(),
            'player': player.to_dict(),
        }


class PlayAdForEveryone(Action):
    def __init__(self):
        self.action = 'playAdForEveryone'
        self.options = {}


class HideUiTextForPlayer(Action):
    def __init__(self, target, entity):
        self.action = 'hideUiTextForPlayer'
        self.options = {
            'target': target.to_dict(),
            'entity': entity.to_dict(),
        }


class ShowUiTextForPlayer(Action):
    def __init__(self, target, entity):
        self.action = 'showUiTextForPlayer'
        self.options = {
            'target': target.to_dict(),
            'entity': entity.to_dict(),
        }


class ResetDebrisPosition(Action):
    def __init__(self, entity):
        self.action = 'resetDebrisPosition'
        self.options = {
            'entity': entity.to_dict(),
        }


class PlayMusic(Action):
    def __init__(self, music):
        self.action = 'playMusic'
        self.options = {
            'music': music.to_dict(),
        }


class AssignPlayerType(Action):
    def __init__(self, entity, playerType):
        self.action = 'assignPlayerType'
        self.options = {
            'entity': entity.to_dict(),
            'playerType': playerType.to_dict(),
        }


class PlayMusicForPlayer(Action):
    def __init__(self, music, player):
        self.action = 'playMusicForPlayer'
        self.options = {
            'music': music.to_dict(),
            'player': player.to_dict(),
        }


class MakeUnitVisibleToNeutralPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitVisibleToNeutralPlayers'
        self.options = {
            'entity': entity.to_dict(),
        }


class MakeUnitVisibleToFriendlyPlayers(Action):
    def __init__(self, entity):
        self.action = 'makeUnitVisibleToFriendlyPlayers'
        self.options = {
            'entity': entity.to_dict(),
        }


class MakeUnitPickupItem(Action):
    def __init__(self, unit, item):
        self.action = 'makeUnitPickupItem'
        self.options = {
            'unit': unit.to_dict(),
            'item': item.to_dict(),
        }


class GiveNewItemWithQuantityToUnit(Action):
    def __init__(self, itemType, number: Number, unit):
        self.action = 'giveNewItemWithQuantityToUnit'
        self.options = {
            'itemType': itemType.to_dict(),
            'number': number.to_dict(),
            'unit': unit.to_dict(),
        }


class DropAllItems(Action):
    def __init__(self, entity):
        self.action = 'dropAllItems'
        self.options = {
            'entity': entity.to_dict(),
        }


class UseItemOnce(Action):
    def __init__(self, item):
        self.action = 'useItemOnce'
        self.options = {
            'item': item.to_dict(),
        }


class StopAcceptingPlayers(Action):
    def __init__(self):
        self.action = 'stopAcceptingPlayers'
        self.options = {}


class SetEntityVelocityAtAngle(Action):
    def __init__(self, entity, speed: Number, angle: Number):
        self.action = 'setEntityVelocityAtAngle'
        self.options = {
            'entity': entity.to_dict(),
            'speed': speed.to_dict(),
            'angle': angle.to_dict(),
        }


class SetEntityAttributeMax(Action):
    def __init__(self, attribute, entity, value: Number):
        self.action = 'setEntityAttributeMax'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
            'value': value.to_dict(),
        }


class SetPlayerAttributeMin(Action):
    def __init__(self, attributeType, player, number: Number):
        self.action = 'setPlayerAttributeMin'
        self.options = {
            'attributeType': attributeType.to_dict(),
            'player': player.to_dict(),
            'number': number.to_dict(),
        }


class MakePlayerTradeWithPlayer(Action):
    def __init__(self, playerA, playerB):
        self.action = 'makePlayerTradeWithPlayer'
        self.options = {
            'playerA': playerA.to_dict(),
            'playerB': playerB.to_dict(),
        }


class UpdateUiTextForTimeForPlayer(Action):
    def __init__(self, target, value: String, player, time: Number):
        self.action = 'updateUiTextForTimeForPlayer'
        self.options = {
            'target': target.to_dict(),
            'value': value.to_dict(),
            'player': player.to_dict(),
            'time': time.to_dict(),
        }


class AiMoveToPosition(Action):
    def __init__(self, unit, position):
        self.action = 'aiMoveToPosition'
        self.options = {
            'unit': unit.to_dict(),
            'position': position.to_dict(),
        }


class AiAttackUnit(Action):
    def __init__(self, unit, targetUnit):
        self.action = 'aiAttackUnit'
        self.options = {
            'unit': unit.to_dict(),
            'targetUnit': targetUnit.to_dict(),
        }


class ChangeSensorRadius(Action):
    def __init__(self, sensor, radius: Number):
        self.action = 'changeSensorRadius'
        self.options = {
            'sensor': sensor.to_dict(),
            'radius': radius.to_dict(),
        }


class LoadPlayerDataAndApplyIt(Action):
    def __init__(self, player, unit):
        self.action = 'loadPlayerDataAndApplyIt'
        self.options = {
            'player': player.to_dict(),
            'unit': unit.to_dict(),
        }


class CreateFloatingText(Action):
    def __init__(self, text: String, position, color: String):
        self.action = 'createFloatingText'
        self.options = {
            'text': text.to_dict(),
            'position': position.to_dict(),
            'color': color.to_dict(),
        }


class SetLastAttackedUnit(Action):
    def __init__(self, unit):
        self.action = 'setLastAttackedUnit'
        self.options = {
            'unit': unit.to_dict(),
        }


class SetLastAttackingUnit(Action):
    def __init__(self, unit):
        self.action = 'setLastAttackingUnit'
        self.options = {
            'unit': unit.to_dict(),
        }


class SetItemFireRate(Action):
    def __init__(self, number: Number, item):
        self.action = 'setItemFireRate'
        self.options = {
            'number': number.to_dict(),
            'item': item.to_dict(),
        }


class ApplyImpulseOnEntityXY(Action):
    def __init__(self, impulse_x: Number, impulse_y: Number, entity):
        self.action = 'applyImpulseOnEntityXY'
        self.options = {
            'impulse.x': impulse_x.to_dict(),
            'impulse.y': impulse_y.to_dict(),
            'entity': entity.to_dict(),
        }


class PlaySoundForPlayer(Action):
    def __init__(self, sound, player):
        self.action = 'playSoundForPlayer'
        self.options = {
            'sound': sound.to_dict(),
            'player': player.to_dict(),
        }


class StopSoundForPlayer(Action):
    def __init__(self, sound, player):
        self.action = 'stopSoundForPlayer'
        self.options = {
            'sound': sound.to_dict(),
            'player': player.to_dict(),
        }


class ShowDismissibleInputModalToPlayer(Action):
    def __init__(self, player, inputLabel: String):
        self.action = 'showDismissibleInputModalToPlayer'
        self.options = {
            'player': player.to_dict(),
            'inputLabel': inputLabel.to_dict(),
        }


class SetItemName(Action):
    def __init__(self, name: String, item):
        self.action = 'setItemName'
        self.options = {
            'name': name.to_dict(),
            'item': item.to_dict(),
        }


class ChangeItemInventoryImage(Action):
    def __init__(self, url: String, item):
        self.action = 'changeItemInventoryImage'
        self.options = {
            'url': url.to_dict(),
            'item': item.to_dict(),
        }


class AddAttributeBuffToUnit(Action):
    def __init__(self, entity, value: Number, attribute, time: Number):
        self.action = 'addAttributeBuffToUnit'
        self.options = {
            'entity': entity.to_dict(),
            'value': value.to_dict(),
            'attribute': attribute.to_dict(),
            'time': time.to_dict(),
        }


class AddPercentageAttributeBuffToUnit(Action):
    def __init__(self, entity, value: Number, attribute, time: Number):
        self.action = 'addPercentageAttributeBuffToUnit'
        self.options = {
            'entity': entity.to_dict(),
            'value': value.to_dict(),
            'attribute': attribute.to_dict(),
            'time': time.to_dict(),
        }


class StunUnit(Action):
    def __init__(self, unit):
        self.action = 'stunUnit'
        self.options = {
            'unit': unit.to_dict(),
        }


class RemoveStunFromUnit(Action):
    def __init__(self, unit):
        self.action = 'removeStunFromUnit'
        self.options = {
            'unit': unit.to_dict(),
        }


class SetLastAttackingItem(Action):
    def __init__(self, item):
        self.action = 'setLastAttackingItem'
        self.options = {
            'item': item.to_dict(),
        }


class MutePlayerMicrophone(Action):
    def __init__(self, player):
        self.action = 'mutePlayerMicrophone'
        self.options = {
            'player': player.to_dict(),
        }


class UnmutePlayerMicrophone(Action):
    def __init__(self, player):
        self.action = 'unmutePlayerMicrophone'
        self.options = {
            'player': player.to_dict(),
        }


class SendPostRequest(Action):
    def __init__(self, string: String, url: String, varName):
        self.action = 'sendPostRequest'
        self.options = {
            'string': string.to_dict(),
            'url': url.to_dict(),
            'varName': varName.to_dict(),
        }


class LoadUnitDataFromString(Action):
    def __init__(self, string: String, unit):
        self.action = 'loadUnitDataFromString'
        self.options = {
            'string': string.to_dict(),
            'unit': unit.to_dict(),
        }


class LoadPlayerDataFromString(Action):
    def __init__(self, string: String, player):
        self.action = 'loadPlayerDataFromString'
        self.options = {
            'string': string.to_dict(),
            'player': player.to_dict(),
        }


class RemoveAllAttributeBuffs(Action):
    def __init__(self, unit):
        self.action = 'removeAllAttributeBuffs'
        self.options = {
            'unit': unit.to_dict(),
        }


class ChangeInventorySlotColor(Action):
    def __init__(self, item, string: String):
        self.action = 'changeInventorySlotColor'
        self.options = {
            'item': item.to_dict(),
            'string': string.to_dict(),
        }


class SetOwnerUnitOfProjectile(Action):
    def __init__(self, unit, projectile):
        self.action = 'setOwnerUnitOfProjectile'
        self.options = {
            'unit': unit.to_dict(),
            'projectile': projectile.to_dict(),
        }


class EnableAI(Action):
    def __init__(self, unit):
        self.action = 'enableAI'
        self.options = {
            'unit': unit.to_dict(),
        }


class DisableAI(Action):
    def __init__(self, unit):
        self.action = 'disableAI'
        self.options = {
            'unit': unit.to_dict(),
        }


class AiGoIdle(Action):
    def __init__(self, unit):
        self.action = 'aiGoIdle'
        self.options = {
            'unit': unit.to_dict(),
        }
