#!/usr/bin/python3 -B

import sys
import os
import tkinter as tk

sys.path.append(sys.path[0] + "/games")
sys.path.append(sys.path[0] + "/players")

import rectgame
import doublerectgame
import together

import human
import tryhard 
import kingofrandom

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
	game = doublerectgame.Doublerectgame(2, window)
	players = [tryhard.Tryhard(game, 0), tryhard.Tryhard(game, 1)]
	# </changeable>

	game.start(players)
	window.after(SLEEPTIME, tick)
	window.mainloop()

if __name__ == "__main__":
	main()
