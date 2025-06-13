import tkinter as tk
from tkinter import messagebox
from ai_logic import find_best_move

EMPTY, BLACK, WHITE = 0, 1, 2
BOARD_SIZE = 8

ai_mode_names = {
    0: "接待モード",
    1: "初心者モード",
    2: "中級者モード",
    3: "上級者モード",
    4: "鬼モード"
}

bg_normal = "#228B22"
bg_ai_move = "#ADFF2F"

class ReversiGame:
    def __init__(self, root, mode, ai_first, ai_level):
        self.root = root
        self.mode = mode
        self.ai_first = ai_first
        self.ai_level = ai_level
        self.last_ai_move = None
        self.turn = BLACK
        self.turn_count = 1  # ← ターン数カウント
        self.game_over = False
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.create_widgets()
        self.init_board()
        self.update_board()
        self.root.after(100, self.check_ai_turn)

    def create_widgets(self):
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)

        self.turn_label = tk.Label(info_frame, text="", font=("Arial", 14))
        self.turn_label.pack(side=tk.LEFT, padx=10)

        self.mode_label = tk.Label(info_frame, text=ai_mode_names.get(self.ai_level, ""), font=("Arial", 14, "italic"))
        self.mode_label.pack(side=tk.LEFT, padx=10)

        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                btn = tk.Button(
                    board_frame, width=4, height=2,
                    font=("Arial", 14),
                    command=lambda x=x, y=y: self.handle_click(x, y)
                )
                btn.grid(row=y, column=x, padx=1, pady=1)
                self.buttons[y][x] = btn

    def init_board(self):
        mid = BOARD_SIZE // 2
        self.board[mid-1][mid-1] = WHITE
        self.board[mid][mid] = WHITE
        self.board[mid-1][mid] = BLACK
        self.board[mid][mid-1] = BLACK

    def handle_click(self, x, y):
        if self.game_over:
            return

        if self.mode == "AI" and self.ai_first == (self.turn == BLACK):
            return

        if not self.is_valid_move(x, y, self.turn):
            return

        self.place_stone(x, y, self.turn)
        self.last_ai_move = None
        self.turn = 3 - self.turn
        self.turn_count += 1
        self.update_board()
        self.root.after(100, self.check_ai_turn)

    def check_ai_turn(self):
        if self.game_over or self.mode != "AI":
            return

        if self.ai_first == (self.turn == BLACK):
            move = find_best_move(self.board, self.turn, self.ai_level)
            if move:
                self.place_stone(*move, self.turn)
                self.last_ai_move = move
                self.turn = 3 - self.turn
                self.turn_count += 1
                # 遅延して次のターンを表示
                self.root.after(1000, self.update_board)
                self.root.after(1100, self.check_ai_turn)
            else:
                if not self.has_valid_moves(3 - self.turn):
                    self.end_game()
                else:
                    self.turn_label.config(text=("白（○）" if self.turn == WHITE else "黒（●）") + " はパスしました")
                    self.turn = 3 - self.turn
                    self.root.after(1000, self.update_board)

    def update_board(self):
        if self.game_over:
            return

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                btn = self.buttons[y][x]
                stone = self.board[y][x]
                btn_bg = bg_normal

                if stone == BLACK:
                    btn.config(text="●", fg="black", bg=btn_bg, font=("Arial", 14))
                elif stone == WHITE:
                    btn.config(text="○", fg="white", bg=btn_bg, font=("Arial", 14, "bold"))
                else:
                    btn.config(text="", bg=btn_bg)

                if self.last_ai_move == (x, y):
                    btn.config(bg=bg_ai_move)

        if not self.has_valid_moves(self.turn):
            if self.has_valid_moves(3 - self.turn):
                self.turn_label.config(text=("白（○）" if self.turn == WHITE else "黒（●）") + " はパスしました")
                self.turn = 3 - self.turn
                self.root.after(1000, self.update_board)
                return
            else:
                self.end_game()
                return

        turn_text = "黒の番（●）" if self.turn == BLACK else "白の番（○）"
        self.turn_label.config(text=f"ターン {self.turn_count}｜{turn_text}")

    def end_game(self):
        if self.game_over:
            return
        self.game_over = True

        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        if black_count > white_count:
            winner = "黒（●）の勝ち！"
        elif white_count > black_count:
            winner = "白（○）の勝ち！"
        else:
            winner = "引き分け！"

        messagebox.showinfo("ゲーム終了", f"{winner}\n黒：{black_count}　白：{white_count}")
        self.root.destroy()

    def is_valid_move(self, x, y, color):
        if self.board[y][x] != EMPTY:
            return False
        return any(self.check_direction(x, y, dx, dy, color) for dx, dy in self.directions())

    def has_valid_moves(self, color):
        return any(self.is_valid_move(x, y, color) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE))

    def directions(self):
        return [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]

    def check_direction(self, x, y, dx, dy, color):
        x += dx
        y += dy
        stones_to_flip = []
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if self.board[y][x] == 3 - color:
                stones_to_flip.append((x, y))
            elif self.board[y][x] == color:
                return len(stones_to_flip) > 0
            else:
                break
            x += dx
            y += dy
        return False

    def place_stone(self, x, y, color):
        self.board[y][x] = color
        for dx, dy in self.directions():
            if self.check_direction(x, y, dx, dy, color):
                self.flip_stones(x, y, dx, dy, color)

    def flip_stones(self, x, y, dx, dy, color):
        x += dx
        y += dy
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[y][x] == 3 - color:
            self.board[y][x] = color
            x += dx
            y += dy
