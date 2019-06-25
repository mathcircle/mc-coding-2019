from random import sample
import numpy
import pandas


SIZE = 3
DIGITS = range(SIZE * SIZE)
UNPLAYED = -1

REPEAT = 2 ** 16


def check(state: list) -> int:
	""" Check which player has won, """
	
	win = UNPLAYED
	
	#  Check rows and colums
	for i in range(SIZE):
		if all(state[i, :] == 0) or all(state[:, i] == 0):
			return 0
		elif all(state[i, :] == 1) or all(state[:, i] == 1):
			return 1
	
	#  Check diagonals
	if all(map(lambda n: n == 0, [state[0, 0], state[1, 1], state[2, 2]])):
		return 0
	elif all(map(lambda n: n == 1, [state[0, 0], state[1, 1], state[2, 2]])):
		return 0
	elif all(map(lambda n: n == 0, [state[0, -1], state[1, -2], state[2, -3]])):
		return 1
	elif all(map(lambda n: n == 1, [state[0, -1], state[1, -2], state[2, -3]])):
		return 1
	
	return UNPLAYED
	# if state[1, 1] == 1 and state[2, 2] == 1 and state[3, 3] == 1:
	# 	win = 1
	# elif state[1, -1] == 1 and state[2, 2] == 1 and state[3, 3] == 1


def play():
	""" Simulate a game. """

	state = numpy.array([[-1] * SIZE] * SIZE)
	sequence = sample(DIGITS, SIZE * SIZE)
	
	for stage in range(SIZE * SIZE):
		state[sequence[stage] // 3, sequence[stage] % 3] = stage % 2
		winner = check(state)
		if winner != UNPLAYED:
			return (winner, stage)
	winner = check(state)
	return (winner, stage)


if __name__ == "__main__":
	#  Frequency of occurrence of the different events.
	#  See data dictionary below for details.
	freq = [0] * 10

	for expt in range(REPEAT):
		result = play()
		if result[0] == 0:
			freq[result[1] - 4] += 1
		elif result[0] == 1:
			freq[5 + result[1] - 5] += 1
		else:
			freq[9] += 1

	#  Collect the data
	prob = list(map(lambda x: x/REPEAT, freq))
	data = {
		'winner': [0] * 5 + [1] * 4 + [-1],
		'round': list(range(4, 9)) + list(range(5, 9)) + [8],
		'frequency': freq,
		'prob': prob
	}

	#  Plot the results
	plt.figure();
	idx = list(map(
	    lambda winner, round: "(" + str(winner) + ", " + str(round) + ")",
	    [0] * 5 + [1] * 4 + [-1],
	    list(range(4, 9)) + list(range(5, 9)) + [8]))
	df = pandas.DataFrame(data=data['probability'], index=idx)
	df.plot.bar()
