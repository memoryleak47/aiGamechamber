#!/usr/bin/python3 -B

import sys
import os
import time

sys.path.append(sys.path[0] + "/games")
sys.path.append(sys.path[0] + "/players")

import rectgame

import human
import tryhard 
import kingofrandom

# <changeable>
RENDER = True
SLEEPTIME = 0.03
# </changeable>


def main():
	# <changeable>
	game = rectgame.Rectgame(2)
	players = [tryhard.Tryhard(game), tryhard.Tryhard(game)]
	# </changeable>

	game.start(players)
	while True:
		for i in range(len(players)):
			if RENDER:
				game.render()
			game.applyAction(players[i].act(), i)
			players[i].evaluate(game.getEvaluation(i))
			time.sleep(SLEEPTIME)

if __name__ == "__main__":
	main()
