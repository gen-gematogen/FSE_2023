from telebot import TeleBot, types
import os
import pickle

from utils.checkers import *


parent_dir = os.path.abspath(__file__).replace('\\', '/').rsplit('/', 2)[0]


def create_markup(pos_list):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    buttons = [types.KeyboardButton(encode_pos(x,y)) for x,y in pos_list] + [types.KeyboardButton('/restart')]
    markup.add(*buttons)
    return markup


def save_state(chat_id, desk, is_move_stage, attack_pos):
    try:
        os.mkdir("user_data/" + str(chat_id))
    except Exception:
        pass
    with open(parent_dir + "/user_data/" + str(chat_id) + "/game_state.pkl", 'wb') as game_data:
        pickle.dump((desk, is_move_stage, attack_pos), game_data)


def restart(chat_id):
    save_state(chat_id, Desk(), False, (0, 0))


def get_state(chat_id):
    try:
        os.mkdir("user_data/" + str(chat_id))
    except Exception:
        pass
    if not os.path.isfile(parent_dir + "/user_data/" + str(chat_id) + "/desk.png"):
        restart(chat_id)
    with open(parent_dir + "/user_data/" + str(chat_id) + "/game_state.pkl", 'rb') as game_data:
        return pickle.load(game_data)


def create_base_response(bot, message, pos_list):
    if os.path.isfile(parent_dir + "/user_data/" + str(message.chat.id) + "/desk.png"):
        with open(parent_dir + "/user_data/" + str(message.chat.id) + "/desk.png", 'rb') as picture:
            bot.send_photo(message.chat.id, picture)
    m = create_markup(pos_list)
    desk, is_move_stage, attack_pos = get_state(message.chat.id)
    turn = "white" if desk._turn == CellState.WHITE else "black"
    if is_move_stage:
        x,y = attack_pos
        bot.send_message(message.chat.id, "Now " + turn + " side must choose, to what place goes piece " + encode_pos(x,y), reply_markup=m)
    else:
        bot.send_message(message.chat.id, "Now " + turn + " side must choose piece to move", reply_markup=m)
    bot.send_message(message.chat.id, "Variants: " + str([encode_pos(x,y) for x,y in pos_list]), reply_markup=m)


if __name__ == "__main__":
    # print(directory.replace('\\', '/').rsplit('/', 2)[0])
    pass