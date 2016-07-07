#!/usr/bin/python3

import random
import sys
import time
from game import *
import tkinter as tk

WIDTH=30
HEIGHT=30
TILESIZE=10

# data [x0, y0, xball0, yball0, speedxball0, speedyball0, x1, y1, xball1, yball1, speedxball1, speedyball1]

class Sniper(Game):
	def __init__(self, noPlayers, window):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)
		self.__window = window

		self.__canvas = tk.Canvas(self.__window, width=800, height=600)
		self.__canvas.pack()

	def _restart(self):
		self._setData([WIDTH-2,1,2,2,0,0,WIDTH-2,HEIGHT-2,2,2,0,0])

	def applyAction(self, action, playerID):
		data = self.getData()

		xpos = self.__spotPositionX(playerID)
		ypos = self.__spotPositionY(playerID)
		xball = self.__spotBallX(playerID)
		yball = self.__spotBallY(playerID)
		xballspeed = self.__spotBallSpeedX(playerID)
		yballspeed = self.__spotBallSpeedY(playerID)

		if action[0] == "-1" and data[xpos] > 1:
			data[xpos] -= 1
		elif action[0] == "1" and data[xpos] < WIDTH-2:
			data[xpos] += 1

		if action[1] == "-1" and data[ypos] > 1:
			data[ypos] -= 1
		elif action[1] == "1" and data[ypos] < HEIGHT-2:
			data[ypos] += 1

		eval0 = -1
		eval1 = -1

		if data[self.__spotPositionX(0)] == data[self.__spotBallX(1)] and data[self.__spotPositionY(0)] == data[self.__spotBallY(1)]:
			eval0 -= 150
			eval1 += 100
			data[self.__spotBallX(1)] = data[self.__spotPositionX(1)]
			data[self.__spotBallY(1)] = data[self.__spotPositionY(1)]
			data[self.__spotBallSpeedX(1)] = 0
			data[self.__spotBallSpeedY(1)] = 0
		if data[self.__spotPositionX(1)] == data[self.__spotBallX(0)] and data[self.__spotPositionY(1)] == data[self.__spotBallY(0)]:
			eval0 += 100
			eval1 -= 150
			data[self.__spotBallX(0)] = data[self.__spotPositionX(0)]
			data[self.__spotBallY(0)] = data[self.__spotPositionY(0)]
			data[self.__spotBallSpeedX(0)] = 0
			data[self.__spotBallSpeedY(0)] = 0

		for id in [0,1]:
			# if ball is outta range
			if data[self.__spotBallX(id)] <= 1:
				data[self.__spotBallSpeedX(id)] = abs(data[self.__spotBallSpeedX(id)])
			elif data[self.__spotBallX(id)] >= WIDTH-2:
				data[self.__spotBallSpeedX(id)] = -abs(data[self.__spotBallSpeedX(id)])

			if data[self.__spotBallY(id)] <= 1:
				data[self.__spotBallSpeedY(id)] = abs(data[self.__spotBallSpeedY(id)])
			elif data[self.__spotBallY(id)] >= HEIGHT-2:
				data[self.__spotBallSpeedY(id)] = -abs(data[self.__spotBallSpeedY(id)])

			# move ball
			data[self.__spotBallX(id)] = data[self.__spotBallX(id)] + data[self.__spotBallSpeedX(id)]
			data[self.__spotBallY(id)] = data[self.__spotBallY(id)] + data[self.__spotBallSpeedY(id)]

		self._evaluatePlayer(0, eval0)
		self._evaluatePlayer(1, eval1)

		if action[2] == "spawn":
			data[xball] = data[xpos]
			data[yball] = data[ypos]
			data[xballspeed] = int(action[0])
			data[yballspeed] = int(action[1])
		
		self._setData(data)

	def render(self):
		data = self.getData()
		self.__window.wm_title("Sniper: red=" + str(self.getScore(0)) + " blue=" + str(self.getScore(1)))
		
		self.__canvas.delete("all")
		self.__canvas.create_rectangle(0, 0, WIDTH*TILESIZE, HEIGHT*TILESIZE, fill="black")
		self.__canvas.create_rectangle(TILESIZE, TILESIZE, (WIDTH-1)*TILESIZE, (HEIGHT-1)*TILESIZE, fill="white")

		# player red (0)
		x = data[self.__spotPositionX(0)]*TILESIZE
		y = data[self.__spotPositionY(0)]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="red")

		# player blue (1)
		x = data[self.__spotPositionX(1)]*TILESIZE
		y = data[self.__spotPositionY(1)]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="blue")

		# ball yellow
		x = data[self.__spotBallX(0)]*TILESIZE
		y = data[self.__spotBallY(0)]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="yellow")

		# ball green
		x = data[self.__spotBallX(1)]*TILESIZE
		y = data[self.__spotBallY(1)]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="green")

	def getDataFormat(self):
		return "(int,int,int,int,int,int,int,int,int,int,int,int)"

	def getActionFormat(self):
		return "({'-1','0','1'},{'-1','0','1'},{'no_spawn','spawn'})"


	def __spotPositionX(self, playerID):
		return playerID*6

	def __spotPositionY(self, playerID):
		return 1 + playerID*6

	def __spotBallX(self, playerID):
		return 2 + playerID*6

	def __spotBallY(self, playerID):
		return 3 + playerID*6

	def __spotBallSpeedX(self, playerID):
		return 4 + playerID*6

	def __spotBallSpeedY(self, playerID):
		return 5 + playerID*6
