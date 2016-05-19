#!/usr/bin/python3 -B

import sys

class Game:
	def __init__(self, noPlayers):
		self.__noPlayers = noPlayers
		self.__data = list()
		self.__history = list()
		self.__players = list()
		self.__startTime = 0

	def _gameOver(self):
		for player in self.__players:
			player.gameOver()
		self.__startTime = self.getTime()
		self._restart()

	def start(self, players):
		self.__players = players
		self._restart()

	def _restart(self):
		print("Game::restart not overwritten")
		sys.exit()

	def applyAction(self, action, playerID):
		print("Game::applyAction not overwritten")
		sys.exit()

	def render(self):
		print("Game::render() not overwritten")

	def getHistory(self):
		return self.__history.copy()

	def getData(self):
		return self.__data.copy()

	def _setData(self, data):
		self.__data = data
		self.__history.append(data)

	def _setDataMember(self, i, member):
		data = self.getData()
		data[i] = member
		self._setData(data)

	def _incDataMember(self, i, addition):
		self._setDataMember(i, self.__data[i] + addition)

	def getNoInput(self):
		print("Game::getNoInput not overwritten")
		sys.exit()

	def getNoOutput(self):
		print("Game::getNoOutput not overwritten")
		sys.exit()

	def getNoPlayers(self):
		return self.__noPlayers

	def getStartTime(self):
		return self.__startTime

	def getTime(self):
		return len(self.__history)

	def _getPlayer(self, i):
		return self.__players[i]