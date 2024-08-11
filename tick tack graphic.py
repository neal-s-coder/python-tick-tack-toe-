import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg='sky blue')
        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.single_player = True  # Set to True for single-player mode

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text=" ", font=('normal', 40), width=5, height=2,
                                   command=lambda row=row, col=col: self.on_button_click(row, col),
                                   bg='sky blue')
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_win(self.current_player):
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.single_player and self.current_player == "O":
                    self.computer_move()

    def computer_move(self):
        if random.random() < 0.5:  # 50% chance to make a random move
            available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
            row, col = random.choice(available_moves)
        else:
            best_score = -float('inf')
            best_move = None
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = "O"
                        score = self.minimax(self.board, 0, False)
                        self.board[row][col] = " "
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
            row, col = best_move
        self.board[row][col] = "O"
        self.buttons[row][col].config(text="O")
        if self.check_win("O"):
            messagebox.showinfo("Tic-Tac-Toe", "Player O wins!")
            self.reset_board()
        elif self.check_draw():
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            self.reset_board()
        else:
            self.current_player = "X"

    def minimax(self, board, depth, is_maximizing):
        if self.check_win("O"):
            return 1
        elif self.check_win("X"):
            return -1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":
                        board[row][col] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":
                        board[row][col] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = " "
                        best_score = min(score, best_score)
            return best_score

    def check_win(self, player):
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def check_draw(self):
        return all([cell in ['X', 'O'] for row in self.board for cell in row])

    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
