import random

class MinesweeperGrid:
    def __init__(self, rows, cols, mine_count):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.board = [[0] * cols for _ in range(rows)]
        self.adjacency_matrix = [[0] * (rows * cols) for _ in range(rows * cols)]
        self.mines = set()
        self.place_mines()
        self.calculate_numbers()
        self.build_adjacency_matrix()

    def place_mines(self):
        while len(self.mines) < self.mine_count:
            mine = random.randint(0, self.rows * self.cols - 1)
            self.mines.add(mine)

    def calculate_numbers(self):
        for mine in self.mines:
            x, y = divmod(mine, self.cols)
            self.board[x][y] = -1
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols and self.board[nx][ny] != -1:
                        self.board[nx][ny] += 1

    def build_adjacency_matrix(self):
        for i in range(self.rows):
            for j in range(self.cols):
                node = i * self.cols + j
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < self.rows and 0 <= ny < self.cols:
                            neighbor = nx * self.cols + ny
                            self.adjacency_matrix[node][neighbor] = 1

    def display_board(self):
        for row in self.board:
            print(" ".join(str(cell) if cell != -1 else "M" for cell in row))

    def display_adjacency_matrix(self):
        for row in self.adjacency_matrix:
            print(row)