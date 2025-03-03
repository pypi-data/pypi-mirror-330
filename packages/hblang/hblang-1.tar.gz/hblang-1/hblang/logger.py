import datetime

class Logging:
    @staticmethod
    def info(message):
        Logging._log("INFO", message)

    @staticmethod
    def error(message):
        Logging._log("ERROR", message)

    @staticmethod
    def warning(message):
        Logging._log("WARNING", message)

    @staticmethod
    def bot_started(bot_id, bot_username):
        message = f"Бот запущен. ID: {bot_id}, Юзернейм: @{bot_username}"
        Logging._log("INFO", message)

    @staticmethod
    def new_user(user_id, username):
        message = f"Новый пользователь: ID: {user_id}, Юзернейм: @{username}"
        Logging._log("INFO", message)

    @staticmethod
    def _log(level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{level}] {timestamp}: {message}"
        print(log_message)  # Вывод в консоль
        with open("bot.log", "a", encoding="utf-8") as log_file:
            log_file.write(log_message + "\n")