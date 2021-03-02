"""
Author: zfj
Date: 2021-03-02 18:24:25
LastEditTime: 2021-03-02 18:24:25
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    # config.py
    # 抓包获取到的app_id,Authorization;
    bot_id = "123"
    group_id = "123"
    app_id = "123"
    authorization = "123"

    class Config:
        extra = "ignore"
