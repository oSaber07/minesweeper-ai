import random

class MinesweeperAI:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1:
                    self.board[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.board[r][c] == -1:
                    count += 1
        return count

    def reveal(self, row, col):
        if not self.revealed[row][col]:
            self.revealed[row][col] = True
            if self.board[row][col] == 0:
                for r in range(max(0, row - 1), min(self.rows, row + 2)):
                    for c in range(max(0, col - 1), min(self.cols, col + 2)):
                        if not self.revealed[r][c]:
                            self.reveal(r, c)
        return self.board[row][col]

    def solve(self):
        # Start by revealing a random cell
        self.reveal(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

        while not self.is_game_won():
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.revealed[row][col] and self.board[row][col] > 0:
                        self.process_cell(row, col)

            # If no progress was made, make a guess
            if not any(any(cell for cell in row) for row in self.revealed):
                unrevealed = [(r, c) for r in range(self.rows) for c in range(self.cols) if not self.revealed[r][c]]
                if unrevealed:
                    row, col = random.choice(unrevealed)
                    self.reveal(row, col)

        return self.revealed, self.flagged

    def process_cell(self, row, col):
        adjacent_unrevealed = self.get_adjacent_unrevealed(row, col)
        adjacent_flags = self.get_adjacent_flags(row, col)

        if len(adjacent_flags) == self.board[row][col]:
            for r, c in adjacent_unrevealed:
                if not self.flagged[r][c]:
                    self.reveal(r, c)
        elif len(adjacent_unrevealed) + len(adjacent_flags) == self.board[row][col]:
            for r, c in adjacent_unrevealed:
                if not self.flagged[r][c]:
                    self.flagged[r][c] = True

    def get_adjacent_unrevealed(self, row, col):
        return [(r, c) for r in range(max(0, row - 1), min(self.rows, row + 2))
                for c in range(max(0, col - 1), min(self.cols, col + 2))
                if not self.revealed[r][c]]

    def get_adjacent_flags(self, row, col):
        return [(r, c) for r in range(max(0, row - 1), min(self.rows, row + 2))
                for c in range(max(0, col - 1), min(self.cols, col + 2))
                if self.flagged[r][c]]

    def is_game_won(self):
        return all(self.revealed[r][c] or self.board[r][c] == -1
                   for r in range(self.rows)
                   for c in range(self.cols))

    def print_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.flagged[row][col]:
                    print('F', end=' ')
                elif not self.revealed[row][col]:
                    print('.', end=' ')
                elif self.board[row][col] == -1:
                    print('*', end=' ')
                else:
                    print(self.board[row][col], end=' ')
            print()
        print()

def main():
    rows, cols, num_mines = 10, 10, 10
    game = MinesweeperAI(rows, cols, num_mines)
    revealed, flagged = game.solve()
    game.print_board()
    print("Game solved!" if game.is_game_won() else "Game not solved.")

if __name__ == "__main__":
    main()