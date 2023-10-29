from enum import Enum
from PIL import Image, ImageDraw, ImageFont
import os

parent_dir = os.path.abspath(__file__).replace('\\', '/').rsplit('/', 2)[0]

class CellState(Enum):
    OUT_OF_BOARD = -1
    NOTHING = 0
    WHITE = 1
    BLACK = 2
    WHITE_KING = 3
    BLACK_KING = 4


class Desk:
    def __init__(self):
        self._desk = [[CellState.NOTHING for i in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    if i < 3:
                        self._desk[i][j] = CellState.WHITE
                    if i > 4:
                        self._desk[i][j] = CellState.BLACK
        self._turn = CellState.WHITE

    def create_image_from_desk_state(self, img_width=1024, img_height=1024, outline_width=50, outline_height=50):
        image = Image.new('RGB', size=(img_width + outline_width * 2, img_height + outline_height * 2))

        scale = img_width // 8
        checker_size_percentage = 0.8
        low_shift = (1 - checker_size_percentage) / 2
        high_shift = 1 - low_shift
        font_size = 50

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(parent_dir + "/fonts/sk_font.otf", font_size)
        draw.rectangle((0, 0, img_width + outline_width * 2, outline_height), fill="#7fc7ff")
        draw.rectangle((0, 0, outline_width, img_height + outline_height * 2), fill="#7fc7ff")
        draw.rectangle((img_width + outline_width, 0, img_width + outline_width * 2, img_height + outline_height * 2), fill="#7fc7ff")
        draw.rectangle((0, img_height + outline_height, img_width + outline_width, img_height + outline_height * 2), fill="#7fc7ff")
        for i in range(8):
            x0 = (i + 0.5) * scale + outline_width
            y0 = outline_height / 2
            draw.text((x0, y0), text=str(i+1), fill="#000000", outline="#ffffff", font=font, font_size=font_size, anchor="mm")
            draw.text((x0, y0 + img_height + outline_height), text=str(i+1), fill="#000000", outline="#ffffff", font=font, font_size=font_size, anchor="mm")
        for i in range(8):
            x0 = outline_width / 2
            y0 = (i + 0.5) * scale + outline_height
            labels = "ABCDEFGH"
            draw.text((x0, y0), text=labels[i], fill="#000000", outline="#ffffff", font=font, font_size=font_size, anchor="mm")
            draw.text((x0 + img_width + outline_width, y0), text=labels[i], fill="#000000", outline="#ffffff", font=font, font_size=font_size, anchor="mm")
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    x0 = i * scale + outline_width
                    y0 = j * scale + outline_height
                    x1 = (i + 1) * scale + outline_width
                    y1 = (j + 1) * scale + outline_height
                    draw.rectangle((x0, y0, x1, y1), fill="#ffffff")

                x0 = (i + low_shift) * scale + outline_width
                y0 = (j + low_shift) * scale + outline_height
                x1 = (i + high_shift) * scale + outline_width
                y1 = (j + high_shift) * scale + outline_height
                if self._desk[i][j] == CellState.WHITE:
                    draw.ellipse((x0, y0, x1, y1), fill="#ffffff", outline="#000000")
                if self._desk[i][j] == CellState.BLACK:
                    draw.ellipse((x0, y0, x1, y1), fill="#000000", outline="#ffffff")
        return image

    def get_turn(self):
        return self._turn

    def get_cell_state(self, x, y):
        if x >= 8 or x <= -1 or y >= 8 or y <= -1:
            return CellState.OUT_OF_BOARD
        return self._desk[x][y]

    def _get_available_moves_with_vector(self, x_self, y_self, move_x, move_y, self_state):
        vector_len = 1 if self_state == CellState.BLACK or CellState.WHITE else 8
        x_max_vector_len = abs(min(max(0, x_self + move_x * 8), 7) - x_self)
        y_max_vector_len = abs(min(max(0, y_self + move_y * 8), 7) - y_self)
        vector_len = min(vector_len, x_max_vector_len, y_max_vector_len)

        can_attack = False
        moves = []
        for i in range(vector_len):
            x = x_self + move_x * (i + 1)
            y = y_self + move_y * (i + 1)
            target_cell_state = self.get_cell_state(x,y)
            if target_cell_state == CellState.OUT_OF_BOARD:
                break
            if target_cell_state == CellState.NOTHING:
                moves.append((x, y))
                continue
            target_white = target_cell_state == CellState.WHITE or target_cell_state == CellState.WHITE_KING
            self_white = self_state == CellState.WHITE or self_state == CellState.WHITE_KING
            if target_white != self_white:
                if self.get_cell_state(x + move_x, y + move_y) == CellState.NOTHING:
                    if not can_attack:
                        moves = []
                    can_attack = True
                    if vector_len == 1:
                        moves.append((x + move_x, y + move_y))
        return can_attack, moves

    def _get_available_moves(self, x, y, self_type):
        attack1, moves1 = self._get_available_moves_with_vector(x,y, 1, 1, self_type)
        attack2, moves2 = self._get_available_moves_with_vector(x,y, 1, -1, self_type)
        attack3, moves3 = self._get_available_moves_with_vector(x,y, -1, 1, self_type)
        attack4, moves4 = self._get_available_moves_with_vector(x,y, -1, -1, self_type)

        moves = []
        attack_state = attack1 or attack2 or attack3 or attack4
        if attack_state:
            moves.extend(moves1 if attack1 else [])
            moves.extend(moves2 if attack2 else [])
            moves.extend(moves3 if attack3 else [])
            moves.extend(moves4 if attack4 else [])
        else:
            moves.extend(moves1)
            moves.extend(moves2)
            moves.extend(moves3)
            moves.extend(moves4)
        return attack_state, moves

    def check_available_moves(self):
        moves = {}
        attack_moves = {}
        attack_state = False
        for i in range(8):
            for j in range(8):
                selected_piece = self._desk[i][j]
                if selected_piece == CellState.NOTHING:
                    continue
                selected_white = selected_piece == CellState.WHITE or selected_piece == CellState.WHITE_KING
                self_white = self._turn == CellState.WHITE or self._turn == CellState.WHITE_KING
                if selected_white == self_white:
                    attack, piece_moves = self._get_available_moves(i, j, selected_piece)
                    if piece_moves:
                        if attack:
                            attack_state = True
                            attack_moves[(i, j)] = piece_moves
                        moves[(i,j)] = piece_moves
        if attack_state:
            moves = attack_moves
        return attack_state, moves

    def count_pieces(self):
        white_cnt = 0
        black_cnt = 0
        for line in self._desk:
            for piece in line:
                if piece == CellState.WHITE or piece == CellState.WHITE_KING:
                    white_cnt += 1
                if piece == CellState.BLACK or piece == CellState.BLACK_KING:
                    black_cnt += 1
        return white_cnt, black_cnt

    def do_move(self, start_pos, end_pos, self_type):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        move_x = 1 if start_x < end_x else -1
        move_y = 1 if start_y < end_y else -1

        attacked = False
        for i in range(1, abs(start_x-end_x)):
            interim_cell = self._desk[start_x + i * move_x][start_y + i * move_y]
            if interim_cell != CellState.NOTHING and interim_cell != CellState.OUT_OF_BOARD:
                interim_white = interim_cell == CellState.WHITE or interim_cell == CellState.WHITE_KING
                self_white = self_type == CellState.WHITE or self_type == CellState.WHITE_KING
                if interim_white != self_white:
                    attacked = True
                    self._desk[start_x + i * move_x][start_y + i * move_y] = CellState.NOTHING
        self._desk[end_x][end_y] = self._desk[start_x][start_y]
        self._desk[start_x][start_y] = CellState.NOTHING
        if not attacked:
            self.change_turn()
        return attacked

    def change_turn(self):
        if self._turn == CellState.WHITE:
            self._turn = CellState.BLACK
        else:
            self._turn = CellState.WHITE


def encode_pos(x,y):
    labels = "ABCDEFGH"
    return labels[y] + str(x + 1)


def decode_pos(selected_pos):
    labels = "ABCDEFGH"
    label2idx = {label: idx for idx, label in enumerate(labels)}
    x_pos = int(selected_pos[1]) - 1
    y_pos = label2idx[selected_pos[0]]
    return x_pos, y_pos



