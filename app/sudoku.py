import random

class Sudoku6x6:
    def __init__(self):
        self.size = 6
        self.rows = 2
        self.cols = 3

    def is_valid(self, grid, row, col, num):
        # Row & Column Check
        for i in range(6):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        
        # 2x3 Box Check
        start_row, start_col = 2 * (row // 2), 3 * (col // 3)
        for r in range(start_row, start_row + 2):
            for c in range(start_col, start_col + 3):
                if grid[r][c] == num:
                    return False
        return True

    def solve(self, grid):
        for row in range(6):
            for col in range(6):
                if grid[row][col] == 0:
                    nums = list(range(1, 7))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def generate_puzzle(self, clues=18):
        board = [[0] * 6 for _ in range(6)]
        self.solve(board)
        
        solution = [row[:] for row in board]
        puzzle = [row[:] for row in board]
        
        cells = [(r, c) for r in range(6) for c in range(6)]
        random.shuffle(cells)
        
        removed = 0
        target_remove = 36 - clues
        for r, c in cells:
            if removed >= target_remove:
                break
            puzzle[r][c] = 0
            removed += 1
            
        return puzzle, solution