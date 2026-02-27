import sys

import pygame
from pygame.locals import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SQUARE_LENGTH = 80
SQUARE_NUMBER = 9
REFERENCE_POINT = 40
CLICK_LEFT = 1
COLOR = {
    "Black": (0, 0, 0),
    "DarkBrown": (222, 184, 135),
    "LightBrown": (238, 203, 173),
    "Red": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "Yellow": (255, 255, 0),
    "White": (255, 255, 255),
}

INITIAL_POSITIONS = {
    # 後手(上段)
    (0, 0): ("KY", False),  # 香車
    (1, 0): ("KE", False),  # 桂馬
    (2, 0): ("GI", False),  # 銀将
    (3, 0): ("KI", False),  # 金将
    (4, 0): ("OU", False),  # 王将
    (5, 0): ("KI", False),  # 金将
    (6, 0): ("GI", False),  # 銀将
    (7, 0): ("KE", False),  # 桂馬
    (8, 0): ("KY", False),  # 香車
    (1, 1): ("HI", False),  # 飛車
    (7, 1): ("KA", False),  # 角行
    (0, 2): ("FU", False),  # 歩兵
    (1, 2): ("FU", False),  # 歩兵
    (2, 2): ("FU", False),  # 歩兵
    (3, 2): ("FU", False),  # 歩兵
    (4, 2): ("FU", False),  # 歩兵
    (5, 2): ("FU", False),  # 歩兵
    (6, 2): ("FU", False),  # 歩兵
    (7, 2): ("FU", False),  # 歩兵
    (8, 2): ("FU", False),  # 歩兵
    # 先手(下段)
    (8, 8): ("KY", True),  # 香車
    (7, 8): ("KE", True),  # 桂馬
    (6, 8): ("GI", True),  # 銀将
    (5, 8): ("KI", True),  # 金将
    (4, 8): ("OU", True),  # 王将
    (3, 8): ("KI", True),  # 金将
    (2, 8): ("GI", True),  # 銀将
    (1, 8): ("KE", True),  # 桂馬
    (0, 8): ("KY", True),  # 香車
    (7, 7): ("HI", True),  # 飛車
    (1, 7): ("KA", True),  # 角行
    (8, 6): ("FU", True),  # 歩兵
    (7, 6): ("FU", True),  # 歩兵
    (6, 6): ("FU", True),  # 歩兵
    (5, 6): ("FU", True),  # 歩兵
    (4, 6): ("FU", True),  # 歩兵
    (3, 6): ("FU", True),  # 歩兵
    (2, 6): ("FU", True),  # 歩兵
    (1, 6): ("FU", True),  # 歩兵
    (0, 6): ("FU", True),  # 歩兵
}

PIECE_MOVES = {
    "FU": [(-1, 0)],
    "KY": [(-1, 0)],
    "KE": [(-2, -1), (-2, 1)],
    "GI": [(-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)],
    "KI": [(-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0)],
    "OU": [(-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1)],
    "GY": [(-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1)],
    "HI": [(-1, 0), (0, -1), (0, 1), (1, 0)],
    "KA": [(-1, -1), (-1, 1), (1, -1), (1, 1)],
}

PROMOTION_PIECE = {
        "FU": "TO",
        "KY": "NY",
        "KE": "NK",
        "GI": "NG",
        "HI": "RY",
        "KA": "UM"
    }

CONTINUOUS_MOVERS = {"KY", "KA", "HI"}

PROMOTION_MOVERS = {"TO","NY","NK","NG","RY","UM"}

selected_pos = None


def initialize_board():
    # 将棋盤の初期配置を設定する
    board = [[None for _ in range(SQUARE_NUMBER)] for _ in range(SQUARE_NUMBER)]

    for position, piece_info in INITIAL_POSITIONS.items():
        col, row = position
        piece_type, is_sente = piece_info
        piece = Piece(piece_type, is_sente)
        board[row][col] = piece
    return board


def write_character(window, point, content, _character_size, color):
    font = pygame.font.SysFont("Arial", _character_size)
    piece_name = font.render(content, True, color)
    window.blit(piece_name, point)


def match_pieces(window, board):
    for x in range(SQUARE_NUMBER):
        for y in range(SQUARE_NUMBER):
            if board[x][y] is None:
                pygame.draw.rect(
                    window,
                    COLOR["White"],
                    (
                        REFERENCE_POINT + SQUARE_LENGTH * x + 5,
                        REFERENCE_POINT + SQUARE_LENGTH * y + 5,
                        SQUARE_LENGTH - 10,
                        SQUARE_LENGTH - 10,
                    ),
                )
                character_size = 40
                if INITIAL_POSITIONS[(x, y)][1]:
                    write_character(
                        window,
                        [
                            REFERENCE_POINT
                            + SQUARE_LENGTH * x
                            + (SQUARE_LENGTH - character_size) / 2,
                            REFERENCE_POINT
                            + SQUARE_LENGTH * y
                            + (SQUARE_LENGTH - character_size) / 2,
                        ],
                        INITIAL_POSITIONS[(x, y)][0],
                        character_size,
                        COLOR["Black"],
                    )
                else:
                    write_character(
                        window,
                        [
                            REFERENCE_POINT
                            + SQUARE_LENGTH * x
                            + (SQUARE_LENGTH - character_size) / 2,
                            REFERENCE_POINT
                            + SQUARE_LENGTH * y
                            + (SQUARE_LENGTH - character_size) / 2,
                        ],
                        INITIAL_POSITIONS[(x, y)][0],
                        character_size,
                        COLOR["Red"],
                    )


def position_pieces(window, piece_image, board):
    for x in range(SQUARE_NUMBER):
        for y in range(SQUARE_NUMBER):
            if board[y][x] is not None:
                piece = piece_image[board[y][x].type]
                if not board[y][x].is_sente:
                    piece = pygame.transform.rotate(piece, 180)
                draw_piece(
                    window,
                    piece,
                    (
                        REFERENCE_POINT + SQUARE_LENGTH * x,
                        REFERENCE_POINT + SQUARE_LENGTH * y,
                    ),
                )


def draw_piece(window, piece_image, pos):
    # if not INITIAL_POSITIONS[pos][1]:
    # piece_image = pygame.transform.rotate(piece_image, 180)
    window.blit(piece_image, pos)


def load_pieces(size):
    pieces = {}
    piece_names = [
        "FU",
        "KY",
        "KE",
        "GI",
        "KI",
        "OU",
        "HI",
        "KA",
        "TO",
        "NY",
        "NK",
        "NG",
        "RY",
        "UM"
    ]
    match_name = {
        "FU": "hohei",
        "KY": "kyousya",
        "KE": "keima",
        "GI": "ginsyou",
        "KI": "kinsyou",
        "OU": "ousyou",
        "HI": "hisya",
        "KA": "kaku",
        "TO": "tokin",
        "NY": "narikyou",
        "NK": "narikei",
        "NG": "narigin",
        "RY": "ryuu",
        "UM": "uma",
    }
    for name in piece_names:
        pieces[name] = pygame.image.load(f"assets/pieces/shogi_{match_name[name]}.png")
        pieces[name] = pygame.transform.scale(pieces[name], size)
    return pieces


def judge_moving(board, clicked_pos, movable_positions):
    if clicked_pos == selected_pos:  # いらないかも
        return False
    if list(clicked_pos) in movable_positions:
        return True
    return False


def get_single_moves(piece, from_pos, board, move_patterns):
    movable_pos = []
    for drow, dcol in move_patterns:
        if piece.is_sente:
            after_moving = [from_pos[0] + dcol, from_pos[1] + drow]
        else:
            after_moving = [from_pos[0] - dcol, from_pos[1] - drow]
        if (
            0 <= after_moving[0] < SQUARE_NUMBER
            and 0 <= after_moving[1] < SQUARE_NUMBER
        ):
            if board[after_moving[1]][after_moving[0]] is None:
                movable_pos.append(after_moving)
            elif (
                board[after_moving[1]][after_moving[0]].is_sente
                != board[from_pos[1]][from_pos[0]].is_sente
            ):
                movable_pos.append(after_moving)
    return movable_pos


def get_continuous_moves(piece, from_pos, board, move_patterns):
    movable_pos = []
    for drow, dcol in move_patterns:
        after_moving = [from_pos[0], from_pos[1]]
        while True:
            if piece.is_sente:
                after_moving = [after_moving[0] + dcol, after_moving[1] + drow]
            else:
                after_moving = [after_moving[0] - dcol, after_moving[1] - drow]
            if (
                0 <= after_moving[0] < SQUARE_NUMBER
                and 0 <= after_moving[1] < SQUARE_NUMBER
            ):
                if board[after_moving[1]][after_moving[0]] is None:
                    movable_pos.append(after_moving)
                elif (
                    board[after_moving[1]][after_moving[0]].is_sente
                    != board[from_pos[1]][from_pos[0]].is_sente
                ):
                    movable_pos.append(after_moving)
                    break
                else:
                    break
            else:
                break
    return movable_pos


def get_piece_moves(piece, from_pos, board):
    if piece.type in CONTINUOUS_MOVERS:
        moves = get_continuous_moves(piece, from_pos, board, PIECE_MOVES[piece.type])
    elif piece.type in PROMOTION_MOVERS:
        if piece.type == "RY":
            moves1 = get_continuous_moves(piece, from_pos, board, PIECE_MOVES["HI"])
            moves2 = get_single_moves(piece, from_pos, board, PIECE_MOVES["OU"])
            moves = moves1 + moves2
        elif piece.type == "UM":
            moves1 = get_continuous_moves(piece, from_pos, board, PIECE_MOVES["KA"])
            moves2 = get_single_moves(piece, from_pos, board, PIECE_MOVES["OU"])
            moves = moves1 + moves2
        else:
            moves = get_single_moves(piece, from_pos, board, PIECE_MOVES["KI"])
    else:
        moves = get_single_moves(piece, from_pos, board, PIECE_MOVES[piece.type])
    return moves


def draw_movable_positions(window, movable_positions):
    for col, row in movable_positions:
        x = REFERENCE_POINT + col * SQUARE_LENGTH
        y = REFERENCE_POINT + row * SQUARE_LENGTH

        center_x = x + SQUARE_LENGTH // 2
        center_y = y + SQUARE_LENGTH // 2
        radius = SQUARE_LENGTH // 4

        circle_surface = pygame.Surface((SQUARE_LENGTH, SQUARE_LENGTH), pygame.SRCALPHA)
        pygame.draw.circle(
            circle_surface,
            (*COLOR["GREEN"], 128),
            (SQUARE_LENGTH // 2, SQUARE_LENGTH // 2),
            radius,
        )
        window.blit(circle_surface, (x, y))  # todo

def check_promotion(piece,x,y):
    if piece is not None:
        if not(piece.is_promoted) and piece.type in PROMOTION_PIECE:
            if piece.is_sente:
                if  y <= 2:
                    return True
            elif not piece.is_sente:
                if y >= SQUARE_NUMBER - 3:
                    return True
    return False

def check_game_over(now_turn,click_piece):
    running = True
    winner = None
    if click_piece is None:
        return (running,winner)
    if click_piece.type == "OU" or click_piece.type == "GY":
        winner = now_turn
        running = False
        return(running,winner)
    return(running,winner)

def game_over(window,winner):
    write_str = "Sente win!" if winner else "Gote win!"
    write_character(
        window,
        [WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50],
        write_str,
        64,
        COLOR["White"]
    )
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


class Piece:
    def __init__(self, type, is_sente):
        self.type = type  # 駒の種類
        self.is_sente = is_sente  # True: 先手, False: 後手
        self.is_promoted = False  # 成り駒か

    def get_display_text(self):
        if self.is_promoted:
            return "N" + self.type  # 成り駒には”N”をつける
        return self.type

    def promotion_pieces(self):
        get_promoted_piece = PROMOTION_PIECE[self.type]
        self.is_promoted = True
        self.type = get_promoted_piece


def main():
    pygame.init()  # 画面初期化処理
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 画面の設定
    pygame.display.set_caption("shogi")  # 画面上部のタイトル設定
    image_things = load_pieces((80, 80))
    running = True
    now_turn = True #True:先手 False:後手
    board = initialize_board()
    global selected_pos
    movable = []
    while running:
        window.fill(COLOR["Black"])
        draw_board(window)
        position_pieces(window, image_things, board)

        # match_pieces(window)
        # write_character(window, [100, 80], INITIAL_POSITIONS[(0, 0)][0])

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                click_pos_x = (event.pos[0] - REFERENCE_POINT) // SQUARE_LENGTH
                click_pos_y = (event.pos[1] - REFERENCE_POINT) // SQUARE_LENGTH
                click_button = event.button
                if click_button == CLICK_LEFT:
                    if (0 <= click_pos_x < SQUARE_NUMBER) and (
                        0 <= click_pos_y < SQUARE_NUMBER
                    ):
                        clicked_pos = (click_pos_x, click_pos_y)
                        piece = board[click_pos_y][click_pos_x]
                        if selected_pos is None:  # 駒を選択
                            if board[click_pos_y][click_pos_x] is not None:
                                if board[click_pos_y][click_pos_x].is_sente == now_turn:
                                    selected_pos = clicked_pos
                                    movable = get_piece_moves(
                                        piece,
                                        selected_pos,
                                        board
                                    )

                        else:  # 駒が選択されてたら
                            if judge_moving(board, clicked_pos, movable):
                                board[click_pos_y][click_pos_x] = board[selected_pos[1]][selected_pos[0]]
                                board[selected_pos[1]][selected_pos[0]] = None
                                running,winner = check_game_over(now_turn,piece)
                                if running is False:
                                    print(winner)
                                if check_promotion(board[click_pos_y][click_pos_x],click_pos_x,click_pos_y):
                                    board[click_pos_y][click_pos_x].promotion_pieces()
                                now_turn = not now_turn
                            selected_pos = None
                            movable = []
            draw_movable_positions(window, movable)
            pygame.display.update()
    window.fill(COLOR["Black"])
    draw_board(window)
    position_pieces(window, image_things,board)
    game_over(window,winner)


def draw_board(window):
    for x in range(SQUARE_NUMBER):
        for y in range(SQUARE_NUMBER):
            if selected_pos == (x, y):
                pygame.draw.rect(
                    window,
                    COLOR["Yellow"],
                    (
                        REFERENCE_POINT + SQUARE_LENGTH * selected_pos[0],
                        REFERENCE_POINT + SQUARE_LENGTH * selected_pos[1],
                        SQUARE_LENGTH,
                        SQUARE_LENGTH,
                    ),
                )
            else:
                if (x + y) % 2 == 0:
                    pygame.draw.rect(
                        window,
                        COLOR["DarkBrown"],
                        (
                            REFERENCE_POINT + SQUARE_LENGTH * x,
                            REFERENCE_POINT + SQUARE_LENGTH * y,
                            SQUARE_LENGTH,
                            SQUARE_LENGTH,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        window,
                        COLOR["LightBrown"],
                        (
                            REFERENCE_POINT + SQUARE_LENGTH * x,
                            REFERENCE_POINT + SQUARE_LENGTH * y,
                            SQUARE_LENGTH,
                            SQUARE_LENGTH,
                        ),
                    )


if __name__ == "__main__":
    main()
