from pymodd.script import Game, Folder, write_game_to_output, write_to_output

from scripts import *
from entity_scripts import * 


class Mafia(Game):
	def _build(self):
		self.entity_scripts = []
		self.scripts = [
			Initialize(),
			Folder('player events', [
				PlayerJoins(),
				PlayerLeaves(),
				WhenAPlayerSubmitsCustomInputModal(),
				WhenPlayerSendsChatMessage(),
				Folder('keybinds', [
					ReadyUp(),
					GameInfo(),
					ViewRole(),
					TalkWithOthers(),
					UseAbility(),
					OpenSkinShop(),
					OpenBoredDialogue(),
					ResetAfkTimer(),
				]),
			]),
			Folder('unit events', [
				WhenAUnitsAttributeBecomes0OrLess(),
				WhenAUnitEntersARegion(),
				WhenUnitUsesItem(),
			]),
			Folder('time based events', [
				EverySecond(),
				UpdateOverlays(),
				EveryFrame(),
			]),
			Folder('scripts', [
				StartNewGame(),
				StartNight(),
				StartDay(),
				CheckLynchVotesAtEnd(),
				FocusOnLynch(),
				CheckIfATeamWon(),
				EndRound(),
				Folder('dialogues', [
					OpenRoleDialogueForTempUnit(),
					OpenRoleDialogueForAll(),
					OpenFinalVoteDialogueForAll(),
					VoteAgainstAccused(),
					VoteForAccused(),
					Folder('role actions', [
						RevealAsMayor(),
					]),
					VoteForClassicGamemode(),
					VoteForChaosGamemode(),
				]),
				SetStateOfChangeUnit(),
				KillKillingPlayer(),
				GiveOutRoles(),
				ResetAllRemainingPlayers(),
				CheckMafias(),
			]),
			
		]

# run `python mafia/mapping.py` to generate this game's files
write_game_to_output(Mafia('mafia/utils/game.json'))
# uncomment the following to quickly generate the json file for a script
# write_to_output('output/', SCRIPT_OBJECT())