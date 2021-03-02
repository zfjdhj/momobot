<!--
 * @Author: zfj
 * @Date: 2021-03-02 18:38:17
 * @LastEditTime: 2021-03-02 18:42:34
 * @LastEditors: zfj
 * @Description: None
 * @GitHub: https://github.com/zfjdhj
-->
# momobot_mimikko

a plugin for nonebot2 to auto sign in for mimikko

## 使用

1. 抓包获取通信数据app_id,Authorization;
2. 默认方式安装插件。
3. 修改`config.py`中数据;

``` python
# /config.py
# 抓包获取到的app_id,Authorization;
bot_id="bot的qq号码"
app_id= "修改为你的app_id"
authorization="修改为你的Authorization"
group_id="定时通知到群"
```

## 说明

暂时自用，有问题提issue

## 功能
| 指令 | 功能 |
| :- | :- |
| mimikko sign | 梦梦奈签到 |
| mimikko energy | 领取能量值 |
| mimikko check | 检查签到状态 |
| (自动)签到任务 | 每日12点定时签到 |
