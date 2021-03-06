# import nonebot
import json
from nonebot import get_driver
from nonebot.plugin import on_regex
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


json_path = config.json_path


# 读取json文件内容,返回字典格式
with open(json_path, "r", encoding="utf8") as fp:
    json_data = json.load(fp)


async def search(bot: Bot, event: Event, state: T_State):
    reply = ""
    res = []
    if state["_matched_groups"][1]:
        keyword = state["_matched_groups"][1]
        # logger.info(f"help search {keyword}")
        # await bot.send(ev,keyword)
        # print(keyword)
        # return
        if keyword and type(json_data) == list:
            for plugin_type in json_data:
                for plugin in plugin_type["plugins_list"]:
                    if plugin["plugin_state"] == "禁用":
                        continue
                    elif plugin["plugin_name"].find(keyword) != -1:
                        for commands in plugin["plugin_commands"]:
                            res.append(
                                {
                                    "plugin_name": plugin["plugin_name"],
                                    "command": commands["command"],
                                    "description": commands["description"],
                                }
                            )
                        continue
                    else:
                        # print(plugin['plugin_name'])
                        for commands in plugin["plugin_commands"]:
                            # print(commands['command'])
                            if commands["command"].find(keyword) != -1:
                                res.append(
                                    {
                                        "plugin_name": plugin["plugin_name"],
                                        "command": commands["command"],
                                        "description": commands["description"],
                                    }
                                )
                                continue
                            # print(commands['description'])
                            if commands["description"].find(keyword) != -1:
                                res.append(
                                    {
                                        "plugin_name": plugin["plugin_name"],
                                        "command": commands["command"],
                                        "description": commands["description"],
                                    }
                                )
                                continue
        # logger.info(f"res in search: {len(res)}")
        if 0 < len(res) <= 20 or event.message_type == "private":
            for index, item in enumerate(res):
                reply += f"{index+1}. {item['command']}: {item['description']}\n"
            reply += f"============\n猫猫共查询到结果{len(res)}条"
            await bot.send(event, reply)
        elif 20 < len(res) <= 60:
            li = []
            for index, item in enumerate(res):
                reply += f"{index+1}. {item['command']}: {item['description']}\n"
                if (index + 1) % 20 == 0:
                    data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
                    li.append(data)
                    reply = ""
            reply += f"============\n猫猫共查询到结果{len(res)}条"
            data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
            li.append(data)
            gid = event.group_id
            await bot.send_group_forward_msg(group_id=gid, messages=li)
        elif 60 < len(res):
            li = []
            for index, item in enumerate(res):
                reply += f"{index+1}. {item['command']}: {item['description']}\n"
                if (index + 1) % 5 == 0:
                    data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
                    li.append(data)
                    reply = ""
            reply += f"============\n猫猫共查询到结果{len(res)}条"
            data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
            li.append(data)
            gid = event.group_id
            await bot.send_group_forward_msg(group_id=gid, messages=li)
        else:
            await bot.send(event, "猫猫没有找到呢~喵~")


on_regex(r"^(help|帮助) (.*)$", handlers=[search])