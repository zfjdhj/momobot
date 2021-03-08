#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

import os
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from nonebot.log import logger, default_format

log_root = "logs/"

os.makedirs(log_root, exist_ok=True)
logger.add(log_root + "{time:YYYYMMDD}.log", rotation="00:00", level="INFO")
logger.add(log_root + "{time:YYYYMMDD}_error.log", rotation="00:00", level="ERROR")
logger.add(log_root + "{time:YYYYMMDD}_debug.log", rotation="00:00", level="DEBUG")

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)


nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")
nonebot.load_plugins("yobot")
nonebot.load_plugin("nonebot_plugin_apscheduler")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.run(app="bot:app")
