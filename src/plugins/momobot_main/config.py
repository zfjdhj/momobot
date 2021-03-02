"""
Author: zfj
Date: 2021-03-02 14:17:57
LastEditTime: 2021-03-02 14:17:57
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
from pydantic import BaseSettings


class Config(BaseSettings):

    # Your Config Here
    # plugin custom config
    plugin_setting: str = "default"

    class Config:
        extra = "ignore"
        res_path = "/home/zfj/workspeace/pcrbot/res"
