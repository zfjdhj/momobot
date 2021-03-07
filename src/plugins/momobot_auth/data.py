import os
import json
import time
import datetime

# from datetime import datetime, timedelta, timezone

plugin_path = os.path.dirname(__file__)

## 打开json文件
def open_jsonfile(path: str) -> dict:
    with open(path, "rb") as f:
        return json.loads(f.read())


## 保存json文件
def write2json(path: str, data) -> None:
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


## 时间戳-时间格式化
def timeStamp2time(timeStamp: int) -> str:
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y年%m月%d日", timeArray)
    # print(type(otherStyleTime))
    return otherStyleTime


# 计算两个日期的间隔
def cal_day(d1: str, d2: str) -> datetime.timedelta:
    d1 = datetime.datetime.strptime(d1, "%Y年%m月%d日")
    d2 = datetime.datetime.strptime(d2, "%Y年%m月%d日")
    delta = d1 - d2
    # print(delta.days)
    # print(delta, type(delta))
    return delta


class auth:
    def __init__(self):
        self.data = open_jsonfile(plugin_path + "/data.json")

    def get_auth_info(self, gid: str) -> dict:
        self.data_refresh()
        return self.data[gid]

    def get_join_time(self, gid: str) -> str:
        return self.data[gid]["join_time"]

    def get_auth_time(self, gid: str) -> str:
        return self.data[gid]["auth_time"]

    def add_auth_time(self, gid: str, addtime: int) -> str:
        auth_time = self.get_auth_time(gid)
        self.data[gid]["auth_time"] = str(int(auth_time) + addtime)
        self.save_data()
        return self.data[gid]["auth_time"]

    def add_new_group(self, gid: str, info: dict) -> str:
        self.data[gid] = info[gid]
        self.save_data()
        return self.data[gid]["auth_time"]

    def save_data(self) -> None:
        write2json(plugin_path + "/data.json", self.data)

    def data_refresh(self):
        self.__init__()


# test
# group_auth = auth()
# test = open_jsonfile(plugin_path + "/data.json")
# for item in test:
#     if item != "群号":
#         print(group_auth.get_auth_info(item))
#         print("群名称", group_auth.get_auth_info(item)["name"])
#         print("加入时间", timeStamp2time(int(group_auth.get_auth_info(item)["join_time"])))
#         print(
#             "有效期",
#             cal_day(
#                 timeStamp2time(int(group_auth.get_auth_info(item)["auth_time"])),
#                 timeStamp2time(int(group_auth.get_auth_info(item)["join_time"])),
#             ),
#         )
#         print("到期时间", timeStamp2time(int(group_auth.get_auth_info(item)["auth_time"])))
