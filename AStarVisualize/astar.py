import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0) #checked
WHITE = (255, 255, 255) #bg
BLACK = (0, 0, 0) #barrier
BLUE = (65, 201, 226) #path
YELLOW = (249, 245, 75) #start
PURPLE = (100, 13, 107) #end
GREEN = (161, 221, 112) #open, considered to be explored
GREY = (199, 183, 163) #grid

class Cube:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows #totl rows, for boundary check

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED # if that cube checked, set it red

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == YELLOW

	def is_end(self):
		return self.color == PURPLE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = YELLOW

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = PURPLE

	def make_path(self):
		self.color = BLUE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
     #check up, down, left, right if it's barrier or not
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP #if that cube is not at the top and ...
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other): #less than (to compare 2 cubes)
		return False

def make_grid(rows, width): 
	grid = []
	gap = width // rows  #with of each cube
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			cube = Cube(i, j, gap, rows)
			grid[i].append(cube)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) #surface, color, start pos, end post
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE) #colorize bg 

	for row in grid:
		for cube in row:
			cube.draw(win) #already defined above #draw cubes

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def reconstruct_path(came_from, current, draw):
    path = []
    
    while current in came_from:
        path.append(current)
        current = came_from[current]
    
    #reverse path to start from the beginning
    path.reverse()
    
    #skip the first element in order to see the scratch cube
    for node in path[0:]:
        node.make_path()
        draw()

def h(p1, p2): #heuristic to calculate distance
	x1, y1 = p1
	x2, y2 = p2
	return  math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def algorithm(draw, grid, start, end):
	count = 0 #to maintain order of cubes when priotities are equal
	open_set = PriorityQueue()
	open_set.put((0, count, start)) #(f_score, count, cube)
	open_set_hash = {start} #add cube to open set (visited)
	came_from = {} #keep track where we came from
	g_score = {cube: float("inf") for row in grid for cube in row} #score from start node to current node
	g_score[start] = 0
	f_score = {cube: float("inf") for row in grid for cube in row} #value of start node is f = 0 + h
	f_score[start] = h(start.get_pos(), end.get_pos())
 

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #to quit if needed (error happens)

		current = open_set.get()[2] #get 2nd node (after start node)
		open_set_hash.remove(current) #remove from open set cause being checked

		if current == end: #found the end (shortest path)
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]: #if new path is better -> update
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
 
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:  #if clicking on left mouse
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				cube = grid[row][col]
				if not start and cube != end: #if there's no start and clicked cube is not end
					start = cube
					start.make_start()
				elif not end and cube != start:
					end = cube
					end.make_end()
				elif cube != end and cube != start:
					cube.make_barrier()

			elif pygame.mouse.get_pressed()[2]:  #if clicking on right mouse
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				cube = grid[row][col]
				cube.reset() #delete cube
				if cube == start:
					start = None #reset
				elif cube == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for cube in row:
							cube.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)  #call algorithm()

				if event.key == pygame.K_c: #reset win
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)