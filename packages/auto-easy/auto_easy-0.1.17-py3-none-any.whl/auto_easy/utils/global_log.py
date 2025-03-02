import logging
import os
from datetime import datetime

from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_dir, log_level=logging.INFO):
    """
    设置日志记录器

    :param log_dir: 日志文件存放的目录
    :param log_level: 日志输出级别，默认为logging.INFO
    :return: 配置好的日志记录器对象
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件名，可以根据需求自定义命名规则，这里简单使用当前日期时间
    # todo: 补丁
    now = datetime.now()
    current_datetime = now.strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"app_{current_datetime}.log")
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # 创建文件处理器，用于将日志写入文件
    file_handler = TimedRotatingFileHandler(log_file, when="H", interval=1, backupCount=12, encoding="utf-8")
    file_handler.setLevel(log_level)

    # 创建控制台处理器，用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 定义日志格式
    datefmt = '%Y/%m/%d-%H:%M:%S'
    # 创建一个格式化器，将时间格式应用到日志格式中
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s', )
    formatter.default_time_format = datefmt
    formatter.default_msec_format = '%s.%03d'
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


from pathlib import Path

current_file = Path(__file__)
root_dir = current_file.parent.parent.parent
log_directory = os.path.join(root_dir, "output_log")
# 获取日志记录器，设置日志级别为DEBUG（可根据需要调整，如logging.INFO等）
logger = setup_logger(log_directory, logging.DEBUG)

# logger.debug('global_log.py:48')
# logger.info("这是一条INFO级别的日志")
# logger.warning("这是一条WARNING级别的日志")
# logger.error("这是一条ERROR级别的日志")
# logger.critical("这是一条CRITICAL级别的日志")
# print('global_log.py:48')
