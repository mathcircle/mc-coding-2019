from random import sample
import numpy
import pandas


SIZE = 3
DIGITS = range(SIZE * SIZE)
UNPLAYED = -1

REPEAT = 2**16


def check(state: list) -> int:
	""" Check which player has won """
	
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
		return 1
	elif all(map(lambda n: n == 0, [state[0, -1], state[1, -2], state[2, -3]])):
		return 0
	elif all(map(lambda n: n == 1, [state[0, -1], state[1, -2], state[2, -3]])):
		return 1
	
	return UNPLAYED


def play():
	""" Simulate a game. """

	sequence = sample(DIGITS, SIZE * SIZE)
	# print(f"DEBUG: sequence: {sequence}")
	state = numpy.array([[-1] * SIZE] * SIZE)
	
	for stage in range(SIZE * SIZE):
		state[sequence[stage] // 3, sequence[stage] % 3] = stage % 2
		winner = check(state)
		if winner != UNPLAYED:
			return (winner, stage)
	
	return (check(state), stage)


if __name__ == "__main__":
	""" This runs if the program is run as a script. """

	#  Frequency of occurrence of the different events.
	#  See data dictionary below for details.
	freq = [0] * 6

	for expt in range(REPEAT):
		result = play()
		if result[0] == 0:
			freq[(result[1] - 4) // 2] += 1
		elif result[0] == 1:
			freq[3 + (result[1] - 5) // 2] += 1
		else:
			freq[5] += 1

	#  Collate the data
	prob = list(map(lambda x: x/REPEAT, freq))
	data = {
		'winner': [0] * 3 + [1] * 2 + [-1],
		'round': list(range(4, 9, 2)) + list(range(5, 9, 2)) + [8],
		'frequency': freq,
		'probability': prob}

	#  Plot the results
	index = list(map(
	    lambda winner, round: "(" + str(winner) + ", " + str(round) + ")",
	    [0] * 3 + [1] * 2 + [-1],
	    list(range(4, 9, 2)) + list(range(5, 9, 2)) + [8]))
	df = pandas.DataFrame(data=data['probability'], index=index)
	df.plot.bar()
	print(df)
