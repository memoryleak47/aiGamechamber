#!/usr/bin/python3

import random
import sys
import time
from game import *
import tkinter as tk

WIDTH=30
HEIGHT=30
TILESIZE=10

class Dodge(Game):
	def __init__(self, noPlayers, window):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)
		self.__window = window

		self.__canvas = tk.Canvas(self.__window, width=800, height=600)
		self.__canvas.pack()

	def _restart(self):
		self._setData([1,1,WIDTH-2,HEIGHT-2,list()])

	def applyAction(self, action, playerID):
		data = self.getData()
		data[4] = data[4].copy()

		if action[0] == "-1" and self.getData()[2*playerID] > 1:
			data[2*playerID] -= 1
		elif action[0] == "1" and self.getData()[2*playerID] < WIDTH-2:
			data[2*playerID] += 1

		if action[1] == "-1" and self.getData()[1 + 2*playerID] > 1:
			data[1 + 2*playerID] -= 1
		elif action[1] == "1" and self.getData()[1 + 2*playerID] < WIDTH-2:
			data[1 + 2*playerID] += 1

		balls = data[4]

		eval0 = -1
		eval1 = -1
		i = 0
		while i < len(balls):
			remove = False
			if (data[0], data[1]) == (balls[i][0], balls[i][1]):
				eval0 -= 100
				eval1 += 100
				remove = True
			if (data[2], data[3]) == (balls[i][0], balls[i][1]):
				eval0 += 100
				eval1 -= 100
				remove = True
			if remove:
				balls.remove(balls[i])
				continue

			# if ball is outta range
			if balls[i][0] <= 1 or balls[i][0] >= WIDTH-2:
				balls[i] = (balls[i][0], balls[i][1], -balls[i][2], balls[i][3])
			if balls[i][1] <= 1 or balls[i][1] >= HEIGHT-2:
				balls[i] = (balls[i][0], balls[i][1], balls[i][2], -balls[i][3])
			# move ball
			balls[i] = (balls[i][0] + balls[i][2], balls[i][1] + balls[i][3], balls[i][2], balls[i][3])
			i += 1
		self._evaluatePlayer(0, eval0)
		self._evaluatePlayer(1, eval1)

		if action[2] != "spawn":# and len(balls) < 5:
			speedX = int(action[0])
			speedY = int(action[1])
			posX = data[playerID*2]
			posY = data[playerID*2+1]

			x = max(1, min(WIDTH-2, posX + speedX))
			y = max(1, min(HEIGHT-2, posY + speedY))
			balls.append((x,y, speedX, speedY))
		self._setData(data)

	def render(self):
		self.__window.wm_title("Dodge: red=" + str(self.getScore(0)) + " grenn=" + str(self.getScore(1)))
		
		self.__canvas.delete("all")
		self.__canvas.create_rectangle(0, 0, WIDTH*TILESIZE, HEIGHT*TILESIZE, fill="black")
		self.__canvas.create_rectangle(TILESIZE, TILESIZE, (WIDTH-1)*TILESIZE, (HEIGHT-1)*TILESIZE, fill="white")

		for ball in self.getData()[4]:
			self.__canvas.create_rectangle(ball[0]*TILESIZE, ball[1]*TILESIZE, ball[0]*TILESIZE+TILESIZE, ball[1]*TILESIZE+TILESIZE, fill="blue")
		x = self.getData()[0]*TILESIZE
		y = self.getData()[1]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="red")
		x = self.getData()[2]*TILESIZE
		y = self.getData()[3]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="green")
			

	def getDataFormat(self):
		return "(int,int,int,int,[(int,int,int,int)])"

	def getActionFormat(self):
		return "({'-1','0','1'},{'-1','0','1'},{'no_spawn','spawn'})"

