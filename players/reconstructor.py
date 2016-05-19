#!/usr/bin/python3 -B

from player import *

class Reconstructor(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)

'''
reconstruct(data, results):
	reconstruct is a function from mathcore.
	It shall return a Func f which applies to `for every i: f(data[i]) == results[i]`.

The principle:
	The Reconstructor has multiple phases.
	In the first phase (the random-phase) the Reconstructor just returns random actions in `act`.
	This phase is needed to get a history.

	After a short history is created the Reconstructor <reconstruct>s two functions.
		- Reconstructor::actFunc and
		- Reconstructor::evaluateFunc
	The actFunc saves how the self.__game.data is altered by the call of `act` of the Reconstructor.
	The actFunc has the argument "gamedata (before) + actions" and the result "gamedata (after)".
	The evaluateFunc saves how the Reconstructor is evaluated by the game.
	The evaluateFunc has the argument "gamedata" and the result "(float) evaluate_value".

	With the actFunc & the evaluateFunc the Reconstructor should be able to find the right thing todo.
	One possible use of these functions is, that the Reconstructor searches for the biggest evaluation.
	He then gets the corresponding gamedata which is needed for this evaluation.
	Then he tries to alter the gamedata, by the `act`-function, so that the searched evaluation is granted.
'''
