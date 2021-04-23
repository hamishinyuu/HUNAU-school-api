# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

LOGIN_SESSION_SAVE_TIME = 3600 * 2

URL_PATH_LIST = [
    {
        # 学生
        "HOME_URL": "/xs_main.aspx?xh=",
        "SCORE_URL": "/xscjcx.aspx?gnmkdm=N121613&xh=",
        "INFO_URL": "/xsgrxx.aspx?gnmkdm=N121501&xh=",
        "SCHEDULE_URL": "/xskbcx.aspx?gnmkdm=N121602&xh=",
    },
    {
        # 教师
        "HOME_URL": "/js_main.aspx?xh=",
        "INFO_URL": "/lw_jsxx.aspx?gnmkdm=N122502&zgh=",
        "SCHEDULE_URL": ["", "/jstjkbcx.aspx?gnmkdm=N122303&zgh="]
    },
    {
        # 部门
        "HOME_URL": "/bm_main.aspx?xh=",
        "SCHEDULE_URL": ["", "/tjkbcx.aspx?gnmkdm=N120313&xh="],
        "PLACE_SCHEDULE_URL": "/kbcx_jxcd.aspx?gnmkdm=N120314&xh="
    }
]

CLASS_TIME = [
    ["8:00", "8:45"],
    ["8:55", "9:40"],
    ["10:05", "10:50"],
    ["11:10", "11:45"],
    ["14:30", "15:15"],
    ["15:25", "16:10"],
    ["16:35", "17:20"],
    ["17:30", "18:15"],
    ["19:30", "20:15"],
    ["20:25", "21:10"],
    ["21:10", "21:35"],
    ["21:35", "22:00"]
]
