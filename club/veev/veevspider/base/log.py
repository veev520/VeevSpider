# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import sys
import time
import os

# 获取logger实例，如果参数为空则返回root logger
logger = None

"""
格式：\033[显示方式;前景色;背景色m
 
说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见
 
例子：
\033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
\033[0m          <!--采用终端默认设置，即取消颜色设置-->
"""

# Define log color
LOG_COLORS = {
    'DEBUG': '\033[1;34;0m',
    'INFO': '\033[0;36;0m',
    'WARNING': '\033[1;33;0m',
    'ERROR': '\033[1;31;0m',
    'CRITICAL': '\033[1;35;0m',
    'EXCEPTION': '\033[1;31;0m',
}


class ColoredFormatter(logging.Formatter):
    """A colorful formatter."""

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)

        return LOG_COLORS.get(level_name, '') + msg


def add_file_handler(fmt):
    # 文件日志
    logs_directory = os.path.join(os.path.dirname(__file__), os.pardir) + "/logs"
    if os.path.isdir(logs_directory) is not True:
        os.mkdir(logs_directory)
    file_name = logs_directory + os.sep + time.strftime("%Y-%m-%d", time.localtime()) + '.log'

    handler = logging.FileHandler(file_name)
    handler.formatter = logging.Formatter(fmt)

    # 为logger添加的日志处理器
    logger.addHandler(handler)


def add_console_handler(fmt):
    # 控制台日志
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(ColoredFormatter(fmt))  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器
    logger.addHandler(handler)


def init_logger():
    global logger
    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger("VeevSpider")
    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)

    # 指定logger输出格式
    fmt = '%(asctime)s %(levelname)-4s: %(message)s'
    # 为logger添加的日志处理器
    # add_file_handler(fmt)   # 暂不输出到文件
    add_console_handler(fmt)
    pass


def i(*args):
    msg = ', '.join(str(x) for x in args)
    logger.info(msg)
    pass


init_logger()

if __name__ == '__main__':
    i('Hello', 'World')
    a = list()
    a.append(0)
    a.append('1')
    a.append(logger)
    i('1', 2, a)

