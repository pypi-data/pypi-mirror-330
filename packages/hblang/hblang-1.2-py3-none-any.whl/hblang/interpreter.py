import logging
import requests
import re

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)


class Bot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.commands = {}
        self.callbacks = {}
        self.variables = {}
        self.bot_info = self.get_me()

    def get_me(self):
        url = f"{self.base_url}/getMe"
        response = requests.get(url).json()
        if response.get("ok"):
            return response["result"]
        return None

    def send_message(self, chat_id, text, keyboard=None):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        if keyboard:
            payload["reply_markup"] = {"inline_keyboard": keyboard}
        requests.post(url, json=payload)

    def add_command(self, command, callback):
        self.commands[command] = callback

    def add_callback(self, callback_data, callback):
        self.callbacks[callback_data] = callback

    def handle_update(self, update):
        if "message" in update:
            message = update["message"]
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")
            user_id = message.get("from", {}).get("id")
            username = message.get("from", {}).get("username")

            if text.startswith("/"):
                command = text.split()[0]
                if command in self.commands:
                    self.commands[command](user_id, username, chat_id)

        elif "callback_query" in update:
            callback_query = update["callback_query"]
            data = callback_query.get("data")
            chat_id = callback_query["message"]["chat"]["id"]
            if data in self.callbacks:
                self.callbacks[data](chat_id)

    def run(self, mode="polling"):
        if mode == "polling":
            offset = 0
            while True:
                url = f"{self.base_url}/getUpdates?offset={offset}"
                response = requests.get(url).json()
                for update in response.get("result", []):
                    self.handle_update(update)
                    offset = update["update_id"] + 1


def v(text, variables):
    placeholders = re.findall(r'`(.*?)`', text)
    for placeholder in placeholders:
        if placeholder in variables:
            text = text.replace(f'`{placeholder}`', str(variables[placeholder]))
    return text


def interpret(code):
    lines = code.split("\n")
    bot = None
    logging_enabled = False
    for line in lines:
        if "Get [Logging]" in line:
            logging_enabled = True
            logging.info("Логирование активировано.")
        elif "Bot {" in line:
            token = None
            for i in range(lines.index(line), len(lines)):
                if "token:" in lines[i]:
                    token = lines[i].split("token:")[1].strip().strip('"')
                    break

            if token:
                bot = Bot(token)
                if logging_enabled and bot.bot_info:
                    logging.info(f"Бот запущен. ID: {bot.bot_info['id']}, Юзернейм: @{bot.bot_info['username']}")
            else:
                logging.error("Токен не найден в блоке Bot.")
        elif "Command_" in line:
            command = line.split("Command_")[1].split("{")[0].strip()
            bot.add_command(f"/{command}", lambda user_id, username, chat_id, cmd=command: (
                logging.info(f"Новый пользователь: ID: {user_id}, Юзернейм: @{username}"),
                bot.send_message(chat_id, "Кнопки", keyboard=[
                    [{"text": "Создатель", "url": "https://t.me/hosarov"}],
                    [{"text": "Пока", "callback_data": "bye"}]
                ])
            ))
            if logging_enabled:
                logging.info(f"Команда /{command} зарегистрирована.")
        elif "Callback_" in line:
            callback_data = line.split("Callback_")[1].split("{")[0].strip()
            bot.add_callback(callback_data, lambda chat_id: bot.send_message(chat_id, "Пока"))
            if logging_enabled:
                logging.info(f"Callback {callback_data} зарегистрирован.")
        elif "send {" in line:
            chat_id = int(line.split("chat_id:")[1].split(",")[0].strip())
            text = line.split("text:")[1].strip().strip('"')
            if text.startswith("v\""):
                text = v(text[2:-1], bot.variables)
            bot.send_message(chat_id, text)
            if logging_enabled:
                logging.info(f"Сообщение отправлено: {text}")
        elif "=" in line:
            var_name, var_value = line.split("=")
            var_name = var_name.strip()
            var_value = var_value.strip().strip('"')
            bot.variables[var_name] = var_value
            if logging_enabled:
                logging.info(f"Переменная {var_name} установлена: {var_value}")
        elif "run {" in line:
            mode = line.split("mode:")[1].strip().strip('"')
            bot.run(mode=mode)
            if logging_enabled:
                logging.info("Бот запущен в режиме polling.")


def main():
    import sys
    if len(sys.argv) != 2:
        print("Использование: hblang <файл.hb>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as file:
        code = file.read()
    interpret(code)


if __name__ == "__main__":
    main()
