class Chat:
    def __init__(self, id):
        self.id = id


class Message:
    def __init__(self, id, text):
        self.chat = Chat(id)
        self.text = text


class TestBot:
    def __init__(self):
        self.message_buffer = []

    def get_last_message(self):
        return self.message_buffer.pop()

    def send_message(self, chat_id, text, reply_markup=""):
        self.message_buffer.append((chat_id, text))

    def send_photo(self, chat_id, photo):
        self.message_buffer.append((chat_id, 'some photo sent'))

    def message_handler(self, commands=None, func=None):
        def _stub(*args, **kwargs):
            pass
        return _stub

