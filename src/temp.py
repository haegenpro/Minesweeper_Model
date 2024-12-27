def detect_holes_and_triangles(self, x, y):
        number = int(self.game.visible_grid[x][y])
        neighbors = self.get_neighbors(x, y)
        unrevealed = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == '*']
        flagged = [n for n in neighbors if self.game.visible_grid[n[0]][n[1]] == 'F']

        for nx, ny in neighbors:
            if self.game.visible_grid[nx][ny].isdigit():
                adjacent_number = int(self.game.visible_grid[nx][ny])
                adjacent_neighbors = self.get_neighbors(nx, ny)
                shared_unrevealed = [n for n in unrevealed if n in adjacent_neighbors]
                if len(shared_unrevealed) == len(unrevealed) and len(shared_unrevealed) == (adjacent_number - len([n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F'])):
                    unique_to_current = [n for n in unrevealed if n not in shared_unrevealed]
                    unique_to_adjacent = [n for n in adjacent_neighbors if n not in shared_unrevealed]

                    diff = number - len(flagged)
                    adj_diff = adjacent_number - len([n for n in adjacent_neighbors if self.game.visible_grid[n[0]][n[1]] == 'F'])

                    if diff == len(unique_to_current):
                        self.flag_cells(unique_to_current)
                    if adj_diff == len(unique_to_adjacent):
                        self.flag_cells(unique_to_adjacent)

                    if diff + adj_diff == len(shared_unrevealed):
                        for sx, sy in shared_unrevealed:
                            self.game.reveal_cell(sx, sy)
                    return True
        return False