import logging
from pathlib import Path


logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot_logger = logging.FileHandler(f'{str(Path.cwd())}/log/bot.log')
bot_logger.setLevel(logging.INFO)
bot_logger.setFormatter(formatter)

command_logger = logging.FileHandler(f'{str(Path.cwd())}/log/command_log.log')
command_logger.setLevel(logging.INFO)
command_logger.setFormatter(formatter)
