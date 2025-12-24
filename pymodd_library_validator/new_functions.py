# auto generated


class GetCameraPosition(Position):
	def __init__(self, ):
		self.function = 'getCameraPosition'
		self.options = {
		}


class LastClickedUiElementId(String):
	def __init__(self, player):
		self.function = 'lastClickedUiElementId'
		self.options = {
			'player': to_dict(player),
		}


class RealtimeCssOfPlayer(String):
	def __init__(self, player):
		self.function = 'realtimeCSSOfPlayer'
		self.options = {
			'player': to_dict(player),
		}


class MathCeiling(Number):
	def __init__(self, value):
		self.function = 'mathCeiling'
		self.options = {
			'value': to_dict(value),
		}


class ToUpperCase(String):
	def __init__(self, string):
		self.function = 'toUpperCase'
		self.options = {
			'string': to_dict(string),
		}


class GetHighScoreOfPlayer(Number):
	def __init__(self, player):
		self.function = 'getHighScoreOfPlayer'
		self.options = {
			'player': to_dict(player),
		}


class IsUnitMoving(Boolean):
	def __init__(self, unit):
		self.function = 'isUnitMoving'
		self.options = {
			'unit': to_dict(unit),
		}