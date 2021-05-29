# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from requests import RequestException, TooManyRedirects
from school_api.client.api.base import BaseSchoolApi
from school_api.exceptions import UserInfoException


class UserInfo(BaseSchoolApi):
    """ 用户信息查询 部门教师不可用 """

    def get_info(self, **kwargs):
        """ 用户信息 获取入口 """
        info_url = self.school_url['INFO_URL'] + self.user.account

        try:
            res = self._get(info_url, **kwargs)
        except TooManyRedirects:
            raise UserInfoException(self.school_code, '用户信息接口已关闭')
        except RequestException:
            raise UserInfoException(self.school_code, '获取用户信息失败')

        return UserInfoParse(self.school_code, self.user.user_type, res.text).user_info


class UserInfoParse:
    """ 信息页面解析模块 """

    def __init__(self, school_code, user_type, html):
        self.data = {}
        self.school_code = school_code
        self.soup = BeautifulSoup(html, "html.parser")
        [self._html_parse_of_student, self._html_parse_of_teacher][user_type]()

    def _html_parse_of_student(self):
        table = self.soup.find("table", {"class": "formlist"})
        if not table:
            raise UserInfoException(self.school_code, '获取学生用户信息失败')

        student_no = table.find(id="xh").text
        real_name = table.find(id="xm").text
        # 当前所在级 grade = table.find(id="lbl_dqszj").text
        class_name = table.find(id="lbl_xzb").text
        college = table.find(id="lbl_xy").text
        speciality = table.find(id="lbl_zymc").text
        # 入学时间 enroll_time = table.find(id="lbl_rxrq").text
        # 学习层次 education_level = table.find(id="lbl_CC").text
        # 学制 educational_system = table.find(id="lbl_xz").text
        # 身份证号 id_card = table.find(id="lbl_sfzh").text
        # 出生日期 birth_date = table.find(id="lbl_csrq").text
        # 性别 sex = table.find(id="lbl_xb").text

        self.data = {
            "student_no": student_no,
            "real_name": real_name,
            "class_name": class_name,
            "college": college,
            "speciality": speciality
        }

    def _html_parse_of_teacher(self):
        table = self.soup.find(id="Table3")
        if not table:
            raise UserInfoException(self.school_code, '获取教师用户信息失败')

        real_name = table.find(id='xm').text
        sex = table.find(id='xb').text
        dept = table.find(id='bm').text
        position = table.find(id='zw').text
        associate_degree = table.find(id='xl').text
        positional_title = table.find(id='zc').text
        self.data = {
            "real_name": real_name,
            "sex": sex,
            "dept": dept,
            "position": position,
            "associate_degree": associate_degree,
            "positional_title": positional_title
        }

    @property
    def user_info(self):
        """ 返回用户信息json格式 """
        return self.data
