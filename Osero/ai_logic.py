import random
import copy

EMPTY, BLACK, WHITE = 0, 1, 2
BOARD_SIZE = 8

def directions():
    return [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]

def is_valid_move(board, x, y, color):
    if board[y][x] != EMPTY:
        return False
    return any(check_direction(board, x, y, dx, dy, color) for dx, dy in directions())

def check_direction(board, x, y, dx, dy, color):
    x += dx
    y += dy
    stones = []
    while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        if board[y][x] == 3 - color:
            stones.append((x, y))
        elif board[y][x] == color:
            return len(stones) > 0
        else:
            break
        x += dx
        y += dy
    return False

def place_stone(board, x, y, color):
    board[y][x] = color
    for dx, dy in directions():
        if check_direction(board, x, y, dx, dy, color):
            flip_stones(board, x, y, dx, dy, color)

def flip_stones(board, x, y, dx, dy, color):
    x += dx
    y += dy
    while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == 3 - color:
        board[y][x] = color
        x += dx
        y += dy

def find_valid_moves(board, color):
    return [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if is_valid_move(board, x, y, color)]

# 評価関数（角が強く、辺が中、その他は低め）
def evaluate_board(board, color):
    weights = [
        [100, -20, 10, 5, 5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [10, -2, 5, 1, 1, 5, -2, 10],
        [5, -2, 1, 0, 0, 1, -2, 5],
        [5, -2, 1, 0, 0, 1, -2, 5],
        [10, -2, 5, 1, 1, 5, -2, 10],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [100, -20, 10, 5, 5, 10, -20, 100]
    ]
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == color:
                score += weights[y][x]
            elif board[y][x] == 3 - color:
                score -= weights[y][x]
    return score

# 最弱：接待モード（常に最悪手を選ぶ）
def find_worst_move(board, color):
    moves = find_valid_moves(board, color)
    if not moves:
        return None
    worst_score = float("inf")
    worst_move = None
    for move in moves:
        sim_board = copy.deepcopy(board)
        place_stone(sim_board, move[0], move[1], color)
        score = evaluate_board(sim_board, color)
        if score < worst_score:
            worst_score = score
            worst_move = move
    return worst_move

# 初心者：ランダム
def find_random_move(board, color):
    moves = find_valid_moves(board, color)
    return random.choice(moves) if moves else None

# 中級者：取れる石数最大の手
def find_greedy_move(board, color):
    moves = find_valid_moves(board, color)
    if not moves:
        return None
    max_gain = -1
    best_move = None
    for move in moves:
        gain = count_flippable_stones(board, move[0], move[1], color)
        if gain > max_gain:
            max_gain = gain
            best_move = move
    return best_move

def count_flippable_stones(board, x, y, color):
    total = 0
    for dx, dy in directions():
        total += count_in_direction(board, x, y, dx, dy, color)
    return total

def count_in_direction(board, x, y, dx, dy, color):
    x += dx
    y += dy
    count = 0
    while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        if board[y][x] == 3 - color:
            count += 1
        elif board[y][x] == color:
            return count
        else:
            break
        x += dx
        y += dy
    return 0

# 上級者：評価関数 + 1手先ミニマックス（深さ1）
def find_minimax_move(board, color, depth=1):
    moves = find_valid_moves(board, color)
    if not moves:
        return None
    best_score = float("-inf")
    best_move = None
    for move in moves:
        sim_board = copy.deepcopy(board)
        place_stone(sim_board, move[0], move[1], color)
        score = minimax(sim_board, depth - 1, False, color)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def minimax(board, depth, maximizing, color):
    if depth == 0:
        return evaluate_board(board, color)

    moves = find_valid_moves(board, color if maximizing else 3 - color)
    if not moves:
        return evaluate_board(board, color)

    if maximizing:
        value = float("-inf")
        for move in moves:
            sim_board = copy.deepcopy(board)
            place_stone(sim_board, move[0], move[1], color)
            value = max(value, minimax(sim_board, depth - 1, False, color))
        return value
    else:
        value = float("inf")
        for move in moves:
            sim_board = copy.deepcopy(board)
            place_stone(sim_board, move[0], move[1], 3 - color)
            value = min(value, minimax(sim_board, depth - 1, True, color))
        return value

# 鬼モード：深さ3 or 将来的に強化学習へ切替予定
def find_oni_move(board, color):
    return find_minimax_move(board, color, depth=3)

# ==== メインAI関数 ====
def find_best_move(board, color, level=1):
    if level == 0:
        return find_worst_move(board, color)
    elif level == 1:
        return find_random_move(board, color)
    elif level == 2:
        return find_greedy_move(board, color)
    elif level == 3:
        return find_minimax_move(board, color, depth=1)
    elif level == 4:
        return find_oni_move(board, color)
    else:
        return find_random_move(board, color)  # fallback
