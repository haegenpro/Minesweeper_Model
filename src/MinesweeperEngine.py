from MinesweeperGame import MinesweeperGame
import random

class MinesweeperEngine:
    def __init__(self, rows, cols, mine_count):
        self.game = MinesweeperGame(rows, cols, mine_count)
    
    def solve(self):
        print("Starting Minesweeper Solver...")
        while not self.game.game_over:
            move_made = self.simulate_solver()
            if not move_made:
                print("No safe moves detected, stopping.")
                break
            self.game.display_visible_grid()
        if self.game.win:
            print("Solver won the game!")
        else:
            print("Solver lost the game.")

    def simulate_solver(self):
        move_made = False
        processed = set()  # Track cells that have been processed

        # Step 1: Safe reveals
        for x in range(self.game.rows):
            for y in range(self.game.cols):
                if (x, y) in processed:  # Skip already processed cells
                    continue
                if self.game.visible_grid[x][y].isdigit():
                    number = int(self.game.visible_grid[x][y])
                    neighbors = self.get_neighbors(x, y)
                    unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
                    flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

                    if len(unrevealed) > 0 and len(flagged) == number:
                        for nx, ny in unrevealed:
                            self.game.reveal_cell(nx, ny)
                            move_made = True
                        processed.add((x, y))  # Mark cell as processed

        # Step 2: Flag mines
        for x in range(self.game.rows):
            for y in range(self.game.cols):
                if (x, y) in processed:  # Skip already processed cells
                    continue
                if self.game.visible_grid[x][y].isdigit():
                    number = int(self.game.visible_grid[x][y])
                    neighbors = self.get_neighbors(x, y)
                    unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
                    flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

                    if len(unrevealed) > 0 and len(unrevealed) + len(flagged) == number:
                        self.flag_cells(unrevealed)
                        move_made = True
                        processed.add((x, y))  # Mark cell as processed

        # Step 3: Apply patterns if no move has been made
        if not move_made:
            move_made = self.apply_patterns(processed)

        # Step 4: Probability-based guess as a last resort
        if not move_made:
            print("Making a probability-based guess.")
            self.probability_guess()
            move_made = True

        # Safeguard: If no progress is possible, stop processing
        if not move_made:
            print("No progress possible. Solver stopping.")
            self.game.game_over = True

        return move_made

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.game.rows and 0 <= ny < self.game.cols:
                    neighbors.append((nx, ny))
        return neighbors
    
    def apply_patterns(self, processed):
        move_made = False

        for x in range(self.game.rows):
            for y in range(self.game.cols):
                if (x, y) in processed:  # Skip cells already processed
                    continue
                if self.game.visible_grid[x][y].isdigit():
                    # Detect patterns, skip further checks if a move is made
                    if self.detect_1_1(x, y, processed):
                        move_made = True
                        print(f"1-1 pattern detected at ({x}, {y}).")
                        break
                    if self.detect_2_1(x, y, processed):
                        move_made = True
                        print(f"2-1 pattern detected at ({x}, {y}).")
                        break
        return move_made

    def probability_guess(self):
        """Make a random guess among unrevealed cells."""
        unrevealed_cells = [(x, y) for x in range(self.game.rows) for y in range(self.game.cols) if self.game.visible_grid[x][y] == '*']
        if unrevealed_cells:
            x, y = random.choice(unrevealed_cells)
            self.game.reveal_cell(x, y)
            return True

    def detect_1_1(self, x, y, processed):
        number = int(self.game.visible_grid[x][y])
        neighbors = self.get_neighbors(x, y)
        unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
        flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

        # Skip cells with no unrevealed neighbors
        if not unrevealed:
            return False

        for nx, ny in neighbors:
            if self.game.visible_grid[nx][ny].isdigit():
                adjacent_number = int(self.game.visible_grid[nx][ny])
                adjacent_neighbors = self.get_neighbors(nx, ny)

                # Compute shared and unique cells
                shared_unrevealed = [n for n in unrevealed if n in adjacent_neighbors]
                for sx, sy in shared_unrevealed:
                    print(f"Shared unrevealed cell at ({sx}, {sy})")
                unique_unrevealed = [n for n in adjacent_neighbors if n not in shared_unrevealed]
                for ux, uy in unique_unrevealed:
                    print(f"Unique unrevealed cell at ({ux}, {uy})")
                adjacent_flagged = [n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

                # Skip if no actionable unique cells or all neighbors are processed
                if not shared_unrevealed or (x, y) in processed or (nx, ny) in processed:
                    continue

                # Ensure the pattern logic is valid
                if len(shared_unrevealed) == len(unrevealed) and adjacent_number - len(adjacent_flagged) == 1:
                    if not unique_unrevealed:
                        processed.add((x, y))
                        processed.add((nx, ny))
                        return False

                    # Reveal unique cells
                    for ux, uy in unique_unrevealed:
                        print(f"Revealing unique cell at ({ux}, {uy})")
                        self.game.reveal_cell(ux, uy)
                    processed.add((x, y))  # Mark as processed
                    processed.add((nx, ny))
                    return True
        return False


    def detect_2_1(self, x, y, processed):
        number = int(self.game.visible_grid[x][y])
        neighbors = self.get_neighbors(x, y)
        unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
        flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

        # Skip cells with no unrevealed neighbors
        if not unrevealed:
            return False

        if number - len(flagged) == 2:  # "2" clue logic
            for nx, ny in neighbors:
                if self.game.visible_grid[nx][ny].isdigit():
                    adjacent_number = int(self.game.visible_grid[nx][ny])
                    adjacent_neighbors = self.get_neighbors(nx, ny)
                    shared_unrevealed = [n for n in unrevealed if n in adjacent_neighbors]
                    unique_to_2 = [n for n in unrevealed if n not in shared_unrevealed]
                    adjacent_flagged = [n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

                    # Ensure the adjacent "1" logic holds
                    if adjacent_number - len(adjacent_flagged) == 1 and len(unique_to_2) == 1:
                        # Flag the unique cell for the "2"
                        for ux, uy in unique_to_2:
                            self.game.flag_cell(ux, uy)
                        processed.add((x, y))  # Mark as processed
                        processed.add((nx, ny))
                        return True
        return False

    def flag_cells(self, cells):
        """Flag a list of cells as mines."""
        for x, y in cells:
            if self.game.visible_grid[x][y] != 'F':
                self.game.flag_cell(x, y)
    
    def save_test_results(self, file_path):
        with open(file_path, "w") as file:
            file.write("Minesweeper Engine Test Results\n")
            file.write("===============================\n")
            file.write(f"Grid Size: {self.game.rows}x{self.game.cols}\n")
            file.write(f"Number of Mines: {self.game.mine_count}\n")
            file.write(f"Game Outcome: {'Win' if self.game.win else 'Loss'}\n")
            file.write("\nFinal Game State:\n")
            for row in self.game.visible_grid:
                file.write(" ".join(row) + "\n")
            file.write("\nSolution Grid:\n")
            for row in self.game.grid.board:
                file.write(" ".join(str(cell) if cell != -1 else "M" for cell in row) + "\n")
        print(f"Test results saved to {file_path}")

engine = MinesweeperEngine(16, 30, 99)
engine.solve()
# Save the results if the game finishes successfully
if engine.game.win or engine.game.game_over:
    engine.save_test_results("Minesweeper_Model/test/test_results_3.txt")
