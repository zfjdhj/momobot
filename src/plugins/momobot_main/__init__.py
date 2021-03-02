"""
Author: zfj
Date: 2021-03-02 14:18:53
LastEditTime: 2021-03-02 14:18:53
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
# import nonebot
import os
import json
import random
import datetime
from nonebot import get_driver, plugin
from nonebot import on_command
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())
plugin_config = Config(**global_config.dict())


plugin_path = os.path.dirname(os.path.abspath(__file__))
res_path = plugin_config.Config.res_path
momo_folder = os.path.join(res_path, "img/zfjbot/momo")
semimonthly_folder = os.path.join(res_path, "img/zfjbot/month")


async def zai_handlers(bot: Bot, event: Event, state: T_State):
    await zai.finish("猫猫在的哦 ~")


async def get_momo(bot: Bot, event: Event):
    print("get_momo")
    files = os.listdir(momo_folder)
    filename = random.choice(files)
    img = os.path.join(momo_folder, filename)
    await bot.send(event, MessageSegment.image(rf"file:///{img}"))


def open_jsonfile(path):
    with open(path, "rb") as f:
        return json.loads(f.read())


zai = on_command("zai", aliases={"在?", "在？", "在吗", "在么？", "在嘛", "在嘛？"}, handlers=[zai_handlers], rule=to_me())
momo = on_command("", handlers=[get_momo], rule=to_me())
semimonthly = on_command("半月刊")


@semimonthly.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["semimonthly_name"] = args
    else:
        state["semimonthly_name"] = "new"


@semimonthly.got("semimonthly_name", prompt="你想查询哪哪一期半月刊呢？\neg:2-1,2-2,3-1\n默认为最新一期")
async def handle_semimonthly(bot: Bot, event: Event, state: T_State):
    data = open_jsonfile(plugin_path + "/data.json")
    if not data["semimonthly"].get(state["semimonthly_name"]):
        await semimonthly.reject("你想查询的半月刊暂不支持，请重新输入！\neg:2-1,2-2,3-1\n默认为最新一期")
    if state["semimonthly_name"] == "new":
        state["semimonthly_name"] = data["semimonthly"]["new"]
    filename = data["semimonthly"][state["semimonthly_name"]]
    img = os.path.join(semimonthly_folder, filename)
    await semimonthly.finish(MessageSegment.image(rf"file:///{img}"))
