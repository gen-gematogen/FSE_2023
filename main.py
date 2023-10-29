from utils.bot import *

desk = Desk()

cur_help_message = \
"""This is bot for playing checkers:
The only command is a /restart
"""


try:
    os.mkdir("user_data")
except Exception:
    print("Folder already exists")


def start(bot, message):
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


def game_restart(bot, message):
    restart(message.chat.id)
    desk, is_move_stage, _ = get_state(message.chat.id)
    attack, moves = desk.check_available_moves()
    image = desk.create_image_from_desk_state()
    image.save("user_data/" + str(message.chat.id) + "/desk.png")
    bot.send_message(chat_id=message.chat.id, text="Game restarted, enjoy")
    create_base_response(bot, message, moves.keys())


def move_logic(bot, message, desk, attack_pos):
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
            attack, moves = desk.check_available_moves()
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


def choosing_piece_logic(bot, message, desk):
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


def general_moves(bot, message):
    desk, is_move_stage, attack_pos = get_state(message.chat.id)
    if is_move_stage:
        move_logic(bot, message, desk, attack_pos)
    else:
        choosing_piece_logic(bot, message, desk)
    desk, is_move_stage, attack_pos = get_state(message.chat.id)
    w, b = desk.count_pieces()
    if w == 0 or b == 0:
        if w == 0:
            bot.send_message(chat_id=message.chat.id, text="Black side won, if you want play more, press /restart")
        if b == 0:
            bot.send_message(chat_id=message.chat.id, text="White side won, if you want play more, press /restart")


def init_telegram_bot(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        start(bot, message)

    @bot.message_handler(commands=['restart'])
    def handle_game_restart(message):
        game_restart(bot, message)

    @bot.message_handler(func=lambda m: True)
    def handle_general_moves(message):
        general_moves(bot, message)


if __name__ == "__main__":
    API_TOKEN = sys.argv[1]  # YOUR API TOKEN HERE
    bot = TeleBot(API_TOKEN, parse_mode=None)
    init_telegram_bot(bot)
    print("Bot started")
    bot.infinity_polling()
