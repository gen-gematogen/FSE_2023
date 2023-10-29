
from utils.bot import *

desk = Desk()

cur_help_message = \
"""This is bot for playing checkers:
The only command is a /restart
"""

API_TOKEN = "6879463439:AAHJsBLzoegnoLeDSydzdU18DfRScoE-X2g"
bot = TeleBot(API_TOKEN, parse_mode=None)


def restart(chat_id):
    save_state(chat_id, Desk(), False, (0, 0))


try:
    os.mkdir("user_data")
except Exception:
    print("Folder already exists")


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(chat_id=message.chat.id, text="Let's start")
    try:
        os.mkdir("user_data/" + str(message.chat.id))
    except Exception:
        print("Folder already exists")
    restart(message.chat.id)
    desk, is_move_stage, _ = get_state(message.chat.id)
    attack, moves = desk.check_available_moves()
    image = desk.create_image_from_desk_state()
    image.save("user_data/" + str(message.chat.id) + "/desk.png")
    bot.send_message(chat_id=message.chat.id, text=cur_help_message)
    create_base_response(bot, message, moves.keys())


@bot.message_handler(commands=['restart'])
def game_restart(message):
    restart(message.chat.id)
    desk, is_move_stage, _ = get_state(message.chat.id)
    attack, moves = desk.check_available_moves()
    image = desk.create_image_from_desk_state()
    image.save("user_data/" + str(message.chat.id) + "/desk.png")
    bot.send_message(chat_id=message.chat.id, text="Game restarted, enjoy")
    create_base_response(bot, message, moves.keys())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    desk, is_move_stage, attack_pos = get_state(message.chat.id)
    if is_move_stage:
        attack, moves = desk.check_available_moves()
        target_pos = moves[attack_pos]
        move_x, move_y = decode_pos(message.text)
        if (move_x, move_y) not in target_pos:
            bot.send_message(chat_id=message.chat.id, text="Wrong move, use buttons")
            create_base_response(bot, message, target_pos)
            return
        x_pos, y_pos = attack_pos
        attacked = desk.do_move(attack_pos, (move_x, move_y), desk.get_cell_state(x_pos, y_pos))
        x_pos = move_x
        y_pos = move_y
        attack, moves = desk.check_available_moves()
        if len(moves.get((x_pos, y_pos), [])) == 0 or not attack:
            if attacked:
                desk.change_turn()
            attacked = False
        if attacked:
            print("You attacked, you can move more")
        save_state(message.chat.id, desk, attacked, (x_pos, y_pos))
        image = desk.create_image_from_desk_state()
        image.save("user_data/" + str(message.chat.id) + "/desk.png")
        if attacked:
            create_base_response(bot, message, moves[(x_pos, y_pos)])
        else:
            create_base_response(bot, message, moves.keys())
    else:
        attack, moves = desk.check_available_moves()
        x_pos, y_pos = decode_pos(message.text)
        if (x_pos, y_pos) not in moves.keys():
            bot.send_message(chat_id=message.chat.id, text="Wrong move, use buttons")
            create_base_response(bot, message, moves.keys())
            return
        save_state(message.chat.id, desk, True, (x_pos, y_pos))
        image = desk.create_image_from_desk_state()
        image.save("user_data/" + str(message.chat.id) + "/desk.png")
        create_base_response(bot, message, moves[(x_pos, y_pos)])


print("Bot started")
bot.infinity_polling()