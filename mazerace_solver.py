import json
from queue import Queue

import requests

api = 'https://api.noopschallenge.com'


def get_maze(maze_url):
	return requests.get(api + maze_url).json()


def bfs(grid, size, path, q, target):
	while not q.empty():
		# Get coordinates of the cell we are currently in
		x, y = q.get()

		# If we are not in the topmost row,
		# and we haven't visited it's top neighbor...
		if x > 0 and grid[x - 1][y] != 'X' \
			and not path[x - 1][y]:

			# We mark the cell as visited by setting it's path to out current
			# + `N`, because we moved up to reach this cell.
			path[x - 1][y] = path[x][y] + 'N'
			q.put((x - 1, y))

			# If we have reached the target, we're done!
			# We simply return the path to the target
			if target == (x - 1, y):
				return path[x - 1][y]

		# Similarly, we check the bottom, right, and left neighbors.
		if x < size - 1 and grid[x + 1][y] != 'X' \
			and not path[x + 1][y]:

			path[x + 1][y] = path[x][y] + 'S'
			q.put((x + 1, y))

			if target == (x + 1, y):
				return path[x + 1][y]

		if y < size - 1 and grid[x][y + 1] != 'X' \
			and not path[x][y + 1]:

			path[x][y + 1] = path[x][y] + 'E'
			q.put((x, y + 1))

			if target == (x, y + 1):
				return path[x][y + 1]

		if y > 0 and grid[x][y - 1] != 'X' \
			and not path[x][y - 1]:

			path[x][y - 1] = path[x][y] + 'W'
			q.put((x, y - 1))

			if target == (x, y - 1):
				return path[x][y - 1]
	# Hmmm. We have visited every cell that we could reach,
	# but haven't found the end point. Something seems off.
	# raise EndNotFoundError


def submit_solution(maze_url, solution):
	directions = {'directions': solution}
	resp = requests.post(api + maze_url, json=directions).json()

	if 'nextMaze' not in resp:
		# Pretty print the response
		print(json.dumps(resp, indent=4))
		return None
	return resp['nextMaze']


def solve_maze(maze_url):
	maze = get_maze(maze_url)
	print(f'Starting maze {maze["name"]}')

	size = len(maze['map'])

	# Create a matrix filled with False's,
	# each denoting we have not visited that cell
	path = [[False for i in range(size)] for j in range(size)]

	# Visit the starting cell, and add it to the queue.
	# We reverse the start (and end) coordinates for row-major traversal,
	# instead of column major.
	q = Queue()
	q.put((reversed(maze['startingPosition'])))
	path[maze['startingPosition'][1]][maze['startingPosition'][0]] = ''

	end = tuple(reversed(maze['endingPosition']))
	solution = bfs(maze['map'], size, path, q, end)

	print(f'Calculated solution is: {solution}')
	return submit_solution(maze_url, solution)


def start_race():
	j = {'login': 'IshanManchanda'}
	return requests.post(api + '/mazebot/race/start', json=j).json()['nextMaze']


def main():
	maze_url = start_race()
	while maze_url:
		maze_url = solve_maze(maze_url)


if __name__ == '__main__':
	main()
