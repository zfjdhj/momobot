<!--
 * @Author: zfj
 * @Date: 2021-03-02 18:38:17
 * @LastEditTime: 2021-03-02 18:42:34
 * @LastEditors: zfj
 * @Description: None
 * @GitHub: https://github.com/zfjdhj
-->
# momobot_pcr_remind
a plugin for nonebot2

## 说明
由于项目的特殊性，仅为自用，作者不负责解答任何问题。

## 使用
1. 修改`config.py`中数据;

    ``` python
    # /config.py
    bot_id="bot的qq号码"
    ```
2. 修改`account.json`;
    1. 抓包或者使用冲冲大佬的[工具](https://github.com/qq1176321897/pcrjjc2)获取登录信息。
    
    2. 将信息填入`account.json`,没有的话就目录下新建一个。
    其中`group_id`为要推送消息的群。


## 功能
| 指令 | 功能 |
| :- | :- |
| equip check | 查看当前时段装备请求 |
| (自动) | 推送新的装备请求 |
| invite check | 查看白名单所属公会 |
| invite <13位uid> | 入会请求邀请(通过)某人 |
| invite onekeyaccept | 一键通过白名单 |
| ~~(自动)~~ | ~~发起白名单邀请~~ 影响农场运作 |
| /pcrval <32位验证码> | 账号risk后过验证码 |

## 感谢
原hoshino插件版:

<https://github.com/zfjdhj/zfjbot-equipmentRemind>

部分代码参考：

<https://github.com/Ice-Cirno/HoshinoBot>

<https://github.com/qq1176321897/pcrjjc2>

<https://github.com/infinityedge01/qqbot2>