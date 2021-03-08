<!--
 * @Author: zfj
 * @Date: 2021-03-03 18:57:23
 * @LastEditTime: 2021-03-03 18:57:23
 * @LastEditors: zfj
 * @Description: None
 * @GitHub: https://github.com/zfjdhj
-->
# momobot
猫猫 for nonebot2

## 说明 
我是彩笔 大佬轻喷

## 插件列表

### 个人插件：

**先慢慢把自已的插件搬过来**

| 插件名称 | 功能 |
| :- | :- |
| momobot_ascii_art | 生成字符画 |
| momobot_auth | 猫猫契约 |
| momobot_help_search | 帮助检索 |
| momobot_main | 一些自定义的回复 |
| momobot_mimikko | mimikko自动签到 |
| momobot_pcr_remind | pcr推送提醒 |
| momobot_translate | 翻译插件 |

### 魔改移植插件：
| 插件名称 | 功能 |
| :- | :- |
| - | - |

## 大佬牛逼：
缝合怪进化 **究~极~缝~合~怪~**
| 软件名称 | 功能 | 链接 |
| :- | :- | :- |
| yobot | pcr公会战辅助机器人 | <https://github.com/pcrbot/yobot> |
| gypsum | 冰石自定义回复机器人 | <https://github.com/yuudi/gypsum> |
### yobot魔改
1. 启动youbot时，自动获取ipv6地址变更
``` python
# yobot.py [line:261]

# update runtime variables
import subprocess
import re

def getIP():
    # interface='eth0'
    interface = ""
    output = subprocess.getoutput("/sbin/ip addr show " + interface + "|grep -v deprecated")
    ipv4 = re.findall(r" inet ([\d.]+)/(\d+) brd [\d./]+ scope global ", output, re.M | re.I)
    ipv6 = re.findall(
        r" inet6 ([^f:][\da-f:]+)/(\d+) scope global .+?\n.+? valid_lft (\d+)sec ", output, re.M | re.I
    )
    # print(output)
    # eui64的ipv6地址按超时时间排序,其他的排前面
    def my_key(a):
        if a[0].find("ff:fe") > 4:
            return int(a[2])
        else:
            return -1

    ipv6.sort(key=my_key, reverse=True)  # 反向排序
    # print("ipv4=", ipv4)
    # print("ipv6=", ipv6)

    return (ipv4, ipv6)

ipv4, ipv6 = getIP()
public_adress = f"http://[{ipv6[0][0]}]:9025/"
self.glo_setting.update({"dirname": dirname, "verinfo": verinfo, "public_address": public_adress})
        
```

2. 新增定时任务`00:08` “yobot重启”，嘛，ipv6每天都变
``` python
# updater.py [line:319]

def jobs(self) -> Iterable[Tuple[CronTrigger, Callable[[], List[Dict[str, Any]]]]]:
    trigger = CronTrigger(hour="00", minute="08")
    job1 = (trigger, self.restart)
    if not self.setting.get("auto_update", True):
        return tuple()
    time = self.setting.get("update-time", "03:30")
    hour, minute = time.split(":")
    trigger = CronTrigger(hour=hour, minute=minute)
    job = (trigger, self.update_auto_async)
    return (
        job,
        job1,
    )
```
3. 状态信息添加当前出刀数
``` shell
# (版本不同，可能代码行数不同，自行查找)
# battle.py [line:22]
from ..momobot.testSqlitedb import *
# battle.py [line:347]
group_id=group.group_id
today = int(time.time()+3600*3)//86400
result = {}
reply = ''
challenge_list = challenge_today_total(today, group_id)
user_qqid_list = get_user_list(group_id)
user_qqid_nickname = get_qqid_nickname(group_id)
reply = f'今日出刀总数是{len(challenge_list)}'
for i, j in user_qqid_nickname.items():
    result[j] = challenge_list.count(i)
    reply += f'\n{j}:{challenge_list.count(i)}/3'
# battle.py [line:343]
boss_summary = (
    f'现在{group.boss_cycle}周目，{group.boss_num}号boss\n'
    f'生命值{group.boss_health:,}\n'
    f'当前出刀{len(challenge_list)}/{len(user_qqid_list)*3}'
)
# battle.py [line:487]
status = BossStatus(
    group.boss_cycle,
    group.boss_num,
    group.boss_health,
    0,
    msg,
    group_id,
)
# battle.py [line:532]
status = BossStatus(
    group.boss_cycle,
    group.boss_num,
    group.boss_health,
    0,
    f'{nik}的出刀记录已被撤销',
    group_id,
)
# battle.py [line:576]
status = BossStatus(
    group.boss_cycle,
    group.boss_num,
    group.boss_health,
    0,
    'boss状态已修改',
    group_id,
)
# battle.py [line:955]
status = BossStatus(
    group.boss_cycle,
    group.boss_num,
    group.boss_health,
    qqid,
    info,
    group_id,
)
# battle.py [line:1005]
status = BossStatus(
    group.boss_cycle,
    group.boss_num,
    group.boss_health,
    0,
    'boss挑战已可申请',
    group_id,
)
# battle.py [line:1437]
today = int(time.time()+3600*3)//86400
result = {}
reply = ''
challenge_list = challenge_today_total(today, group_id)
user_qqid_list = get_user_list(group_id)
reply = f'今日出刀总数是{len(challenge_list)}'
for item in user_qqid_list:
    result[get_qqid_nickname(item)[item]] = challenge_list.count(item)
tmp=zip(result.values(),result.keys())
new_tmp=list(sorted(tmp))
for i in range(0,len(new_tmp)):
    reply += f'\n{new_tmp[i][1]} : {new_tmp[i][0]}/3'
# battle.py [line:1454]
return '请在面板中查看：'+url+'\n'+reply
# typing.py [line:3]
import time
from ..momobot.testSqlitedb import *
# typing.py [line:19]
group_id: int
# typing.py [line:22]
group_id=self.group_id
    today = int(time.time()+3600*3)//86400
    result = {}
    reply = ''
    challenge_list = challenge_today_total(today, group_id)
    user_qqid_list = get_user_list(group_id)
    # print(f'今日出刀总数是{len(challenge_list)}')
    reply = f'\n今日出刀总数是{len(challenge_list)}'
# typing.py [line:27]
summary = ("现在{}周目，{}号boss\n" "生命值{:,}\n" "当前出刀{}/{}").format(
            self.cycle, self.num, self.health, len(challenge_list), len(user_qqid_list) * 3
        )
```

## 感谢
原hoshino插件版:

<https://github.com/zfjdhj/zfjbot>

鸽了，嗯，鸽了

部分代码参考：

<https://github.com/Ice-Cirno/HoshinoBot>
