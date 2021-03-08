# -*- coding: UTF-8 -*-
import sqlite3
import os


DB_PATH = os.path.abspath("./yobot_data/yobotdata.db")


def get_user_list(group_id):
    user_list = []
    conn = sqlite3.connect(DB_PATH)
    nickname_data = conn.execute("select * from clan_member where group_id = %d" % group_id)
    for item in nickname_data:
        user_list.append(item[1])
    conn.close()
    return user_list


def get_qqid_nickname(qq_id):
    qqid_nickname = {}
    conn = sqlite3.connect(DB_PATH)
    data = conn.execute("select * from user where qqid = %d" % qq_id)
    for item in data:
        qqid_nickname[item[0]] = item[1]
    return qqid_nickname


def challenge_today_total(pcrdate_today, group_id):
    challenge_list = []
    #    search=[pcrdate_today,group_id]
    # 打开数据库连接
    conn = sqlite3.connect(DB_PATH)
    #    print("Opened database successfully")
    # 读取表students
    #    cur = conn.cursor()
    data = conn.execute(
        "SELECT * from clan_challenge where challenge_pcrdate = %s and gid = %s and not is_continue = true"
        % (pcrdate_today, group_id)
    )
    for x in data:
        data2 = conn.execute("select * from user where qqid = %d" % x[3])
        #        print(type(x))
        for y in data2:
            challenge_list.append(y[0])
    #            print(y[1])
    # print(type(challenge_list))
    conn.close()
    return challenge_list


def get_battle_damage_today(pcrdate_today, group_id):
    damage_list = []
    conn = sqlite3.connect(DB_PATH)
    data = conn.execute(
        "SELECT * from clan_challenge where challenge_pcrdate = %s and gid = %s" % (pcrdate_today, group_id)
    )
    for x in data:
        damage_list.append(x[9])
    conn.close()
    return damage_list


def get_battle_damage_today_all(pcrdate_today, group_id):
    # 返回dict={damage:nickname,...}
    challenge_list = {}
    conn = sqlite3.connect(DB_PATH)
    # print(pcrdate_today, group_id)
    data = conn.execute(
        "SELECT * from clan_challenge where challenge_pcrdate = %s and gid = %s" % (pcrdate_today, group_id)
    )
    for x in data:
        data2 = conn.execute("select * from user where qqid = %d" % x[3])
        #        print(type(x))
        # challenge_list[f'{x[9]}'] = x[3]
        for y in data2:
            challenge_list[f"{x[9]}"] = y[1]
    #            print(y[1])
    # print(len(challenge_list))
    conn.close()
    # print(challenge_list)
    return challenge_list


def set_battle_damage_today(group_id, old_damage, new_damage):
    damage_list = []
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "update clan_challenge set challenge_damage = %s where gid = %s and challenge_damage = %s"
        % (new_damage, group_id, old_damage)
    )
    conn.commit()
    conn.close()
    return