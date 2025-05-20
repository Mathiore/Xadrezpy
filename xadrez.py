import pygame
import os
from tkinter import messagebox, Tk

# Inicializa o pygame
pygame.init()

# Dimensões
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Cores
WHITE = (255, 255, 255)
GREEN = (118, 150, 86)
BEIGE = (238, 238, 210)
HIGHLIGHT = (255, 255, 0, 100)

# Carrega imagens
PIECE_IMAGES = {}
for piece in ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
              'bp', 'br', 'bn', 'bb', 'bq', 'bk']:
    PIECE_IMAGES[piece] = pygame.transform.scale(
        pygame.image.load(os.path.join('pieces', piece + '.png')),
        (SQUARE_SIZE, SQUARE_SIZE)
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

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(WIN, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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

def main():
    global selected, possible_moves, board, turn
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        draw_board()
        draw_pieces()
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
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
                else:
                    if board[row][col] != "" and board[row][col][0] == turn:
                        selected = (row, col)
                        possible_moves = valid_moves(board[row][col], (row, col))

    pygame.quit()

if __name__ == "__main__":
    main()
