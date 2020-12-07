class Spot():
    def __init__(self):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0

    def addNeighbors(self, i, j):
        """
        0 1 2 3 4 5 6 7 8 9
       0 * * * * * * * * * *
       1 * * * * * * * * * *
       2 * * * * * * * * * *
       3 * * * * * * * * * *
       5 * * * * * * * * * *
       6 * * * * * * * * * *
       7 * * * * * * * * * *
       8 * * * * * * * * * *
       9 * * * * * * * * * *

        """
        # assigning neighbours for left  and right neighbours in the grid
        if i > 0: # i is column and j is row
            self.neighbors.append(grid[i - 1][j]) # left neighbour
        if i < rows - 1: # i< 10 -1 = i< 9
            self.neighbors.append(grid[i + 1][j]) # right neighbour
        # assigning neighbours for above and below  neighbours in the grid
        if j < cols - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])
