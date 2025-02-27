import logging
import os
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def init_log():
    # global myapp
    # myapp = tpapp
    logger.setLevel(logging.INFO)
    LOG_PATH='./logs/'
    if not os.path.exists(LOG_PATH):
        # 如果目录不存在，使用os.makedirs创建它
        os.makedirs(LOG_PATH)
    logfile = LOG_PATH + 'app.log'
    # 文件日志配置
    file_handler = RotatingFileHandler(logfile, maxBytes=1024 * 1024 * 100, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    log_format = logging.Formatter('%(asctime)s \t %(name)s \t %(levelname)s \t %(message)s')
    file_handler.setFormatter(log_format)

    # if not current_app.debug:
    logger.addHandler(file_handler)

    # 控制台日志配置
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 记录一些日志
    # logger.debug('This is a debug message.')
    # logger.info('This is an info message.')
    # logger.warning('This is a warning message.')
    # logger.error('This is an error message.')
    # logger.critical('This is a critical message.')


def info(str_msg):
    logger.info(str_msg)

def error(str_msg):
    logger.error(str_msg)

def debug(str_msg):
    logger.debug(str_msg)

def warning(str_msg):
    logger.warning(str_msg)