import numpy as np
import random
import math


# Define the board size and number of mines for each difficulty level
class MinesweeperGame:
    def __init__(self, level):
        """
        Initializes a Minesweeper game with the specified level of difficulty.

        Args:
            level (str): The level of difficulty, which can be "easy", "medium", or "hard".

        Returns:
            None
        """
        self.level_config = {
            "easy": {"row_size": 9, "col_size": 9, "num_mines": 10},
            "medium": {"row_size": 16, "col_size": 16, "num_mines": 25},
            "hard": {"row_size": 30, "col_size": 16, "num_mines": 99},
        }

        self.row_size = self.level_config[level]["row_size"]
        self.col_size = self.level_config[level]["col_size"]
        self.num_mines = self.level_config[level]["num_mines"]

        self.num_total_cells = self.row_size * self.col_size
        self.board = np.array(self.create_new_board())
        self.original_board = self.board.copy()
        self.n_safe = round(math.sqrt(self.row_size * self.col_size))
        self.is_marked = np.zeros((self.row_size, self.col_size))
        self.init_safe_cells = self.get_safe_cells()

    def create_new_board(self):
        """
        Creates a new Minesweeper board with the specified level of difficulty.

        Returns:
            board (list): A 2D list representing the Minesweeper board.
        """
        board = np.zeros((self.row_size, self.col_size)).astype(int)

        # Randomly place the specified number of mines on the board
        for _ in range(self.num_mines):
            row = random.randint(0, self.row_size - 1)
            col = random.randint(0, self.col_size - 1)

            # If the cell already contains a mine, try again
            while board[row][col] == -1:
                row = random.randint(0, self.row_size - 1)
                col = random.randint(0, self.col_size - 1)

            # Place the mine in the cell
            board[row][col] = -1

        # Calculate the number of surrounding mines for each cell
        for row in range(self.row_size):
            for col in range(self.col_size):
                if board[row][col] == -1:
                    continue

                count = 0
                for i in range(max(0, row - 1), min(row + 2, self.row_size)):
                    for j in range(max(0, col - 1), min(col + 2, self.col_size)):
                        if board[i][j] == -1:
                            count += 1

                board[row][col] = count

        return board

    def update_hint(self, cell):
        """
        Updates the hint for the specified cell.
        """
        row, col = cell
        for i in range(max(0, row - 1), min(row + 2, self.row_size)):
            for j in range(max(0, col - 1), min(col + 2, self.col_size)):
                if self.board[i, j] != -1:
                    self.board[i, j] -= 1

    def get_hint(self, cell):
        """
        Returns the hint for the specified cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            hint (int): The hint for the specified cell.
        """
        return self.board[cell]

    def get_unmarked_neighbor(self, cell):
        """
        Returns a list of neighbors for the specified cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            neighbors (list): A list of neighbors for the specified cell.
        """
        unmarked_neighbors = []
        row, col = cell
        for i in range(max(0, row - 1), min(row + 2, self.row_size)):
            for j in range(max(0, col - 1), min(col + 2, self.col_size)):
                if i == row and j == col:
                    continue
                if self.is_marked[i, j] == 0:
                    unmarked_neighbors.append((i, j))
        return unmarked_neighbors

    def get_safe_cells(self):
        """
        Returns a list of safe cells for the initial move.

        Args:
            None

        Returns:
            safe_cells (list): A list of safe cells for the initial move.
        """
        # Calculate the number of initial safe cells using the formula round(sqrt(#cells))
        num_safe_cells = self.n_safe

        # Generate a list of random safe cells
        safe_cells = []
        while len(safe_cells) < num_safe_cells:
            row = random.randint(0, self.row_size - 1)
            col = random.randint(0, self.col_size - 1)

            if (row, col) not in safe_cells and self.board[row][col] != -1:
                safe_cells.append((row, col))

        return safe_cells

    def get_unmarked_cells(self):
        """
        Returns a list of unmarked cells on the game board.
        """
        cells = []
        for i in range(0, self.row_size):
            for j in range(0, self.col_size):
                if self.is_marked[i, j] == 0:
                    cells.append((i, j))
        return cells

    def get_num_unmarked_mines(self):
        """
        Returns the number of unmarked mines on the game board.
        """
        return np.count_nonzero(self.is_marked[np.where(self.board == -1)] == 0)

    def get_num_unmarked_cells(self):
        """
        Returns the number of unmarked cells on the game board.
        """
        return np.count_nonzero(self.is_marked == 0)

    def get_mark_rate(self):
        """
        Returns the mark rate of the game board.
        """
        return np.count_nonzero(self.is_marked) / self.num_total_cells

    def display(self):
        """
        Displays the current state of the game board.

        Args:
            game: MinesweeperGame object
            KB: KnowledgeBase object
            board: game board
        """
        for row in range(self.is_marked.shape[0]):
            for col in range(self.is_marked.shape[1]):
                if self.is_marked[row, col] == 0:
                    print(". ", end="")
                else:
                    if self.board[row, col] == -1:
                        print("m ", end="")
                    else:
                        print(f"{self.original_board[row, col]} ", end="")
            print()
        print("---------------------------------------")


# if __name__ == "__main__":
#     level = input("Please select a level of difficulty (easy, medium, hard): ")
#     game = MinesweeperGame(level)
#     print("board:")
#     print(game.board)
#     print(f"Board size: {game.row_size} x {game.col_size}")
#     print(f"Number of mines: {game.num_mines}")
#     print(f"Initial safe cells: {game.init_safe_cells}")
