#!/usr/bin/python3 -B

class Reconstructor:
	def __init__(self, noInput, noOutput):
		self.noInput = noInput
		self.noOutput = noOutput

'''
history:
	The Game should save the gameinfo-history and the actions of player.
	If this is not done by the game, the Reconstructor has to do it.

reconstruct(data, results):
	reconstruct is a function from mathcore.
	It shall return a Func f which applies to `for every i: f(data[i]) == results[i]`.

The principle:
	The Reconstructor has multiple phases.
	In the first phase (the random-phase) the Reconstructor just returns random actions in `act`.
	This phase is needed to get a <history>.

	After a short <history> is created the Reconstructor <reconstruct>s two functions.
		- Reconstructor::actFunc and
		- Reconstructor::assessFunc
	The actFunc saves how the gameinfo is altered by the call of `act` of the Reconstructor.
	The actFunc has the argument "gameinfo (before) + actions" and the result "gameinfo (after)".
	The assessFunc saves how the Reconstructor is assessed by the game.
	The assessFunc has the argument "gameinfo" and the result "(float) assess_value".

	With the actFunc & the assessFunc the Reconstructor should be able to find the right thing todo.
	One possible use of these functions is, that the Reconstructor searches for the biggest assession.
	He then gets the corresponding gameinfo which is needed for this assession.
	Then he tries to alter the gameinfo, by the `act`-function, so that the searched assession is granted.
'''
