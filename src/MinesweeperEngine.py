from MinesweeperGame import MinesweeperGame

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

                    if len(unrevealed) == number:
                        self.flag_cells(unrevealed)
                        move_made = True
                        processed.add((x, y))  # Mark cell as processed

        # Step 3: Apply patterns if no move has been made
        if not move_made:
            move_made = self.apply_patterns()

        # Step 4: Probability-based guess as a last resort
        if not move_made:
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
    
    def apply_patterns(self):
        move_made = False
        for x in range(self.game.rows):
            for y in range(self.game.cols):
                if self.game.visible_grid[x][y].isdigit():
                    if move_made:  # Stop further checks once a move is made
                        break
                    if self.detect_1_1(x, y):
                        move_made = True
                    if self.detect_1_2(x, y):
                        move_made = True
                    if self.detect_holes_and_triangles(x, y):
                        move_made = True
        return move_made

    def probability_guess(self):
        # Placeholder for probability-based guessing logic
        for x in range(self.game.rows):
            for y in range(self.game.cols):
                if self.game.visible_grid[x][y] == '*':
                    self.game.reveal_cell(x, y)
                    return
    
    def detect_1_1(self, x, y):
        number = int(self.game.visible_grid[x][y])
        neighbors = self.get_neighbors(x, y)
        unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
        flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

        if number - len(flagged) == 1:  # Check if current number can form part of 1-1 pattern
            for nx, ny in neighbors:
                if self.game.visible_grid[nx][ny].isdigit():
                    adjacent_number = int(self.game.visible_grid[nx][ny])
                    adjacent_neighbors = self.get_neighbors(nx, ny)
                    unique_unrevealed = [n for n in adjacent_neighbors if n not in unrevealed]
                    shared_unrevealed = [n for n in unrevealed if n in adjacent_neighbors]
                    adjacent_flagged = [n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']
                    
                    if (adjacent_number - len(adjacent_flagged)) == 1 and len(shared_unrevealed) == 1:
                        # Open the unique unrevealed cells adjacent only to the second number
                        for sx, sy in unique_unrevealed:
                            self.game.reveal_cell(sx, sy)
                        return True
        return False

    def detect_1_2(self, x, y):
        number = int(self.game.visible_grid[x][y])
        neighbors = self.get_neighbors(x, y)
        unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
        flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

        if number - len(flagged) == 1:  # Check if current number can form part of 1-2 pattern
            for nx, ny in neighbors:
                if self.game.visible_grid[nx][ny].isdigit():
                    adjacent_number = int(self.game.visible_grid[nx][ny])
                    adjacent_neighbors = self.get_neighbors(nx, ny)
                    shared_unrevealed = [n for n in unrevealed if n in adjacent_neighbors]
                    adjacent_flagged = [n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']
                    
                    if (adjacent_number - len(adjacent_flagged)) == 2 and len(shared_unrevealed) == 1:
                        # Apply reduction logic and reveal safe cells
                        safe_cells = [n for n in unrevealed if n not in shared_unrevealed]
                        for sx, sy in safe_cells:
                            self.game.reveal_cell(sx, sy)
                        # Flag mines in shared cells
                        for fx, fy in shared_unrevealed:
                            self.game.flag_cell(fx, fy)
                        return True
        return False

    def detect_holes_and_triangles(self, x, y):
        number = int(self.game.visible_grid[x][y])
        neighbors = self.get_neighbors(x, y)
        unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
        flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

        for nx, ny in neighbors:
            if self.game.visible_grid[nx][ny].isdigit():
                adjacent_number = int(self.game.visible_grid[nx][ny])
                adjacent_neighbors = self.get_neighbors(nx, ny)
                adjacent_unrevealed = [n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
                adjacent_flagged = [n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

                shared_unrevealed = [n for n in unrevealed if n in adjacent_unrevealed]
                unique_to_current = [n for n in unrevealed if n not in shared_unrevealed]
                unique_to_adjacent = [n for n in adjacent_unrevealed if n not in shared_unrevealed]

                # Analyze based on the difference in numbers
                diff = number - len(flagged)
                adj_diff = adjacent_number - len(adjacent_flagged)

                # Flag unique cells if conditions are met
                if diff == len(unique_to_current):
                    for ux, uy in unique_to_current:
                        self.game.flag_cell(ux, uy)
                if adj_diff == len(unique_to_adjacent):
                    for ux, uy in unique_to_adjacent:
                        self.game.flag_cell(ux, uy)

                # Reveal shared cells if no mines remain to be flagged
                if diff + adj_diff == len(shared_unrevealed):
                    for sx, sy in shared_unrevealed:
                        self.game.reveal_cell(sx, sy)

                return True  # A move was made
        return False
    def flag_cells(self, cells):
        """Flag a list of cells as mines."""
        for x, y in cells:
            if self.game.visible_grid[x][y] != 'F':
                self.game.flag_cell(x, y)
    
engine = MinesweeperEngine(8, 8, 10)
engine.solve()
