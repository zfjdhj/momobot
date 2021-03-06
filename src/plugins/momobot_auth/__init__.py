# import nonebot
from nonebot import get_driver, get_bots

from nonebot.plugin import on_command, on_regex, on_startswith

from nonebot.adapters import Bot, Event
import nonebot.adapters.cqhttp.message

from nonebot_plugin_apscheduler import scheduler
from .config import Config


global_config = get_driver().config
config = Config(**global_config.dict())

from .data import *
import time


group_auth = auth()
GROUP_LIST = {}

leave_msg = {
    "5": "喵？到时间了喵~？",
    "4": "骑士君真的不想要猫猫了吗？",
    "3": "我还不想要离开骑士君~呜喵~",
    "2": "バーカー，猫猫讨厌骑士君...",
    "1": "猫猫真的要走了哦",
    "0": "骑士君！别れるのはつらいけど、まだどちらでお会いにできるかもしれないので、それを楽しみしてます。",
}

black_list = [
    128520726,
    174086370,
    185263682,
    340032534,
]


def check(gid: str = "", msg: str = "========猫猫契约========") -> str:
    if gid == "":
        for item in group_auth.data:
            if item != "群号":
                msg = check(item, msg)
    else:
        auth_info = group_auth.get_auth_info(gid)
        if auth_info:
            # print(auth_info)
            msg += f"\n群名称: {auth_info['name']}"
            msg += f"\n猫猫已陪伴骑士君{cal_day(timeStamp2time(time.time()),timeStamp2time(int(auth_info['join_time']))).days}天"
            msg += f"\n还会陪伴大家{cal_day(timeStamp2time(int(auth_info['auth_time'])),timeStamp2time(time.time())).days}天"
            # msg += f"\n到期: {timeStamp2time(int(auth_info['auth_time']))}"
            msg += f"\n================"
            rest_day = cal_day(timeStamp2time(int(auth_info["auth_time"])), timeStamp2time(time.time())).days
            if rest_day < 0:
                msg += "\nNya~ 还有人记得猫猫吗？猫猫不要和コッコロちゃん一样！"
            elif rest_day <= 5:
                msg += f"\n{leave_msg[str(rest_day)]}"
        else:
            msg = "暂无本群信息"
    return msg


def add_auth_time(gid: str, addtime: int) -> str:
    # group_auth.add_auth_time("426770092",1*3600*24)
    group_auth.add_auth_time(gid, addtime * 3600 * 24)
    msg = "操作成功，猫猫记住了。\n"
    msg += check(gid)
    return msg


async def main(bot: Bot, event: Event):
    global GROUP_LIST
    gl = await bot.get_group_list()
    for g in gl:
        if not g["group_id"] in black_list:
            GROUP_LIST[str(g["group_id"])] = {"name": g["group_name"]}
    # print(GROUP_LIST)
    args = event.message.extract_plain_text().split()[1:]
    msg = ""
    user_id = event.user_id
    if str(user_id) in bot.config.superusers:
        is_admin = True
    else:
        is_admin = False
    if event.message_type == "group":
        if not event.group_id in black_list and group_auth.data.get(str(event.group_id)):
            if len(args) == 0:
                msg = "猫猫不懂唉~\n可用命令：\nauth check"
            elif len(args) == 1:
                if args[0] == "all":
                    if is_admin:
                        msg = check()
                    else:
                        msg = "猫猫不懂唉~\n可用命令：\nauth check"
                elif args[0] == "check":
                    msg = check(str(event.group_id))
                else:
                    msg = "猫猫不懂唉~\n可用命令：\nauth check"
            elif len(args) == 2 and args[0] == "add":
                if is_admin:
                    add_time = args[1]
                    msg = add_auth_time(str(event.group_id), int(add_time))
                else:
                    msg = "猫猫不懂唉~\n可用命令：\nauth check"
        elif not event.group_id in black_list:
            item = str(event.group_id)
            print(f"add new group_info{item}")
            new_group_info = {
                item: {
                    "name": GROUP_LIST[str(item)]["name"],
                    "join_time": str(int(time.time())),
                    "auth_time": str(int(time.time()) + 7 * 24 * 3600),
                }
            }
            print(new_group_info)
            group_auth.add_new_group(item, new_group_info)
            msg = "暂无本群信息，已自动签订契约，要善待猫猫哦"
            msg += check(str(event.group_id))

    elif event.message_type == "private":
        if is_admin:
            msg = check()
        else:
            msg = "猫猫不懂唉~"
    # print(msg)
    await bot.send(event, msg)


on_startswith("auth", handlers=[main])

# @sv.scheduled_job("cron", minute='*/1')
async def check_auth():
    bot = get_bots()[config.bot_id]
    global GROUP_LIST
    gl = await bot.get_group_list()
    for g in gl:
        if not g["group_id"] in black_list:
            GROUP_LIST[str(g["group_id"])] = g["group_name"]
    try:
        for item in GROUP_LIST.keys():
            msg = ""
            if group_auth.data.get(item):
                group_id = item
                auth_info = group_auth.get_auth_info(item)
                rest_day = cal_day(timeStamp2time(int(auth_info["auth_time"])), timeStamp2time(time.time())).days
                if rest_day <= 5:
                    if rest_day < 0:
                        msg += "Nia~ 还有人记得猫猫吗？猫猫不要和コッコロちゃん一样！"
                    elif rest_day <= 5:
                        msg += leave_msg[str(rest_day)]
                    msg += f"\n猫猫还会陪伴大家{cal_day(timeStamp2time(int(auth_info['auth_time'])),timeStamp2time(time.time())).days}天"
                    print(group_id, msg)
                    await bot.send_group_msg(group_id=group_id, message=msg)
            else:
                print(f"add new group_info: {item}")
                new_group_info = {
                    item: {
                        "name": GROUP_LIST[item],
                        "join_time": str(int(time.time())),
                        "auth_time": str(int(time.time()) + 7 * 24 * 3600),
                    }
                }
                print(new_group_info)
                group_auth.add_new_group(item, new_group_info)
    except Exception as e:
        await bot.send_group_msg(group_id="426770092", message=f"zfjbot-auth：{e}")


scheduler.add_job(check_auth, "cron", hour=18)
# test
# scheduler.add_job(check_auth, "interval", seconds=20)
