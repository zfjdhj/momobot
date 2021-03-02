"""
Author: zfj
Date: 2021-03-02 16:53:14
LastEditTime: 2021-03-02 16:53:14
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
import re
import os
import datetime
from nonebot import get_driver, CommandGroup, plugin, get_bots
from nonebot.adapters.cqhttp.message import MessageSegment, Message

from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot, Event
from .PilCalendar import drawMonth
from .PilMimikkoSignCard import drawSigncard
from .mimikkoAutoSignIn.mimikko import mimikko, timeStamp2time
from .config import Config
from nonebot_plugin_apscheduler import scheduler

global_config = get_driver().config
config = Config(**global_config.dict())

group_id = config.group_id
app_id = config.app_id
authorization = config.authorization
plugin_path = os.path.dirname(os.path.abspath(__file__))


async def mimikko_sign(bot: Bot, event: Event):
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id, authorization)
    res = "Sign Data:\n"
    res += f"code:, {sign_data['code']}\n"
    res += f"获得成长值Reward：{sign_data['body']['Reward']}\n"
    res += f"获得硬币GetCoin：{sign_data['body']['GetCoin']}\n"
    res += f"================\nEnergy Info:\n"
    res += f"code: {energy_info_data['code']}\n"
    res += f"msg: {energy_info_data['msg']}\n"
    res += f"经验：{energy_info_data['body']['Favorability']}/{energy_info_data['body']['MaxFavorability']}\n"
    res += f"Energy: {energy_info_data['body']['Energy']}"
    await bot.send(event, res)


async def mimikko_energy(bot: Bot, event: Event):
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id, authorization)
    res = f"Energy Info:\n"
    res += f"code: {energy_info_data['code']}\n"
    res += f"msg: {energy_info_data['msg']}\n"
    res += f"经验：{energy_info_data['body']['Favorability']}/{energy_info_data['body']['MaxFavorability']}\n"
    res += f"Energy: {energy_info_data['body']['Energy']}\n"
    res += "================\nEnergy Reward:\n"
    res += f"{energy_reward_data}\n"
    await bot.send(event, res)


async def mimikko_check(bot: Bot, event: Event):
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id, authorization)
    res = "Sign Data:\n"
    res += f"获得成长值Reward：{sign_data['body']['Reward']}\n"
    res += f"获得硬币GetCoin：{sign_data['body']['GetCoin']}\n"
    if sign_data["code"] == "0":
        res += f"[CQ:image,file=file:///{drawSigncard(sign_data)}]\n"
    res += f"================\nEnergy Info:\n"
    res += f"code: {energy_info_data['code']}\n"
    res += f"msg: {energy_info_data['msg']}\n"
    res += f"经验：{energy_info_data['body']['Favorability']}/{energy_info_data['body']['MaxFavorability']}\n"
    res += f"Energy: {energy_info_data['body']['Energy']}\n"
    res += "================\nEnergy Reward:\n"
    res += f"{energy_reward_data}\n"
    res += "================\nSign Info:\n"
    res += f"code: {sign_info['code']}\n"
    res += f"IsSign: {sign_info['body']['IsSign']}\n"
    res += f"连续登录天数: {sign_info['body']['ContinuousSignDays']}\n"
    res += "================\nSign History:\n"
    res += f"code: {sign_history['code']}\n"
    res += f"startTime: {timeStamp2time(sign_history['body']['startTime'])}\n"
    res += f"endTime: {timeStamp2time(sign_history['body']['endTime'])}\n"
    res += "signLogs:"
    day_list = []
    for item in sign_history["body"]["signLogs"]:
        rex_data = re.search("(?P<月>.*)月(?P<日>.*)日", timeStamp2time(item["signDate"]))
        if rex_data.group("月") == re.search(
            "(?P<月>.*)月(?P<日>.*)日", timeStamp2time(sign_history["body"]["startTime"])
        ).group("月"):
            day_list.append(rex_data.group("日"))
    img_path = drawMonth(datetime.datetime.now().month, day_list, plugin_path)
    res += f"[CQ:image,file=file:///{plugin_path}/{img_path}]"
    await bot.send(event, Message(res))


async def mimikko_sign_in_auto():
    bot = get_bots()[config.bot_id]
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id, authorization)
    res = "Sign Data:\n"
    res += f"获得成长值Reward：{sign_data['body']['Reward']}\n"
    res += f"获得硬币GetCoin：{sign_data['body']['GetCoin']}\n"
    if sign_data["code"] == "0":
        res += f"[CQ:image,file=file:///{drawSigncard(sign_data)}]\n"
    res += "================\nSign History:\n"
    day_list = []
    for item in sign_history["body"]["signLogs"]:
        rex_data = re.search("(?P<月>.*)月(?P<日>.*)日", timeStamp2time(item["signDate"]))
        if rex_data.group("月") == re.search(
            "(?P<月>.*)月(?P<日>.*)日", timeStamp2time(sign_history["body"]["startTime"])
        ).group("月"):
            day_list.append(rex_data.group("日"))
    img_path = drawMonth(datetime.datetime.now().month, day_list, plugin_path)
    res += f"[CQ:image,file=file:///{plugin_path}/{img_path}]"
    await bot.send_group_msg(group_id=group_id, message=Message(res))


# 1. mimikko sign: 梦梦奈签到
# 2. mimikko energy: 领取能量值
# 3. mimikko check: 检查签到状态
# 4. 自动签到任务
mimikko_com = CommandGroup("mimikko")
bots = mimikko_com.command("sign", handlers=[mimikko_sign])
matchers = mimikko_com.command("energy", handlers=[mimikko_energy])
event = mimikko_com.command("check", handlers=[mimikko_check])
scheduler.add_job(mimikko_sign_in_auto, "cron", hour="12")