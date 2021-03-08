from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional
import time
from ..momobot.testSqlitedb import *

Pcr_date = NewType("Pcr_date", int)
Pcr_time = NewType("Pcr_time", int)
QQid = NewType("QQid", int)
Groupid = NewType("Groupid", int)


@dataclass
class BossStatus:
    cycle: int
    num: int
    health: int
    challenger: QQid
    info: str
    group_id: int

    def __str__(self):
        group_id = self.group_id
        today = int(time.time() + 3600 * 3) // 86400
        challenge_list = challenge_today_total(today, group_id)
        user_qqid_list = get_user_list(group_id)
        # print(f'今日出刀总数是{len(challenge_list)}')
        summary = ("现在{}周目，{}号boss\n" "生命值{:,}\n" "当前出刀{}/{}").format(
            self.cycle, self.num, self.health, len(challenge_list), len(user_qqid_list) * 3
        )
        # if self.challenger:
        #     summary += '\n' + '{}正在挑战boss'.format(self.challenger)
        if self.info:
            summary = self.info + "\n" + summary
        return summary


@dataclass
class BossChallenge:
    date: Pcr_date
    time: Pcr_time
    cycle: int
    num: int
    health_ramain: int
    damage: int
    is_continue: bool
    team: Optional[List[int]]
    message: Optional[str]


ClanBattleReport = NewType("ClanBattleReport", List[Dict[str, Any]])
