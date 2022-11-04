from .script import Base


class Function(Base):
    def __init__(self):
        self.function = None
        self.options = {}

    def to_dict(self):
        # check for direct values
        if type(self.function) is dict and self.function.get('direct'):
            return self.function.get('value')

        data = {
            'function': self.function
        }
        data.update(self.options) if self.options is not None else None
        return data


# ---------------------------------------------------------------------------- #
#                                    Entitys                                   #
# ---------------------------------------------------------------------------- #


class Entity(Function):
    pass


class SelectedEntity(Entity):
    def __init__(self):
        self.function = 'getSelectedEntity'
        self.options = {}


class ThisEntity(Entity):
    def __init__(self):
        self.function = 'thisEntity'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Player                                    #
# ---------------------------------------------------------------------------- #


class Player(Entity):
    pass


class LastPlayerSelectingDialogueOption(Player):
    def __init__(self):
        self.function = 'getLastPlayerSelectingDialogueOption'
        self.options = {}


class LastTriggeringPlayer(Player):
    def __init__(self):
        self.function = 'getTriggeringPlayer'
        self.options = {}


class OwnerOfEntity(Player):
    def __init__(self, entity):
        self.function = 'getOwner'
        self.options = {
            'entity': entity.to_dict(),
        }


class SelectedPlayer(Player):
    def __init__(self):
        self.function = 'selectedPlayer'
        self.options = {}


class PlayerFromId(Player):
    def __init__(self, string):
        self.function = 'getPlayerFromId'
        self.options = {
            'string': string.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                     Units                                    #
# ---------------------------------------------------------------------------- #


class Unit(Entity):
    pass


class LastPurchasedUnit(Unit):
    def __init__(self):
        self.function = 'getLastPurchasedUnit'
        self.options = {}


class LastOverlappingUnit(Unit):
    def __init__(self):
        self.function = 'getLastOverlappingUnit'
        self.options = {}


class LastOverlappedUnit(Unit):
    def __init__(self):
        self.function = 'getLastOverlappedUnit'
        self.options = {}


class LastTouchingUnit(Unit):
    def __init__(self):
        self.function = 'getLastTouchingUnit'
        self.options = {}


class SourceUnitOfProjectile(Unit):
    def __init__(self, entity):
        self.function = 'getSourceUnitOfProjectile'
        self.options = {
            'entity': entity.to_dict(),
        }


class LastCastingUnit(Unit):
    def __init__(self):
        self.function = 'getLastCastingUnit'
        self.options = {}


class LastTouchedUnit(Unit):
    def __init__(self):
        self.function = 'getLastTouchedUnit'
        self.options = {}


class LastCreatedUnit(Unit):
    def __init__(self):
        self.function = 'getLastCreatedUnit'
        self.options = {}


class OwnerOfItem(Unit):
    def __init__(self, entity):
        self.function = 'getOwnerOfItem'
        self.options = {
            'entity': entity.to_dict(),
        }


class LastTriggeringUnit(Unit):
    def __init__(self):
        self.function = 'getTriggeringUnit'
        self.options = {}


class SelectedUnit(Unit):
    def __init__(self):
        self.function = 'selectedUnit'
        self.options = {}


class LastAttackedUnit(Unit):
    def __init__(self):
        self.function = 'getLastAttackedUnit'
        self.options = {}


class LastAttackingUnit(Unit):
    def __init__(self):
        self.function = 'getLastAttackingUnit'
        self.options = {}


class OwnerUnitOfSensor(Unit):
    def __init__(self, sensor):
        self.function = 'ownerUnitOfSensor'
        self.options = {
            'sensor': sensor.to_dict(),
        }


class UnitFromId(Unit):
    def __init__(self, string):
        self.function = 'getUnitFromId'
        self.options = {
            'string': string.to_dict(),
        }


class TargetUnit(Unit):
    def __init__(self, unit):
        self.function = 'targetUnit'
        self.options = {
            'unit': unit.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                     Items                                    #
# ---------------------------------------------------------------------------- #


class Item(Entity):
    pass


class ItemInFrontOfUnit(Item):
    def __init__(self, entity):
        self.function = 'getItemInFrontOfUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class ItemAtSlot(Item):
    def __init__(self, slot, unit):
        self.function = 'getItemAtSlot'
        self.options = {
            'slot': slot.to_dict(),
            'unit': unit.to_dict(),
        }


class SelectedItem(Item):
    def __init__(self):
        self.function = 'selectedItem'
        self.options = {}


class TriggeringItem(Item):
    def __init__(self):
        self.function = 'getTriggeringItem'
        self.options = {}


class ItemCurrentlyHeldByUnit(Item):
    def __init__(self, entity):
        self.function = 'getItemCurrentlyHeldByUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class LastUsedItem(Item):
    def __init__(self):
        self.function = 'lastUsedItem'
        self.options = {}


class SourceItemOfProjectile(Item):
    def __init__(self, entity):
        self.function = 'getSourceItemOfProjectile'
        self.options = {
            'entity': entity.to_dict(),
        }


class LastCreatedItem(Item):
    def __init__(self):
        self.function = 'getLastCreatedItem'
        self.options = {}


class LastOverlappingItem(Item):
    def __init__(self):
        self.function = 'getLastOverlappingItem'
        self.options = {}


class ItemInInventorySlot(Item):
    def __init__(self, slot, entity):
        self.function = 'getItemInInventorySlot'
        self.options = {
            'slot': slot.to_dict(),
            'entity': entity.to_dict(),
        }


class LastTouchedItem(Item):
    def __init__(self):
        self.function = 'getLastTouchedItem'
        self.options = {}


class LastAttackingItem(Item):
    def __init__(self):
        self.function = 'getLastAttackingItem'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                  Projectiles                                 #
# ---------------------------------------------------------------------------- #


class Projectile(Entity):
    pass


class SelectedProjectile(Projectile):
    def __init__(self):
        self.function = 'selectedProjectile'
        self.options = {}


class LastCreatedProjectile(Projectile):
    def __init__(self):
        self.function = 'getLastCreatedProjectile'
        self.options = {}


class LastTriggeringProjectile(Projectile):
    def __init__(self):
        self.function = 'getTriggeringProjectile'
        self.options = {}


class LastTouchedProjectile(Projectile):
    def __init__(self):
        self.function = 'getLastTouchedProjectile'
        self.options = {}


class LastOverlappingProjectile(Projectile):
    def __init__(self):
        self.function = 'getLastOverlappingProjectile'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Debris                                    #
# ---------------------------------------------------------------------------- #


class Debris(Entity):
    pass


class SelectedDebris(Debris):
    def __init__(self):
        self.function = 'selectedDebris'
        self.options = {}


class LastTriggeringDebris(Debris):
    def __init__(self):
        self.function = 'getTriggeringDebris'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                   Positions                                  #
# ---------------------------------------------------------------------------- #


class Position(Function):
    pass


class XyCoordinate(Position):
    def __init__(self, x, y):
        self.function = 'xyCoordinate'
        self.options = {
            'x': x.to_dict(),
            'y': y.to_dict(),
        }


class MouseCursorPosition(Position):
    def __init__(self, player):
        self.function = 'getMouseCursorPosition'
        self.options = {
            'player': player.to_dict(),
        }


class CenterOfRegion(Position):
    def __init__(self, region):
        self.function = 'centerOfRegion'
        self.options = {
            'region': region.to_dict(),
        }


class EntityLastRaycastCollisionPosition(Position):
    def __init__(self, entity):
        self.function = 'entityLastRaycastCollisionPosition'
        self.options = {
            'entity': entity.to_dict(),
        }


class EntityPosition(Position):
    def __init__(self, entity):
        self.function = 'getEntityPosition'
        self.options = {
            'entity': entity.to_dict(),
        }


class RandomPositionInRegion(Position):
    def __init__(self, region):
        self.function = 'getRandomPositionInRegion'
        self.options = {
            'region': region.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                    Regions                                   #
# ---------------------------------------------------------------------------- #


class Region(Function):
    pass


class LastTriggeringRegion(Region):
    def __init__(self):
        self.function = 'getTriggeringRegion'
        self.options = {}


class EntireMapRegion(Region):
    def __init__(self):
        self.function = 'getEntireMapRegion'
        self.options = {}


class SelectedRegion(Region):
    def __init__(self):
        self.function = 'selectedRegion'
        self.options = {}


class EntityBounds(Region):
    def __init__(self, entity):
        self.function = 'entityBounds'
        self.options = {
            'entity': entity.to_dict(),
        }


class DynamicRegion(Region):
    def __init__(self, x, y, width, height):
        self.function = 'dynamicRegion'
        self.options = {
            'x': x.to_dict(),
            'y': y.to_dict(),
            'width': width.to_dict(),
            'height': height.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                  Attributes                                  #
# ---------------------------------------------------------------------------- #


class Attribute(Function):
    pass


class TriggeringAttribute(Attribute):
    def __init__(self):
        self.function = 'getTriggeringAttribute'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Sensor                                    #
# ---------------------------------------------------------------------------- #


class Sensor(Function):
    pass


class SensorOfUnit(Sensor):
    def __init__(self, unit):
        self.function = 'getSensorOfUnit'
        self.options = {
            'unit': unit.to_dict(),
        }


class TriggeringSensor(Sensor):
    def __init__(self):
        self.function = 'getTriggeringSensor'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    States                                    #
# ---------------------------------------------------------------------------- #


class State(Function):
    def __init__(self, state_id):
        self.function = {
            'direct': True,
            'value': state_id,
        }


class EntityState(State):
    def __init__(self, entity):
        self.function = 'getEntityState'
        self.options = {
            'entity': entity.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                    Numbers                                   #
# ---------------------------------------------------------------------------- #


class Number(Function):
    def __init__(self, number):
        self.function = {
            'direct': True,
            'value': number,
        }


class RandomNumberBetween(Number):
    def __init__(self, min, max):
        self.function = 'getRandomNumberBetween'
        self.options = {
            'min': min.to_dict(),
            'max': max.to_dict(),
        }


class UnitsFacingAngle(Number):
    def __init__(self, unit):
        self.function = 'unitsFacingAngle'
        self.options = {
            'unit': unit.to_dict(),
        }


class MapHeight(Number):
    def __init__(self):
        self.function = 'getMapHeight'
        self.options = {}


class ToFixed(Number):
    def __init__(self, value, precision):
        self.function = 'toFixed'
        self.options = {
            'value': value.to_dict(),
            'precision': precision.to_dict(),
        }


class ItemQuantity(Number):
    def __init__(self, item):
        self.function = 'getItemQuantity'
        self.options = {
            'item': item.to_dict(),
        }


class Cos(Number):
    def __init__(self, angle):
        self.function = 'cos'
        self.options = {
            'angle': angle.to_dict(),
        }


class EntityHeight(Number):
    def __init__(self, entity):
        self.function = 'entityHeight'
        self.options = {
            'entity': entity.to_dict(),
        }


class PlayerAttributeMax(Number):
    def __init__(self, attribute, entity):
        self.function = 'playerAttributeMax'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
        }


class PlayerAttribute(Number):
    def __init__(self, attribute, entity):
        self.function = 'getPlayerAttribute'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
        }


class MapWidth(Number):
    def __init__(self):
        self.function = 'getMapWidth'
        self.options = {}


class EntityWidth(Number):
    def __init__(self, entity):
        self.function = 'entityWidth'
        self.options = {
            'entity': entity.to_dict(),
        }


class PlayerCount(Number):
    def __init__(self):
        self.function = 'getPlayerCount'
        self.options = {}


class Arctan(Number):
    def __init__(self, number):
        self.function = 'arctan'
        self.options = {
            'number': number.to_dict(),
        }


class MathFloor(Number):
    def __init__(self, value):
        self.function = 'mathFloor'
        self.options = {
            'value': value.to_dict(),
        }


class YCoordinateOfRegion(Number):
    def __init__(self, region):
        self.function = 'getYCoordinateOfRegion'
        self.options = {
            'region': region.to_dict(),
        }


class SquareRoot(Number):
    def __init__(self, number):
        self.function = 'squareRoot'
        self.options = {
            'number': number.to_dict(),
        }


class UnitCount(Number):
    def __init__(self):
        self.function = 'getUnitCount'
        self.options = {}


class AngleBetweenPositions(Number):
    def __init__(self, position_a, position_b):
        self.function = 'angleBetweenPositions'
        self.options = {
            'positionA': position_a.to_dict(),
            'positionB': position_b.to_dict(),
        }


class WidthOfRegion(Number):
    def __init__(self, region):
        self.function = 'getWidthOfRegion'
        self.options = {
            'region': region.to_dict(),
        }


class EntityAttributeMin(Number):
    def __init__(self, attribute, entity):
        self.function = 'entityAttributeMin'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
        }


class StringToNumber(Number):
    def __init__(self, value):
        self.function = 'stringToNumber'
        self.options = {
            'value': value.to_dict(),
        }


class QuantityOfUnitTypeInUnitTypeGroup(Number):
    def __init__(self, unit_type, unit_type_group):
        self.function = 'getQuantityOfUnitTypeInUnitTypeGroup'
        self.options = {
            'unitType': unit_type.to_dict(),
            'unitTypeGroup': unit_type_group.to_dict(),
        }


class PositionY(Number):
    def __init__(self, position):
        self.function = 'getPositionY'
        self.options = {
            'position': position.to_dict(),
        }


class DistanceBetweenPositions(Number):
    def __init__(self, position_a, position_b):
        self.function = 'distanceBetweenPositions'
        self.options = {
            'positionA': position_a.to_dict(),
            'positionB': position_b.to_dict(),
        }


class EntityAttributeMax(Number):
    def __init__(self, attribute, entity):
        self.function = 'entityAttributeMax'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
        }


class PlayerAttributeMin(Number):
    def __init__(self, attribute, entity):
        self.function = 'playerAttributeMin'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
        }


class Sin(Number):
    def __init__(self, angle):
        self.function = 'sin'
        self.options = {
            'angle': angle.to_dict(),
        }


class XCoordinateOfRegion(Number):
    def __init__(self, region):
        self.function = 'getXCoordinateOfRegion'
        self.options = {
            'region': region.to_dict(),
        }


class EntityVelocityY(Number):
    def __init__(self, entity):
        self.function = 'getEntityVelocityY'
        self.options = {
            'entity': entity.to_dict(),
        }


class PositionX(Number):
    def __init__(self, position):
        self.function = 'getPositionX'
        self.options = {
            'position': position.to_dict(),
        }


class LastPlayedTimeOfPlayer(Number):
    def __init__(self, player):
        self.function = 'lastPlayedTimeOfPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class Max(Number):
    def __init__(self, num_a, num_b):
        self.function = 'getMax'
        self.options = {
            'num1': num_a.to_dict(),
            'num2': num_b.to_dict(),
        }


class RotateSpeed(Number):
    def __init__(self, unit_type):
        self.function = 'getRotateSpeed'
        self.options = {
            'unitType': unit_type.to_dict(),
        }


class CurrentAmmoOfItem(Number):
    def __init__(self, item):
        self.function = 'getCurrentAmmoOfItem'
        self.options = {
            'item': item.to_dict(),
        }


class HeightOfRegion(Number):
    def __init__(self, region):
        self.function = 'getHeightOfRegion'
        self.options = {
            'region': region.to_dict(),
        }


class ItemMaxQuantity(Number):
    def __init__(self, item):
        self.function = 'getItemMaxQuantity'
        self.options = {
            'item': item.to_dict(),
        }


class AbsoluteValueOfNumber(Number):
    def __init__(self, number):
        self.function = 'absoluteValueOfNumber'
        self.options = {
            'number': number.to_dict(),
        }


class EntityAttribute(Number):
    def __init__(self, attribute, entity):
        self.function = 'getEntityAttribute'
        self.options = {
            'attribute': attribute.to_dict(),
            'entity': entity.to_dict(),
        }


class CurrentTimeStamp(Number):
    def __init__(self):
        self.function = 'currentTimeStamp'
        self.options = {}


class EntityVelocityX(Number):
    def __init__(self, entity):
        self.function = 'getEntityVelocityX'
        self.options = {
            'entity': entity.to_dict(),
        }


class DefaultQuantityOfItemType(Number):
    def __init__(self, item_type):
        self.function = 'defaultQuantityOfItemType'
        self.options = {
            'itemType': item_type.to_dict(),
        }


class QuantityOfItemTypeInItemTypeGroup(Number):
    def __init__(self, item_type, item_type_group):
        self.function = 'getQuantityOfItemTypeInItemTypeGroup'
        self.options = {
            'itemType': item_type.to_dict(),
            'itemTypeGroup': item_type_group.to_dict(),
        }


class NumberOfItemsPresent(Number):
    def __init__(self):
        self.function = 'getNumberOfItemsPresent'
        self.options = {}


class Min(Number):
    def __init__(self, num_a, num_b):
        self.function = 'getMin'
        self.options = {
            'num1': num_a.to_dict(),
            'num2': num_b.to_dict(),
        }


class MaxValueOfItemType(Number):
    def __init__(self, item_type):
        self.function = 'maxValueOfItemType'
        self.options = {
            'itemType': item_type.to_dict(),
        }


class AngleBetweenMouseAndWindowCenter(Number):
    def __init__(self, player):
        self.function = 'angleBetweenMouseAndWindowCenter'
        self.options = {
            'player': player.to_dict(),
        }


class Exponent(Number):
    def __init__(self, base, power):
        self.function = 'getExponent'
        self.options = {
            'base': base.to_dict(),
            'power': power.to_dict(),
        }


class NumberOfUnitsOfUnitType(Number):
    def __init__(self, unit_type):
        self.function = 'getNumberOfUnitsOfUnitType'
        self.options = {
            'unitType': unit_type.to_dict(),
        }


class NumberOfPlayersOfPlayerType(Number):
    def __init__(self, player_type):
        self.function = 'getNumberOfPlayersOfPlayerType'
        self.options = {
            'playerType': player_type.to_dict(),
        }


class LengthOfString(Number):
    def __init__(self, string):
        self.function = 'getLengthOfString'
        self.options = {
            'string': string.to_dict(),
        }


class StringArrayLength(Number):
    def __init__(self, string):
        self.function = 'getStringArrayLength'
        self.options = {
            'string': string.to_dict(),
        }


class SelectedInventorySlot(Number):
    def __init__(self, unit):
        self.function = 'selectedInventorySlot'
        self.options = {
            'unit': unit.to_dict(),
        }


class LogBase10(Number):
    def __init__(self, value):
        self.function = 'log10'
        self.options = {
            'value': value.to_dict(),
        }


class UnitSensorRadius(Number):
    def __init__(self, unit):
        self.function = 'unitSensorRadius'
        self.options = {
            'unit': unit.to_dict(),
        }


class Calculate(Number):
    def __init__(self, item_a: Number, operator: str, item_b: Number):
        self.function = 'calculate'
        self.options = {
            'items': [
                {
                    'operator': operator
                },
                item_a.to_dict(),
                item_b.to_dict(),
            ]
        }


# ---------------------------------------------------------------------------- #
#                                    Strings                                   #
# ---------------------------------------------------------------------------- #


class String(Function):
    def __init__(self, string):
        self.function = {
            'direct': True,
            'value': string,
        }


class EntityType(String):
    def __init__(self, entity):
        self.function = 'getEntityType'
        self.options = {
            'entity': entity.to_dict(),
        }


class PlayerCustomInput(String):
    def __init__(self, player):
        self.function = 'playerCustomInput'
        self.options = {
            'player': player.to_dict(),
        }


class Concat(String):
    def __init__(self, text_a, text_b):
        self.function = 'concat'
        self.options = {
            'textA': text_a.to_dict(),
            'textB': text_b.to_dict(),
        }


class PlayerName(String):
    def __init__(self, entity):
        self.function = 'getPlayerName'
        self.options = {
            'entity': entity.to_dict(),
        }


class UnitTypeName(String):
    def __init__(self, unit_type):
        self.function = 'getUnitTypeName'
        self.options = {
            'unitType': unit_type.to_dict(),
        }


class NameOfRegion(String):
    def __init__(self, region):
        self.function = 'nameOfRegion'
        self.options = {
            'region': region.to_dict(),
        }


class ItemTypeName(String):
    def __init__(self, item_type):
        self.function = 'getItemTypeName'
        self.options = {
            'itemType': item_type.to_dict(),
        }


class SubstringOf(String):
    def __init__(self, string, from_index, to_index):
        self.function = 'substringOf'
        self.options = {
            'string': string.to_dict(),
            'fromIndex': from_index.to_dict(),
            'toIndex': to_index.to_dict(),
        }


class LastChatMessageSentByPlayer(String):
    def __init__(self, player):
        self.function = 'getLastChatMessageSentByPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class ToLowerCase(String):
    def __init__(self, string):
        self.function = 'toLowerCase'
        self.options = {
            'string': string.to_dict(),
        }


class ReplaceValuesInString(String):
    def __init__(self, match_string, source_string, new_string):
        self.function = 'replaceValuesInString'
        self.options = {
            'matchString': match_string.to_dict(),
            'sourceString': source_string.to_dict(),
            'newString': new_string.to_dict(),
        }


class TimeString(String):
    def __init__(self, seconds):
        self.function = 'getTimeString'
        self.options = {
            'seconds': seconds.to_dict(),
        }


class ItemDescription(String):
    def __init__(self, item):
        self.function = 'getItemDescription'
        self.options = {
            'item': item.to_dict(),
        }


class UnitData(String):
    def __init__(self, unit):
        self.function = 'getUnitData'
        self.options = {
            'unit': unit.to_dict(),
        }


class PlayerData(String):
    def __init__(self, player):
        self.function = 'getPlayerData'
        self.options = {
            'player': player.to_dict(),
        }


class UnitId(String):
    def __init__(self, unit):
        self.function = 'getUnitId'
        self.options = {
            'unit': unit.to_dict(),
        }


class PlayerId(String):
    def __init__(self, player):
        self.function = 'getPlayerId'
        self.options = {
            'player': player.to_dict(),
        }


class StringArrayElement(String):
    def __init__(self, number, string):
        self.function = 'getStringArrayElement'
        self.options = {
            'number': number.to_dict(),
            'string': string.to_dict(),
        }


class InsertStringArrayElement(String):
    def __init__(self, value, string):
        self.function = 'insertStringArrayElement'
        self.options = {
            'value': value.to_dict(),
            'string': string.to_dict(),
        }


class UpdateStringArrayElement(String):
    def __init__(self, number, string, value):
        self.function = 'updateStringArrayElement'
        self.options = {
            'number': number.to_dict(),
            'string': string.to_dict(),
            'value': value.to_dict(),
        }


class RemoveStringArrayElement(String):
    def __init__(self, number, string):
        self.function = 'removeStringArrayElement'
        self.options = {
            'number': number.to_dict(),
            'string': string.to_dict(),
        }


class EntityName(String):
    def __init__(self, entity):
        self.function = 'entityName'
        self.options = {
            'entity': entity.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                   Booleans                                   #
# ---------------------------------------------------------------------------- #


class Boolean(Function):
    def __init__(self, boolean):
        self.function = {
            'direct': True,
            'value': boolean,
        }


class IsPlayerLoggedIn(Boolean):
    def __init__(self, player):
        self.function = 'isPlayerLoggedIn'
        self.options = {
            'player': player.to_dict(),
        }


class PlayersAreFriendly(Boolean):
    def __init__(self, player_a, player_b):
        self.function = 'playersAreFriendly'
        self.options = {
            'playerA': player_a.to_dict(),
            'playerB': player_b.to_dict(),
        }


class PlayerIsControlledByHuman(Boolean):
    def __init__(self, player):
        self.function = 'playerIsControlledByHuman'
        self.options = {
            'player': player.to_dict(),
        }


class PlayersAreHostile(Boolean):
    def __init__(self, player_a, player_b):
        self.function = 'playersAreHostile'
        self.options = {
            'playerA': player_a.to_dict(),
            'playerB': player_b.to_dict(),
        }


class RegionOverlapsWithRegion(Boolean):
    def __init__(self, region_a, region_b):
        self.function = 'regionOverlapsWithRegion'
        self.options = {
            'regionA': region_a.to_dict(),
            'regionB': region_b.to_dict(),
        }


class PlayersAreNeutral(Boolean):
    def __init__(self, player_a, player_b):
        self.function = 'playersAreNeutral'
        self.options = {
            'playerA': player_a.to_dict(),
            'playerB': player_b.to_dict(),
        }


class PlayerHasAdblockEnabled(Boolean):
    def __init__(self, player):
        self.function = 'playerHasAdblockEnabled'
        self.options = {
            'player': player.to_dict(),
        }


class EntityExists(Boolean):
    def __init__(self, entity):
        self.function = 'entityExists'
        self.options = {
            'entity': entity.to_dict(),
        }


class IsPositionInWall(Boolean):
    def __init__(self, positionx, positiony):
        self.function = 'isPositionInWall'
        self.options = {
            'position.x': positionx.to_dict(),
            'position.y': positiony.to_dict(),
        }


class SubString(Boolean):
    def __init__(self, source_string, pattern_string):
        self.function = 'subString'
        self.options = {
            'sourceString': source_string.to_dict(),
            'patternString': pattern_string.to_dict(),
        }


class StringStartsWith(Boolean):
    def __init__(self, source_string, pattern_string):
        self.function = 'stringStartsWith'
        self.options = {
            'sourceString': source_string.to_dict(),
            'patternString': pattern_string.to_dict(),
        }


class StringEndsWith(Boolean):
    def __init__(self, source_string, pattern_string):
        self.function = 'stringEndsWith'
        self.options = {
            'sourceString': source_string.to_dict(),
            'patternString': pattern_string.to_dict(),
        }


class IsAIEnabled(Boolean):
    def __init__(self, unit):
        self.function = 'isAIEnabled'
        self.options = {
            'unit': unit.to_dict(),
        }


class IsBotPlayer(Boolean):
    def __init__(self, player):
        self.function = 'isBotPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class IsComputerPlayer(Boolean):
    def __init__(self, player_is_a_computer):
        self.function = 'isComputerPlayer'
        self.options = {
            'player is a computer': player_is_a_computer.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                   Particles                                  #
# ---------------------------------------------------------------------------- #


class Particle(Function):
    pass


class ItemParticle(Particle):
    def __init__(self, particle_type, entity):
        self.function = 'getItemParticle'
        self.options = {
            'particleType': particle_type.to_dict(),
            'entity': entity.to_dict(),
        }


class SelectedParticle(Particle):
    def __init__(self):
        self.function = 'selectedParticle'
        self.options = {}


class UnitParticle(Particle):
    def __init__(self, particle_type, entity):
        self.function = 'getUnitParticle'
        self.options = {
            'particleType': particle_type.to_dict(),
            'entity': entity.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                   Variables                                  #
# ---------------------------------------------------------------------------- #


class Variable(Function):
    def __init__(self, variable_name, variable_type=None):
        self.function = 'getVariable'
        self.name = variable_name
        self.type = variable_type
        self.options = {
            'variableName': variable_name
        }


# ---------------------------------------------------------------------------- #
#                                  Unit Types                                  #
# ---------------------------------------------------------------------------- #


class UnitType(Function):
    def __init__(self, unit_type_id):
        self.function = {
            'direct': True,
            'value': unit_type_id,
        }


class UnitTypeOfUnit(UnitType):
    def __init__(self, entity):
        self.function = 'getUnitTypeOfUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class LastPurchasedUnitTypetId(UnitType):
    def __init__(self):
        self.function = 'lastPurchasedUnitTypetId'
        self.options = {}


class RandomUnitTypeFromUnitTypeGroup(UnitType):
    def __init__(self, unit_type_group):
        self.function = 'getRandomUnitTypeFromUnitTypeGroup'
        self.options = {
            'unitTypeGroup': unit_type_group.to_dict(),
        }


class SelectedUnitType(UnitType):
    def __init__(self):
        self.function = 'selectedUnitType'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                 Player Types                                 #
# ---------------------------------------------------------------------------- #


class PlayerType(Function):
    def __init__(self, player_type_id):
        self.function = {
            'direct': True,
            'value': player_type_id,
        }


class PlayerTypeOfPlayer(PlayerType):
    def __init__(self, player):
        self.function = 'playerTypeOfPlayer'
        self.options = {
            'player': player.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                  Item Types                                  #
# ---------------------------------------------------------------------------- #


class ItemType(Function):
    def __init__(self, item_type_id):
        self.function = {
            'direct': True,
            'value': item_type_id,
        }


class SelectedItemType(ItemType):
    def __init__(self):
        self.function = 'selectedItemType'
        self.options = {}


class ItemTypeOfItem(ItemType):
    def __init__(self, entity):
        self.function = 'getItemTypeOfItem'
        self.options = {
            'entity': entity.to_dict(),
        }


class RandomItemTypeFromItemTypeGroup(ItemType):
    def __init__(self, item_type_group):
        self.function = 'getRandomItemTypeFromItemTypeGroup'
        self.options = {
            'itemTypeGroup': item_type_group.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                               Projectile Types                               #
# ---------------------------------------------------------------------------- #


class ProjectileType(Function):
    def __init__(self, projectile_type_id):
        self.function = {
            'direct': True,
            'value': projectile_type_id,
        }


class ProjectileTypeOfProjectile(ProjectileType):
    def __init__(self, entity):
        self.function = 'getProjectileTypeOfProjectile'
        self.options = {
            'entity': entity.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                Attribute Types                               #
# ---------------------------------------------------------------------------- #


class AttributeType(Function):
    def __init__(self, attribute_type_id):
        self.function = {
            'direct': True,
            'value': attribute_type_id,
        }


class AttributeTypeOfAttribute(AttributeType):
    def __init__(self, entity):
        self.function = 'getAttributeTypeOfAttribute'
        self.options = {
            'entity': entity.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                    Groups                                    #
# ---------------------------------------------------------------------------- #


class Group(Function):
    pass


# ---------------------------------------------------------------------------- #
#                                 Entity Groups                                #
# ---------------------------------------------------------------------------- #


class EntityGroup(Group):
    pass


class EntitiesCollidingWithLastRaycast(EntityGroup):
    def __init__(self):
        self.function = 'entitiesCollidingWithLastRaycast'
        self.options = {}


class AllEntities(EntityGroup):
    def __init__(self):
        self.function = 'allEntities'
        self.options = {}


class EntitiesInRegion(EntityGroup):
    def __init__(self, region):
        self.function = 'entitiesInRegion'
        self.options = {
            'region': region.to_dict(),
        }


class EntitiesInRegionInFrontOfEntityAtDistance(EntityGroup):
    def __init__(self, width: Number, height: Number, entity, distance: Number):
        self.function = 'entitiesInRegionInFrontOfEntityAtDistance'
        self.options = {
            'width': width.to_dict(),
            'height': height.to_dict(),
            'entity': entity.to_dict(),
            'distance': distance.to_dict(),
        }


class EntitiesBetweenTwoPositions(EntityGroup):
    def __init__(self, position_a, position_b):
        self.function = 'entitiesBetweenTwoPositions'
        self.options = {
            'positionA': position_a.to_dict(),
            'positionB': position_b.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                  Unit Groups                                 #
# ---------------------------------------------------------------------------- #


class UnitGroup(Group):
    pass


class AllUnitsOwnedByPlayer(UnitGroup):
    def __init__(self, player):
        self.function = 'allUnitsOwnedByPlayer'
        self.options = {
            'player': player.to_dict(),
        }


class AllUnitsAttachedToUnit(UnitGroup):
    def __init__(self, entity):
        self.function = 'allUnitsAttachedToUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class AllUnits(UnitGroup):
    def __init__(self):
        self.function = 'allUnits'
        self.options = {}


class AllUnitsAttachedToItem(UnitGroup):
    def __init__(self, entity):
        self.function = 'allUnitsAttachedToItem'
        self.options = {
            'entity': entity.to_dict(),
        }


class AllUnitsMountedOnUnit(UnitGroup):
    def __init__(self, entity):
        self.function = 'allUnitsMountedOnUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class AllUnitsInRegion(UnitGroup):
    def __init__(self, region):
        self.function = 'allUnitsInRegion'
        self.options = {
            'region': region.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                               Projectile Groups                              #
# ---------------------------------------------------------------------------- #


class ProjectileGroup(Group):
    pass


class AllProjectilesAttachedToUnit(ProjectileGroup):
    def __init__(self, entity):
        self.function = 'allProjectilesAttachedToUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class AllProjectiles(ProjectileGroup):
    def __init__(self):
        self.function = 'allProjectiles'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                  Item Groups                                 #
# ---------------------------------------------------------------------------- #


class ItemGroup(Group):
    pass


class AllItemsDroppedOnGround(ItemGroup):
    def __init__(self):
        self.function = 'allItemsDroppedOnGround'
        self.options = {}


class AllItems(ItemGroup):
    def __init__(self):
        self.function = 'allItems'
        self.options = {}


class AllItemsAttachedToUnit(ItemGroup):
    def __init__(self, entity):
        self.function = 'allItemsAttachedToUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


class AllItemsOwnedByUnit(ItemGroup):
    def __init__(self, entity):
        self.function = 'allItemsOwnedByUnit'
        self.options = {
            'entity': entity.to_dict(),
        }


# ---------------------------------------------------------------------------- #
#                                 Player Groups                                #
# ---------------------------------------------------------------------------- #


class PlayerGroup(Group):
    pass


class AllHumanPlayers(PlayerGroup):
    def __init__(self):
        self.function = 'humanPlayers'
        self.options = {}


class AllComputerPlayers(PlayerGroup):
    def __init__(self):
        self.function = 'computerPlayers'
        self.options = {}


class AllPlayers(PlayerGroup):
    def __init__(self):
        self.function = 'allPlayers'
        self.options = {}


class AllBotPlayers(PlayerGroup):
    def __init__(self):
        self.function = 'botPlayers'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                               Item Type Groups                               #
# ---------------------------------------------------------------------------- #


class ItemTypeGroup(Group):
    pass


class AllItemTypesInGame(ItemTypeGroup):
    def __init__(self):
        self.function = 'allItemTypesInGame'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                               Unit Type Groups                               #
# ---------------------------------------------------------------------------- #


class UnitTypeGroup(Group):
    pass


class AllUnitTypesInGame(UnitTypeGroup):
    def __init__(self):
        self.function = 'allUnitTypesInGame'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                 Debris Groups                                #
# ---------------------------------------------------------------------------- #


class DebrisGroup(Group):
    pass


class AllDebris(DebrisGroup):
    def __init__(self):
        self.function = 'allDebris'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                 Region Groups                                #
# ---------------------------------------------------------------------------- #


class RegionGroup(Group):
    pass


class AllRegions(RegionGroup):
    def __init__(self):
        self.function = 'allRegions'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                     Shops                                    #
# ---------------------------------------------------------------------------- #


class Shop(Function):
    def __init__(self, shop_id):
        self.function = {
            'direct': True,
            'value': shop_id,
        }


# ---------------------------------------------------------------------------- #
#                                  Animations                                  #
# ---------------------------------------------------------------------------- #


class AnimationType(Function):
    def __init__(self, animation_type_id):
        self.function = {
            'direct': True,
            'value': animation_type_id,
        }


# ---------------------------------------------------------------------------- #
#                                     Music                                    #
# ---------------------------------------------------------------------------- #


class Music(Function):
    def __init__(self, music_id):
        self.function = {
            'direct': True,
            'value': music_id,
        }


# ---------------------------------------------------------------------------- #
#                                    Sounds                                    #
# ---------------------------------------------------------------------------- #


class Sound(Function):
    def __init__(self, sound_id):
        self.function = {
            'direct': True,
            'value': sound_id,
        }
