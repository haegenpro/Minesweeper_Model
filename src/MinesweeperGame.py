from MinesweeperGrid import MinesweeperGrid

class MinesweeperGame:
    UNOPENED_CELL = '*'

    def __init__(self, rows, cols, mine_count):
        self.grid = MinesweeperGrid(rows, cols, mine_count)
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.visible_grid = [[self.UNOPENED_CELL for _ in range(cols)] for _ in range(rows)]
        self.revealed = set()
        self.flagged = set()
        self.game_over = False
        self.win = False

    def reveal_cell(self, x, y):
        if (x, y) in self.revealed or (x, y) in self.flagged or self.game_over:
            return
        if self.grid.board[x][y] == -1:
            self.game_over = True
            self.visible_grid[x][y] = 'M'
            print("A mine was hit! Game over.")
            return
        self.revealed.add((x, y))
        self.visible_grid[x][y] = str(self.grid.board[x][y])
        if self.grid.board[x][y] == 0:
            self._reveal_safe_zone(x, y)
        self.check_win()

    def flag_cell(self, x, y):
        if (x, y) in self.revealed or self.game_over:
            return
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))
            self.visible_grid[x][y] = self.UNOPENED_CELL
        else:
            self.flagged.add((x, y))
            self.visible_grid[x][y] = 'F'

    def _reveal_safe_zone(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and (nx, ny) not in self.revealed:
                    self.reveal_cell(nx, ny)

    def check_win(self):
        if len(self.revealed) == self.rows * self.cols - self.mine_count:
            self.win = True
            self.game_over = True

    def display_visible_grid(self):
        for row in self.visible_grid:
            print(" ".join(cell if cell != ' ' else self.UNOPENED_CELL for cell in row))
        print()
    
