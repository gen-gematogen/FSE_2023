import shutil
import numpy as np
import cv2

from utils.test_utils import *
from main import *

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
