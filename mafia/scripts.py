from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Script, Trigger, UiTarget, Flip

from game_variables import *


class Initialize(Script):
    def _build(self):
        self.key = 'initialize'
        self.triggers = [Trigger.GAME_START]
        self.actions = [
            assign_player_type(Variables.AI, PlayerTypes.AI),
            assign_player_type(Variables.GRAVEYARD_MANAGER,
                               PlayerTypes.AI_SHOW_S_NAME),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.NIGHT, Variables.AI, XyCoordinate('1024', '1024'), '2200', '2200', '0'),
            set_variable(Variables.NIGHT_UNIT, LastCreatedUnit()),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.HANGER, Variables.AI, XyCoordinate(1061, 1037), 45.31, 87.5, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.MAP, Variables.AI, XyCoordinate('1024', '1024'), '2048', '2048', '0'),
            for_all_regions(AllRegions(), [
                if_else(Condition(StringStartsWith(NameOfRegion(SelectedRegion()), 'boundary'), '==', True), [
                        create_entity_for_player_at_position_with_dimensions(UnitTypes.BOUNDARY, Variables.AI, CenterOfRegion(
                            SelectedRegion()), HeightOfRegion(SelectedRegion()), WidthOfRegion(SelectedRegion()), 0),

                        ], [

                ]),

            ]),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(483, 1201), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1950, 50), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1789, 71), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1867, 175), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1539, 72), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1661, 6), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1664, 123), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1778, 164), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1909, 295), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1469, 359), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1662, 277), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(2001, 185), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1803, 313), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1518, 202), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1411, 71), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1637, 445), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(2024, 325), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1789, 71), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1326, 293), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1828, 461), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1099, 450), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(193, 1798), '139.5', 144, '0'),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(306, 1893), '139.5', 144, '0'),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1979, 446), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1727, 646), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1927, 718), 139.5, 144, 0),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(1846, 9), '139.5', 144, '0'),
            create_entity_for_player_at_position_with_dimensions(
                UnitTypes.TREE, Variables.AI, XyCoordinate(2027, 86), '139.5', 144, '0'),

        ]


# ╭
# PLAYER EVENTS
# |

class PlayerJoins(Script):
    def _build(self):
        self.key = 'playerJoinsGame'
        self.triggers = [Trigger.PLAYER_JOINS_GAME]
        self.actions = [
            send_chat_message_to_player(
                'Welcome to mafia! press P for help', LastTriggeringPlayer()),
            assign_player_type(LastTriggeringPlayer(), PlayerTypes.VILLAGERS),
            load_player_data_and_apply_it(LastTriggeringPlayer(), Undefined()),
            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.UNBAN_TIME, LastTriggeringPlayer()), '!=', 0), [
                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.UNBAN_TIME, LastTriggeringPlayer()), '<=', CurrentTimeStamp()), [
                    set_player_variable(
                        LastTriggeringPlayer(), PlayerVariables.UNBAN_TIME, 0),
                    send_chat_message_to_player(
                        'Your ban has ended', LastTriggeringPlayer()),

                ], [
                    if_else(Condition(StringContainsString(Variables.UNBAN_WAITING_LIST, Concat('''"''', Concat(PlayerName(LastTriggeringPlayer()), '''"'''))), '==', True), [
                        set_player_variable(
                            LastTriggeringPlayer(), PlayerVariables.UNBAN_TIME, 0),
                        send_chat_message_to_player(
                            'You have been unbanned by a mod', LastTriggeringPlayer()),
                        for_range(Variables.G, 0, LengthOfString(Variables.UNBAN_WAITING_LIST), [
                            if_else(Condition(StringArrayElement(Variables.G, Variables.UNBAN_WAITING_LIST), '==', PlayerName(LastTriggeringPlayer())), [
                                set_variable(Variables.UNBAN_WAITING_LIST, RemoveStringArrayElement(
                                    Variables.G, Variables.UNBAN_WAITING_LIST)),

                            ], [

                            ]),

                        ]),

                    ], [
                        send_chat_message_to_player(Concat('You will be unbanned in ', Concat(Calculate(Calculate(ValueOfPlayerVariable(
                            PlayerVariables.UNBAN_TIME, LastTriggeringPlayer()), '-', CurrentTimeStamp()), '/', 60000), ' minutes')), LastTriggeringPlayer()),
                        kick_player(LastTriggeringPlayer()),
                        return_loop(),

                    ]),

                ]),

            ], [

            ]),
            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, LastTriggeringPlayer()), '==', 0), [
                set_player_variable(LastTriggeringPlayer(
                ), PlayerVariables.SKIN_NUMBER, RandomNumberBetween(1, 70)),

            ], [

            ]),
            if_else(Condition(IsPlayerLoggedIn(LastTriggeringPlayer()), '==', False), [
                set_player_name(LastTriggeringPlayer(), Concat(StringArrayElement(RandomNumberBetween(0, Calculate(
                    StringArrayLength(Variables.NAMES), '-', 1)), Variables.NAMES), RandomNumberBetween(1001, 9999))),

            ], [

            ]),
            if_else(Condition(Condition(Condition(Variables.STATE, '!=', 'round-end'), 'AND', Condition(Variables.STATE, '!=', 'ready-up-time')), 'AND', Condition(Variables.STATE, '!=', 'pre-round-1')), [
                create_unit_for_player_at_position(
                    UnitTypes.DEAD, LastTriggeringPlayer(), CenterOfRegion(Regions.SPAWN), 0),
                ban_player_from_chat(LastTriggeringPlayer()),
                send_chat_message_to_player(
                    'Press C to access the dead chat', LastTriggeringPlayer()),
                open_dialogue_for_player(
                    Dialogues.GAME_INFO, LastTriggeringPlayer()),
                assign_player_type(
                    LastTriggeringPlayer(), PlayerTypes.DEAD),

            ], [
                create_unit_for_player_at_position(
                    UnitTypes.LOBBY_UNIT, LastTriggeringPlayer(), CenterOfRegion(Regions.SPAWN), 0),
                set_variable(Variables.CHANGE_UNIT, LastCreatedUnit()),
                run_script('I4fUUokJaS'),

            ]),
            player_camera_track_unit(
                LastTriggeringPlayer(), LastCreatedUnit()),

        ]


class PlayerLeaves(Script):
    def _build(self):
        self.key = 'playerLeavesGame'
        self.triggers = [Trigger.PLAYER_LEAVES_GAME]
        self.actions = [
            save_player_data(LastTriggeringPlayer()),
            if_else(Condition(StringContainsString(Variables.CULT_MEMBERS, PlayerId(LastTriggeringPlayer())), '==', True), [
                for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.CULT_MEMBERS), '-', 1), [
                    if_else(Condition(StringArrayElement(Variables.I, Variables.CULT_MEMBERS), '==', PlayerId(LastTriggeringPlayer())), [
                        set_variable(Variables.CULT_MEMBERS, RemoveStringArrayElement(
                            Variables.I, Variables.CULT_MEMBERS)),
                        break_loop(),

                    ], [

                    ]),

                ]),

            ], [

            ]),
            if_else(Condition(Condition(Variables.EXECUTIONER, '!=', Undefined()), 'AND', Condition(LastTriggeringPlayer(), '==', Variables.EXECUTIONER_TARGET)), [
                if_else(Condition(Condition(Condition(Variables.STATE, '!=', 'round-end'), 'AND', Condition(Variables.STATE, '!=', 'ready-up-time')), 'AND', Condition(Variables.STATE, '!=', 'pre-round-1')), [
                    if_else(Condition(PlayerTypeOfPlayer(LastTriggeringPlayer()), '!=', PlayerTypes.DEAD), [
                        if_else(Condition(Variables.LYNCHING_PLAYER, '!=', Variables.EXECUTIONER_TARGET), [
                            set_player_variable(
                                Variables.EXECUTIONER, PlayerVariables.ROLE, 'joker'),
                            send_chat_message_to_player(
                                'Your target left so you turned into a joker!', Variables.EXECUTIONER),
                            for_all_units(AllUnitsOwnedByPlayer(Variables.EXECUTIONER), [
                                set_variable(
                                    Variables.TEMP_UNIT, SelectedUnit()),
                                run_script('kI6LRzkLcf'),

                            ]),
                            set_variable(
                                Variables.EXECUTIONER, Undefined()),

                        ], [
                            if_else(Condition(Variables.STATE, '!=', 'lynch-time'), [
                                update_ui_text_for_time_for_player(UiTarget.CENTER, Concat(
                                    PlayerName(Variables.LYNCHING_PLAYER), ' wins!'), Undefined(), 7500),
                                send_chat_message(
                                    "The executioner's target left while he was about to be lynched..."),
                                set_variable(
                                    Variables.DIALOGUE_TITLE, 'The executioner wins!'),
                                set_player_attribute(AttributeTypes.WINS, Variables.EXECUTIONER, Calculate(
                                    PlayerAttribute(AttributeTypes.WINS, Variables.EXECUTIONER), '+', 1)),
                                run_script(
                                    'UvglYEu3P5'),

                            ], [

                            ]),

                        ]),

                    ], [

                    ]),

                ], [

                ]),

            ], [
                if_else(Condition(LastTriggeringPlayer(), '==', Variables.EXECUTIONER), [
                    set_variable(
                        Variables.EXECUTIONER, Undefined()),

                ], [
                    if_else(Condition(LastTriggeringPlayer(), '==', Variables.GODFATHER), [
                        set_variable(
                            Variables.GODFATHER, Undefined()),
                        set_variable(
                            Variables.GODFATHER_IS_PRESENT, False),

                    ], [
                        if_else(Condition(LastTriggeringPlayer(), '==', Variables.CULTIST), [
                            set_variable(
                                Variables.CULTIST, Undefined()),
                            set_variable(
                                Variables.CULT_MEMBERS, '[]'),

                        ], [

                        ]),

                    ]),

                ]),

            ]),
            for_all_units(AllUnitsOwnedByPlayer(LastTriggeringPlayer()), [
                if_else(Condition(Condition(UnitTypeOfUnit(SelectedUnit()), '==', UnitTypes.LOBBY_UNIT), 'AND', Condition(EntityAttribute(AttributeTypes.READY, SelectedUnit()), '==', 1)), [
                        decrease_variable_by_number(
                            Variables.PLAYERS_READIED_UP, 1),

                        ], [

                ]),
                destroy_entity(SelectedUnit()),

            ]),

        ]


class WhenAPlayerSubmitsCustomInputModal(Script):
    def _build(self):
        self.key = 'iGpHeSEKhW'
        self.triggers = [Trigger.PLAYER_CUSTOM_INPUT]
        self.actions = [
            if_else(Condition(StringStartsWith(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer()), 'tempBan'), '==', True), [
                set_variable(Variables.TEMP_STRING, SubstringOf(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer(
                )), 9, LengthOfString(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer())))),
                if_else(Condition(StringContainsString(Variables.MODS, PlayerName(PlayerFromId(Variables.TEMP_STRING))), '==', False), [
                    set_player_variable(PlayerFromId(Variables.TEMP_STRING), PlayerVariables.UNBAN_TIME, Calculate(
                        CurrentTimeStamp(), '+', Calculate(StringToNumber(PlayerCustomInput(LastTriggeringPlayer())), '*', 60000))),
                    send_chat_message_to_player(Concat('You have been banned for ', Concat(PlayerCustomInput(
                        LastTriggeringPlayer()), ' minutes')), PlayerFromId(Variables.TEMP_STRING)),
                    send_chat_message_to_player(Concat(Concat('You have banned ', Concat(PlayerName(PlayerFromId(Variables.TEMP_STRING)), ' for ')), Concat(Calculate(Calculate(
                        ValueOfPlayerVariable(PlayerVariables.UNBAN_TIME, PlayerFromId(Variables.TEMP_STRING)), '-', CurrentTimeStamp()), '/', 60000), ' minutes')), LastTriggeringPlayer()),
                    kick_player(PlayerFromId(
                        Variables.TEMP_STRING)),
                    break_loop(),

                ], [
                    send_chat_message_to_player(
                        "You can't temp-ban another mod", LastTriggeringPlayer()),

                ]),

            ], [
                if_else(Condition(PlayerTypeOfPlayer(LastTriggeringPlayer()), '==', PlayerTypes.DEAD), [
                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer()), '==', 'message'), [
                        for_all_players(AllHumanPlayers(), [
                            if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypes.DEAD), [
                                send_chat_message_to_player(Concat(PlayerName(LastTriggeringPlayer()), Concat(
                                    ': ', PlayerCustomInput(LastTriggeringPlayer()))), SelectedPlayer()),

                            ], [

                            ]),

                        ]),

                    ], [

                    ]),

                ], [
                    if_else(Condition(Variables.STATE, '==', 'night-time'), [
                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer()), '==', 'message'), [
                            for_all_players(AllHumanPlayers(), [
                                if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypeOfPlayer(LastTriggeringPlayer())), [
                                    send_chat_message_to_player(Concat(Concat(PlayerName(LastTriggeringPlayer()), Concat(' (', Concat(ValueOfPlayerVariable(
                                        PlayerVariables.ROLE, LastTriggeringPlayer()), ')'))), Concat(': ', PlayerCustomInput(LastTriggeringPlayer()))), SelectedPlayer()),
                                    break_loop(),

                                ], [

                                ]),

                            ]),

                        ], [
                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer()), '==', 'vote'), [
                                set_variable(
                                    Variables.TEMP_PLAYER, Undefined()),
                                for_all_players(AllHumanPlayers(), [
                                    if_else(Condition(PlayerCustomInput(LastTriggeringPlayer()), '==', PlayerName(SelectedPlayer())), [
                                        set_variable(
                                            Variables.TEMP_PLAYER, SelectedPlayer()),
                                        break_loop(),

                                    ], [

                                    ]),

                                ]),
                                if_else(Condition(Variables.TEMP_PLAYER, '!=', Undefined()), [
                                    if_else(Condition(PlayerTypeOfPlayer(Variables.TEMP_PLAYER), '!=', PlayerTypes.DEAD), [
                                        set_player_variable(
                                            LastTriggeringPlayer(), PlayerVariables.DID_VOTE, True),
                                        if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'mafia'), 'OR', Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', Variables.GODFATHER)), [
                                            if_else(Condition(PlayerTypeOfPlayer(Variables.TEMP_PLAYER), '==', PlayerTypes.MAFIA), [
                                                set_player_variable(
                                                    LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                send_chat_message_to_player(
                                                    "you can't vote against another evil player!", LastTriggeringPlayer()),
                                                return_loop(),

                                            ], [

                                            ]),
                                            set_variable(Variables.MAFIA_VOTES, InsertStringArrayElement(
                                                PlayerId(Variables.TEMP_PLAYER), Variables.MAFIA_VOTES)),
                                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', Variables.GODFATHER), [
                                                set_variable(Variables.MAFIA_VOTES, InsertStringArrayElement(
                                                    PlayerId(Variables.TEMP_PLAYER), Variables.MAFIA_VOTES)),

                                            ], [

                                            ]),
                                            for_all_players(AllHumanPlayers(), [
                                                if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypeOfPlayer(LastTriggeringPlayer())), [
                                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', Variables.GODFATHER), [
                                                        send_chat_message_to_player(Concat(PlayerName(LastTriggeringPlayer()), Concat(
                                                            ' voted to kill ', Concat(PlayerName(Variables.TEMP_PLAYER), ' (doubled)'))), SelectedPlayer()),

                                                    ], [
                                                        send_chat_message_to_player(Concat(PlayerName(LastTriggeringPlayer()), Concat(
                                                            ' voted to kill ', PlayerName(Variables.TEMP_PLAYER))), SelectedPlayer()),

                                                    ]),

                                                ], [

                                                ]),

                                            ]),
                                            return_loop(),

                                        ], [
                                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'sheriff'), [
                                                send_chat_message_to_player(Concat('You have decided to investigate ', Concat(
                                                    PlayerName(Variables.TEMP_PLAYER), '...')), LastTriggeringPlayer()),
                                                send_chat_message_to_player(
                                                    '(results will be collected in the morning)', LastTriggeringPlayer()),
                                                set_variable(
                                                    Variables.INVESTIGATED_PLAYER, Variables.TEMP_PLAYER),

                                            ], [
                                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'doctor'), [
                                                    if_else(Condition(Variables.TEMP_PLAYER, '==', LastTriggeringPlayer()), [
                                                        set_player_variable(
                                                            LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                        send_chat_message_to_player(
                                                            "you can't save yourself!", LastTriggeringPlayer()),
                                                        return_loop(),

                                                    ], [

                                                    ]),
                                                    send_chat_message_to_player(Concat('You decided to heal ', PlayerName(
                                                        Variables.TEMP_PLAYER)), LastTriggeringPlayer()),
                                                    set_variable(
                                                        Variables.HEALED_PLAYER, Variables.TEMP_PLAYER),

                                                ], [
                                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'vigilante'), [
                                                        if_else(Condition(Variables.VIGILANTE_ARROWS, '>', 0), [
                                                            if_else(Condition(Variables.TEMP_PLAYER, '==', LastTriggeringPlayer()), [
                                                                set_player_variable(
                                                                    LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                                send_chat_message_to_player(
                                                                    "you can't shoot yourself!", LastTriggeringPlayer()),
                                                                return_loop(),

                                                            ], [

                                                            ]),
                                                            send_chat_message_to_player(Concat('You decided to shoot ', PlayerName(
                                                                Variables.TEMP_PLAYER)), LastTriggeringPlayer()),
                                                            set_variable(Variables.TO_DIE, InsertStringArrayElement(
                                                                PlayerId(Variables.TEMP_PLAYER), Variables.TO_DIE)),
                                                            decrease_variable_by_number(
                                                                Variables.VIGILANTE_ARROWS, 1),
                                                            if_else(Condition(PlayerTypeOfPlayer(Variables.TEMP_PLAYER), '==', PlayerTypes.VILLAGERS), [
                                                                set_variable(
                                                                    Variables.DID_VIGILANTE_SCREW_UP, True),

                                                            ], [

                                                            ]),

                                                        ], [
                                                            send_chat_message_to_player(
                                                                "You don't have any arrows left!", LastTriggeringPlayer()),

                                                        ]),

                                                    ], [
                                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'framer'), [
                                                            if_else(Condition(PlayerTypeOfPlayer(Variables.TEMP_PLAYER), '==', PlayerTypes.MAFIA), [
                                                                set_player_variable(
                                                                    LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                                send_chat_message_to_player(
                                                                    "you can't frame another evil player!", LastTriggeringPlayer()),
                                                                return_loop(),

                                                            ], [

                                                            ]),
                                                            if_else(Condition(PlayerTypeOfPlayer(Variables.TEMP_PLAYER), '!=', PlayerTypes.NEUTRAL), [
                                                                set_variable(
                                                                    Variables.FRAMED_PLAYER, Variables.TEMP_PLAYER),

                                                            ], [

                                                            ]),
                                                            for_all_players(AllHumanPlayers(), [
                                                                if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypeOfPlayer(LastTriggeringPlayer())), [
                                                                    send_chat_message_to_player(Concat(PlayerName(LastTriggeringPlayer()), Concat(
                                                                        ' decided to frame ', PlayerName(Variables.TEMP_PLAYER))), SelectedPlayer()),

                                                                ], [

                                                                ]),

                                                            ]),

                                                        ], [
                                                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'watcher'), [
                                                                send_chat_message_to_player(Concat('You decided to watch ', PlayerName(
                                                                    Variables.TEMP_PLAYER)), LastTriggeringPlayer()),
                                                                send_chat_message_to_player(
                                                                    '(results will be collected in the morning)', LastTriggeringPlayer()),
                                                                set_variable(
                                                                    Variables.WATCHER_TARGET, Variables.TEMP_PLAYER),

                                                            ], [
                                                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'cookie giver'), [
                                                                    if_else(Condition(Variables.TEMP_PLAYER, '==', LastTriggeringPlayer()), [
                                                                        set_player_variable(
                                                                            LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                                        send_chat_message_to_player(
                                                                            "you can't give a cookie to yourself", LastTriggeringPlayer()),
                                                                        return_loop(),

                                                                    ], [

                                                                    ]),
                                                                    send_chat_message_to_player(Concat('You gave a cookie to ', PlayerName(
                                                                        Variables.TEMP_PLAYER)), LastTriggeringPlayer()),
                                                                    set_variable(
                                                                        Variables.COOKIE_TARGET, Variables.TEMP_PLAYER),

                                                                ], [
                                                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', Variables.CULTIST), [
                                                                        if_else(Condition(StringContainsString(Variables.CULT_MEMBERS, PlayerId(Variables.TEMP_PLAYER)), '==', True), [
                                                                            set_player_variable(
                                                                                LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                                            send_chat_message_to_player(Concat(PlayerName(
                                                                                Variables.TEMP_PLAYER), ' is already a part of your cult'), LastTriggeringPlayer()),
                                                                            return_loop(),

                                                                        ], [
                                                                            if_else(Condition(Variables.TEMP_PLAYER, '==', LastTriggeringPlayer()), [
                                                                                set_player_variable(
                                                                                    LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                                                send_chat_message_to_player(
                                                                                    "You're the leader of the cult...", LastTriggeringPlayer()),
                                                                                return_loop(),

                                                                            ], [

                                                                            ]),

                                                                        ]),
                                                                        send_chat_message_to_player(Concat('You have chosen ', Concat(PlayerName(
                                                                            Variables.TEMP_PLAYER), ' to join your cult')), LastTriggeringPlayer()),
                                                                        set_variable(Variables.CULT_MEMBERS, InsertStringArrayElement(
                                                                            PlayerId(Variables.TEMP_PLAYER), Variables.CULT_MEMBERS)),

                                                                    ], [
                                                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'serial killer'), [
                                                                            if_else(Condition(Variables.TEMP_PLAYER, '==', LastTriggeringPlayer()), [
                                                                                set_player_variable(
                                                                                    LastTriggeringPlayer(), PlayerVariables.DID_VOTE, False),
                                                                                send_chat_message_to_player(
                                                                                    'you want to kill yourself? ...', LastTriggeringPlayer()),
                                                                                return_loop(),

                                                                            ], [

                                                                            ]),
                                                                            set_variable(Variables.TO_DIE, InsertStringArrayElement(
                                                                                PlayerId(Variables.TEMP_PLAYER), Variables.TO_DIE)),
                                                                            send_chat_message_to_player(Concat('You have selected ', Concat(PlayerName(
                                                                                Variables.TEMP_PLAYER), ' to die tonight')), LastTriggeringPlayer()),

                                                                        ], [

                                                                        ]),

                                                                    ]),

                                                                ]),

                                                            ]),

                                                        ]),

                                                    ]),

                                                ]),

                                            ]),

                                        ]),
                                        if_else(Condition(Condition(Variables.TEMP_PLAYER, '==', Variables.WATCHER_TARGET), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '!=', 'watcher')), [
                                            set_variable(Variables.WATCHER_TARGET_VISITORS, InsertStringArrayElement(
                                                PlayerName(LastTriggeringPlayer()), Variables.WATCHER_TARGET_VISITORS)),

                                        ], [

                                        ]),

                                    ], [
                                        send_chat_message_to_player(Concat(PlayerCustomInput(LastTriggeringPlayer(
                                        )), ' is not a valid player (they are dead)'), LastTriggeringPlayer()),

                                    ]),

                                ], [
                                    send_chat_message_to_player(Concat(PlayerCustomInput(
                                        LastTriggeringPlayer()), ' is not a valid player name'), LastTriggeringPlayer()),

                                ]),

                            ], [

                            ]),

                        ]),

                    ], [
                        if_else(Condition(Variables.STATE, '==', 'day-time'), [
                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.CURRENTLY_INPUTTING, LastTriggeringPlayer()), '==', 'lynch'), [
                                if_else(Condition(PlayerCustomInput(LastTriggeringPlayer()), '==', ''), [
                                    send_chat_message(
                                        Concat(PlayerName(LastTriggeringPlayer()), ' has decided to abstain')),
                                    set_player_variable(
                                        LastTriggeringPlayer(), PlayerVariables.DID_VOTE, True),
                                    increase_variable_by_number(
                                        Variables.PLAYERS_VOTED, 1),
                                    increase_variable_by_number(
                                        Variables.PLAYERS_ABSTAINED, 1),
                                    if_else(Condition(Variables.TIMER, '>', 25), [
                                        decrease_variable_by_number(
                                            Variables.TIMER, 7),

                                    ], [

                                    ]),

                                ], [
                                    set_variable(
                                        Variables.TEMP_PLAYER, Undefined()),
                                    for_all_players(AllHumanPlayers(), [
                                        if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), [
                                            if_else(Condition(PlayerName(SelectedPlayer()), '==', PlayerCustomInput(LastTriggeringPlayer())), [
                                                set_variable(
                                                    Variables.TEMP_PLAYER, SelectedPlayer()),
                                                break_loop(),

                                            ], [

                                            ]),

                                        ], [

                                        ]),

                                    ]),
                                    if_else(Condition(Variables.TEMP_PLAYER, '!=', Undefined()), [
                                        if_else(Condition(Variables.TEMP_PLAYER, '==', LastTriggeringPlayer()), [
                                            send_chat_message_to_player(
                                                "you can't vote for yourself!", LastTriggeringPlayer()),
                                            return_loop(),

                                        ], [

                                        ]),
                                        set_player_variable(
                                            LastTriggeringPlayer(), PlayerVariables.DID_VOTE, True),
                                        set_variable(Variables.LYNCH_VOTES, InsertStringArrayElement(
                                            PlayerId(Variables.TEMP_PLAYER), Variables.LYNCH_VOTES)),
                                        if_else(Condition(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastTriggeringPlayer()), '==', 'mayor'), 'AND', Condition(Variables.DID_MAYOR_REVAL, '==', True)), 'OR', Condition(Variables.COOKIE_TARGET, '==', LastTriggeringPlayer())), [
                                            send_chat_message(Concat(PlayerName(LastTriggeringPlayer()), Concat(
                                                ' voted to lynch ', Concat(PlayerCustomInput(LastTriggeringPlayer()), ' (doubled)')))),
                                            set_variable(Variables.LYNCH_VOTES, InsertStringArrayElement(
                                                PlayerId(Variables.TEMP_PLAYER), Variables.LYNCH_VOTES)),

                                        ], [
                                            send_chat_message(Concat(PlayerName(LastTriggeringPlayer()), Concat(
                                                ' voted to lynch ', PlayerCustomInput(LastTriggeringPlayer())))),

                                        ]),
                                        increase_variable_by_number(
                                            Variables.PLAYERS_VOTED, 1),
                                        if_else(Condition(Variables.TIMER, '>', 25), [
                                            decrease_variable_by_number(
                                                Variables.TIMER, 7),

                                        ], [

                                        ]),

                                    ], [
                                        send_chat_message_to_player(Concat(PlayerCustomInput(
                                            LastTriggeringPlayer()), ' is not a valid player name'), LastTriggeringPlayer()),

                                    ]),

                                ]),

                            ], [

                            ]),

                        ], [

                        ]),

                    ]),

                ]),

            ]),

        ]


class WhenPlayerSendsChatMessage(Script):
    def _build(self):
        self.key = 'VOorNon90B'
        self.triggers = [Trigger.PLAYER_SENDS_CHAT_MESSAGE]
        self.actions = [
            if_else(None(), [
                if_else(Condition(Condition(StringContainsString(Variables.MODS, Concat('''"''', Concat(PlayerName(LastTriggeringPlayer()), '''"'''))), '==', True), 'OR', Condition(StringContainsString(Variables.TRIAL_MODS, Concat('''"''', Concat(PlayerName(LastTriggeringPlayer()), '''"'''))), '==', True)), [
                    if_else(Condition(StringStartsWith(LastChatMessageSentByPlayer(LastTriggeringPlayer()), '/tempban'), '==', True), [
                        for_all_players(AllHumanPlayers(), [
                            if_else(Condition(StringEndsWith(LastChatMessageSentByPlayer(LastTriggeringPlayer()), PlayerName(SelectedPlayer())), '==', True), [
                                show_dismissible_input_modal_to_player(LastTriggeringPlayer(), Concat(
                                    'Ban ', Concat(PlayerName(SelectedPlayer()), ' for how many minutes?'))),
                                set_player_variable(LastTriggeringPlayer(), PlayerVariables.CURRENTLY_INPUTTING, Concat(
                                                    'tempBan', PlayerId(SelectedPlayer()))),
                                return_loop(),

                            ], [

                            ]),

                        ]),
                        send_chat_message_to_player(Concat(SubstringOf(LastChatMessageSentByPlayer(LastTriggeringPlayer()), 11, LengthOfString(
                            LastChatMessageSentByPlayer(LastTriggeringPlayer()))), ' is not a valid name'), LastTriggeringPlayer()),

                    ], [
                        if_else(Condition(StringStartsWith(LastChatMessageSentByPlayer(LastTriggeringPlayer()), '/unban'), '==', True), [
                            if_else(Condition(LengthOfString(LastChatMessageSentByPlayer(LastTriggeringPlayer())), '>=', 8), [
                                set_variable(Variables.UNBAN_WAITING_LIST, InsertStringArrayElement(SubstringOf(LastChatMessageSentByPlayer(
                                    LastTriggeringPlayer()), 9, LengthOfString(LastChatMessageSentByPlayer(LastTriggeringPlayer()))), Variables.UNBAN_WAITING_LIST)),
                                send_chat_message_to_player(Concat(StringArrayElement(Calculate(StringArrayLength(
                                                            Variables.UNBAN_WAITING_LIST), '-', 1), Variables.UNBAN_WAITING_LIST), ' will be unbanned the next time he joins'), LastTriggeringPlayer()),

                            ], [
                                send_chat_message_to_player(
                                    'please enter a player name to unban', LastTriggeringPlayer()),

                            ]),

                        ], [
                            if_else(Condition(StringContainsString(Variables.MODS, Concat('''"''', Concat(PlayerName(LastTriggeringPlayer()), '''"'''))), '==', True), [
                                if_else(Condition(StringContainsString(LastChatMessageSentByPlayer(LastTriggeringPlayer()), 'skipState'), '==', True), [
                                    set_variable(
                                        Variables.TIMER, 0),

                                ], [
                                    if_else(Condition(StringContainsString(LastChatMessageSentByPlayer(LastTriggeringPlayer()), 'reset'), '==', True), [
                                        set_variable(
                                            Variables.DIALOGUE_TITLE, 'Round was terminated'),
                                        send_chat_message(
                                            Concat('Round was terminated by ', PlayerName(LastTriggeringPlayer()))),
                                        run_script(
                                            'UvglYEu3P5'),

                                    ], [
                                        if_else(Condition(StringContainsString(LastChatMessageSentByPlayer(LastTriggeringPlayer()), 'points'), '==', True), [
                                            set_player_attribute(AttributeTypes.WINS, LastTriggeringPlayer(), Calculate(
                                                PlayerAttribute(AttributeTypes.WINS, LastTriggeringPlayer()), '+', 2)),

                                        ], [
                                            if_else(Condition(StringContainsString(LastChatMessageSentByPlayer(LastTriggeringPlayer()), 'test'), '==', True), [
                                                comment(
                                                    'for testing purposes'),
                                                send_chat_message(
                                                    Concat('current time: ', CurrentTimeStamp())),

                                            ], [

                                            ]),

                                        ]),

                                    ]),

                                ]),

                            ], [
                                if_else(Condition(StringContainsString(Variables.TRIAL_MODS, Concat('''"''', Concat(PlayerName(LastTriggeringPlayer()), '''"'''))), '==', True), [
                                    if_else(Condition(StringStartsWith(LastChatMessageSentByPlayer(LastTriggeringPlayer()), '/kick'), '==', True), [
                                        for_all_players(AllHumanPlayers(), [
                                            if_else(Condition(StringEndsWith(LastChatMessageSentByPlayer(LastTriggeringPlayer()), PlayerName(SelectedPlayer())), '==', True), [
                                                send_chat_message_to_player(Concat(PlayerName(
                                                    SelectedPlayer()), ' was kicked successfully'), LastTriggeringPlayer()),
                                                kick_player(
                                                    SelectedPlayer()),
                                                return_loop(),

                                            ], [

                                            ]),

                                        ]),
                                        send_chat_message_to_player(
                                            'Invalid player name', LastTriggeringPlayer()),

                                    ], [

                                    ]),

                                ], [

                                ]),

                            ]),

                        ]),

                    ]),

                ], [

                ]),

            ], [

            ]),

        ]


# ╭
# KEYBINDS
# |

class ReadyUp(Script):
    def _build(self):
        self.key = 'gjjYQFDyEf'
        self.triggers = []
        self.actions = [
            if_else(Condition(Condition(Variables.STATE, '==', 'ready-up-time'), 'OR', Condition(Variables.STATE, '==', 'pre-round-1')), [
                if_else(Condition(EntityAttribute(AttributeTypes.READY, LastCastingUnit()), '==', 0), [
                    set_entity_attribute(
                        AttributeTypes.READY, LastCastingUnit(), 1),
                    send_chat_message(
                        Concat(PlayerName(OwnerOfEntity(LastCastingUnit())), ' readied up')),
                    set_entity_attribute(
                        AttributeTypes.AFK_TIMER, LastCastingUnit(), 100),
                    increase_variable_by_number(
                        Variables.PLAYERS_READIED_UP, 1),

                ], [

                ]),

            ], [

            ]),

        ]


class GameInfo(Script):
    def _build(self):
        self.key = 'eFVnfNgRPx'
        self.triggers = []
        self.actions = [
            open_dialogue_for_player(
                Dialogues.GAME_INFO, OwnerOfEntity(LastCastingUnit())),

        ]


class ViewRole(Script):
    def _build(self):
        self.key = 'xVYMut2B2Q'
        self.triggers = []
        self.actions = [
            set_variable(Variables.TEMP_UNIT, LastCastingUnit()),
            run_script('kI6LRzkLcf'),

        ]


class TalkWithOthers(Script):
    def _build(self):
        self.key = 'j0HBhYvEw7'
        self.triggers = []
        self.actions = [
            if_else(Condition(UnitTypeOfUnit(LastCastingUnit()), '==', UnitTypes.DEAD), [
                show_dismissible_input_modal_to_player(OwnerOfEntity(
                    LastCastingUnit()), 'Send a message to the dead chat'),
                set_player_variable(OwnerOfEntity(
                    LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'message'),

            ], [
                if_else(Condition(Variables.STATE, '==', 'night-time'), [
                    if_else(Condition(PlayerTypeOfPlayer(OwnerOfEntity(LastCastingUnit())), '==', PlayerTypes.MAFIA), [
                        show_dismissible_input_modal_to_player(OwnerOfEntity(
                            LastCastingUnit()), 'Enter a message to send to your fellow mafias'),
                        set_player_variable(OwnerOfEntity(
                                            LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'message'),

                    ], [

                    ]),

                ], [

                ]),

            ]),

        ]


class UseAbility(Script):
    def _build(self):
        self.key = 'y5oW0UPEj3'
        self.triggers = []
        self.actions = [
            if_else(Condition(Condition(Variables.STATE, '==', 'night-time'), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.DID_VOTE, OwnerOfEntity(LastCastingUnit())), '==', False)), [
                if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'mafia'), 'OR', Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', Variables.GODFATHER)), [
                    show_dismissible_input_modal_to_player(OwnerOfEntity(
                        LastCastingUnit()), 'Vote someone to kill (enter their name)'),
                    set_player_variable(OwnerOfEntity(
                        LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                ], [
                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'sheriff'), [
                        show_dismissible_input_modal_to_player(OwnerOfEntity(
                            LastCastingUnit()), 'Choose someone to investigate (enter their name)'),
                        set_player_variable(OwnerOfEntity(
                                            LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                    ], [
                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'doctor'), [
                            show_dismissible_input_modal_to_player(OwnerOfEntity(
                                LastCastingUnit()), 'Choose someone to save (enter their name)'),
                            set_player_variable(OwnerOfEntity(
                                LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                        ], [
                            if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'mayor'), 'AND', Condition(Variables.DID_MAYOR_REVAL, '==', False)), [
                                open_dialogue_for_player(
                                    Dialogues.MAYOR_REVEAL_CHOICE, OwnerOfEntity(LastCastingUnit())),

                            ], [
                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'vigilante'), [
                                    show_dismissible_input_modal_to_player(OwnerOfEntity(LastCastingUnit()), Concat(
                                        'Who do you want to shoot? (', Concat(Variables.VIGILANTE_ARROWS, ' arrows left)'))),
                                    set_player_variable(OwnerOfEntity(
                                        LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                                ], [
                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'framer'), [
                                        show_dismissible_input_modal_to_player(OwnerOfEntity(
                                            LastCastingUnit()), 'Who do you want to frame? (enter their name)'),
                                        set_player_variable(OwnerOfEntity(
                                            LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                                    ], [
                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'watcher'), [
                                            show_dismissible_input_modal_to_player(OwnerOfEntity(
                                                LastCastingUnit()), 'Who do you want to watch? (enter their name)'),
                                            set_player_variable(OwnerOfEntity(
                                                LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                                        ], [
                                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'cookie giver'), [
                                                show_dismissible_input_modal_to_player(OwnerOfEntity(
                                                    LastCastingUnit()), 'Who do you want to give a cookie to? (enter their name)'),
                                                set_player_variable(OwnerOfEntity(
                                                    LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                                            ], [
                                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', Variables.CULTIST), [
                                                    show_dismissible_input_modal_to_player(OwnerOfEntity(
                                                        LastCastingUnit()), 'Hoax someone to join your cult (enter their name)'),
                                                    set_player_variable(OwnerOfEntity(
                                                        LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                                                ], [
                                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(LastCastingUnit())), '==', 'serial killer'), [
                                                        show_dismissible_input_modal_to_player(OwnerOfEntity(
                                                            LastCastingUnit()), 'Select someone to kill (enter their name)'),
                                                        set_player_variable(OwnerOfEntity(
                                                            LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'vote'),

                                                    ], [

                                                    ]),

                                                ]),

                                            ]),

                                        ]),

                                    ]),

                                ]),

                            ]),

                        ]),

                    ]),

                ]),

            ], [
                if_else(Condition(Condition(Variables.STATE, '==', 'day-time'), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.DID_VOTE, OwnerOfEntity(LastCastingUnit())), '==', False)), [
                    show_dismissible_input_modal_to_player(OwnerOfEntity(LastCastingUnit(
                    )), 'Vote someone to lynch (submit nothing if you want to abstain)'),
                    set_player_variable(OwnerOfEntity(
                        LastCastingUnit()), PlayerVariables.CURRENTLY_INPUTTING, 'lynch'),

                ], [

                ]),

            ]),

        ]


class OpenSkinShop(Script):
    def _build(self):
        self.key = 'ohUsuklIoJ'
        self.triggers = []
        self.actions = [
            open_shop_for_player(
                Shops.SKIN_SHOP, OwnerOfEntity(LastCastingUnit())),

        ]


class OpenBoredDialogue(Script):
    def _build(self):
        self.key = 'MUVhlLj8qB'
        self.triggers = []
        self.actions = [
            open_dialogue_for_player(
                Dialogues.HELP_BOREDOM, OwnerOfEntity(LastCastingUnit())),

        ]


class ResetAfkTimer(Script):
    def _build(self):
        self.key = 'ap115gJBBZ'
        self.triggers = []
        self.actions = [
            set_entity_attribute(AttributeTypes.AFK_TIMER,
                                 LastCastingUnit(), 100),

        ]


# |
# ╰

# |
# ╰

# ╭
# UNIT EVENTS
# |

class WhenAUnitsAttributeBecomes0OrLess(Script):
    def _build(self):
        self.key = 'maVFxjmk9i'
        self.triggers = [Trigger.UNIT_ATTRIBUTE_BECOMES_ZERO]
        self.actions = [
            if_else(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '==', UnitTypes.KNIFE), [
                if_else(Condition(AttributeTypeOfAttribute(TriggeringAttribute()), '==', AttributeTypes.HEALTH), [
                    destroy_entity(LastTriggeringUnit()),

                ], [

                ]),

            ], [
                if_else(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '==', UnitTypes.LOBBY_UNIT), [
                    if_else(Condition(AttributeTypeOfAttribute(TriggeringAttribute()), '==', AttributeTypes.AFK_TIMER), [
                        send_chat_message_to_player(
                            'you were kicked for afk activity', OwnerOfEntity(LastTriggeringUnit())),
                        kick_player(OwnerOfEntity(
                            LastTriggeringUnit())),

                    ], [

                    ]),

                ], [

                ]),

            ]),

        ]


class WhenAUnitEntersARegion(Script):
    def _build(self):
        self.key = 'USxUCjdHsD'
        self.triggers = [Trigger.UNIT_ENTERS_REGION]
        self.actions = [
            if_else(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '!=', UnitTypes.DEAD), [
                if_else(Condition(StringStartsWith(NameOfRegion(LastTriggeringRegion()), 'mud'), '==', True), [
                    create_floating_text('trudge trudge', EntityPosition(
                        LastTriggeringUnit()), '#804d52'),

                ], [
                    if_else(Condition(StringStartsWith(NameOfRegion(LastTriggeringRegion()), 'water'), '==', True), [
                        create_floating_text('splish splash', EntityPosition(
                            LastTriggeringUnit()), '#7fbdd4'),

                    ], [

                    ]),

                ]),

            ], [

            ]),

        ]


class WhenUnitUsesItem(Script):
    def _build(self):
        self.key = 'CGT5D2lkXT'
        self.triggers = [Trigger.UNIT_USES_ITEM]
        self.actions = [
            set_player_variable(OwnerOfEntity(LastTriggeringUnit()), PlayerVariables.SKIN_NUMBER,
                                ValueOfEntityVariable(PlayerVariables.SKIN_NUMBER, LastUsedItem())),
            send_chat_message_to_player(Concat('You have changed your skin to ', ItemTypeName(
                ItemTypeOfItem(LastUsedItem()))), OwnerOfEntity(LastTriggeringUnit())),
            if_else(Condition(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '!=', UnitTypes.DEAD), 'AND', Condition(UnitTypeOfUnit(LastTriggeringUnit()), '!=', UnitTypes.MAYOR)), [
                set_variable(Variables.CHANGE_UNIT,
                             LastTriggeringUnit()),
                run_script('I4fUUokJaS'),

            ], [
                send_chat_message_to_player(
                    '(your skin will change on the next round)', OwnerOfEntity(LastTriggeringUnit())),

            ]),

        ]


# |
# ╰

# ╭
# TIME BASED EVENTS
# |

class EverySecond(Script):
    def _build(self):
        self.key = 'bxZFYUvR8u'
        self.triggers = [Trigger.EVERY_SECOND]
        self.actions = [
            if_else(Condition(Variables.TIMER, '<=', 0), [
                if_else(Condition(Variables.STATE, '==', 'pre-round-1'), [
                    set_variable(Variables.STATE, 'pre-round-2'),
                    set_variable(Variables.TIMER, 10),
                    if_else(Condition(StringToNumber(StringArrayElement(0, Variables.GAMEMODE_VOTES)), '>=', StringToNumber(StringArrayElement(1, Variables.GAMEMODE_VOTES))), [
                        set_variable(
                            Variables.GAMEMODE, 'classic'),
                        set_variable(
                            Variables.GAMEMODE_ROLES, Variables.OTHER_ROLES),

                    ], [
                        set_variable(
                            Variables.GAMEMODE, 'chaos'),
                        set_variable(
                            Variables.GAMEMODE_ROLES, Variables.CHAOS_ROLES),

                    ]),
                    run_script('88pzZdjoIK'),
                    send_chat_message(
                        'Press H to view your roles again'),
                    send_chat_message('Press P for game info'),

                ], [
                    if_else(Condition(Variables.STATE, '==', 'pre-round-2'), [
                        run_script('VVYggrkVzm'),
                        set_variable(
                            Variables.PLAYERS_READIED_UP, 0),

                    ], [
                        if_else(Condition(Variables.STATE, '==', 'night-time'), [
                            run_script('sx1o5NHSNp'),

                        ], [
                            if_else(Condition(Variables.STATE, '==', 'day-time'), [
                                run_script(
                                    'o4WXONJNWn'),

                            ], [
                                if_else(Condition(Variables.STATE, '==', 'plead-guilty'), [
                                    set_variable(
                                        Variables.STATE, 'final-vote'),
                                    set_variable(
                                        Variables.PLAYERS_VOTED, 0),
                                    run_script(
                                        'i9bdhnnTLy'),
                                    set_variable(
                                        Variables.TIMER, 20),

                                ], [
                                    if_else(Condition(Variables.STATE, '==', 'final-vote'), [
                                        run_script(
                                            'o4WXONJNWn'),

                                    ], [
                                        if_else(Condition(Variables.STATE, '==', 'lynch-time'), [
                                            run_script(
                                                'VVYggrkVzm'),

                                        ], [
                                            if_else(Condition(Variables.STATE, '==', 'round-end'), [
                                                set_variable(
                                                    Variables.STATE, 'ready-up-time'),

                                            ], [

                                            ]),

                                        ]),

                                    ]),

                                ]),

                            ]),

                        ]),

                    ]),

                ]),

            ], [
                decrease_variable_by_number(Variables.TIMER, 1),
                if_else(Condition(Variables.STATE, '==', 'day-time'), [
                    if_else(Condition(Variables.TIMER, '==', 75), [
                        send_chat_message(
                            'Press E to vote a player to lynch!'),

                    ], [

                    ]),
                    if_else(Condition(Condition(Variables.PLAYERS_ABSTAINED, '>', Calculate(Calculate(PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '/', 2)), 'AND', Condition(Variables.TIMER, '>', 10)), [
                        send_chat_message(
                            'more than half of the citizens abstained, moving onto the next stage'),
                        set_variable(Variables.TIMER, 10),

                    ], [
                        if_else(Condition(Condition(Variables.PLAYERS_VOTED, '==', Calculate(Calculate(PlayerCount(), '-', 1), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD))), 'AND', Condition(Variables.TIMER, '>', 15)), [
                            if_else(Condition(Calculate(PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '>', 4), [
                                send_chat_message(
                                    'basically everyone voted, moving onto the next stage in 15 seconds'),
                                set_variable(
                                    Variables.TIMER, 15),

                            ], [

                            ]),

                        ], [
                            if_else(Condition(Condition(Variables.PLAYERS_VOTED, '>', Calculate(Calculate(PlayerCount(), '-', 1), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD))), 'AND', Condition(Variables.TIMER, '>', 5)), [
                                send_chat_message(
                                    'everyone voted, moving onto the next stage in 5 seconds'),
                                set_variable(
                                    Variables.TIMER, 5),

                            ], [

                            ]),

                        ]),

                    ]),

                ], [
                    if_else(Condition(Variables.STATE, '==', 'final-vote'), [
                        if_else(Condition(Condition(Variables.PLAYERS_VOTED, '==', Calculate(Calculate(PlayerCount(), '-', 1), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD))), 'AND', Condition(Variables.TIMER, '>', 5)), [
                            send_chat_message(
                                'everyone voted, moving onto the next stage in 5 seconds'),
                            set_variable(
                                Variables.TIMER, 5),

                        ], [

                        ]),

                    ], [
                        if_else(Condition(Variables.STATE, '==', 'pre-round-1'), [
                            if_else(Condition(PlayerCount(), '<', 4), [
                                set_variable(
                                    Variables.STATE, 'ready-up-time'),

                            ], [

                            ]),

                        ], [

                        ]),

                    ]),

                ]),

            ]),
            if_else(Condition(Variables.STATE, '==', 'ready-up-time'), [
                if_else(Condition(PlayerCount(), '>', 4), [
                    set_variable(Variables.PLAYERS_NEEDED_TO_READY_UP, Calculate(
                        PlayerCount(), '-', MathFloor(Calculate(PlayerCount(), '/', 3)))),
                    for_all_players(AllHumanPlayers(), [
                                    for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                                        set_entity_attribute_regeneration_rate(
                                            AttributeTypes.AFK_TIMER, SelectedUnit(), -0.6),

                                    ]),

                                    ]),

                ], [
                    set_variable(
                        Variables.PLAYERS_NEEDED_TO_READY_UP, 4),

                ]),
                if_else(Condition(Variables.PLAYERS_READIED_UP, '>=', Variables.PLAYERS_NEEDED_TO_READY_UP), [
                    run_script('qSgJOHTuZF'),

                ], [

                ]),

            ], [

            ]),
            if_else(Condition(Calculate(PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '<=', 1), [
                set_variable(Variables.STATE, 'ready-up-time'),
                for_all_players(AllHumanPlayers(), [
                    for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                                if_else(Condition(UnitTypeOfUnit(SelectedUnit()), '!=', UnitTypes.LOBBY_UNIT), [
                                    destroy_entity(SelectedUnit()),
                                    create_unit_for_player_at_position(
                                        UnitTypes.LOBBY_UNIT, SelectedPlayer(), CenterOfRegion(Regions.SPAWN), 0),
                                    set_variable(
                                        Variables.CHANGE_UNIT, LastCreatedUnit()),
                                    run_script('I4fUUokJaS'),
                                    player_camera_track_unit(
                                        SelectedPlayer(), LastCreatedUnit()),
                                    unban_player_from_chat(
                                        SelectedPlayer()),
                                    assign_player_type(
                                        SelectedPlayer(), PlayerTypes.VILLAGERS),

                                ], [

                                ]),

                                ]),

                ]),
                set_entity_state(Variables.NIGHT_UNIT, States.DEFAULT),

            ], [

            ]),
            run_script('on2fQCyvGb'),

        ]


class UpdateOverlays(Script):
    def _build(self):
        self.key = 'on2fQCyvGb'
        self.triggers = []
        self.actions = [
            show_ui_text_for_everyone(UiTarget.TOP),
            show_ui_text_for_everyone(UiTarget.SCOREBOARD),
            if_else(Condition(Variables.STATE, '==', 'ready-up-time'), [
                update_ui_text_for_everyone(UiTarget.TOP, Concat('Press R to ready up! (', Concat(
                    Variables.PLAYERS_READIED_UP, Concat('/', Concat(Variables.PLAYERS_NEEDED_TO_READY_UP, ')'))))),
                update_ui_text_for_everyone(UiTarget.SCOREBOARD, ''),

            ], [
                if_else(Condition(Variables.STATE, '==', 'pre-round-1'), [
                    update_ui_text_for_everyone(UiTarget.TOP, Concat(
                        'Round starting in ', Concat(Variables.TIMER, ' seconds'))),
                    update_ui_text_for_everyone(
                        UiTarget.SCOREBOARD, ''),

                ], [
                    update_ui_text_for_everyone(UiTarget.SCOREBOARD, Concat(Concat('Gamemode: ', Variables.GAMEMODE), Concat(
                        Variables.BREAK, Concat('Players Alive: ', Calculate(PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)))))),
                    if_else(Condition(Variables.STATE, '==', 'pre-round-2'), [
                        update_ui_text_for_everyone(UiTarget.TOP, Concat(
                            'Night arrives in ', Concat(Variables.TIMER, ' seconds'))),

                    ], [
                        if_else(Condition(Variables.STATE, '==', 'night-time'), [
                            update_ui_text_for_everyone(UiTarget.TOP, Concat(
                                'Day begins in ', Concat(Variables.TIMER, ' seconds'))),

                        ], [
                            if_else(Condition(Variables.STATE, '==', 'day-time'), [
                                update_ui_text_for_everyone(UiTarget.TOP, Concat(
                                                            'Choose someone to lynch in ', Concat(Variables.TIMER, ' seconds (press E to lynch)'))),

                            ], [
                                if_else(Condition(Variables.STATE, '==', 'plead-guilty'), [
                                    update_ui_text_for_everyone(UiTarget.TOP, Concat(Concat(PlayerName(
                                        Variables.LYNCHING_PLAYER), ' has '), Concat(Variables.TIMER, ' seconds to defend themselves'))),

                                ], [
                                    if_else(Condition(Variables.STATE, '==', 'final-vote'), [
                                        update_ui_text_for_everyone(UiTarget.TOP, Concat(Concat('Vote whether to lynch ', Concat(
                                            PlayerName(Variables.LYNCHING_PLAYER), ' in ')), Concat(Variables.TIMER, ' seconds'))),

                                    ], [
                                        if_else(Condition(Variables.STATE, '==', 'lynch-time'), [
                                            hide_ui_text_for_everyone(
                                                UiTarget.TOP),

                                        ], [
                                            if_else(Condition(Variables.STATE, '==', 'round-end'), [
                                                update_ui_text_for_everyone(UiTarget.TOP, Concat(
                                                    'New round starting in ', Concat(Variables.TIMER, ' seconds'))),

                                            ], [

                                            ]),

                                        ]),

                                    ]),

                                ]),

                            ]),

                        ]),

                    ]),

                ]),

            ]),

        ]


class EveryFrame(Script):
    def _build(self):
        self.key = 'EoWxRIFoZo'
        self.triggers = [Trigger.EVERY_FRAME]
        self.actions = [
            if_else(Condition(StringContainsString(Variables.VILLAGER_PLAYERS, '(cookie giver)'), '==', True), [
                for_all_units(AllUnitsOwnedByPlayer(Variables.AI), [
                    if_else(Condition(UnitTypeOfUnit(SelectedUnit()), '==', UnitTypes.COOKIE), [
                        if_else(Condition(Condition(EntityExists(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit())), '==', False), 'OR', Condition(Condition(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit()), '==', Undefined()), 'OR', Condition(Variables.COOKIE_TARGET, '==', Undefined()))), [
                            destroy_entity(SelectedUnit()),

                        ], [
                            move_entity(SelectedUnit(), XyCoordinate(Calculate(Calculate(53, '*', Sin(UnitsFacingAngle(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit())))), '+', PositionX(EntityPosition(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit())))), Calculate(
                                        Calculate(-53, '*', Cos(UnitsFacingAngle(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit())))), '+', PositionY(EntityPosition(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit())))))),
                            rotate_entity_to_face_position(SelectedUnit(), MouseCursorPosition(OwnerOfEntity(
                                ValueOfEntityVariable(EntityVariables.TARGET_UNIT, SelectedUnit())))),

                        ]),
                        break_loop(),

                    ], [

                    ]),

                ]),

            ], [

            ]),

        ]


# |
# ╰

# ╭
# SCRIPTS
# |

class StartNewGame(Script):
    def _build(self):
        self.key = 'qSgJOHTuZF'
        self.triggers = []
        self.actions = [
            comment('runs when all players are readied up'),
            set_variable(Variables.STATE, 'pre-round-1'),
            set_variable(Variables.TIMER, 15),
            set_variable(Variables.NIGHT_NUMBER, 0),
            set_variable(Variables.NO_KILLING_NIGHTS, 0),
            set_variable(Variables.VIGILANTE_ARROWS, 3),
            set_variable(Variables.DID_MAYOR_REVAL, False),
            set_variable(Variables.GODFATHER_IS_PRESENT, False),
            set_variable(Variables.EXECUTIONER_TARGET, Undefined()),
            set_variable(Variables.EXECUTIONER, Undefined()),
            set_variable(Variables.GODFATHER, Undefined()),
            set_variable(Variables.CULTIST, Undefined()),
            set_variable(Variables.LYNCHING_PLAYER, Undefined()),
            set_variable(Variables.CULT_MEMBERS, '[]'),
            for_all_units(AllUnitsOwnedByPlayer(Variables.GRAVEYARD_MANAGER), [
                destroy_entity(SelectedUnit()),

            ]),
            set_variable(Variables.GAMEMODE_VOTES, '''["0","0","0"]'''),
            for_all_players(AllHumanPlayers(), [
                open_dialogue_for_player(
                    Dialogues.MODE_SELECTION, SelectedPlayer()),

            ]),

        ]


class StartNight(Script):
    def _build(self):
        self.key = 'VVYggrkVzm'
        self.triggers = []
        self.actions = [
            if_else(Condition(StringArrayLength(Variables.CULT_MEMBERS), '>=', Calculate(Calculate(PlayerCount(), '-', 1), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD))), [
                send_chat_message('Cultist won!'),
                update_ui_text_for_time_for_player(
                    UiTarget.CENTER, 'Cultist won!', Undefined(), 7500),
                set_variable(Variables.DIALOGUE_TITLE, 'Cultist won!'),
                run_script('UvglYEu3P5'),
                return_loop(),

            ], [

            ]),
            set_variable(Variables.COOKIE_TARGET, Undefined()),
            set_variable(Variables.LYNCHING_PLAYER, Undefined()),
            set_entity_state(Variables.NIGHT_UNIT, States.DAY),
            set_variable(Variables.TIMER, Calculate(
                25, '+', Calculate(NumberOfPlayersOfPlayerType(PlayerTypes.MAFIA), '*', 10))),
            set_variable(Variables.STATE, 'night-time'),
            increase_variable_by_number(Variables.NIGHT_NUMBER, 1),
            set_entity_state(Variables.NIGHT_UNIT, States.NIGHT),
            set_variable(Variables.MAFIA_VOTES, '[]'),
            set_variable(Variables.TO_DIE, '[]'),
            run_script('IU5OhhsDWr'),
            run_script('oQEoDv6AhW'),
            run_script('ZAlu7eggyV'),
            set_variable(Variables.TEMP_STRING, 'Your fellow mafias: '),
            for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.MAFIA_PLAYERS), '-', 1), [
                if_else(Condition(Variables.I, '>', 0), [
                        set_variable(Variables.TEMP_STRING, Concat(Variables.TEMP_STRING, Concat(
                            ', ', StringArrayElement(Variables.I, Variables.MAFIA_PLAYERS)))),

                        ], [
                        set_variable(Variables.TEMP_STRING, Concat(Variables.TEMP_STRING, Concat(
                            '', StringArrayElement(Variables.I, Variables.MAFIA_PLAYERS)))),

                        ]),

            ]),
            set_time_out(1500, [
                if_else(Condition(Variables.STATE, '==', 'round-end'), [
                        return_loop(),

                        ], [

                ]),
                for_all_players(AllHumanPlayers(), [
                    if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), [
                                close_dialogue_for_player(
                                    SelectedPlayer()),
                                ban_player_from_chat(SelectedPlayer()),
                                if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypes.MAFIA), [
                                    send_chat_message_to_player(
                                        Variables.TEMP_STRING, SelectedPlayer()),

                                ], [

                                ]),
                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'villager'), [
                                    open_dialogue_for_player(
                                        Dialogues.HELP_BOREDOM, SelectedPlayer()),

                                ], [
                                    if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'mayor'), 'AND', Condition(Variables.DID_MAYOR_REVAL, '==', True)), [
                                        open_dialogue_for_player(
                                            Dialogues.HELP_BOREDOM, SelectedPlayer()),

                                    ], [
                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'joker'), [
                                            open_dialogue_for_player(
                                                Dialogues.HELP_BOREDOM, SelectedPlayer()),

                                        ], [
                                            for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                                                set_variable(
                                                    Variables.TEMP_UNIT, SelectedUnit()),
                                                run_script(
                                                    'kI6LRzkLcf'),
                                                break_loop(),

                                            ]),

                                        ]),

                                    ]),

                                ]),

                                ], [

                    ]),

                ]),

            ]),

        ]


class StartDay(Script):
    def _build(self):
        self.key = 'sx1o5NHSNp'
        self.triggers = []
        self.actions = [
            set_variable(Variables.STATE, 'day-time'),
            set_variable(Variables.TIMER, Calculate(140, '+', Calculate(Calculate(
                PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '*', 10))),
            if_else(Condition(Variables.TIMER, '>', 225), [
                set_variable(Variables.TIMER, 225),

            ], [

            ]),
            set_entity_state(Variables.NIGHT_UNIT, States.DAY),
            set_variable(Variables.PLAYERS_VOTED, 0),
            set_variable(Variables.LYNCH_VOTES, '[]'),
            set_variable(Variables.PLAYERS_ABSTAINED, 0),
            set_variable(Variables.FINAL_LYNCH_VOTE, 0),
            set_variable(Variables.LYNCHING_PLAYER, Undefined()),
            set_variable(Variables.TEMP_PLAYER, Undefined()),
            for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.MAFIA_VOTES), '-', 1), [
                set_player_variable(PlayerFromId(StringArrayElement(Variables.I, Variables.MAFIA_VOTES)), PlayerVariables.VOTES, Calculate(
                    ValueOfPlayerVariable(PlayerVariables.VOTES, PlayerFromId(StringArrayElement(Variables.I, Variables.MAFIA_VOTES))), '+', 1)),
                if_else(Condition(Condition(Variables.TEMP_PLAYER, '==', Undefined()), 'OR', Condition(ValueOfPlayerVariable(PlayerVariables.VOTES, PlayerFromId(StringArrayElement(Variables.I, Variables.MAFIA_VOTES))), '>', ValueOfPlayerVariable(PlayerVariables.VOTES, Variables.TEMP_PLAYER))), [
                        set_variable(Variables.TEMP_PLAYER, PlayerFromId(
                            StringArrayElement(Variables.I, Variables.MAFIA_VOTES))),

                        ], [

                ]),

            ]),
            if_else(Condition(Variables.TEMP_PLAYER, '!=', Undefined()), [
                set_variable(Variables.NO_KILLING_NIGHTS, 0),
                set_variable(Variables.TO_DIE, InsertStringArrayElement(
                    PlayerId(Variables.TEMP_PLAYER), Variables.TO_DIE)),
                if_else(Condition(Variables.TEMP_PLAYER, '==', Variables.WATCHER_TARGET), [
                    for_all_players(AllHumanPlayers(), [
                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'mafia'), [
                                        set_variable(Variables.WATCHER_TARGET_VISITORS, InsertStringArrayElement(
                                            PlayerName(SelectedPlayer()), Variables.WATCHER_TARGET_VISITORS)),
                                        break_loop(),

                                    ], [

                                    ]),

                                    ]),

                ], [

                ]),

            ], [
                increase_variable_by_number(
                    Variables.NO_KILLING_NIGHTS, 1),

            ]),
            set_variable(Variables.I, 0),
            while_do(Condition(Variables.I, '<', StringArrayLength(Variables.TO_DIE)), [
                if_else(Condition(Condition(Variables.CULTIST, '==', ValueOfPlayerVariable(PlayerVariables.ROLE, PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE)))), 'OR', Condition(Condition('serial killer', '==', ValueOfPlayerVariable(PlayerVariables.ROLE, PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE)))), 'OR', Condition(Condition('survivor', '==', ValueOfPlayerVariable(PlayerVariables.ROLE, PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE)))), 'OR', Condition('new role', '==', 'undecided')))), [
                        set_variable(Variables.TO_DIE, RemoveStringArrayElement(
                            Variables.I, Variables.TO_DIE)),

                        ], [
                        increase_variable_by_number(Variables.I, 1),

                        ]),

            ]),
            for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.TO_DIE), '-', 1), [
                if_else(Condition(PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE)), '!=', Variables.HEALED_PLAYER), [
                        for_all_units(AllUnitsOwnedByPlayer(PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE))), [
                            destroy_entity(SelectedUnit()),

                        ]),

                        ], [

                ]),

            ]),
            if_else(Condition(Variables.CULTIST, '!=', Undefined()), [
                for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.CULT_MEMBERS), '-', 1), [
                    if_else(Condition(StringArrayElement(Variables.I, Variables.CULT_MEMBERS), '==', PlayerId(LastTriggeringPlayer())), [
                        set_variable(Variables.CULT_MEMBERS, RemoveStringArrayElement(
                            Variables.I, Variables.CULT_MEMBERS)),
                        break_loop(),

                    ], [

                    ]),

                ]),

            ], [

            ]),
            set_time_out(1500, [
                if_else(Condition(Variables.STATE, '==', 'round-end'), [
                        return_loop(),

                        ], [

                ]),
                if_else(Condition(StringArrayLength(Variables.TO_DIE), '==', 0), [
                        send_chat_message('... no one got attacked?'),

                        ], [
                        for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.TO_DIE), '-', 1), [
                            if_else(Condition(PlayerTypeOfPlayer(PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE))), '!=', PlayerTypes.DEAD), [
                                if_else(Condition(PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE)), '!=', Variables.HEALED_PLAYER), [
                                    send_chat_message(Concat(PlayerName(PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE))), StringArrayElement(
                                        RandomNumberBetween(0, Calculate(StringArrayLength(Variables.WAYS_TO_DIE), '-', 1)), Variables.WAYS_TO_DIE))),
                                    send_chat_message(Concat('They were a ', ValueOfPlayerVariable(
                                        PlayerVariables.ROLE, PlayerFromId(StringArrayElement(Variables.I, Variables.TO_DIE))))),
                                    set_variable(Variables.KILLING_PLAYER, PlayerFromId(
                                        StringArrayElement(Variables.I, Variables.TO_DIE))),
                                    run_script(
                                        '7vW6FtAnmz'),

                                ], [
                                    send_chat_message(Concat(PlayerName(PlayerFromId(StringArrayElement(
                                        Variables.I, Variables.TO_DIE))), ' was attacked during the night, but they were healed by the doctor.')),

                                ]),

                            ], [

                            ]),

                        ]),

                        ]),
                for_all_players(AllHumanPlayers(), [
                    if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), [
                                unban_player_from_chat(
                                    SelectedPlayer()),
                                if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'sheriff'), 'AND', Condition(Variables.INVESTIGATED_PLAYER, '!=', Undefined())), [
                                    set_variable(Variables.DIALOGUE_TITLE, Concat(
                                        'You investigated ', PlayerName(Variables.INVESTIGATED_PLAYER))),
                                    set_variable(
                                        Variables.DIALOGUE_MESSAGE, 'They are '),
                                    if_else(Condition(Condition(Condition(PlayerTypeOfPlayer(Variables.INVESTIGATED_PLAYER), '==', PlayerTypes.MAFIA), 'AND', Condition(Variables.GODFATHER, '!=', Variables.INVESTIGATED_PLAYER)), 'OR', Condition(Condition(Variables.INVESTIGATED_PLAYER, '==', Variables.FRAMED_PLAYER), 'AND', Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypes.VILLAGERS))), [
                                        set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                                            Variables.SPAN_RED, Concat('evil!', Variables.SPAN_END)))),

                                    ], [
                                        if_else(Condition(PlayerTypeOfPlayer(Variables.INVESTIGATED_PLAYER), '==', PlayerTypes.NEUTRAL), [
                                            set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                                                Variables.SPAN_GREY, Concat('neutral', Variables.SPAN_END)))),

                                        ], [
                                            set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                                                Variables.SPAN_GREEN, Concat('good!', Variables.SPAN_END)))),

                                        ]),

                                    ]),
                                    open_dialogue_for_player(
                                        Dialogues.ABILITY_RESULT, SelectedPlayer()),

                                ], [
                                    if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'mayor'), 'AND', Condition(Variables.DID_MAYOR_REVAL, '==', True)), [
                                        for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                                            if_else(Condition(UnitTypeOfUnit(SelectedUnit()), '==', UnitTypes.CITIZEN), [
                                                change_unit_type(
                                                    SelectedUnit(), UnitTypes.MAYOR),
                                                send_chat_message(Concat(PlayerName(
                                                    SelectedPlayer()), ' has chosen to reveal himself as the mayor!')),

                                            ], [

                                            ]),

                                        ]),

                                    ], [
                                        if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'vigilante'), 'AND', Condition(Variables.DID_VIGILANTE_SCREW_UP, '==', True)), [
                                            for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                                                destroy_entity(
                                                    SelectedUnit()),
                                                send_chat_message(
                                                    Concat(PlayerName(SelectedPlayer()), ' committed suicide out of guilt.')),
                                                send_chat_message(
                                                    'They were a vigilante'),
                                                set_variable(
                                                    Variables.KILLING_PLAYER, SelectedPlayer()),
                                                run_script(
                                                    '7vW6FtAnmz'),

                                            ]),

                                        ], [
                                            if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'watcher'), 'AND', Condition(Variables.WATCHER_TARGET, '!=', Undefined())), [
                                                set_variable(Variables.DIALOGUE_TITLE, Concat(
                                                    'You watched ', PlayerName(Variables.WATCHER_TARGET))),
                                                if_else(Condition(StringArrayLength(Variables.WATCHER_TARGET_VISITORS), '==', 0), [
                                                    set_variable(
                                                        Variables.DIALOGUE_MESSAGE, 'No one visited them tonight'),

                                                ], [
                                                    set_variable(Variables.DIALOGUE_MESSAGE, Concat(
                                                        'Players that visited:', Variables.BREAK)),
                                                    for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.WATCHER_TARGET_VISITORS), '-', 1), [
                                                        set_variable(Variables.DIALOGUE_MESSAGE, Concat(Concat(Concat(Variables.DIALOGUE_MESSAGE, ' • '), StringArrayElement(
                                                            Variables.I, Variables.WATCHER_TARGET_VISITORS)), Variables.BREAK)),

                                                    ]),

                                                ]),
                                                open_dialogue_for_player(
                                                    Dialogues.ABILITY_RESULT, SelectedPlayer()),

                                            ], [
                                                if_else(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'cookie giver'), 'AND', Condition(Variables.COOKIE_TARGET, '!=', Undefined())), [
                                                    create_unit_for_player_at_position(
                                                        UnitTypes.COOKIE, Variables.AI, XyCoordinate(0, 0), 0),
                                                    for_all_units(AllUnitsOwnedByPlayer(Variables.COOKIE_TARGET), [
                                                        set_entity_variable(
                                                            LastCreatedUnit(), EntityVariables.TARGET_UNIT, SelectedUnit()),

                                                    ]),
                                                    send_chat_message_to_player(
                                                        'Someone gave you a cookie!!', Variables.COOKIE_TARGET),

                                                ], [

                                                ]),

                                            ]),

                                        ]),

                                    ]),

                                ]),

                                ], [

                    ]),

                ]),
                run_script('IU5OhhsDWr'),
                run_script('oQEoDv6AhW'),
                run_script('ZAlu7eggyV'),
                if_else(Condition(StringArrayLength(Variables.CULT_MEMBERS), '==', Calculate(Calculate(PlayerCount(), '-', 1), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD))), [
                        send_chat_message(
                            'Everyone is now a cult member'),
                        send_chat_message(
                            'Lynch the cultist before dusk in order to survive'),

                        ], [

                ]),

            ]),

        ]


class CheckLynchVotesAtEnd(Script):
    def _build(self):
        self.key = 'o4WXONJNWn'
        self.triggers = []
        self.actions = [
            if_else(Condition(Variables.STATE, '==', 'day-time'), [
                set_variable(Variables.TEMP_PLAYER, Undefined()),
                for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.LYNCH_VOTES), '-', 1), [
                    set_player_variable(PlayerFromId(StringArrayElement(Variables.I, Variables.LYNCH_VOTES)), PlayerVariables.VOTES, Calculate(
                        ValueOfPlayerVariable(PlayerVariables.VOTES, PlayerFromId(StringArrayElement(Variables.I, Variables.LYNCH_VOTES))), '+', 1)),
                    if_else(Condition(Condition(Variables.TEMP_PLAYER, '==', Undefined()), 'OR', Condition(ValueOfPlayerVariable(PlayerVariables.VOTES, PlayerFromId(StringArrayElement(Variables.I, Variables.LYNCH_VOTES))), '>', ValueOfPlayerVariable(PlayerVariables.VOTES, Variables.TEMP_PLAYER))), [
                        set_variable(Variables.TEMP_PLAYER, PlayerFromId(
                            StringArrayElement(Variables.I, Variables.LYNCH_VOTES))),

                    ], [

                    ]),

                ]),
                if_else(Condition(Condition(Variables.TEMP_PLAYER, '!=', Undefined()), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.VOTES, Variables.TEMP_PLAYER), '>=', Calculate(Calculate(PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '/', 2))), [
                    set_variable(
                        Variables.LYNCHING_PLAYER, Variables.TEMP_PLAYER),
                    set_variable(Variables.STATE, 'plead-guilty'),
                    for_all_units(AllUnitsOwnedByPlayer(Variables.LYNCHING_PLAYER), [
                        move_entity(SelectedUnit(), CenterOfRegion(
                            Regions.LYNCH_ZONE)),

                    ]),
                    set_variable(Variables.TIMER, 30),
                    return_loop(),

                ], [
                    send_chat_message(
                        'not enough votes were collected to conduct a trial against anybody'),

                ]),

            ], [
                if_else(Condition(Variables.STATE, '==', 'final-vote'), [
                    if_else(Condition(Variables.FINAL_LYNCH_VOTE, '>=', 1), [
                        set_variable(
                            Variables.STATE, 'lynch-time'),
                        set_variable(Variables.TIMER, 8),
                        run_script('xrdqgU7mtG'),
                        return_loop(),

                    ], [
                        for_all_units(AllUnitsOwnedByPlayer(Variables.LYNCHING_PLAYER), [
                            move_entity(
                                SelectedUnit(), CenterOfRegion(Regions.SPAWN)),

                        ]),
                        send_chat_message(Concat(PlayerName(
                            Variables.LYNCHING_PLAYER), ' has been decided to not be lynched')),

                    ]),

                ], [

                ]),

            ]),
            run_script('VVYggrkVzm'),

        ]


class FocusOnLynch(Script):
    def _build(self):
        self.key = 'xrdqgU7mtG'
        self.triggers = []
        self.actions = [
            for_all_players(AllHumanPlayers(), [
                position_camera(SelectedPlayer(),
                                CenterOfRegion(Regions.LYNCH_ZONE)),

            ]),
            set_time_out(4000, [
                for_all_units(AllUnitsOwnedByPlayer(Variables.LYNCHING_PLAYER), [
                    if_else(Condition(PlayerTypeOfPlayer(Variables.LYNCHING_PLAYER), '==', PlayerTypes.MAFIA), [
                        create_unit_for_player_at_position(
                            UnitTypes.KNIFE, Variables.AI, EntityPosition(SelectedUnit()), 0),
                        apply_force_on_entity_xy(
                            30, 140, LastCreatedUnit()),
                        apply_torque_on_entity(
                            20, LastCreatedUnit()),

                    ], [

                    ]),
                    destroy_entity(SelectedUnit()),
                    break_loop(),

                ]),
                if_else(Condition(Variables.EXECUTIONER, '==', Variables.LYNCHING_PLAYER), [
                        set_variable(
                            Variables.EXECUTIONER, Undefined()),

                        ], [

                ]),
                set_variable(Variables.LYNCHED_ROLE, ValueOfPlayerVariable(
                    PlayerVariables.ROLE, Variables.LYNCHING_PLAYER)),
                create_unit_for_player_at_position(
                    UnitTypes.GRAVESTONE, Variables.GRAVEYARD_MANAGER, RandomPositionInRegion(Regions.GRAVEYARD), 0),
                set_unit_name_label(LastCreatedUnit(), Concat(PlayerName(
                    Variables.LYNCHING_PLAYER), Concat(' (', Concat(Variables.LYNCHED_ROLE, ')')))),
                if_else(Condition(PlayerTypeOfPlayer(Variables.LYNCHING_PLAYER), '==', PlayerTypes.VILLAGERS), [
                        set_entity_state(
                            LastCreatedUnit(), States.FLOWER),

                        ], [
                        set_entity_state(
                            LastCreatedUnit(), States.NO_FLOWER),

                        ]),
                assign_player_type(
                    Variables.LYNCHING_PLAYER, PlayerTypes.DEAD),
                create_unit_for_player_at_position(
                    UnitTypes.DEAD, Variables.LYNCHING_PLAYER, EntityPosition(LastCreatedUnit()), 0),
                player_camera_track_unit(
                    Variables.LYNCHING_PLAYER, LastCreatedUnit()),
                ban_player_from_chat(Variables.LYNCHING_PLAYER),
                send_chat_message_to_player(
                    'Press C to access the dead chat', Variables.LYNCHING_PLAYER),
                if_else(Condition(StringContainsString(Variables.CULT_MEMBERS, PlayerId(Variables.LYNCHING_PLAYER)), '==', True), [
                        for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.CULT_MEMBERS), '-', 1), [
                            if_else(Condition(StringArrayElement(Variables.I, Variables.CULT_MEMBERS), '==', PlayerId(Variables.LYNCHING_PLAYER)), [
                                set_variable(Variables.CULT_MEMBERS, RemoveStringArrayElement(
                                    Variables.I, Variables.CULT_MEMBERS)),
                                break_loop(),

                            ], [

                            ]),

                        ]),

                        ], [
                        if_else(Condition(Variables.LYNCHED_ROLE, '==', Variables.CULTIST), [
                            set_variable(
                                Variables.CULTIST, Undefined()),
                            set_variable(
                                Variables.CULT_MEMBERS, '[]'),

                        ], [

                        ]),

                        ]),
                set_time_out(2000, [
                    send_chat_message(Concat(PlayerName(Variables.LYNCHING_PLAYER), Concat(
                        ' has been lynched. They were a ', Variables.LYNCHED_ROLE))),
                    for_all_players(AllHumanPlayers(), [
                        for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                            player_camera_track_unit(
                                    SelectedPlayer(), SelectedUnit()),

                        ]),

                    ]),
                    if_else(Condition(Variables.LYNCHED_ROLE, '==', 'joker'), [
                        send_chat_message(Concat(PlayerName(
                            Variables.LYNCHING_PLAYER), ' was lynched as joker and won!')),
                        update_ui_text_for_time_for_player(UiTarget.CENTER, Concat(
                            PlayerName(Variables.LYNCHING_PLAYER), ' wins!'), Undefined(), 10000),
                        set_variable(Variables.DIALOGUE_TITLE, Concat(
                            PlayerName(Variables.LYNCHING_PLAYER), 'wins!')),
                        set_player_attribute(AttributeTypes.WINS, Variables.LYNCHING_PLAYER, Calculate(
                            PlayerAttribute(AttributeTypes.WINS, Variables.LYNCHING_PLAYER), '+', 1)),
                        run_script('UvglYEu3P5'),

                    ], [
                        if_else(Condition(Condition(Variables.EXECUTIONER, '!=', Undefined()), 'AND', Condition(Variables.LYNCHING_PLAYER, '==', Variables.EXECUTIONER_TARGET)), [
                            if_else(Condition(StringContainsString(Variables.NEUTRAL_PLAYERS, Concat(Concat('''"''', PlayerName(Variables.EXECUTIONER)), ''' (executioner)"''')), '==', True), [
                                update_ui_text_for_time_for_player(UiTarget.CENTER, Concat(
                                    PlayerName(Variables.LYNCHING_PLAYER), ' wins!'), Undefined(), 7500),
                                send_chat_message(
                                    "The executioner's target was lynched so he won!"),
                                set_variable(
                                    Variables.DIALOGUE_TITLE, 'The executioner wins!'),
                                set_player_attribute(AttributeTypes.WINS, Variables.EXECUTIONER, Calculate(
                                    PlayerAttribute(AttributeTypes.WINS, Variables.EXECUTIONER), '+', 1)),
                                run_script(
                                    'UvglYEu3P5'),
                                break_loop(),

                            ], [

                            ]),

                        ], [
                            if_else(Condition(Variables.EXECUTIONER, '==', Variables.LYNCHING_PLAYER), [
                                set_variable(
                                    Variables.EXECUTIONER, Undefined()),

                            ], [
                                if_else(Condition(Variables.GODFATHER, '==', Variables.LYNCHING_PLAYER), [
                                    set_variable(
                                        Variables.GODFATHER, Undefined()),
                                    run_script(
                                        'ZAlu7eggyV'),

                                ], [
                                    if_else(Condition(Variables.CULTIST, '==', Variables.LYNCHING_PLAYER), [
                                        set_variable(
                                            Variables.CULTIST, Undefined()),
                                        set_variable(
                                            Variables.CULT_MEMBERS, '[]'),

                                    ], [

                                    ]),

                                ]),

                            ]),

                        ]),

                    ]),

                ]),

            ]),

        ]


class CheckIfATeamWon(Script):
    def _build(self):
        self.key = 'ZAlu7eggyV'
        self.triggers = []
        self.actions = [
            if_else(Condition(Calculate(PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '<=', 2), [
                for_all_players(AllHumanPlayers(), [
                    if_else(Condition(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'serial killer')), [
                                update_ui_text_for_time_for_player(
                                    UiTarget.CENTER, 'The serial killer wins!', Undefined(), 7500),
                                send_chat_message(
                                    'The serial killer killed everyone and won!'),
                                set_variable(Variables.DIALOGUE_TITLE, Concat(
                                    PlayerName(SelectedPlayer()), ' wins!')),
                                set_player_attribute(AttributeTypes.WINS, SelectedPlayer(), Calculate(
                                    PlayerAttribute(AttributeTypes.WINS, SelectedPlayer()), '+', 1)),
                                run_script('UvglYEu3P5'),
                                return_loop(),

                                ], [

                    ]),

                ]),

            ], [

            ]),
            if_else(Condition(Condition(NumberOfPlayersOfPlayerType(PlayerTypes.MAFIA), '==', 0), 'OR', Condition(Condition(Variables.NO_KILLING_NIGHTS, '>=', 3), 'OR', Condition(Condition(Variables.GODFATHER_IS_PRESENT, '==', True), 'AND', Condition(Variables.GODFATHER, '==', Undefined())))), [
                send_chat_message(
                    'All the mafia are dead so the villagers won!'),
                update_ui_text_for_time_for_player(
                    UiTarget.CENTER, 'Villagers win!', Undefined(), 7500),
                set_variable(Variables.DIALOGUE_TITLE,
                             'Villagers win!'),
                for_all_players(AllHumanPlayers(), [
                    if_else(Condition(StringContainsString(Variables.VILLAGER_PLAYERS, Concat(Concat('''"''', PlayerName(SelectedPlayer())), ' (')), '==', True), [
                                set_player_attribute(AttributeTypes.WINS, SelectedPlayer(), Calculate(
                                    PlayerAttribute(AttributeTypes.WINS, SelectedPlayer()), '+', 1)),

                                ], [
                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'survivor'), [
                            set_player_attribute(AttributeTypes.WINS, SelectedPlayer(), Calculate(
                                PlayerAttribute(AttributeTypes.WINS, SelectedPlayer()), '+', 1)),
                            send_chat_message(Concat('The survivor, ', Concat(PlayerName(
                                SelectedPlayer()), ', survived until the and and won as well'))),

                        ], [

                        ]),

                    ]),

                ]),
                run_script('UvglYEu3P5'),

            ], [
                if_else(Condition(NumberOfPlayersOfPlayerType(PlayerTypes.MAFIA), '>=', Calculate(NumberOfPlayersOfPlayerType(PlayerTypes.VILLAGERS), '+', NumberOfPlayersOfPlayerType(PlayerTypes.NEUTRAL))), [
                    send_chat_message(
                        'Mafias outnumbered the villagers and won!'),
                    update_ui_text_for_time_for_player(
                        UiTarget.CENTER, 'Mafia win!', Undefined(), 7500),
                    set_variable(
                        Variables.DIALOGUE_TITLE, 'Mafia wins!'),
                    for_all_players(AllHumanPlayers(), [
                                    if_else(Condition(StringContainsString(Variables.MAFIA_PLAYERS, Concat(Concat('''"''', PlayerName(SelectedPlayer())), ' (')), '==', True), [
                                        set_player_attribute(AttributeTypes.WINS, SelectedPlayer(), Calculate(
                                            PlayerAttribute(AttributeTypes.WINS, SelectedPlayer()), '+', 1)),

                                    ], [
                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'survivor'), [
                                            set_player_attribute(AttributeTypes.WINS, SelectedPlayer(), Calculate(
                                                PlayerAttribute(AttributeTypes.WINS, SelectedPlayer()), '+', 1)),
                                            send_chat_message(Concat('The survivor, ', Concat(PlayerName(
                                                SelectedPlayer()), ', survived until the and and won as well'))),

                                        ], [

                                        ]),

                                    ]),

                                    ]),
                    run_script('UvglYEu3P5'),

                ], [

                ]),

            ]),

        ]


class EndRound(Script):
    def _build(self):
        self.key = 'UvglYEu3P5'
        self.triggers = []
        self.actions = [
            set_variable(Variables.STATE, 'round-end'),
            set_entity_state(Variables.NIGHT_UNIT, States.DEFAULT),
            set_variable(Variables.TIMER, 15),
            set_variable(Variables.NIGHT_NUMBER, 0),
            set_variable(Variables.PLAYERS_READIED_UP, 0),
            set_variable(Variables.DIALOGUE_MESSAGE, ''),
            set_variable(Variables.DIALOGUE_MESSAGE2, ''),
            if_else(Condition(StringArrayLength(Variables.NEUTRAL_PLAYERS), '>=', 1), [
                set_variable(Variables.DIALOGUE_MESSAGE3, ''),

            ], [
                set_variable(Variables.DIALOGUE_MESSAGE3, Flip.NONE),

            ]),
            for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.VILLAGER_PLAYERS), '-', 1), [
                set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                    StringArrayElement(Variables.I, Variables.VILLAGER_PLAYERS), Variables.BREAK))),

            ]),
            for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.MAFIA_PLAYERS), '-', 1), [
                set_variable(Variables.DIALOGUE_MESSAGE2, Concat(Variables.DIALOGUE_MESSAGE2, Concat(
                    StringArrayElement(Variables.I, Variables.MAFIA_PLAYERS), Variables.BREAK))),

            ]),
            for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.NEUTRAL_PLAYERS), '-', 1), [
                set_variable(Variables.DIALOGUE_MESSAGE3, Concat(Variables.DIALOGUE_MESSAGE3, Concat(
                    StringArrayElement(Variables.I, Variables.NEUTRAL_PLAYERS), Variables.BREAK))),

            ]),
            for_all_players(AllHumanPlayers(), [
                unban_player_from_chat(SelectedPlayer()),
                open_dialogue_for_player(
                    Dialogues.ROUND_OVER, SelectedPlayer()),
                for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                    destroy_entity(SelectedUnit()),

                ]),
                create_unit_for_player_at_position(
                    UnitTypes.LOBBY_UNIT, SelectedPlayer(), CenterOfRegion(Regions.SPAWN), 0),
                set_variable(Variables.CHANGE_UNIT, LastCreatedUnit()),
                run_script('I4fUUokJaS'),
                player_camera_track_unit(SelectedPlayer(), LastCreatedUnit()),
                assign_player_type(SelectedPlayer(), PlayerTypes.VILLAGERS),

            ]),

        ]


# ╭
# DIALOGUES
# |

class OpenRoleDialogueForTempUnit(Script):
    def _build(self):
        self.key = 'kI6LRzkLcf'
        self.triggers = []
        self.actions = [
            if_else(Condition(PlayerTypeOfPlayer(OwnerOfEntity(Variables.TEMP_UNIT)), '==', PlayerTypes.MAFIA), [
                set_variable(Variables.DIALOGUE_TITLE, Concat('You are a ', Concat(Variables.SPAN_RED, Concat(
                    ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), Variables.SPAN_END)))),
                set_variable(
                    Variables.DIALOGUE_MESSAGE, 'You are evil! Win by killing off every good guy'),

            ], [
                if_else(Condition(PlayerTypeOfPlayer(OwnerOfEntity(Variables.TEMP_UNIT)), '==', PlayerTypes.VILLAGERS), [
                    set_variable(Variables.DIALOGUE_TITLE, Concat('You are a ', Concat(Variables.SPAN_GREEN, Concat(
                        ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), Variables.SPAN_END)))),
                    set_variable(
                        Variables.DIALOGUE_MESSAGE, 'You are good! Win by lynching the bad bois'),

                ], [
                    if_else(Condition(PlayerTypeOfPlayer(OwnerOfEntity(Variables.TEMP_UNIT)), '==', PlayerTypes.NEUTRAL), [
                        set_variable(Variables.DIALOGUE_TITLE, Concat('You are a ', Concat(Variables.SPAN_GREY, Concat(
                            ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), Variables.SPAN_END)))),
                        set_variable(
                            Variables.DIALOGUE_MESSAGE, 'You are neutral.'),

                    ], [

                    ]),

                ]),

            ]),
            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'villager'), [
                set_variable(
                    Variables.C_MESSAGE, 'unable to talk with others during the night'),
                set_variable(Variables.E_MESSAGE,
                             'no ability during the night'),

            ], [
                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'sheriff'), [
                    set_variable(
                        Variables.C_MESSAGE, 'unable to talk with others during the night'),
                    set_variable(
                        Variables.E_MESSAGE, 'find out whether a player is good or bad (during the night)'),

                ], [
                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'mafia'), [
                        set_variable(
                            Variables.C_MESSAGE, 'talk with other mafias (during the night)'),
                        set_variable(
                            Variables.E_MESSAGE, 'vote to kill someone during the night (player with highest votes will be killed)'),

                    ], [
                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'doctor'), [
                            set_variable(
                                Variables.C_MESSAGE, 'unable to talk with others during the night'),
                            set_variable(
                                Variables.E_MESSAGE, "choose someone to save during the night (can't save yourself)"),

                        ], [
                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'mayor'), [
                                set_variable(
                                    Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                set_variable(
                                    Variables.E_MESSAGE, 'choose to reveal yourself as a mayor the following day (lynch votes will be doubled)'),

                            ], [
                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'vigilante'), [
                                    set_variable(
                                        Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                    set_variable(
                                        Variables.E_MESSAGE, 'pick a person to shoot each night. if you shoot an innocent, you will commit suicide a day after out of guilt.'),

                                ], [
                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'framer'), [
                                        set_variable(
                                            Variables.C_MESSAGE, 'talk with other mafias (during the night)'),
                                        set_variable(
                                            Variables.E_MESSAGE, 'choose someone to frame every night. the person who gets framed resets every night and the framed player shows up as evil when investigated upon (by the sheriff).'),

                                    ], [
                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'joker'), [
                                            set_variable(
                                                Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                            set_variable(
                                                Variables.E_MESSAGE, 'no ability during the night'),
                                            set_variable(Variables.DIALOGUE_MESSAGE, Concat(
                                                Variables.DIALOGUE_MESSAGE, ' Win by being lynched (voted out) by the town')),

                                        ], [
                                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', Variables.EXECUTIONER), [
                                                set_variable(
                                                    Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                                set_variable(
                                                    Variables.E_MESSAGE, 'no ability during the night'),
                                                set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                                                    ' Win by lynching (voting out) your target: ', PlayerName(Variables.EXECUTIONER_TARGET)))),

                                            ], [
                                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'watcher'), [
                                                    set_variable(
                                                        Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                                    set_variable(
                                                        Variables.E_MESSAGE, 'choose someone to watch during the night. you will get a list of all the players that visited the player you chose to watch'),

                                                ], [
                                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', Variables.GODFATHER), [
                                                        set_variable(
                                                            Variables.C_MESSAGE, 'talk with other mafias during the night'),
                                                        set_variable(
                                                            Variables.E_MESSAGE, 'vote someone to kill during the night (your votes get doubled)'),

                                                    ], [
                                                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'cookie giver'), [
                                                            set_variable(
                                                                Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                                            set_variable(
                                                                Variables.E_MESSAGE, 'choose someone to give a cookie (they wont know who gave them the cookie, and they will lose the cookie after the next night)'),

                                                        ], [
                                                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', Variables.CULTIST), [
                                                                set_variable(
                                                                    Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                                                set_variable(
                                                                    Variables.E_MESSAGE, 'bamboozle people into cult members during the night'),
                                                                set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                                                                    ' Win by fooling everyone to join your cult.', Concat(Variables.BREAK, 'Current members: ')))),
                                                                if_else(Condition(StringArrayLength(Variables.CULT_MEMBERS), '==', 0), [
                                                                    set_variable(Variables.DIALOGUE_MESSAGE, Concat(
                                                                        Variables.DIALOGUE_MESSAGE, Flip.NONE)),

                                                                ], [
                                                                    for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.CULT_MEMBERS), '-', 1), [
                                                                        if_else(Condition(Variables.I, '==', Calculate(StringArrayLength(Variables.CULT_MEMBERS), '-', 1)), [
                                                                            set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, PlayerName(
                                                                                PlayerFromId(StringArrayElement(Variables.I, Variables.CULT_MEMBERS))))),

                                                                        ], [
                                                                            set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(
                                                                                PlayerName(PlayerFromId(StringArrayElement(Variables.I, Variables.CULT_MEMBERS))), ', '))),

                                                                        ]),

                                                                    ]),

                                                                ]),
                                                                set_variable(Variables.DIALOGUE_MESSAGE, Concat(Variables.DIALOGUE_MESSAGE, Concat(' ... ', Concat(Calculate(Calculate(
                                                                    PlayerCount(), '-', NumberOfPlayersOfPlayerType(PlayerTypes.DEAD)), '-', StringArrayLength(Variables.CULT_MEMBERS)), ' left')))),

                                                            ], [
                                                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'serial killer'), [
                                                                    set_variable(
                                                                        Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                                                    set_variable(
                                                                        Variables.E_MESSAGE, 'select a player to kill during the night'),
                                                                    set_variable(Variables.DIALOGUE_MESSAGE, Concat(
                                                                        Variables.DIALOGUE_MESSAGE, ' Be the last person standing in order to win')),

                                                                ], [
                                                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, OwnerOfEntity(Variables.TEMP_UNIT)), '==', 'survivor'), [
                                                                        set_variable(
                                                                            Variables.C_MESSAGE, 'unable to talk with others during the night'),
                                                                        set_variable(
                                                                            Variables.E_MESSAGE, 'no ability during the night'),
                                                                        set_variable(Variables.DIALOGUE_MESSAGE, Concat(
                                                                            Variables.DIALOGUE_MESSAGE, ' Stay alive until the game ends')),

                                                                    ], [

                                                                    ]),

                                                                ]),

                                                            ]),

                                                        ]),

                                                    ]),

                                                ]),

                                            ]),

                                        ]),

                                    ]),

                                ]),

                            ]),

                        ]),

                    ]),

                ]),

            ]),
            open_dialogue_for_player(
                Dialogues.ROLE_DESCRIPTOR, OwnerOfEntity(Variables.TEMP_UNIT)),

        ]


class OpenRoleDialogueForAll(Script):
    def _build(self):
        self.key = '1Ltqi09pDC'
        self.triggers = []
        self.actions = [
            for_all_players(AllHumanPlayers(), [
                if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), [
                        for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                            set_variable(
                                Variables.TEMP_UNIT, SelectedUnit()),
                            run_script('kI6LRzkLcf'),
                            break_loop(),

                        ]),

                        ], [

                ]),

            ]),

        ]


class OpenFinalVoteDialogueForAll(Script):
    def _build(self):
        self.key = 'i9bdhnnTLy'
        self.triggers = []
        self.actions = [
            set_variable(Variables.PLAYERS_VOTED, 0),
            for_all_players(AllHumanPlayers(), [
                if_else(Condition(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), 'AND', Condition(SelectedPlayer(), '!=', Variables.LYNCHING_PLAYER)), [
                        set_variable(Variables.DIALOGUE_TITLE, Concat(
                            'Vote to lynch ', PlayerName(Variables.LYNCHING_PLAYER))),
                        open_dialogue_for_player(
                            Dialogues.FINAL_VOTE, SelectedPlayer()),

                        ], [

                ]),

            ]),

        ]


class VoteAgainstAccused(Script):
    def _build(self):
        self.key = 'X1aGBU8fjA'
        self.triggers = []
        self.actions = [
            increase_variable_by_number(Variables.FINAL_LYNCH_VOTE, 1),
            if_else(Condition(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastPlayerSelectingDialogueOption()), '==', 'mayor'), 'AND', Condition(Variables.DID_MAYOR_REVAL, '==', True)), 'OR', Condition(Variables.COOKIE_TARGET, '==', LastPlayerSelectingDialogueOption())), [
                send_chat_message(Concat(PlayerName(LastPlayerSelectingDialogueOption()), Concat(
                    ' voted ', Concat(PlayerName(Variables.LYNCHING_PLAYER), ' guilty (doubled)')))),
                increase_variable_by_number(
                    Variables.FINAL_LYNCH_VOTE, 1),

            ], [
                send_chat_message(Concat(PlayerName(LastPlayerSelectingDialogueOption()), Concat(
                    ' voted ', Concat(PlayerName(Variables.LYNCHING_PLAYER), ' guilty')))),

            ]),
            increase_variable_by_number(Variables.PLAYERS_VOTED, 1),

        ]


class VoteForAccused(Script):
    def _build(self):
        self.key = 'l9jvbd4NoV'
        self.triggers = []
        self.actions = [
            decrease_variable_by_number(Variables.FINAL_LYNCH_VOTE, 1),
            if_else(Condition(Condition(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, LastPlayerSelectingDialogueOption()), '==', 'mayor'), 'AND', Condition(Variables.DID_MAYOR_REVAL, '==', True)), 'OR', Condition(Variables.COOKIE_TARGET, '==', LastPlayerSelectingDialogueOption())), [
                send_chat_message(Concat(PlayerName(LastPlayerSelectingDialogueOption()), Concat(
                    ' voted ', Concat(PlayerName(Variables.LYNCHING_PLAYER), ' innocent (doubled)')))),
                decrease_variable_by_number(
                    Variables.FINAL_LYNCH_VOTE, 1),

            ], [
                send_chat_message(Concat(PlayerName(LastPlayerSelectingDialogueOption()), Concat(
                    ' voted ', Concat(PlayerName(Variables.LYNCHING_PLAYER), ' innocent')))),

            ]),
            increase_variable_by_number(Variables.PLAYERS_VOTED, 1),

        ]


# ╭
# ROLE ACTIONS
# |

class RevealAsMayor(Script):
    def _build(self):
        self.key = 'ou49yrCtDa'
        self.triggers = []
        self.actions = [
            send_chat_message_to_player(
                'You have decided to reveal yourself as the mayor', LastPlayerSelectingDialogueOption()),
            send_chat_message_to_player(
                'Your votes will be doubled from now on', LastPlayerSelectingDialogueOption()),
            set_variable(Variables.DID_MAYOR_REVAL, True),

        ]


# |
# ╰

class VoteForClassicGamemode(Script):
    def _build(self):
        self.key = 'Nw41QQJ1o0'
        self.triggers = []
        self.actions = [
            set_variable(Variables.GAMEMODE_VOTES, UpdateStringArrayElement(0, Variables.GAMEMODE_VOTES, Concat(
                '', Calculate(StringToNumber(StringArrayElement(0, Variables.GAMEMODE_VOTES)), '+', 1)))),
            send_chat_message_to_player(
                'You voted for classic', LastPlayerSelectingDialogueOption()),

        ]


class VoteForChaosGamemode(Script):
    def _build(self):
        self.key = 'soh2aKulY7'
        self.triggers = []
        self.actions = [
            set_variable(Variables.GAMEMODE_VOTES, UpdateStringArrayElement(1, Variables.GAMEMODE_VOTES, Concat(
                '', Calculate(StringToNumber(StringArrayElement(1, Variables.GAMEMODE_VOTES)), '+', 1)))),
            send_chat_message_to_player(
                'You voted for chaos', LastPlayerSelectingDialogueOption()),

        ]


# |
# ╰

class SetStateOfChangeUnit(Script):
    def _build(self):
        self.key = 'I4fUUokJaS'
        self.triggers = []
        self.actions = [
            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 10), [
                set_entity_state(Variables.CHANGE_UNIT, States.ANGRY),

            ], [
                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 20), [
                    set_entity_state(
                        Variables.CHANGE_UNIT, States.CUTE),

                ], [
                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 30), [
                        set_entity_state(
                            Variables.CHANGE_UNIT, States.CRYING),

                    ], [
                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 40), [
                            set_entity_state(
                                Variables.CHANGE_UNIT, States.HAPPY),

                        ], [
                            if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 50), [
                                set_entity_state(
                                    Variables.CHANGE_UNIT, States.LAZY),

                            ], [
                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 60), [
                                    set_entity_state(
                                        Variables.CHANGE_UNIT, States.SCARED),

                                ], [
                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.SKIN_NUMBER, OwnerOfEntity(Variables.CHANGE_UNIT)), '<=', 70), [
                                        set_entity_state(
                                            Variables.CHANGE_UNIT, States.WHALE),

                                    ], [

                                    ]),

                                ]),

                            ]),

                        ]),

                    ]),

                ]),

            ]),

        ]


class KillKillingPlayer(Script):
    def _build(self):
        self.key = '7vW6FtAnmz'
        self.triggers = []
        self.actions = [
            if_else(Condition(Variables.EXECUTIONER, '!=', Undefined()), [
                if_else(Condition(Condition(Variables.STATE, '==', 'day-time'), 'AND', Condition(Variables.EXECUTIONER_TARGET, '==', Variables.KILLING_PLAYER)), [
                    set_player_variable(
                        Variables.EXECUTIONER, PlayerVariables.ROLE, 'joker'),
                    send_chat_message_to_player(
                        'Your target died so you turned into a joker!', Variables.EXECUTIONER),
                    for_all_units(AllUnitsOwnedByPlayer(Variables.EXECUTIONER), [
                        set_variable(
                            Variables.TEMP_UNIT, SelectedUnit()),
                        run_script('kI6LRzkLcf'),

                    ]),
                    set_variable(
                        Variables.EXECUTIONER, Undefined()),

                ], [

                ]),

            ], [

            ]),
            if_else(Condition(Variables.EXECUTIONER, '==', Variables.KILLING_PLAYER), [
                set_variable(Variables.EXECUTIONER, Undefined()),

            ], [
                if_else(Condition(Variables.GODFATHER, '==', Variables.KILLING_PLAYER), [
                    set_variable(Variables.GODFATHER, Undefined()),
                    run_script('ZAlu7eggyV'),

                ], [

                ]),

            ]),
            create_unit_for_player_at_position(
                UnitTypes.GRAVESTONE, Variables.GRAVEYARD_MANAGER, RandomPositionInRegion(Regions.GRAVEYARD), 0),
            set_unit_name_label(LastCreatedUnit(), Concat(PlayerName(Variables.KILLING_PLAYER), Concat(
                ' (', Concat(ValueOfPlayerVariable(PlayerVariables.ROLE, Variables.KILLING_PLAYER), ')')))),
            if_else(Condition(PlayerTypeOfPlayer(Variables.KILLING_PLAYER), '==', PlayerTypes.VILLAGERS), [
                set_entity_state(LastCreatedUnit(), States.FLOWER),

            ], [
                set_entity_state(LastCreatedUnit(), States.NO_FLOWER),

            ]),
            create_unit_for_player_at_position(
                UnitTypes.DEAD, Variables.KILLING_PLAYER, EntityPosition(LastCreatedUnit()), 0),
            player_camera_track_unit(
                Variables.KILLING_PLAYER, LastCreatedUnit()),
            assign_player_type(Variables.KILLING_PLAYER, PlayerTypes.DEAD),
            ban_player_from_chat(Variables.KILLING_PLAYER),
            send_chat_message_to_player(
                'Press C to access the dead chat', Variables.KILLING_PLAYER),
            if_else(Condition(StringContainsString(Variables.CULT_MEMBERS, PlayerId(Variables.KILLING_PLAYER)), '==', True), [
                for_range(Variables.I, 0, Calculate(StringArrayLength(Variables.CULT_MEMBERS), '-', 1), [
                    if_else(Condition(StringArrayElement(Variables.I, Variables.CULT_MEMBERS), '==', PlayerId(Variables.KILLING_PLAYER)), [
                        set_variable(Variables.CULT_MEMBERS, RemoveStringArrayElement(
                            Variables.I, Variables.CULT_MEMBERS)),
                        break_loop(),

                    ], [

                    ]),

                ]),

            ], [
                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, Variables.KILLING_PLAYER), '==', Variables.CULTIST), [
                    set_variable(Variables.CULTIST, Undefined()),
                    set_variable(Variables.CULT_MEMBERS, '[]'),

                ], [

                ]),

            ]),
            if_else(Condition(Condition(Variables.NIGHT_NUMBER, '==', 1), 'AND', Condition(Variables.STATE, '==', 'day-time')), [
                open_dialogue_for_player(
                    Dialogues.FIRST_NIGHT_DEATH, Variables.KILLING_PLAYER),

            ], [

            ]),

        ]


class GiveOutRoles(Script):
    def _build(self):
        self.key = '88pzZdjoIK'
        self.triggers = []
        self.actions = [
            set_variable(Variables.VILLAGER_PLAYERS, '[]'),
            set_variable(Variables.MAFIA_PLAYERS, '[]'),
            set_variable(Variables.NEUTRAL_PLAYERS, '[]'),
            set_variable(Variables.AVAILABLE_ROLES, '[]'),
            set_variable(Variables.RANDOM_NEUTRAL_ROLES,
                         '''["cultistN","serial killerN" "survivorN"]'''),
            set_variable(Variables.I, PlayerCount()),
            if_else(Condition(PlayerCount(), '>=', 16), [
                repeat(3, [
                    set_variable(Variables.AVAILABLE_ROLES, InsertStringArrayElement(
                        'mafiaB', Variables.AVAILABLE_ROLES)),
                    decrease_variable_by_number(Variables.I, 1),

                ]),

            ], [
                repeat(Calculate(MathFloor(Calculate(PlayerCount(), '/', 10)), '+', 1), [
                    set_variable(Variables.AVAILABLE_ROLES, InsertStringArrayElement(
                        'mafiaB', Variables.AVAILABLE_ROLES)),
                    decrease_variable_by_number(Variables.I, 1),

                ]),

            ]),
            for_range(Variables.J, 0, Calculate(StringArrayLength(Variables.GAMEMODE_ROLES), '-', 1), [
                if_else(Condition(StringArrayElement(Variables.J, Variables.GAMEMODE_ROLES), '==', 'skip'), [
                        if_else(Condition(Variables.I, '==', 3), [
                            break_loop(),

                        ], [
                            continue_loop(),

                        ]),

                        ], [

                ]),
                if_else(Condition(Condition(Variables.I, '>', 2), 'OR', Condition(Condition(Variables.GAMEMODE, '!=', 'classic'), 'AND', Condition(Variables.I, '>', 0))), [
                        if_else(Condition(StringArrayElement(Variables.J, Variables.GAMEMODE_ROLES), '==', 'randomNeutralRole'), [
                            if_else(Condition(LengthOfString(Variables.RANDOM_NEUTRAL_ROLES), '>', 0), [
                                set_variable(Variables.G, RandomNumberBetween(0, Calculate(
                                    StringArrayLength(Variables.RANDOM_NEUTRAL_ROLES), '-', 1))),
                                set_variable(Variables.AVAILABLE_ROLES, InsertStringArrayElement(StringArrayElement(
                                    Variables.G, Variables.RANDOM_NEUTRAL_ROLES), Variables.AVAILABLE_ROLES)),
                                set_variable(Variables.RANDOM_NEUTRAL_ROLES, RemoveStringArrayElement(
                                    Variables.G, Variables.RANDOM_NEUTRAL_ROLES)),

                            ], [

                            ]),

                        ], [
                            set_variable(Variables.AVAILABLE_ROLES, InsertStringArrayElement(StringArrayElement(
                                Variables.J, Variables.GAMEMODE_ROLES), Variables.AVAILABLE_ROLES)),

                        ]),
                        decrease_variable_by_number(Variables.I, 1),

                        ], [
                        break_loop(),

                        ]),

            ]),
            repeat(Variables.I, [
                set_variable(Variables.AVAILABLE_ROLES, InsertStringArrayElement(
                    'villagerG', Variables.AVAILABLE_ROLES)),

            ]),
            for_all_players(AllHumanPlayers(), [
                set_variable(Variables.I, RandomNumberBetween(0, Calculate(
                    StringArrayLength(Variables.AVAILABLE_ROLES), '-', 1))),
                for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                    change_unit_type(
                        SelectedUnit(), UnitTypes.CITIZEN),
                    set_player_variable(OwnerOfEntity(SelectedUnit()), PlayerVariables.ROLE, SubstringOf(StringArrayElement(
                        Variables.I, Variables.AVAILABLE_ROLES), 0, Calculate(LengthOfString(StringArrayElement(Variables.I, Variables.AVAILABLE_ROLES)), '-', 1))),
                    if_else(Condition(StringEndsWith(StringArrayElement(Variables.I, Variables.AVAILABLE_ROLES), 'B'), '==', True), [
                            assign_player_type(
                                SelectedPlayer(), PlayerTypes.MAFIA),
                            if_else(Condition(Condition(Condition(PlayerCount(), '>=', 10), 'AND', Condition(Variables.GODFATHER, '==', Undefined())), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'mafia')), [
                                set_variable(
                                    Variables.GODFATHER, SelectedPlayer()),
                                set_player_variable(
                                    SelectedPlayer(), PlayerVariables.ROLE, Variables.GODFATHER),
                                set_variable(
                                    Variables.GODFATHER_IS_PRESENT, True),

                            ], [

                            ]),
                            set_variable(Variables.MAFIA_PLAYERS, InsertStringArrayElement(Concat(PlayerName(SelectedPlayer()), Concat(
                                ' (', Concat(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), ')'))), Variables.MAFIA_PLAYERS)),

                            ], [
                            if_else(Condition(StringEndsWith(StringArrayElement(Variables.I, Variables.AVAILABLE_ROLES), 'N'), '==', True), [
                                assign_player_type(
                                    SelectedPlayer(), PlayerTypes.NEUTRAL),
                                set_variable(Variables.NEUTRAL_PLAYERS, InsertStringArrayElement(Concat(PlayerName(SelectedPlayer()), Concat(
                                    ' (', Concat(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), ')'))), Variables.NEUTRAL_PLAYERS)),
                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', Variables.EXECUTIONER), [
                                    set_variable(
                                        Variables.EXECUTIONER, SelectedPlayer()),

                                ], [
                                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', Variables.CULTIST), [
                                        set_variable(
                                            Variables.CULTIST, SelectedPlayer()),

                                    ], [

                                    ]),

                                ]),

                            ], [
                                assign_player_type(
                                    SelectedPlayer(), PlayerTypes.VILLAGERS),
                                set_variable(Variables.VILLAGER_PLAYERS, InsertStringArrayElement(Concat(PlayerName(SelectedPlayer()), Concat(
                                    ' (', Concat(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), ')'))), Variables.VILLAGER_PLAYERS)),
                                if_else(Condition(Condition(Variables.EXECUTIONER_TARGET, '==', Undefined()), 'AND', Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '!=', 'mayor')), [
                                    set_variable(
                                        Variables.EXECUTIONER_TARGET, SelectedPlayer()),

                                ], [

                                ]),

                            ]),

                            ]),
                    set_variable(Variables.AVAILABLE_ROLES, RemoveStringArrayElement(
                        Variables.I, Variables.AVAILABLE_ROLES)),
                    break_loop(),

                ]),

            ]),
            run_script('1Ltqi09pDC'),

        ]


class ResetAllRemainingPlayers(Script):
    def _build(self):
        self.key = 'oQEoDv6AhW'
        self.triggers = []
        self.actions = [
            comment('takes place at the start of each day and night'),
            set_variable(Variables.HEALED_PLAYER, Undefined()),
            set_variable(Variables.INVESTIGATED_PLAYER, Undefined()),
            set_variable(Variables.DID_VIGILANTE_SCREW_UP, False),
            set_variable(Variables.FRAMED_PLAYER, Undefined()),
            set_variable(Variables.WATCHER_TARGET, Undefined()),
            set_variable(Variables.WATCHER_TARGET_VISITORS, '[]'),
            for_all_players(AllHumanPlayers(), [
                if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '!=', PlayerTypes.DEAD), [
                        set_player_variable(
                            SelectedPlayer(), PlayerVariables.VOTES, 0),
                        set_player_variable(
                            SelectedPlayer(), PlayerVariables.DID_VOTE, False),

                        ], [

                ]),

            ]),

        ]


class CheckMafias(Script):
    def _build(self):
        self.key = 'IU5OhhsDWr'
        self.triggers = []
        self.actions = [
            if_else(Condition(Condition(StringContainsString(Variables.MAFIA_PLAYERS, '(framer)'), '==', True), 'AND', Condition(NumberOfPlayersOfPlayerType(PlayerTypes.MAFIA), '==', 1)), [
                for_all_players(AllHumanPlayers(), [
                    if_else(Condition(PlayerTypeOfPlayer(SelectedPlayer()), '==', PlayerTypes.MAFIA), [
                                if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'framer'), [
                                    set_player_variable(
                                        SelectedPlayer(), PlayerVariables.ROLE, 'mafia'),
                                    send_chat_message_to_player(
                                        'You turned into a mafia as you are the only one left!', SelectedPlayer()),
                                    for_all_units(AllUnitsOwnedByPlayer(SelectedPlayer()), [
                                        set_variable(
                                            Variables.TEMP_UNIT, SelectedUnit()),
                                        run_script('kI6LRzkLcf'),

                                    ]),

                                ], [

                                ]),
                                break_loop(),

                                ], [

                    ]),

                ]),

            ], [

            ]),
            if_else(Condition(NumberOfPlayersOfPlayerType(PlayerTypes.MAFIA), '<=', 2), [
                for_all_players(AllHumanPlayers(), [
                    if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'mafia'), [
                                return_loop(),

                                ], [
                        if_else(Condition(ValueOfPlayerVariable(PlayerVariables.ROLE, SelectedPlayer()), '==', 'framer'), [
                            break_loop(),

                        ], [

                        ]),

                    ]),

                ]),
                set_player_variable(
                    Variables.GODFATHER, PlayerVariables.ROLE, 'mafia'),
                send_chat_message_to_player(
                    'Your mafias died so you became a mafia', Variables.GODFATHER),
                for_all_units(AllUnitsOwnedByPlayer(Variables.GODFATHER), [
                    set_variable(Variables.TEMP_UNIT, SelectedUnit()),
                    run_script('kI6LRzkLcf'),

                ]),
                set_variable(Variables.GODFATHER, Undefined()),
                set_variable(Variables.GODFATHER_IS_PRESENT, False),

            ], [

            ]),

        ]


# |
# ╰
