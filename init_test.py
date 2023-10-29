import shutil
import numpy as np
import cv2

from utils.test_utils import *
from main import *
from utils.bot import *

def test_bot_start():
    bot = TestBot()
    init_telegram_bot(bot)
    msg = Message("test", "/start")
    start(bot, msg)
    assert bot.get_last_message() == ('test', "Variants: ['A3', 'C3', 'E3', 'G3']")
    shutil.rmtree("user_data/test")
    
def test_bot_restart():
    bot = TestBot()
    init_telegram_bot(bot)
    
    msg = Message("test", "/start")
    start(bot, msg)
    
    id = "test"
    restart(id)
    
    assert bot.get_last_message() == ('test', "Variants: ['A3', 'C3', 'E3', 'G3']")
    shutil.rmtree("user_data/test")
    
def test_bot_general_moves():
    bot = TestBot()
    init_telegram_bot(bot)
    
    chat_id = 'test'
    
    desk = Desk()
    desk._desk = np.array([[CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.WHITE, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.BLACK, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING],
                [CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING, CellState.NOTHING]]).T

    state_img = desk.create_image_from_desk_state()
    os.makedirs(f"user_data/{chat_id}")
    state_img.save(f"user_data/{chat_id}/desk.png")
    save_state(chat_id, desk, True, (3, 3))
    
    #desk, is_move_stage, attack_pos = get_state(chat_id)
    
    msg = Message(chat_id, "F6")
    general_moves(bot, msg)
    
    last_msg = bot.get_last_message()
    
    assert last_msg == (chat_id, 'White side won, if you want play more, press /restart')


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
