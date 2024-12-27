
# Minesweeper Engine with Graph and Logical Implications


### Overview
This repository contains a comprehensive implementation of a Minesweeper engine powered by graph-based logic and pattern recognition. The project includes core modules for the Minesweeper grid, game mechanics, and engine logic, as well as a simulator to evaluate the engine's performance across different difficulty levels.

The engine uses advanced algorithms to solve Minesweeper puzzles, leveraging logical deductions and heuristic methods. Key features include:

- Basic and advanced Minesweeper patterns (e.g., 1-1, 1-2).
- Modular design for extensibility and clarity.
- A simulator to measure engine win rates.

### Modules

#### MinesweeperGrid
Handles the static structure of the Minesweeper board, including mine placement and number calculations.
Key Features:

- Randomized mine placement.
- Calculation of adjacent mine numbers.
- Grid display for debugging.

Code Snippet:
```sh
import random

class MinesweeperGrid:
    def __init__(self, rows, cols, mine_count):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.board = [[0] * cols for _ in range(rows)]
        self.mines = set()
        self.place_mines()
        self.calculate_numbers()

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
```

#### MinesweeperGame
Implements the interactive gameplay mechanics for Minesweeper.
Key Features:

- Revealing cells and flagging mines.
- Propagation of zero-valued cells.
- Win/loss condition checks.

Code Snippet:

```sh
class MinesweeperGame:
    def __init__(self, rows, cols, mine_count):
        self.grid = MinesweeperGrid(rows, cols, mine_count)
        self.visible_grid = [['*' for _ in range(cols)] for _ in range(rows)]
        self.revealed = set()
        self.flagged = set()
        self.game_over = False
        self.win = False

    def reveal_cell(self, x, y):
        if (x, y) in self.revealed or (x, y) in self.flagged or self.game_over:
            return
        if self.grid.board[x][y] == -1:
            self.game_over = True
            print("Game Over! You hit a mine.")
            return
        self.revealed.add((x, y))
        self.visible_grid[x][y] = str(self.grid.board[x][y])
        if self.grid.board[x][y] == 0:
            self._reveal_safe_zone(x, y)
        self.check_win()
```

#### MinesweeperEngine
The logic-based solver engine that automates Minesweeper gameplay.
Key Features:

- Pattern-based cell analysis (e.g., 1-1, 1-2).
- Recursive logic for safe cell opening.
- Probabilistic guessing for edge cases.

Code Snippet:
```sh
class MinesweeperEngine:
    def __init__(self, rows, cols, mine_count):
        self.game = MinesweeperGame(rows, cols, mine_count)

    def solve(self):
        while not self.game.game_over:
            move_made = self.simulate_solver()
            if not move_made:
                print("No safe moves detected, making a guess.")
                self.probability_guess()
```

#### Simulator
Evaluates the engine's performance by simulating multiple games at different difficulty levels.
Key Features:

- Adjustable iterations and difficulty settings.
- Calculates win rates for Beginner, Intermediate, and Expert levels.

Code Snippet:
```sh
def simulate_win_rate(difficulty, rows, cols, mines, iterations):
    wins = 0
    for i in range(iterations):
        engine = MinesweeperEngine(rows, cols, mines)
        engine.solve()
        if engine.game.win:
            wins += 1
    win_rate = (wins / iterations) * 100
    return win_rate
```
### How to Run

1. Setup:
Ensure Python 3 is installed on your machine. Clone the repository and navigate to the directory.

2. Run the Simulator:
Execute the Simulator.py to simulate games and evaluate win rates.
```sh
python Simulator.py
```

3. Adjust Parameters:
Modify grid dimensions, mine counts, or iterations in the Simulator.py file to test custom configurations.

### Future Enhancements

- Develop a GUI for interactive gameplay.
- Enhance the engine with additional pattern recognition.
- Implement advanced algorithms for dependency chains and endgame strategies.
- Feel free to explore the code and customize it for your needs!

### Contributors
Developer: Haegen Quinston

### License
This repository is licensed under the rules of the MIT License.