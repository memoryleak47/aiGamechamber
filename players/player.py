#!/usr/bin/python3 -B

class Player:
	def __init__(self, game, id):
		self.__id = id
		self._game = game

	def act(self):
		pass

	def evaluate(self, value):
		pass

	def gameOver(self):
		pass

	def getID(self):
		return self.__id

	def getDataFormat(self)
		return self._game.getDataFormat()

	def getActionFormat(self):
		return self._game.getActionFormat()
