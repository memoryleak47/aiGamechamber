#!/usr/bin/python3 -B

import sys
import os

sys.path.append(sys.path[0] + "/games")
sys.path.append(sys.path[0] + "/players")

import rectgame

import human

players=list()
while True:
	playerstr = input("Enter player\n>> ").strip()
	if playerstr == "":
		break
	else:
		eval("players.append(" + playerstr.lower() + "." + playerstr[0].upper() + playerstr[1:].lower() + "())")

gamestr = input("Enter Game\n>> ")
eval(gamestr.lower() + "." + gamestr[0].upper() + gamestr[1:].lower() + "(players).run()")
