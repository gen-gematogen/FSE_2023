import shutil

from utils.test_utils import *
from main import *

def first_test():
    bot = TestBot()
    init_telegram_bot(bot)
    msg = Message("test", "/start")
    start(bot, msg)
    assert bot.get_last_message() == ('test', "Variants: ['A3', 'C3', 'E3', 'G3']")
    shutil.rmtree("user_data/test")

first_test()