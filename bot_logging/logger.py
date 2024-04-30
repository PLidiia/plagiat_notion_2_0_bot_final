import logging


class BotLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger("bot_logger")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, level, message):
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)


with open("bot_logging/telegram_bot.txt", 'a', encoding='windows-1251') as txtfile:
    logger = BotLogger("bot_logging/telegram_bot.txt")
