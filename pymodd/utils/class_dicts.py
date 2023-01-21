TRIGGER_TO_ENUM = {
    'gameStart': 'GAME_START',
    'frameTick': 'EVERY_FRAME',
    'secondTick': 'EVERY_SECOND',
    'serverShuttingDown': 'SERVER_SHUTTING_DOWN',
    'unitTouchesWall': 'UNIT_TOUCHES_WALL',
    'unitUsesItem': 'UNIT_USES_ITEM',
    'unitAttributeBecomesZero': 'UNIT_ATTRIBUTE_BECOMES_ZERO',
    'unitStartsUsingAnItem': 'UNIT_STARTS_USING_AN_ITEM',
    'unitAttributeBecomesFull': 'UNIT_ATTRIBUTE_BECOMES_FULL',
    'unitDroppedAnItem': 'UNIT_DROPPED_AN_ITEM',
    'unitEntersRegion': 'UNIT_ENTERS_REGION',
    'unitTouchesItem': 'UNIT_TOUCHES_ITEM',
    'unitPickedAnItem': 'UNIT_PICKED_AN_ITEM',
    'unitTouchesUnit': 'UNIT_TOUCHES_UNIT',
    'unitTouchesDebris': 'UNIT_TOUCHES_DEBRIS',
    'unitTouchesProjectile': 'UNIT_TOUCHES_PROJECTILE',
    'unitStopsUsingAnItem': 'UNIT_STOPS_USING_AN_ITEM',
    'unitAttacksUnit': 'UNIT_ATTACKS_UNIT',
    'unitSelectsItem': 'UNIT_SELECTS_ITEM',
    'unitSelectsInventorySlot': 'UNIT_SELECTS_INVENTORY_SLOT',
    'unitEntersSensor': 'UNIT_ENTERS_SENSOR',
    'projectileTouchesItem': 'PROJECTILE_TOUCHES_ITEM',
    'projectileTouchesDebris': 'PROJECTILE_TOUCHES_DEBRIS',
    'projectileAttributeBecomesZero': 'PROJECTILE_ATTRIBUTE_BECOMES_ZERO',
    'projectileTouchesWall': 'PROJECTILE_TOUCHES_WALL',
    'projectileEntersSensor': 'PROJECTILE_ENTERS_SENSOR',
    'playerCustomInput': 'PLAYER_CUSTOM_INPUT',
    'playerAttributeBecomesFull': 'PLAYER_ATTRIBUTE_BECOMES_FULL',
    'playerJoinsGame': 'PLAYER_JOINS_GAME',
    'playerPurchasesUnit': 'PLAYER_PURCHASES_UNIT',
    'playerLeavesGame': 'PLAYER_LEAVES_GAME',
    'playerAttributeBecomesZero': 'PLAYER_ATTRIBUTE_BECOMES_ZERO',
    'playerSendsChatMessage': 'PLAYER_SENDS_CHAT_MESSAGE',
    'itemAttributeBecomesFull': 'ITEM_ATTRIBUTE_BECOMES_FULL',
    'itemEntersRegion': 'ITEM_ENTERS_REGION',
    'itemTouchesWall': 'ITEM_TOUCHES_WALL',
    'itemAttributeBecomesZero': 'ITEM_ATTRIBUTE_BECOMES_ZERO',
    'itemIsUsed': 'ITEM_IS_USED',
    'itemEntersSensor': 'ITEM_ENTERS_SENSOR',
    'raycastItemFired': 'RAYCAST_ITEM_FIRED',
    'entityCreated': 'ENTITY_CREATED',
    'entityTouchesWall': 'ENTITY_TOUCHES_WALL',
    'entityTouchesItem': 'ENTITY_TOUCHES_ITEM',
    'entityTouchesUnit': 'ENTITY_TOUCHES_UNIT',
    'entityTouchesProjectile': 'ENTITY_TOUCHES_PROJECTILE',
    'entityAttributeBecomesZero': 'ENTITY_ATTRIBUTE_BECOMES_ZERO',
    'entityAttributeBecomesFull': 'ENTITY_ATTRIBUTE_BECOMES_FULL',
    'entityEntersRegion': 'ENTITY_ENTERS_REGION',
    'debrisEntersRegion': 'DEBRIS_ENTERS_REGION'
}

CONSTANTS_TO_ENUM = {
    'ui_target_to_enum': {
        'top': 'TOP',
        'center-lg': 'CENTER',
        'scoreboard': 'SCOREBOARD'
    },
    'flip_direction_to_enum': {
        'none': 'NONE',
        'horizontal': 'HORIZONTAL',
        'vertical': 'VERTICAL',
        'both': 'BOTH'
    }
}

FUNCTION_TO_CLASS = {
    'undefinedValue': {
        'className': 'Undefined',
        'arguments': []
    },
    'getSelectedEntity': {
        'className': 'SelectedEntity',
        'arguments': []
    },
    'thisEntity': {
        'className': 'ThisEntity',
        'arguments': []
    },
    'getLastPlayerSelectingDialogueOption': {
        'className': 'LastPlayerSelectingDialogueOption',
        'arguments': []
    },
    'getTriggeringPlayer': {
        'className': 'LastTriggeringPlayer',
        'arguments': []
    },
    'getOwner': {
        'className': 'OwnerOfEntity',
        'arguments': [
            'entity'
        ]
    },
    'selectedPlayer': {
        'className': 'SelectedPlayer',
        'arguments': []
    },
    'getPlayerFromId': {
        'className': 'PlayerFromId',
        'arguments': [
            'string'
        ]
    },
    'getLastPurchasedUnit': {
        'className': 'LastPurchasedUnit',
        'arguments': []
    },
    'getLastOverlappingUnit': {
        'className': 'LastOverlappingUnit',
        'arguments': []
    },
    'getLastOverlappedUnit': {
        'className': 'LastOverlappedUnit',
        'arguments': []
    },
    'getLastTouchingUnit': {
        'className': 'LastTouchingUnit',
        'arguments': []
    },
    'getSourceUnitOfProjectile': {
        'className': 'SourceUnitOfProjectile',
        'arguments': [
            'entity'
        ]
    },
    'getLastCastingUnit': {
        'className': 'LastCastingUnit',
        'arguments': []
    },
    'getLastTouchedUnit': {
        'className': 'LastTouchedUnit',
        'arguments': []
    },
    'getLastCreatedUnit': {
        'className': 'LastCreatedUnit',
        'arguments': []
    },
    'getOwnerOfItem': {
        'className': 'OwnerOfItem',
        'arguments': [
            'entity'
        ]
    },
    'getTriggeringUnit': {
        'className': 'LastTriggeringUnit',
        'arguments': []
    },
    'selectedUnit': {
        'className': 'SelectedUnit',
        'arguments': []
    },
    'getLastAttackedUnit': {
        'className': 'LastAttackedUnit',
        'arguments': []
    },
    'getLastAttackingUnit': {
        'className': 'LastAttackingUnit',
        'arguments': []
    },
    'ownerUnitOfSensor': {
        'className': 'OwnerUnitOfSensor',
        'arguments': [
            'sensor'
        ]
    },
    'getUnitFromId': {
        'className': 'UnitFromId',
        'arguments': [
            'string'
        ]
    },
    'targetUnit': {
        'className': 'TargetUnit',
        'arguments': [
            'unit'
        ]
    },
    'getItemInFrontOfUnit': {
        'className': 'ItemInFrontOfUnit',
        'arguments': [
            'entity'
        ]
    },
    'getItemAtSlot': {
        'className': 'ItemAtSlot',
        'arguments': [
            'slot',
            'unit'
        ]
    },
    'selectedItem': {
        'className': 'SelectedItem',
        'arguments': []
    },
    'getTriggeringItem': {
        'className': 'TriggeringItem',
        'arguments': []
    },
    'getItemCurrentlyHeldByUnit': {
        'className': 'ItemCurrentlyHeldByUnit',
        'arguments': [
            'entity'
        ]
    },
    'lastUsedItem': {
        'className': 'LastUsedItem',
        'arguments': []
    },
    'getSourceItemOfProjectile': {
        'className': 'SourceItemOfProjectile',
        'arguments': [
            'entity'
        ]
    },
    'getLastCreatedItem': {
        'className': 'LastCreatedItem',
        'arguments': []
    },
    'getLastOverlappingItem': {
        'className': 'LastOverlappingItem',
        'arguments': []
    },
    'getItemInInventorySlot': {
        'className': 'ItemInInventorySlot',
        'arguments': [
            'slot',
            'entity'
        ]
    },
    'getLastTouchedItem': {
        'className': 'LastTouchedItem',
        'arguments': []
    },
    'getLastAttackingItem': {
        'className': 'LastAttackingItem',
        'arguments': []
    },
    'selectedProjectile': {
        'className': 'SelectedProjectile',
        'arguments': []
    },
    'getLastCreatedProjectile': {
        'className': 'LastCreatedProjectile',
        'arguments': []
    },
    'getTriggeringProjectile': {
        'className': 'LastTriggeringProjectile',
        'arguments': []
    },
    'getLastTouchedProjectile': {
        'className': 'LastTouchedProjectile',
        'arguments': []
    },
    'getLastOverlappingProjectile': {
        'className': 'LastOverlappingProjectile',
        'arguments': []
    },
    'selectedDebris': {
        'className': 'SelectedDebris',
        'arguments': []
    },
    'getTriggeringDebris': {
        'className': 'LastTriggeringDebris',
        'arguments': []
    },
    'xyCoordinate': {
        'className': 'XyCoordinate',
        'arguments': [
            'x',
            'y'
        ]
    },
    'getMouseCursorPosition': {
        'className': 'MouseCursorPosition',
        'arguments': [
            'player'
        ]
    },
    'centerOfRegion': {
        'className': 'CenterOfRegion',
        'arguments': [
            'region'
        ]
    },
    'entityLastRaycastCollisionPosition': {
        'className': 'EntityLastRaycastCollisionPosition',
        'arguments': [
            'entity'
        ]
    },
    'getEntityPosition': {
        'className': 'EntityPosition',
        'arguments': [
            'entity'
        ]
    },
    'getRandomPositionInRegion': {
        'className': 'RandomPositionInRegion',
        'arguments': [
            'region'
        ]
    },
    'getTriggeringAttribute': {
        'className': 'TriggeringAttribute',
        'arguments': []
    },
    'getSensorOfUnit': {
        'className': 'SensorOfUnit',
        'arguments': [
            'unit'
        ]
    },
    'getTriggeringSensor': {
        'className': 'TriggeringSensor',
        'arguments': []
    },
    'getEntityState': {
        'className': 'EntityState',
        'arguments': [
            'entity'
        ]
    },
    'getRandomNumberBetween': {
        'className': 'RandomNumberBetween',
        'arguments': [
            'min',
            'max'
        ]
    },
    'unitsFacingAngle': {
        'className': 'UnitsFacingAngle',
        'arguments': [
            'unit'
        ]
    },
    'getMapHeight': {
        'className': 'MapHeight',
        'arguments': []
    },
    'toFixed': {
        'className': 'ToFixed',
        'arguments': [
            'value',
            'precision'
        ]
    },
    'getItemQuantity': {
        'className': 'ItemQuantity',
        'arguments': [
            'item'
        ]
    },
    'cos': {
        'className': 'Cos',
        'arguments': [
            'angle'
        ]
    },
    'entityHeight': {
        'className': 'EntityHeight',
        'arguments': [
            'entity'
        ]
    },
    'playerAttributeMax': {
        'className': 'PlayerAttributeMax',
        'arguments': [
            'attribute',
            'entity'
        ]
    },
    'getPlayerAttribute': {
        'className': 'PlayerAttribute',
        'arguments': [
            'attribute',
            'entity'
        ]
    },
    'getMapWidth': {
        'className': 'MapWidth',
        'arguments': []
    },
    'entityWidth': {
        'className': 'EntityWidth',
        'arguments': [
            'entity'
        ]
    },
    'getPlayerCount': {
        'className': 'PlayerCount',
        'arguments': []
    },
    'arctan': {
        'className': 'Arctan',
        'arguments': [
            'number'
        ]
    },
    'mathFloor': {
        'className': 'MathFloor',
        'arguments': [
            'value'
        ]
    },
    'getYCoordinateOfRegion': {
        'className': 'YCoordinateOfRegion',
        'arguments': [
            'region'
        ]
    },
    'squareRoot': {
        'className': 'SquareRoot',
        'arguments': [
            'number'
        ]
    },
    'getUnitCount': {
        'className': 'UnitCount',
        'arguments': []
    },
    'angleBetweenPositions': {
        'className': 'AngleBetweenPositions',
        'arguments': [
            'position_a',
            'position_b'
        ]
    },
    'getWidthOfRegion': {
        'className': 'WidthOfRegion',
        'arguments': [
            'region'
        ]
    },
    'entityAttributeMin': {
        'className': 'EntityAttributeMin',
        'arguments': [
            'attribute',
            'entity'
        ]
    },
    'stringToNumber': {
        'className': 'StringToNumber',
        'arguments': [
            'value'
        ]
    },
    'getQuantityOfUnitTypeInUnitTypeGroup': {
        'className': 'QuantityOfUnitTypeInUnitTypeGroup',
        'arguments': [
            'unit_type',
            'unit_type_group'
        ]
    },
    'getPositionY': {
        'className': 'PositionY',
        'arguments': [
            'position'
        ]
    },
    'distanceBetweenPositions': {
        'className': 'DistanceBetweenPositions',
        'arguments': [
            'position_a',
            'position_b'
        ]
    },
    'entityAttributeMax': {
        'className': 'EntityAttributeMax',
        'arguments': [
            'attribute',
            'entity'
        ]
    },
    'playerAttributeMin': {
        'className': 'PlayerAttributeMin',
        'arguments': [
            'attribute',
            'entity'
        ]
    },
    'sin': {
        'className': 'Sin',
        'arguments': [
            'angle'
        ]
    },
    'getXCoordinateOfRegion': {
        'className': 'XCoordinateOfRegion',
        'arguments': [
            'region'
        ]
    },
    'getEntityVelocityY': {
        'className': 'EntityVelocityY',
        'arguments': [
            'entity'
        ]
    },
    'getPositionX': {
        'className': 'PositionX',
        'arguments': [
            'position'
        ]
    },
    'lastPlayedTimeOfPlayer': {
        'className': 'LastPlayedTimeOfPlayer',
        'arguments': [
            'player'
        ]
    },
    'getMax': {
        'className': 'Max',
        'arguments': [
            'num_a',
            'num_b'
        ]
    },
    'getRotateSpeed': {
        'className': 'RotateSpeed',
        'arguments': [
            'unit_type'
        ]
    },
    'getCurrentAmmoOfItem': {
        'className': 'CurrentAmmoOfItem',
        'arguments': [
            'item'
        ]
    },
    'getHeightOfRegion': {
        'className': 'HeightOfRegion',
        'arguments': [
            'region'
        ]
    },
    'getItemMaxQuantity': {
        'className': 'ItemMaxQuantity',
        'arguments': [
            'item'
        ]
    },
    'absoluteValueOfNumber': {
        'className': 'AbsoluteValueOfNumber',
        'arguments': [
            'number'
        ]
    },
    'getEntityAttribute': {
        'className': 'EntityAttribute',
        'arguments': [
            'attribute',
            'entity'
        ]
    },
    'currentTimeStamp': {
        'className': 'CurrentTimeStamp',
        'arguments': []
    },
    'getEntityVelocityX': {
        'className': 'EntityVelocityX',
        'arguments': [
            'entity'
        ]
    },
    'defaultQuantityOfItemType': {
        'className': 'DefaultQuantityOfItemType',
        'arguments': [
            'item_type'
        ]
    },
    'getQuantityOfItemTypeInItemTypeGroup': {
        'className': 'QuantityOfItemTypeInItemTypeGroup',
        'arguments': [
            'item_type',
            'item_type_group'
        ]
    },
    'getNumberOfItemsPresent': {
        'className': 'NumberOfItemsPresent',
        'arguments': []
    },
    'getMin': {
        'className': 'Min',
        'arguments': [
            'num_a',
            'num_b'
        ]
    },
    'maxValueOfItemType': {
        'className': 'MaxValueOfItemType',
        'arguments': [
            'item_type'
        ]
    },
    'angleBetweenMouseAndWindowCenter': {
        'className': 'AngleBetweenMouseAndWindowCenter',
        'arguments': [
            'player'
        ]
    },
    'getExponent': {
        'className': 'Exponent',
        'arguments': [
            'base',
            'power'
        ]
    },
    'getNumberOfUnitsOfUnitType': {
        'className': 'NumberOfUnitsOfUnitType',
        'arguments': [
            'unit_type'
        ]
    },
    'getNumberOfPlayersOfPlayerType': {
        'className': 'NumberOfPlayersOfPlayerType',
        'arguments': [
            'player_type'
        ]
    },
    'getLengthOfString': {
        'className': 'LengthOfString',
        'arguments': [
            'string'
        ]
    },
    'getStringArrayLength': {
        'className': 'StringArrayLength',
        'arguments': [
            'string'
        ]
    },
    'selectedInventorySlot': {
        'className': 'SelectedInventorySlot',
        'arguments': [
            'unit'
        ]
    },
    'log10': {
        'className': 'LogBase10',
        'arguments': [
            'value'
        ]
    },
    'unitSensorRadius': {
        'className': 'UnitSensorRadius',
        'arguments': [
            'unit'
        ]
    },
    'calculate': {
        'className': 'Calculate',
        'arguments': [
            'item_a',
            'operator',
            'item_b'
        ]
    },
    'getEntityType': {
        'className': 'EntityTypeOfEntity',
        'arguments': [
            'entity'
        ]
    },
    'playerCustomInput': {
        'className': 'PlayerCustomInput',
        'arguments': [
            'player'
        ]
    },
    'concat': {
        'className': 'Concat',
        'arguments': [
            'text_a',
            'text_b'
        ]
    },
    'getPlayerName': {
        'className': 'PlayerName',
        'arguments': [
            'entity'
        ]
    },
    'getUnitTypeName': {
        'className': 'UnitTypeName',
        'arguments': [
            'unit_type'
        ]
    },
    'nameOfRegion': {
        'className': 'NameOfRegion',
        'arguments': [
            'region'
        ]
    },
    'getItemTypeName': {
        'className': 'ItemTypeName',
        'arguments': [
            'item_type'
        ]
    },
    'substringOf': {
        'className': 'SubstringOf',
        'arguments': [
            'string',
            'from_index',
            'to_index'
        ]
    },
    'getLastChatMessageSentByPlayer': {
        'className': 'LastChatMessageSentByPlayer',
        'arguments': [
            'player'
        ]
    },
    'toLowerCase': {
        'className': 'ToLowerCase',
        'arguments': [
            'string'
        ]
    },
    'replaceValuesInString': {
        'className': 'ReplaceValuesInString',
        'arguments': [
            'match_string',
            'source_string',
            'new_string'
        ]
    },
    'getTimeString': {
        'className': 'TimeString',
        'arguments': [
            'seconds'
        ]
    },
    'getItemDescription': {
        'className': 'ItemDescription',
        'arguments': [
            'item'
        ]
    },
    'getUnitData': {
        'className': 'UnitData',
        'arguments': [
            'unit'
        ]
    },
    'getPlayerData': {
        'className': 'PlayerData',
        'arguments': [
            'player'
        ]
    },
    'getUnitId': {
        'className': 'UnitId',
        'arguments': [
            'unit'
        ]
    },
    'getPlayerId': {
        'className': 'PlayerId',
        'arguments': [
            'player'
        ]
    },
    'getStringArrayElement': {
        'className': 'StringArrayElement',
        'arguments': [
            'number',
            'string'
        ]
    },
    'insertStringArrayElement': {
        'className': 'InsertStringArrayElement',
        'arguments': [
            'value',
            'string'
        ]
    },
    'updateStringArrayElement': {
        'className': 'UpdateStringArrayElement',
        'arguments': [
            'number',
            'string',
            'value'
        ]
    },
    'removeStringArrayElement': {
        'className': 'RemoveStringArrayElement',
        'arguments': [
            'number',
            'string'
        ]
    },
    'entityName': {
        'className': 'EntityName',
        'arguments': [
            'entity'
        ]
    },
    'isPlayerLoggedIn': {
        'className': 'IsPlayerLoggedIn',
        'arguments': [
            'player'
        ]
    },
    'playersAreFriendly': {
        'className': 'PlayersAreFriendly',
        'arguments': [
            'player_a',
            'player_b'
        ]
    },
    'playerIsControlledByHuman': {
        'className': 'PlayerIsControlledByHuman',
        'arguments': [
            'player'
        ]
    },
    'playersAreHostile': {
        'className': 'PlayersAreHostile',
        'arguments': [
            'player_a',
            'player_b'
        ]
    },
    'regionOverlapsWithRegion': {
        'className': 'RegionOverlapsWithRegion',
        'arguments': [
            'region_a',
            'region_b'
        ]
    },
    'playersAreNeutral': {
        'className': 'PlayersAreNeutral',
        'arguments': [
            'player_a',
            'player_b'
        ]
    },
    'playerHasAdblockEnabled': {
        'className': 'PlayerHasAdblockEnabled',
        'arguments': [
            'player'
        ]
    },
    'entityExists': {
        'className': 'EntityExists',
        'arguments': [
            'entity'
        ]
    },
    'isPositionInWall': {
        'className': 'IsPositionInWall',
        'arguments': [
            'positionx',
            'positiony'
        ]
    },
    'subString': {
        'className': 'SubString',
        'arguments': [
            'source_string',
            'pattern_string'
        ]
    },
    'stringStartsWith': {
        'className': 'StringStartsWith',
        'arguments': [
            'source_string',
            'pattern_string'
        ]
    },
    'stringEndsWith': {
        'className': 'StringEndsWith',
        'arguments': [
            'source_string',
            'pattern_string'
        ]
    },
    'isAIEnabled': {
        'className': 'IsAIEnabled',
        'arguments': [
            'unit'
        ]
    },
    'isBotPlayer': {
        'className': 'IsBotPlayer',
        'arguments': [
            'player'
        ]
    },
    'isComputerPlayer': {
        'className': 'IsComputerPlayer',
        'arguments': [
            'player_is_a_computer'
        ]
    },
    'getItemParticle': {
        'className': 'ItemParticle',
        'arguments': [
            'particle_type',
            'entity'
        ]
    },
    'selectedParticle': {
        'className': 'SelectedParticle',
        'arguments': []
    },
    'getUnitParticle': {
        'className': 'UnitParticle',
        'arguments': [
            'particle_type',
            'entity'
        ]
    },
    'getVariable': {
        'className': 'Variable',
        'arguments': [
            'variable_name',
            'variable_type'
        ]
    },
    'getEntityVariable': {
        'className': 'EntityVariable',
        'arguments': [
            'variable_name',
            'variable_type'
        ]
    },
    'getValueOfEntityVariable': {
        'className': 'ValueOfEntityVariable',
        'arguments': [
            'entity_variable_type',
            'entity'
        ]
    },
    'getPlayerVariable': {
        'className': 'PlayerVariable',
        'arguments': [
            'variable_name',
            'variable_type'
        ]
    },
    'getValueOfPlayerVariable': {
        'className': 'ValueOfPlayerVariable',
        'arguments': [
            'player_variable_type',
            'player'
        ]
    },
    'getTriggeringRegion': {
        'className': 'LastTriggeringRegion',
        'arguments': []
    },
    'getEntireMapRegion': {
        'className': 'EntireMapRegion',
        'arguments': []
    },
    'selectedRegion': {
        'className': 'SelectedRegion',
        'arguments': []
    },
    'entityBounds': {
        'className': 'EntityBounds',
        'arguments': [
            'entity'
        ]
    },
    'dynamicRegion': {
        'className': 'DynamicRegion',
        'arguments': [
            'x',
            'y',
            'width',
            'height'
        ]
    },
    'getUnitTypeOfUnit': {
        'className': 'UnitTypeOfUnit',
        'arguments': [
            'entity'
        ]
    },
    'lastPurchasedUnitTypetId': {
        'className': 'LastPurchasedUnitTypetId',
        'arguments': []
    },
    'getRandomUnitTypeFromUnitTypeGroup': {
        'className': 'RandomUnitTypeFromUnitTypeGroup',
        'arguments': [
            'unit_type_group'
        ]
    },
    'selectedUnitType': {
        'className': 'SelectedUnitType',
        'arguments': []
    },
    'selectedItemType': {
        'className': 'SelectedItemType',
        'arguments': []
    },
    'getItemTypeOfItem': {
        'className': 'ItemTypeOfItem',
        'arguments': [
            'entity'
        ]
    },
    'getRandomItemTypeFromItemTypeGroup': {
        'className': 'RandomItemTypeFromItemTypeGroup',
        'arguments': [
            'item_type_group'
        ]
    },
    'getProjectileTypeOfProjectile': {
        'className': 'ProjectileTypeOfProjectile',
        'arguments': [
            'entity'
        ]
    },
    'playerTypeOfPlayer': {
        'className': 'PlayerTypeOfPlayer',
        'arguments': [
            'player'
        ]
    },
    'getAttributeTypeOfAttribute': {
        'className': 'AttributeTypeOfAttribute',
        'arguments': [
            'entity'
        ]
    },
    'entitiesCollidingWithLastRaycast': {
        'className': 'EntitiesCollidingWithLastRaycast',
        'arguments': []
    },
    'allEntities': {
        'className': 'AllEntities',
        'arguments': []
    },
    'entitiesInRegion': {
        'className': 'EntitiesInRegion',
        'arguments': [
            'region'
        ]
    },
    'entitiesInRegionInFrontOfEntityAtDistance': {
        'className': 'EntitiesInRegionInFrontOfEntityAtDistance',
        'arguments': [
            'width',
            'height',
            'entity',
            'distance'
        ]
    },
    'entitiesBetweenTwoPositions': {
        'className': 'EntitiesBetweenTwoPositions',
        'arguments': [
            'position_a',
            'position_b'
        ]
    },
    'allUnitsOwnedByPlayer': {
        'className': 'AllUnitsOwnedByPlayer',
        'arguments': [
            'player'
        ]
    },
    'allUnitsAttachedToUnit': {
        'className': 'AllUnitsAttachedToUnit',
        'arguments': [
            'entity'
        ]
    },
    'allUnits': {
        'className': 'AllUnits',
        'arguments': []
    },
    'allUnitsAttachedToItem': {
        'className': 'AllUnitsAttachedToItem',
        'arguments': [
            'entity'
        ]
    },
    'allUnitsMountedOnUnit': {
        'className': 'AllUnitsMountedOnUnit',
        'arguments': [
            'entity'
        ]
    },
    'allUnitsInRegion': {
        'className': 'AllUnitsInRegion',
        'arguments': [
            'region'
        ]
    },
    'allProjectilesAttachedToUnit': {
        'className': 'AllProjectilesAttachedToUnit',
        'arguments': [
            'entity'
        ]
    },
    'allProjectiles': {
        'className': 'AllProjectiles',
        'arguments': []
    },
    'allItemsDroppedOnGround': {
        'className': 'AllItemsDroppedOnGround',
        'arguments': []
    },
    'allItems': {
        'className': 'AllItems',
        'arguments': []
    },
    'allItemsAttachedToUnit': {
        'className': 'AllItemsAttachedToUnit',
        'arguments': [
            'entity'
        ]
    },
    'allItemsOwnedByUnit': {
        'className': 'AllItemsOwnedByUnit',
        'arguments': [
            'entity'
        ]
    },
    'humanPlayers': {
        'className': 'AllHumanPlayers',
        'arguments': []
    },
    'computerPlayers': {
        'className': 'AllComputerPlayers',
        'arguments': []
    },
    'allPlayers': {
        'className': 'AllPlayers',
        'arguments': []
    },
    'botPlayers': {
        'className': 'AllBotPlayers',
        'arguments': []
    },
    'allItemTypesInGame': {
        'className': 'AllItemTypesInGame',
        'arguments': []
    },
    'allUnitTypesInGame': {
        'className': 'AllUnitTypesInGame',
        'arguments': []
    },
    'allDebris': {
        'className': 'AllDebris',
        'arguments': []
    },
    'allRegions': {
        'className': 'AllRegions',
        'arguments': []
    }
}

ACTION_TO_CLASS = {
    'condition': {
        'className': 'IfStatement',
        'arguments': [
            'condition',
            'then_actions',
            'else_actions'
        ]
    },
    'setPlayerVariable': {
        'className': 'SetPlayerVariable',
        'arguments': [
            'player',
            'variable_type',
            'value'
        ]
    },
    'setEntityVariable': {
        'className': 'SetEntityVariable',
        'arguments': [
            'entity',
            'variable_type',
            'value'
        ]
    },
    'playAdForPlayer': {
        'className': 'PlayAdForPlayer',
        'arguments': [
            'entity'
        ]
    },
    'setTimeOut': {
        'className': 'SetTimeOut',
        'arguments': [
            'duration',
            'actions'
        ]
    },
    'rotateEntityToFacePosition': {
        'className': 'RotateEntityToFacePosition',
        'arguments': [
            'entity',
            'position'
        ]
    },
    'destroyEntity': {
        'className': 'DestroyEntity',
        'arguments': [
            'entity'
        ]
    },
    'setEntityDepth': {
        'className': 'SetEntityDepth',
        'arguments': [
            'entity',
            'value'
        ]
    },
    'hideUnitFromPlayer': {
        'className': 'HideUnitFromPlayer',
        'arguments': [
            'entity',
            'player'
        ]
    },
    'showUnitToPlayer': {
        'className': 'ShowUnitToPlayer',
        'arguments': [
            'entity',
            'player'
        ]
    },
    'sendChatMessage': {
        'className': 'SendChatMessage',
        'arguments': [
            'message'
        ]
    },
    'playSoundAtPosition': {
        'className': 'PlaySoundAtPosition',
        'arguments': [
            'sound',
            'position'
        ]
    },
    'dropItemAtPosition': {
        'className': 'DropItemAtPosition',
        'arguments': [
            'item',
            'position'
        ]
    },
    'applyForceOnEntityAngle': {
        'className': 'ApplyForceOnEntityAngle',
        'arguments': [
            'force',
            'entity',
            'angle'
        ]
    },
    'showInputModalToPlayer': {
        'className': 'ShowInputModalToPlayer',
        'arguments': [
            'player',
            'inputLabel'
        ]
    },
    'openDialogueForPlayer': {
        'className': 'OpenDialogueForPlayer',
        'arguments': [
            'dialogue',
            'player'
        ]
    },
    'continue': {
        'className': 'Continue',
        'arguments': []
    },
    'openWebsiteForPlayer': {
        'className': 'OpenWebsiteForPlayer',
        'arguments': [
            'string',
            'player'
        ]
    },
    'setEntityLifeSpan': {
        'className': 'SetEntityLifeSpan',
        'arguments': [
            'entity',
            'lifeSpan'
        ]
    },
    'hideUnitNameLabel': {
        'className': 'HideUnitNameLabel',
        'arguments': [
            'entity'
        ]
    },
    'setTriggeringUnit': {
        'className': 'SetTriggeringUnit',
        'arguments': [
            'entity'
        ]
    },
    'createUnitAtPosition': {
        'className': 'CreateUnitForPlayerAtPosition',
        'arguments': [
            'unitType',
            'player',
            'position',
            'angle'
        ]
    },
    'hideUiTextForEveryone': {
        'className': 'HideUiTextForEveryone',
        'arguments': [
            'target'
        ]
    },
    'hideGameSuggestionsForPlayer': {
        'className': 'HideGameSuggestionsForPlayer',
        'arguments': [
            'player'
        ]
    },
    'transformRegionDimensions': {
        'className': 'TransformRegionDimensions',
        'arguments': [
            'region',
            'x',
            'y',
            'width',
            'height'
        ]
    },
    'makeUnitInvisibleToFriendlyPlayers': {
        'className': 'MakeUnitInvisibleToFriendlyPlayers',
        'arguments': [
            'entity'
        ]
    },
    'setEntityAttributeMin': {
        'className': 'SetEntityAttributeMin',
        'arguments': [
            'attribute',
            'entity',
            'value'
        ]
    },
    'showInviteFriendsModal': {
        'className': 'ShowInviteFriendsModal',
        'arguments': [
            'player'
        ]
    },
    'showCustomModalToPlayer': {
        'className': 'ShowCustomModalToPlayer',
        'arguments': [
            'htmlContent',
            'player'
        ]
    },
    'showUiTextForEveryone': {
        'className': 'ShowUiTextForEveryone',
        'arguments': [
            'target'
        ]
    },
    'moveDebris': {
        'className': 'MoveDebris',
        'arguments': [
            'entity',
            'position'
        ]
    },
    'forAllItems': {
        'className': 'ForAllItems',
        'arguments': [
            'itemGroup',
            'actions'
        ]
    },
    'removePlayerFromPlayerGroup': {
        'className': 'RemovePlayerFromPlayerGroup',
        'arguments': [
            'player',
            'playerGroup'
        ]
    },
    'setUnitOwner': {
        'className': 'SetUnitOwner',
        'arguments': [
            'unit',
            'player'
        ]
    },
    'updateItemQuantity': {
        'className': 'UpdateItemQuantity',
        'arguments': [
            'entity',
            'quantity'
        ]
    },
    'applyForceOnEntityAngleLT': {
        'className': 'ApplyForceOnEntityAngleLT',
        'arguments': [
            'force',
            'entity',
            'angle'
        ]
    },
    'setEntityState': {
        'className': 'SetEntityState',
        'arguments': [
            'entity',
            'state'
        ]
    },
    'hideUnitInPlayerMinimap': {
        'className': 'HideUnitInPlayerMinimap',
        'arguments': [
            'unit',
            'player'
        ]
    },
    'return': {
        'className': 'Return',
        'arguments': []
    },
    'runScript': {
        'className': 'RunScript',
        'arguments': [
            'scriptName'
        ]
    },
    'playerCameraSetZoom': {
        'className': 'PlayerCameraSetZoom',
        'arguments': [
            'player',
            'zoom'
        ]
    },
    'setUnitNameLabel': {
        'className': 'SetUnitNameLabel',
        'arguments': [
            'unit',
            'name'
        ]
    },
    'openShopForPlayer': {
        'className': 'OpenShopForPlayer',
        'arguments': [
            'shop',
            'player'
        ]
    },
    'closeDialogueForPlayer': {
        'className': 'CloseDialogueForPlayer',
        'arguments': [
            'player'
        ]
    },
    'comment': {
        'className': 'Comment',
        'arguments': [
            'comment'
        ]
    },
    'createEntityAtPositionWithDimensions': {
        'className': 'CreateEntityAtPositionWithDimensions',
        'arguments': [
            'entity',
            'position',
            'height',
            'width',
            'angle'
        ]
    },
    'setVariable': {
        'className': 'SetVariable',
        'arguments': [
            'variable',
            'value'
        ]
    },
    'increaseVariableByNumber': {
        'className': 'IncreaseVariableByNumber',
        'arguments': [
            'variable',
            'number'
        ]
    },
    'playerCameraTrackUnit': {
        'className': 'PlayerCameraTrackUnit',
        'arguments': [
            'player',
            'unit'
        ]
    },
    'castAbility': {
        'className': 'CastAbility',
        'arguments': [
            'entity',
            'abilityName'
        ]
    },
    'playEntityAnimation': {
        'className': 'PlayEntityAnimation',
        'arguments': [
            'entity',
            'animation'
        ]
    },
    'while': {
        'className': 'While',
        'arguments': [
            'conditions',
            'actions'
        ]
    },
    'applyForceOnEntityXY': {
        'className': 'ApplyForceOnEntityXY',
        'arguments': [
            'force_x',
            'force_y',
            'entity'
        ]
    },
    'showUnitInPlayerMinimap': {
        'className': 'ShowUnitInPlayerMinimap',
        'arguments': [
            'unit',
            'color',
            'player'
        ]
    },
    'savePlayerData': {
        'className': 'SavePlayerData',
        'arguments': [
            'player'
        ]
    },
    'hideUnitNameLabelFromPlayer': {
        'className': 'HideUnitNameLabelFromPlayer',
        'arguments': [
            'entity',
            'player'
        ]
    },
    'setPlayerAttribute': {
        'className': 'SetPlayerAttribute',
        'arguments': [
            'attribute',
            'entity',
            'value'
        ]
    },
    'updateUiTextForPlayer': {
        'className': 'UpdateUiTextForPlayer',
        'arguments': [
            'target',
            'value',
            'entity'
        ]
    },
    'showUnitNameLabel': {
        'className': 'ShowUnitNameLabel',
        'arguments': [
            'entity'
        ]
    },
    'closeShopForPlayer': {
        'className': 'CloseShopForPlayer',
        'arguments': [
            'player'
        ]
    },
    'attachDebrisToUnit': {
        'className': 'AttachDebrisToUnit',
        'arguments': [
            'entity',
            'unit'
        ]
    },
    'repeat': {
        'className': 'Repeat',
        'arguments': [
            'count',
            'actions'
        ]
    },
    'stopMusic': {
        'className': 'StopMusic',
        'arguments': []
    },
    'emitParticleOnceAtPosition': {
        'className': 'EmitParticleOnceAtPosition',
        'arguments': [
            'particleType',
            'position'
        ]
    },
    'setVelocityOfEntityXY': {
        'className': 'SetVelocityOfEntityXY',
        'arguments': [
            'velocity_x',
            'velocity_y',
            'entity'
        ]
    },
    'showUnitNameLabelToPlayer': {
        'className': 'ShowUnitNameLabelToPlayer',
        'arguments': [
            'entity',
            'player'
        ]
    },
    'spawnItem': {
        'className': 'SpawnItem',
        'arguments': [
            'itemType',
            'position'
        ]
    },
    'createItemWithMaxQuantityAtPosition': {
        'className': 'CreateItemWithMaxQuantityAtPosition',
        'arguments': [
            'itemType',
            'position'
        ]
    },
    'showMenu': {
        'className': 'ShowMenu',
        'arguments': [
            'player'
        ]
    },
    'startAcceptingPlayers': {
        'className': 'StartAcceptingPlayers',
        'arguments': []
    },
    'forAllEntities': {
        'className': 'ForAllEntities',
        'arguments': [
            'entityGroup',
            'actions'
        ]
    },
    'makePlayerSelectUnit': {
        'className': 'MakePlayerSelectUnit',
        'arguments': [
            'player',
            'unit'
        ]
    },
    'setEntityAttribute': {
        'className': 'SetEntityAttribute',
        'arguments': [
            'attribute',
            'entity',
            'value'
        ]
    },
    'forAllItemTypes': {
        'className': 'ForAllItemTypes',
        'arguments': [
            'itemTypeGroup',
            'actions'
        ]
    },
    'createEntityForPlayerAtPositionWithDimensions': {
        'className': 'CreateEntityForPlayerAtPositionWithDimensions',
        'arguments': [
            'entity',
            'player',
            'position',
            'height',
            'width',
            'angle'
        ]
    },
    'endGame': {
        'className': 'EndGame',
        'arguments': []
    },
    'updateUiTextForEveryone': {
        'className': 'UpdateUiTextForEveryone',
        'arguments': [
            'target',
            'value'
        ]
    },
    'forAllUnits': {
        'className': 'ForAllUnits',
        'arguments': [
            'unitGroup',
            'actions'
        ]
    },
    'forAllProjectiles': {
        'className': 'ForAllProjectiles',
        'arguments': [
            'projectileGroup',
            'actions'
        ]
    },
    'stopMusicForPlayer': {
        'className': 'StopMusicForPlayer',
        'arguments': [
            'player'
        ]
    },
    'positionCamera': {
        'className': 'PositionCamera',
        'arguments': [
            'player',
            'position'
        ]
    },
    'createProjectileAtPosition': {
        'className': 'CreateProjectileAtPosition',
        'arguments': [
            'projectileType',
            'position',
            'force',
            'angle'
        ]
    },
    'showMenuAndSelectCurrentServer': {
        'className': 'ShowMenuAndSelectCurrentServer',
        'arguments': [
            'player'
        ]
    },
    'setFadingTextOfUnit': {
        'className': 'SetFadingTextOfUnit',
        'arguments': [
            'unit',
            'text',
            'color'
        ]
    },
    'changeScaleOfEntityBody': {
        'className': 'ChangeScaleOfEntityBody',
        'arguments': [
            'entity',
            'scale'
        ]
    },
    'forAllRegions': {
        'className': 'ForAllRegions',
        'arguments': [
            'regionGroup',
            'actions'
        ]
    },
    'rotateEntityToRadiansLT': {
        'className': 'RotateEntityToRadiansLT',
        'arguments': [
            'entity',
            'radians'
        ]
    },
    'setPlayerAttributeMax': {
        'className': 'SetPlayerAttributeMax',
        'arguments': [
            'attributeType',
            'player',
            'number'
        ]
    },
    'setPlayerAttributeRegenerationRate': {
        'className': 'SetPlayerAttributeRegenerationRate',
        'arguments': [
            'attributeType',
            'player',
            'number'
        ]
    },
    'forAllUnitTypes': {
        'className': 'ForAllUnitTypes',
        'arguments': [
            'unitTypeGroup',
            'actions'
        ]
    },
    'decreaseVariableByNumber': {
        'className': 'DecreaseVariableByNumber',
        'arguments': [
            'variable',
            'number'
        ]
    },
    'kickPlayer': {
        'className': 'KickPlayer',
        'arguments': [
            'entity'
        ]
    },
    'forAllPlayers': {
        'className': 'ForAllPlayers',
        'arguments': [
            'playerGroup',
            'actions'
        ]
    },
    'removeUnitFromUnitGroup': {
        'className': 'RemoveUnitFromUnitGroup',
        'arguments': [
            'unit',
            'unitGroup'
        ]
    },
    'flipEntitySprite': {
        'className': 'FlipEntitySprite',
        'arguments': [
            'entity',
            'flip'
        ]
    },
    'makeUnitInvisibleToNeutralPlayers': {
        'className': 'MakeUnitInvisibleToNeutralPlayers',
        'arguments': [
            'entity'
        ]
    },
    'saveUnitData': {
        'className': 'SaveUnitData',
        'arguments': [
            'unit'
        ]
    },
    'applyTorqueOnEntity': {
        'className': 'ApplyTorqueOnEntity',
        'arguments': [
            'torque',
            'entity'
        ]
    },
    'giveNewItemToUnit': {
        'className': 'GiveNewItemToUnit',
        'arguments': [
            'itemType',
            'unit'
        ]
    },
    'startUsingItem': {
        'className': 'StartUsingItem',
        'arguments': [
            'entity'
        ]
    },
    'moveEntity': {
        'className': 'MoveEntity',
        'arguments': [
            'entity',
            'position'
        ]
    },
    'for': {
        'className': 'For',
        'arguments': [
            'variable',
            'start',
            'stop',
            'actions'
        ]
    },
    'showMenuAndSelectBestServer': {
        'className': 'ShowMenuAndSelectBestServer',
        'arguments': [
            'player'
        ]
    },
    'applyForceOnEntityXYRelative': {
        'className': 'ApplyForceOnEntityXYRelative',
        'arguments': [
            'force_x',
            'force_y',
            'entity'
        ]
    },
    'applyForceOnEntityXYLT': {
        'className': 'ApplyForceOnEntityXYLT',
        'arguments': [
            'force_x',
            'force_y',
            'entity'
        ]
    },
    'attachEntityToEntity': {
        'className': 'AttachEntityToEntity',
        'arguments': [
            'entity',
            'targetingEntity'
        ]
    },
    'banPlayerFromChat': {
        'className': 'BanPlayerFromChat',
        'arguments': [
            'player'
        ]
    },
    'changeUnitType': {
        'className': 'ChangeUnitType',
        'arguments': [
            'entity',
            'unitType'
        ]
    },
    'forAllDebris': {
        'className': 'ForAllDebris',
        'arguments': [
            'debrisGroup',
            'actions'
        ]
    },
    'playMusicForPlayerRepeatedly': {
        'className': 'PlayMusicForPlayerRepeatedly',
        'arguments': [
            'music',
            'player'
        ]
    },
    'showGameSuggestionsForPlayer': {
        'className': 'ShowGameSuggestionsForPlayer',
        'arguments': [
            'player'
        ]
    },
    'setEntityAttributeRegenerationRate': {
        'className': 'SetEntityAttributeRegenerationRate',
        'arguments': [
            'attribute',
            'entity',
            'value'
        ]
    },
    'makeUnitSelectItemAtSlot': {
        'className': 'MakeUnitSelectItemAtSlot',
        'arguments': [
            'unit',
            'slotIndex'
        ]
    },
    'stopUsingItem': {
        'className': 'StopUsingItem',
        'arguments': [
            'entity'
        ]
    },
    'makeUnitVisible': {
        'className': 'MakeUnitVisible',
        'arguments': [
            'entity'
        ]
    },
    'makeUnitInvisible': {
        'className': 'MakeUnitInvisible',
        'arguments': [
            'entity'
        ]
    },
    'break': {
        'className': 'Break',
        'arguments': []
    },
    'changeScaleOfEntitySprite': {
        'className': 'ChangeScaleOfEntitySprite',
        'arguments': [
            'entity',
            'scale'
        ]
    },
    'setPlayerName': {
        'className': 'SetPlayerName',
        'arguments': [
            'player',
            'name'
        ]
    },
    'makeUnitPickupItemAtSlot': {
        'className': 'MakeUnitPickupItemAtSlot',
        'arguments': [
            'unit',
            'item',
            'slotIndex'
        ]
    },
    'dropItemInInventorySlot': {
        'className': 'DropItemInInventorySlot',
        'arguments': [
            'unit',
            'slotIndex'
        ]
    },
    'unbanPlayerFromChat': {
        'className': 'UnbanPlayerFromChat',
        'arguments': [
            'player'
        ]
    },
    'changeDescriptionOfItem': {
        'className': 'ChangeDescriptionOfItem',
        'arguments': [
            'item',
            'string'
        ]
    },
    'sendChatMessageToPlayer': {
        'className': 'SendChatMessageToPlayer',
        'arguments': [
            'message',
            'player'
        ]
    },
    'playAdForEveryone': {
        'className': 'PlayAdForEveryone',
        'arguments': []
    },
    'hideUiTextForPlayer': {
        'className': 'HideUiTextForPlayer',
        'arguments': [
            'target',
            'entity'
        ]
    },
    'showUiTextForPlayer': {
        'className': 'ShowUiTextForPlayer',
        'arguments': [
            'target',
            'entity'
        ]
    },
    'resetDebrisPosition': {
        'className': 'ResetDebrisPosition',
        'arguments': [
            'entity'
        ]
    },
    'playMusic': {
        'className': 'PlayMusic',
        'arguments': [
            'music'
        ]
    },
    'assignPlayerType': {
        'className': 'AssignPlayerType',
        'arguments': [
            'entity',
            'playerType'
        ]
    },
    'playMusicForPlayer': {
        'className': 'PlayMusicForPlayer',
        'arguments': [
            'music',
            'player'
        ]
    },
    'makeUnitVisibleToNeutralPlayers': {
        'className': 'MakeUnitVisibleToNeutralPlayers',
        'arguments': [
            'entity'
        ]
    },
    'makeUnitVisibleToFriendlyPlayers': {
        'className': 'MakeUnitVisibleToFriendlyPlayers',
        'arguments': [
            'entity'
        ]
    },
    'makeUnitPickupItem': {
        'className': 'MakeUnitPickupItem',
        'arguments': [
            'unit',
            'item'
        ]
    },
    'giveNewItemWithQuantityToUnit': {
        'className': 'GiveNewItemWithQuantityToUnit',
        'arguments': [
            'itemType',
            'number',
            'unit'
        ]
    },
    'dropAllItems': {
        'className': 'DropAllItems',
        'arguments': [
            'entity'
        ]
    },
    'useItemOnce': {
        'className': 'UseItemOnce',
        'arguments': [
            'item'
        ]
    },
    'stopAcceptingPlayers': {
        'className': 'StopAcceptingPlayers',
        'arguments': []
    },
    'setEntityVelocityAtAngle': {
        'className': 'SetEntityVelocityAtAngle',
        'arguments': [
            'entity',
            'speed',
            'angle'
        ]
    },
    'setEntityAttributeMax': {
        'className': 'SetEntityAttributeMax',
        'arguments': [
            'attribute',
            'entity',
            'value'
        ]
    },
    'setPlayerAttributeMin': {
        'className': 'SetPlayerAttributeMin',
        'arguments': [
            'attributeType',
            'player',
            'number'
        ]
    },
    'makePlayerTradeWithPlayer': {
        'className': 'MakePlayerTradeWithPlayer',
        'arguments': [
            'playerA',
            'playerB'
        ]
    },
    'updateUiTextForTimeForPlayer': {
        'className': 'UpdateUiTextForTimeForPlayer',
        'arguments': [
            'target',
            'value',
            'player',
            'time'
        ]
    },
    'aiMoveToPosition': {
        'className': 'AiMoveToPosition',
        'arguments': [
            'unit',
            'position'
        ]
    },
    'aiAttackUnit': {
        'className': 'AiAttackUnit',
        'arguments': [
            'unit',
            'targetUnit'
        ]
    },
    'changeSensorRadius': {
        'className': 'ChangeSensorRadius',
        'arguments': [
            'sensor',
            'radius'
        ]
    },
    'loadPlayerDataAndApplyIt': {
        'className': 'LoadPlayerDataAndApplyIt',
        'arguments': [
            'player',
            'unit'
        ]
    },
    'createFloatingText': {
        'className': 'CreateFloatingText',
        'arguments': [
            'text',
            'position',
            'color'
        ]
    },
    'setLastAttackedUnit': {
        'className': 'SetLastAttackedUnit',
        'arguments': [
            'unit'
        ]
    },
    'setLastAttackingUnit': {
        'className': 'SetLastAttackingUnit',
        'arguments': [
            'unit'
        ]
    },
    'setItemFireRate': {
        'className': 'SetItemFireRate',
        'arguments': [
            'number',
            'item'
        ]
    },
    'applyImpulseOnEntityXY': {
        'className': 'ApplyImpulseOnEntityXY',
        'arguments': [
            'impulse_x',
            'impulse_y',
            'entity'
        ]
    },
    'playSoundForPlayer': {
        'className': 'PlaySoundForPlayer',
        'arguments': [
            'sound',
            'player'
        ]
    },
    'stopSoundForPlayer': {
        'className': 'StopSoundForPlayer',
        'arguments': [
            'sound',
            'player'
        ]
    },
    'showDismissibleInputModalToPlayer': {
        'className': 'ShowDismissibleInputModalToPlayer',
        'arguments': [
            'player',
            'inputLabel'
        ]
    },
    'setItemName': {
        'className': 'SetItemName',
        'arguments': [
            'name',
            'item'
        ]
    },
    'changeItemInventoryImage': {
        'className': 'ChangeItemInventoryImage',
        'arguments': [
            'url',
            'item'
        ]
    },
    'addAttributeBuffToUnit': {
        'className': 'AddAttributeBuffToUnit',
        'arguments': [
            'entity',
            'value',
            'attribute',
            'time'
        ]
    },
    'addPercentageAttributeBuffToUnit': {
        'className': 'AddPercentageAttributeBuffToUnit',
        'arguments': [
            'entity',
            'value',
            'attribute',
            'time'
        ]
    },
    'stunUnit': {
        'className': 'StunUnit',
        'arguments': [
            'unit'
        ]
    },
    'removeStunFromUnit': {
        'className': 'RemoveStunFromUnit',
        'arguments': [
            'unit'
        ]
    },
    'setLastAttackingItem': {
        'className': 'SetLastAttackingItem',
        'arguments': [
            'item'
        ]
    },
    'mutePlayerMicrophone': {
        'className': 'MutePlayerMicrophone',
        'arguments': [
            'player'
        ]
    },
    'unmutePlayerMicrophone': {
        'className': 'UnmutePlayerMicrophone',
        'arguments': [
            'player'
        ]
    },
    'sendPostRequest': {
        'className': 'SendPostRequest',
        'arguments': [
            'string',
            'url',
            'varName'
        ]
    },
    'loadUnitDataFromString': {
        'className': 'LoadUnitDataFromString',
        'arguments': [
            'string',
            'unit'
        ]
    },
    'loadPlayerDataFromString': {
        'className': 'LoadPlayerDataFromString',
        'arguments': [
            'string',
            'player'
        ]
    },
    'removeAllAttributeBuffs': {
        'className': 'RemoveAllAttributeBuffs',
        'arguments': [
            'unit'
        ]
    },
    'changeInventorySlotColor': {
        'className': 'ChangeInventorySlotColor',
        'arguments': [
            'item',
            'string'
        ]
    },
    'setOwnerUnitOfProjectile': {
        'className': 'SetOwnerUnitOfProjectile',
        'arguments': [
            'unit',
            'projectile'
        ]
    },
    'enableAI': {
        'className': 'EnableAI',
        'arguments': [
            'unit'
        ]
    },
    'disableAI': {
        'className': 'DisableAI',
        'arguments': [
            'unit'
        ]
    },
    'aiGoIdle': {
        'className': 'AiGoIdle',
        'arguments': [
            'unit'
        ]
    }
}