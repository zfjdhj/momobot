"""
Author: zfj
Date: 2021-03-03 17:28:39
LastEditTime: 2021-03-03 17:28:39
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
# import nonebot
import re
import os
from nonebot import get_driver, on_startswith


from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message

from .config import Config

from .ascii_art import char_to_pixels, ascii_art


global_config = get_driver().config
config = Config(**global_config.dict())

save_path = os.path.dirname(os.path.abspath(__file__))


async def main(bot: Bot, event: Event):
    receive = re.search(
        r"^字符画(?P<text>.*?)\[CQ:image,file=.*,url=(?P<file>.*)\]$",
        str(event.message).replace("\n", "").replace("\r", ""),
    )
    if receive:
        file = receive.group("file")
        draw_text = receive.group("text")
        if draw_text:
            draw_text_list = char_to_pixels(draw_text)
            # print(draw_text_list)
            draw_text = ""
            for item in draw_text_list:
                draw_text += item[1]
            if await ascii_art(file=file, draw_string=draw_text, save_path=save_path):
                reply = f"[CQ:image,file=file:///{save_path}/temp.ascii.png]"
            else:
                reply = "error：生成图片失败"
        else:
            if await ascii_art(file=file, save_path=save_path):
                reply = f"[CQ:image,file=file:///{save_path}/temp.ascii.png]"
            else:
                reply = "error：生成图片失败"

    else:
        reply = "error:缺少图片"
    # print(reply)
    await bot.send(event, Message(reply))


ascii_art_cmd = on_startswith("字符画", handlers=[main])
