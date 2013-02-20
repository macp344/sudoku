import httplib2
import copy
from datetime import *
from random import *

class Sudoku:
    "Sudoku simple representation"
	GRID_SIZE = 9
	def __init__(self, gridValue, maskValue, level, gridDate):
		# check parameters
		assert isinstance(gridValue, str)
		assert isinstance(maskValue, str)
		assert len(gridValue) == 81
		assert len(maskValue) == 81
		assert isinstance(level, int)
		assert isinstance(gridDate, date)

		self.grid = gridValue
		self.mask = maskValue	
		self.level = level
		self.gridDate = gridDate

	# index of cell in internal grid representation
	def getCellIndex(self, row, col):
		assert 0<=row<self.GRID_SIZE and 0<=col<self.GRID_SIZE
		return row*self.GRID_SIZE+col;

	# Return an int which is the value at [row,col]
	def getCell(self, row, col):
		return self.grid[self.getCellIndex(row,col)]

	# Set the value of a cell value is 0 if not specified
	def setCell(self, row, col, value=0):
		assert 0<=int(value)<=9
		cellIndex = self.getCellIndex(row,col)
		gridList = list(self.grid)
		gridList[cellIndex] = value
		self.grid = "".join(gridList)

	# Return an int which is the value at [row,col]
	def getMask(self, row, col):
		return self.mask[self.getCellIndex(row,col)]

	# Set the value of a cell value is 0 if not specified
	def setMask(self, row, col, value=0):
		assert 0<=int(value)<=9
		cellIndex = self.getCellIndex(row,col)
		maskList = list(self.mask)
		maskList[cellIndex] = value
		self.mask = "".join(maskList)

	def getgrid(self):
		return self._grid
	def setgrid(self, value):
		self._grid = value
	
	# Internal display
	def __printSudoku(self, grid):
		# Print given grid
		for row in range(0,self.GRID_SIZE):
			# iterate rows
			print(grid[self.GRID_SIZE * row:self.GRID_SIZE*(row+1)-1])

	# Display the mask
	def printSudokuMask(self):
		print('Printing Grid Mask :')
		self.__printSudoku(self.grid)

	# display the unrevealed grid
	def printSudokuSolution(self):
		print('Printing Grid Solution :')
		self.__printSudoku(self.mask)

	# displays the grid as the user see it
	def printSudokuGame(self):
		print('Printing Grid Game :')
		gameGrid = ''
		for iCell in range(0,81):
			gameGrid += self.grid[iCell] if self.mask[iCell] == '1' else '_'
		self.__printSudoku(gameGrid)
		

class SudokuGetter:
	# Toolbox class
	@staticmethod
	def getAll(url=""):
		print('Requesting Sudokus from url : '+url)
		response, content = httplib2.Http().request(url)		
		sudokus = []
		 # date grid mask level
		print('Sequence lenght : ' + str(len(content)))
		for gridLine in str(content).split(','):
			# TODO : Remove check and find problem in php (first character wrong)
			if len(str(gridLine))!=171:
				gridLine = gridLine[2:]
			if len(str(gridLine))!=171:
				continue 
			year = gridLine[0:4]
			month = gridLine[4:6]
			day = gridLine[6:8]
			grid = gridLine[8:89]
			mask = gridLine[89:170]
			level = gridLine[170]
			sudoku = Sudoku(grid, mask, int(level), date(int(year), int(month), int(day)))
			sudokus.append(sudoku)

		print('Found %d sudoku grids' % len(sudokus))
		return sudokus

class SudokuRandomizer:
	# Used to randomize

	# return a permutation ex : [2,5,3,1,6,7,9,8]
	@staticmethod
	def __generatePermutations(size):
		permutations = []
		while len(permutations) != size:
			number = 1+int(random() * size)
			if number not in permutations:
				permutations.append(number)
		return permutations

	def applyNumberPermutations(self, sudoku, permutations):
		print('Applying numbers permutations : '+str(permutations))
		grid = sudoku.grid
		newGrid = ''
		for cellValue in grid:
			newGrid += str(permutations[int(cellValue)-1]);
		sudoku.grid = newGrid  

	def applyRowPermutations(self, sudoku, permutations):
		print('Applying row permutations : '+str(permutations))
		newGrid = ''
		newMask = ''
		for iGroup in range(0,3):
			index = Sudoku.GRID_SIZE*3*(int(permutations[iGroup])-1)
			newGrid += str(sudoku.grid[index:index+Sudoku.GRID_SIZE*3])
			newMask += str(sudoku.mask[index:index+Sudoku.GRID_SIZE*3])
		sudoku.grid = newGrid
		sudoku.mask = newMask

	# Permute group of column
	def applyColPermutations(self, sudoku, permutations):
		print('Applying column permutations : '+str(permutations))
		sudokuCopy = copy.copy(sudoku)
		for iGroup in range(0,3):
			for iCol in range(0,3):
				for iRow in range(0,9):
					indexCell = sudoku.getCellIndex(iRow, 3*iGroup + iCol)
					indexColGroupInCopy = int(permutations[iGroup])-1
					sudoku.setCell(iRow, iCol+iGroup*3, sudokuCopy.getCell(iRow, 3*indexColGroupInCopy+iCol))
					sudoku.setMask(iRow, iCol+iGroup*3, sudokuCopy.getMask(iRow, 3*indexColGroupInCopy+iCol))

	def randomizeSudoku(self, sudoku):
		assert isinstance(sudoku, Sudoku)
		numberPermutations = self.__generatePermutations(9)
		columnPermutations = self.__generatePermutations(3)
		rowPermutations = self.__generatePermutations(3)
		print('Sudoku grid before randomization :')
		sudoku.printSudokuGame()
		self.applyNumberPermutations(sudoku, numberPermutations)
		self.applyRowPermutations(sudoku, rowPermutations)
		self.applyColPermutations(sudoku, columnPermutations)
		print('Sudoku grid AFTER randomization :')
		sudoku.printSudokuGame()
		
###########################################################################
# entry point
sudokus = SudokuGetter.getAll()
# init randomizer
seed()
randomizer = SudokuRandomizer()
randomizer.randomizeSudoku(sudokus[0])
