#!/usr/bin/python3 -B

import sys
import os

sys.path.append(sys.path[0] + "/games")
sys.path.append(sys.path[0] + "/players")

import rectgame

import human
import tryhard 

noplayers = int(input("Number of players\n>> "))

gamestr = input("Enter Game\n>> ")
game = eval(gamestr.lower() + "." + gamestr[0].upper() + gamestr[1:].lower() + "(noplayers)")

players=list()
for i in range(noplayers):
	playerstr = input("Enter player\n>> ").strip()
	eval("players.append(" + playerstr.lower() + "." + playerstr[0].upper() + playerstr[1:].lower() + "(game.getNoInfos()))")
game.run(players)
