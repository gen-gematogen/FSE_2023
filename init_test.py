import shutil
import numpy as np
import cv2

from utils.test_utils import *
from main import *

def test_bot_response():
    bot = TestBot()
    init_telegram_bot(bot)
    msg = Message("test", "/start")
    start(bot, msg)
    assert bot.get_last_message() == ('test', "Variants: ['A3', 'C3', 'E3', 'G3']")
    shutil.rmtree("user_data/test")



def test_desk_initialization():
    desk = Desk()
    
    desk_state = desk._desk

    true_desk = [[CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                 [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK],
                 [CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                 [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK],
                 [CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                 [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK],
                 [CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                 [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK]]
    
    a = np.array(desk_state).T
    b = np.array(true_desk)

    assert np.all(a == b) == True


def test_image_generation():
    def image_difference():
        desk = Desk()
        desk._desk = np.array([[CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                    [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK],
                    [CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                    [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK],
                    [CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                    [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK],
                    [CellState.WHITE, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING],
                    [CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.BLACK]]).T
        state_img = desk.create_image_from_desk_state()
        state_img.save("test_images/test_images_generated_state.png")

        true_img_cv2 = cv2.imread("test_images/test_images_true_state.png")
        state_img_cv2 = cv2.imread("test_images/test_images_generated_state.png")

        if true_img_cv2.shape == state_img_cv2.shape:
            difference = cv2.subtract(true_img_cv2, state_img_cv2)
            
            b, g, r = cv2.split(difference)
            if (cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)) / (3 * true_img_cv2.shape[0] * true_img_cv2.shape[1]) < 0.001:
                os.remove("test_images/test_images_generated_state.png")
                return True
        os.remove("test_images/test_images_generated_state.png")
        return False
    
    assert image_difference() == True

def test_turn_logic():
    desk = Desk()
    turn_1 = desk.get_turn()
    desk.change_turn()
    turn_2 = desk.get_turn()
    desk.change_turn()
    turn_3 = desk.get_turn()

    assert (turn_1, turn_2, turn_3) == (CellState.WHITE, CellState.BLACK, CellState.WHITE)

def test_get_cell_state():
    desk = Desk()
    state_1 = desk.get_cell_state(0, 0)

    state_2 = desk.get_cell_state(0, 1)

    state_3 = desk.get_cell_state(-1, 0)
    state_4 = desk.get_cell_state(10, 0)
    state_5 = desk.get_cell_state(0, -1)
    state_6 = desk.get_cell_state(0, 10)

    desk._desk[0][5] = CellState.BLACK_KING
    desk._desk[0][6] = CellState.WHITE_KING

    state_7 = desk.get_cell_state(0, 5)
    state_8 = desk.get_cell_state(0, 6)

    assert (state_1, state_2, state_3, state_4, state_5, state_6, state_7, state_8) == \
    (CellState.WHITE, CellState.NOTHING, CellState.OUT_OF_BOARD, CellState.OUT_OF_BOARD,
     CellState.OUT_OF_BOARD, CellState.OUT_OF_BOARD, CellState.BLACK_KING, CellState.WHITE_KING)
    

def test_get_moves():
    desk = Desk()
    white_no_amv = desk._get_available_moves(1, 1, CellState.WHITE)
    white_no_a_yes_mv = desk._get_available_moves(2, 2, CellState.WHITE)
    white_yes_amv = desk._get_available_moves(6, 6, CellState.WHITE)
    black_no_amv = desk._get_available_moves(6, 6, CellState.BLACK)
    black_no_a_yes_mv = desk._get_available_moves(5, 5, CellState.BLACK)
    black_yes_amv = desk._get_available_moves(1, 1, CellState.BLACK)
    
    invalid_nothing = desk._get_available_moves(5, 5, CellState.NOTHING)
    invalid_out_of_desk = desk._get_available_moves(5, 5, CellState.OUT_OF_BOARD)
    invalid_bounds = desk._get_available_moves(-5, -5, CellState.BLACK)

    assert (white_no_amv, white_no_a_yes_mv, white_yes_amv, 
            black_no_amv, black_no_a_yes_mv, black_yes_amv, 
            invalid_nothing, invalid_out_of_desk, invalid_bounds) == \
            ((False, []), (False, [(3, 3), (3, 1)]), (True, [(4, 4)]),
             (False, []), (False, [(4, 6), (4, 4)]), (True, [(3, 3)]),
             (False, []),  (False, []), (False, []))
    

def test_move_check():
    desk = Desk()
    avaliable_moves_0 = desk.check_available_moves()
    desk.do_move((2, 2), (3, 3), CellState.WHITE)
    avaliable_moves_1 = desk.check_available_moves()
    desk.do_move((5, 1), (4, 2), CellState.BLACK)
    avaliable_moves_2 = desk.check_available_moves()

    desk._desk = np.full((8, 8), CellState.NOTHING).tolist()
    avaliable_moves_empty = desk.check_available_moves()
    attacks = avaliable_moves_0[0], avaliable_moves_1[0], avaliable_moves_2[0], avaliable_moves_empty[0]
    moves = avaliable_moves_0[1], avaliable_moves_2[1], avaliable_moves_empty[1]

    assert (attacks == (False, False, True, False)) and \
        (moves == ({(2, 0): [(3, 1)], (2, 2): [(3, 3), (3, 1)], (2, 4): [(3, 5), (3, 3)], (2, 6): [(3, 7), (3, 5)]}, 
                   {(3, 3): [(5, 1)]}, 
                   {}))
    
def test_switch_turn():
    desk = Desk()
    turn_0 = desk.get_turn()
    desk.change_turn()
    turn_1 = desk.get_turn()
    
    desk._turn = CellState.NOTHING
    turn_invalid_0 = desk.get_turn()
    desk.change_turn()
    turn_invalid_1 = desk.get_turn()

    assert (turn_0 != turn_1) and (turn_invalid_0 == turn_invalid_1)

def test_encoder_decoder():
    position_valid = (1, 1)
    position_invalid = (-10, 11)
    
    encoded_valid = encode_pos(*position_valid)
    encoded_invalid = encode_pos(*position_invalid)

    decoded_valid = decode_pos(encoded_valid)
    decoded_invalid = decode_pos(encoded_invalid)

    assert (position_valid == decoded_valid) and (encoded_invalid == 'INVALID_POSITION') and (decoded_invalid == (None, None))
