import logging
import os.path

import colorlog
import settings


def setup_logging(log_file):
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，用于将日志写入文件
    save_path = os.path.join(settings.LOGGER_SAVE_DIR, log_file)
    file_handler = logging.FileHandler(save_path)
    file_handler.setLevel(logging.DEBUG)

    # 创建控制台处理器，用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置控制台处理器的日志颜色
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # 创建格式化器，用于设置日志的显示格式
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 示例用法
logger = setup_logging("my_log.txt")
logger.debug("这是一个调试日志")
logger.info("这是一个信息日志")
logger.warning("这是一个警告日志")
logger.error("这是一个错误日志")
logger.critical("这是一个严重错误日志")
