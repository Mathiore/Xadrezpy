import pygame
import os
from tkinter import messagebox, Tk
import random

# Inicializa o pygame
pygame.init()

# Dimensões
WIDTH, HEIGHT = 1000, 640  # Aumentado para comportar mini tabuleiros e menu
ROWS, COLS = 8, 8
SQUARE_SIZE = 640 // COLS

# Cores
WHITE = (255, 255, 255)
GREEN = (118, 150, 86)
BEIGE = (238, 238, 210)
HIGHLIGHT = (255, 255, 0, 100)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Carrega imagens
PIECE_IMAGES = {}
for piece in ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
              'bp', 'br', 'bn', 'bb', 'bq', 'bk']:
    PIECE_IMAGES[piece] = pygame.transform.scale(
        pygame.image.load(os.path.join('pieces', piece + '.png')),
        (SQUARE_SIZE, SQUARE_SIZE)
    )

MINI_PIECE_IMAGES = {}
for piece in PIECE_IMAGES:
    MINI_PIECE_IMAGES[piece] = pygame.transform.scale(
        PIECE_IMAGES[piece], (SQUARE_SIZE//3, SQUARE_SIZE//3)
    )

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess with Rules")

# Tabuleiro inicial
def get_initial_board():
    return [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["wp"] * 8,
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
    ]

board = get_initial_board()
selected = None
turn = 'w'
possible_moves = []
mode = None

PIECE_VALUES = {
    'p': 10,
    'n': 30,
    'b': 30,
    'r': 50,
    'q': 90,
    'k': 900
}



def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(WIN, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Marcar a peça selecionada
    if selected:
        sel_row, sel_col = selected
        pygame.draw.rect(WIN, (255, 255, 0), (sel_col*SQUARE_SIZE, sel_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    # Desenhar círculos nos movimentos possíveis
    for move in possible_moves:
        r, c = move
        pygame.draw.circle(WIN, (255, 255, 0), (c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2), 10)


def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                WIN.blit(PIECE_IMAGES[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))


def get_row_col_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE


def valid_moves(piece, start):
    row, col = start
    moves = []
    color = piece[0]
    kind = piece[1]

    directions = {
        'p': [(-1, 0), (-2, 0), (-1, -1), (-1, 1)] if color == 'w' else [(1, 0), (2, 0), (1, -1), (1, 1)],
        'r': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        'n': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
        'b': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'q': [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
        'k': [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    }

    if kind == 'p':
        step = 1 if color == 'b' else -1
        if 0 <= row + step < 8 and board[row+step][col] == "":
            moves.append((row+step, col))
            if (color == 'w' and row == 6) or (color == 'b' and row == 1):
                if board[row+2*step][col] == "":
                    moves.append((row+2*step, col))
        for dx in [-1, 1]:
            if 0 <= col+dx < 8 and 0 <= row+step < 8:
                target = board[row+step][col+dx]
                if target != "" and target[0] != color:
                    moves.append((row+step, col+dx))

    elif kind in ['r', 'b', 'q']:
        for dr, dc in directions[kind]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "":
                    moves.append((r, c))
                elif board[r][c][0] != color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    elif kind == 'n' or kind == 'k':
        for dr, dc in directions[kind]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "" or board[r][c][0] != color:
                    moves.append((r, c))

    return moves


def check_victory():
    kings = {'w': False, 'b': False}
    for row in board:
        for piece in row:
            if piece == 'wk':
                kings['w'] = True
            if piece == 'bk':
                kings['b'] = True
    if not kings['w']:
        return 'Black wins!'
    if not kings['b']:
        return 'White wins!'
    return None


def show_victory_message(message):
    root = Tk()
    root.withdraw()
    response = messagebox.askquestion("Game Over", f"{message}\nDo you want to play again?")
    root.destroy()
    return response == 'yes'


def move_piece(start, end):
    global turn
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if piece == "" or piece[0] != turn:
        return False
    if (er, ec) in valid_moves(piece, start):
        board[er][ec] = piece
        board[sr][sc] = ""
        turn = 'b' if turn == 'w' else 'w'
        return True
    return False


def draw_mini_board(x_offset, y_offset, player_color):
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else GREEN
            square = pygame.Rect(x_offset + col*SQUARE_SIZE//3, y_offset + row*SQUARE_SIZE//3, SQUARE_SIZE//3, SQUARE_SIZE//3)
            pygame.draw.rect(WIN, color, square)
            piece = board[row][col]
            if piece != "" and piece[0] == player_color:
                WIN.blit(MINI_PIECE_IMAGES[piece], (x_offset + col*SQUARE_SIZE//3, y_offset + row*SQUARE_SIZE//3))


def menu():
    font = pygame.font.SysFont(None, 40)
    WIN.fill(WHITE)

    pvp_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 120, 200, 50)
    ai_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
    pygame.draw.rect(WIN, GRAY, pvp_btn)
    pygame.draw.rect(WIN, GRAY, ai_btn)
    WIN.blit(font.render("Player vs Player", True, BLACK), (WIDTH//2 - 90, HEIGHT//2 - 105))
    WIN.blit(font.render("Player vs AI", True, BLACK), (WIDTH//2 - 65, HEIGHT//2 - 45))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_btn.collidepoint(event.pos):
                    return 'pvp', None
                if ai_btn.collidepoint(event.pos):
                    return difficulty_menu()

def difficulty_menu():
    font = pygame.font.SysFont(None, 40)
    WIN.fill(WHITE)

    easy_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
    hard_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50)
    pygame.draw.rect(WIN, GRAY, easy_btn)
    pygame.draw.rect(WIN, GRAY, hard_btn)
    WIN.blit(font.render("Médio (Depth 2)", True, BLACK), (WIDTH//2 - 90, HEIGHT//2 - 45))
    WIN.blit(font.render("Difícil (Depth 3)", True, BLACK), (WIDTH//2 - 90, HEIGHT//2 + 25))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    return 'ai', 2
                if hard_btn.collidepoint(event.pos):
                    return 'ai', 3


def main():
    global selected, possible_moves, board, turn, mode
    clock = pygame.time.Clock()
    mode, ai_depth = menu()
    run = True

    while run:
        clock.tick(60)
        draw_board()
        draw_pieces()
        draw_mini_board(660, 10, 'b')
        draw_mini_board(660, 330, 'w')
        pygame.display.update()

        winner = check_victory()
        if winner:
            again = show_victory_message(winner)
            if again:
                board = get_initial_board()
                turn = 'w'
                selected = None
                possible_moves = []
            else:
                run = False
                continue

        if mode == 'ai' and turn == 'b':
            ai_move(ai_depth)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= WIDTH or pos[1] >= HEIGHT:
                    continue
                row, col = get_row_col_from_mouse(pos)

                if selected:
                    if (row, col) == selected:
                        selected = None
                        possible_moves = []
                    else:
                        moved = move_piece(selected, (row, col))
                        if moved:
                            selected = None
                            possible_moves = []
                else:
                    if board[row][col] != "" and board[row][col][0] == turn:
                        selected = (row, col)
                        possible_moves = valid_moves(board[row][col], (row, col))

    pygame.quit()



def ai_move(depth):
    global turn
    if check_victory():
        return

    def evaluate_board():
        piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 1000}
        score = 0
        for row in board:
            for piece in row:
                if piece != "":
                    value = piece_values.get(piece[1], 0)
                    score += value if piece[0] == 'b' else -value
        return score

    def get_all_moves(color):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != "" and piece[0] == color:
                    for move in valid_moves(piece, (r, c)):
                        moves.append(((r, c), move))
        return moves

    def minimax(depth, alpha, beta, maximizing):
        if depth == 0 or check_victory():
            return evaluate_board(), None

        color = 'b' if maximizing else 'w'
        best = None
        if maximizing:
            max_eval = float('-inf')
            for move in get_all_moves(color):
                backup = board[move[1][0]][move[1][1]]
                piece = board[move[0][0]][move[0][1]]
                board[move[1][0]][move[1][1]] = piece
                board[move[0][0]][move[0][1]] = ""
                eval, _ = minimax(depth - 1, alpha, beta, False)
                board[move[0][0]][move[0][1]] = piece
                board[move[1][0]][move[1][1]] = backup
                if eval > max_eval:
                    max_eval = eval
                    best = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best
        else:
            min_eval = float('inf')
            for move in get_all_moves(color):
                backup = board[move[1][0]][move[1][1]]
                piece = board[move[0][0]][move[0][1]]
                board[move[1][0]][move[1][1]] = piece
                board[move[0][0]][move[0][1]] = ""
                eval, _ = minimax(depth - 1, alpha, beta, True)
                board[move[0][0]][move[0][1]] = piece
                board[move[1][0]][move[1][1]] = backup
                if eval < min_eval:
                    min_eval = eval
                    best = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best

    _, best = minimax(depth, float('-inf'), float('inf'), True)
    if best:
        print(f"IA move: {best}")
        move_piece(*best)
    else:
        print("IA sem movimentos válidos.")
        winner = check_victory()
        if not winner:
            turn = 'w'  # devolve o turno ao jogador humano


if __name__ == "__main__":
    main()