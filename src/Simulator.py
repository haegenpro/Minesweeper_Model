from MinesweeperEngine import MinesweeperEngine

def simulate_win_rate(difficulty, rows, cols, mines, iterations):
    wins = 0
    for i in range(iterations):
        engine = MinesweeperEngine(rows, cols, mines)
        engine.solve()
        if engine.game.win:
            wins += 1
        print(f"Game {i + 1}/{iterations}: {'Win' if engine.game.win else 'Loss'}")
    win_rate = (wins / iterations) * 100
    return win_rate

def main():
    difficulties = {
        "Beginner": (9, 9, 10),
        "Intermediate": (16, 16, 40),
        "Expert": (16, 30, 99)
    }
    iterations = 100
    print("Simulating Minesweeper Win Rates...\n")
    for difficulty, (rows, cols, mines) in difficulties.items():
        print(f"Simulating {difficulty} Level ({iterations} games)")
        win_rate = simulate_win_rate(difficulty, rows, cols, mines, iterations)
        print(f"{difficulty} Level Win Rate: {win_rate:.2f}%\n")

if __name__ == "__main__":
    main()
