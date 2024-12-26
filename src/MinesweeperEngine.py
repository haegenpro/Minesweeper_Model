from MinesweeperGame import MinesweeperGame

class MinesweeperEngine:
    def __init__(self, rows, cols, mine_count):
        self.game = MinesweeperGame(rows, cols, mine_count)
        self.game.display_visible_grid()

    def play_game(self):
        while not self.game.game_over:
            x, y, action = self.get_user_input()
            if action == 'R':
                self.game.reveal_cell(x, y)
            elif action == 'F':
                self.game.flag_cell(x, y)
            self.game.display_visible_grid()
        if self.game.win:
            print("Congratulations! You won the game.")
        else:
            print("Game Over! You lost the game.")

    def get_user_input(self):
        x, y, action = input("Enter x, y coordinates and action (R for reveal, F for flag): ").split()
        x, y = int(x), int(y)
        return x, y, action

    def simulate_solver(self):
        self.game.simulate_solver()
    
        