"""
Author: zfj
Date: 2021-03-02 14:18:53
LastEditTime: 2021-03-02 14:18:53
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
import nonebot
import os
import json
import random
import datetime
from nonebot import on_command, get_driver, on_metaevent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.event import LifecycleMetaEvent
from nonebot.config import Env
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from pydantic.tools import T
from nonebot.plugin import export
from .config import Config
from .util import aiorequests

# 1. 在？               判断bot是否在线
# 2. (自动发送)猫猫上线  猫猫上线跟主人打招呼
# 3. @bot\|<bot昵称>    随机一张猫猫表情
# 4. 半月刊 [编号]      查看“公主连结”半月刊，编号：2-1，2-2，etc.
# 5. 孤儿装             查看“公主连结”孤儿装囤装思路
# 6. 刷新过滤器         刷新gocq事件过滤器

global_config = get_driver().config
plugin_config = Config(**global_config.dict())


from pathlib import Path

import nonebot

# # store all subplugins
# _sub_plugins = set()
# # load sub plugins
# _sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "util").resolve()))

plugin_path = os.path.dirname(os.path.abspath(__file__))
res_path = plugin_config.Config.res_path
momo_folder = os.path.join(res_path, "img/zfjbot/momo")
semimonthly_folder = os.path.join(res_path, "img/zfjbot/month")
nomomeq_folder = os.path.join(res_path, "img/zfjbot/nomom")


def open_jsonfile(path):
    with open(path, "rb") as f:
        return json.loads(f.read())


# 1. 在？               判断bot是否在线
async def zai_handlers(bot: Bot, event: Event, state: T_State):
    await zai.finish("猫猫在的哦 ~")


zai = on_command("zai", aliases={"在?", "在？", "在吗", "在么？", "在嘛", "在嘛？"}, handlers=[zai_handlers], rule=to_me())

# 2. (自动发送)猫猫上线  猫猫上线跟主人打招呼


async def lifecycle(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, LifecycleMetaEvent)


lisenlife = on_metaevent(rule=lifecycle)


@lisenlife.handle()
async def _(bot: Bot, event: LifecycleMetaEvent):
    if event.sub_type == "connect":
        for su in bot.config.superusers:
            await bot.send_private_msg(user_id=int(su), message="猫猫已上线 ~")


# 3. @bot\|<bot昵称>    随机一张猫猫表情


async def get_momo(bot: Bot, event: Event):
    print("get_momo")
    files = os.listdir(momo_folder)
    filename = random.choice(files)
    img = os.path.join(momo_folder, filename)
    await bot.send(event, MessageSegment.image(rf"file:///{img}"))


async def at_momo(bot: Bot, event: Event, satae: T_State) -> bool:
    if str(event.message) != "":
        return False
    return True


momo = on_command("", handlers=[get_momo], rule=at_momo)

# 4. 半月刊 [编号]      查看“公主连结”半月刊，编号：2-1，2-2，etc.

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

    from nonebot.adapters.cqhttp.message import MessageSegment

    img = os.path.join(semimonthly_folder, filename)
    await semimonthly.finish(MessageSegment.image(rf"file:///{img}"))


# 5. 孤儿装             查看“公主连结”孤儿装囤装思路
async def get_nomumeq(bot: Bot, event: Event):
    data = open_jsonfile(plugin_path + "/data.json")
    res = f"【公主连结】孤儿装囤积思路V1.0 一图流\nhttps://www.bigfunapp.cn/post/870083"
    for item in data["nomomeq"]:
        res += f"\n[CQ:image,file=file:///{nomomeq_folder}/{item}]"
    await bot.send(event, Message(res))


sima = on_command("孤儿装", handlers=[get_nomumeq])


# 6. 刷新过滤器         刷新gocq事件过滤器
async def reload_event_filter(bot: Bot):
    await bot.call_api("reload_event_filter")


reload_filter = on_command("刷新过滤器", handlers=[reload_event_filter])

# test1
# @export()
async def test1(bot: Bot):
    print("test1:", bot.config.superusers)


on_command("test1", handlers=[test1])
# test2
async def test2(bot: Bot, event: Event):
    print(event.__dict__.keys())
    for item in event.__dict__.keys():
        print(item, event.__dict__.get(item))


on_command("test2", handlers=[test2])