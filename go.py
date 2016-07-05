#!/usr/bin/python3 -B

import sys
import os
import tkinter as tk
import formatter

sys.path.append(sys.path[0] + "/games")
sys.path.append(sys.path[0] + "/players")

import rectgame
import doublerectgame
import together

import human
import functryhard 
import algotryhard 
import kingofrandom
import dodge

# <changeable>
SLEEPTIME = 50
# </changeable>

def tick():
	global players
	global game
	global window
	for i in range(len(players)):
		game.render()
		game.applyAction(players[i].act(), i)
	window.after(SLEEPTIME, tick)

def main():
	global players
	global game
	global window

	window = tk.Tk()
	window.minsize(800, 600)
	window.maxsize(800, 600)
	# <changeable>
	game = dodge.Dodge(2, window)
	players = [functryhard.FuncTryhard(game, 0), functryhard.FuncTryhard(game, 1)]
	#players = [kingofrandom.KingOfRandom(game, 0), kingofrandom.KingOfRandom(game, 1)]
	# </changeable>

	game.start(players)
	window.after(SLEEPTIME, tick)
	window.mainloop()

if __name__ == "__main__":
	main()
