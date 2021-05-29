# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from bs4 import BeautifulSoup
from requests import RequestException, TooManyRedirects
import traceback
from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_alert_tip
from school_api.exceptions import ScoreException


class Score(BaseSchoolApi):
    ''' 学生成绩获取 '''

    def get_score(self, score_year=None, score_term=None, use_api=0, **kwargs):
        ''' 成绩信息 获取入口
        :param score_year: 成绩学年
        :param score_term: 成绩学期
        :param use_api:    0.接口1, 1.接口2, 2.接口3 ...
        :param kwargs: requests模块参数
        return
        '''
        score_url = self.school_url['SCORE_URL'] + self.user.account

        try:
            view_state = self._get_view_state(score_url, **kwargs)
        except TooManyRedirects:
            msg = '可能是成绩接口地址不对，请尝试更改use_api值'
            raise ScoreException(self.school_code, msg)
        except RequestException:
            msg = '获取成绩请求参数失败'
            traceback.format_exc()
            raise ScoreException(self.school_code, msg)
        payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': view_state,
            'hidLanguage': '',
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'btn_zcj': '历年成绩'
        }
        try:
            res = self._post(score_url, data=payload, **kwargs)
        except TooManyRedirects:
            raise ScoreException(self.school_code, '成绩接口已关闭')
        except RequestException:
            raise ScoreException(self.school_code, '获取成绩信息失败')

        tip = get_alert_tip(res.text)
        if tip:
            raise ScoreException(self.school_code, tip)
        return ScoreParse(self.school_code, res.text, use_api).get_score(score_year, score_term)


class ScoreParse():
    ''' 成绩页面解析模块 '''

    def __init__(self, school_code, html, use_api):
        self.school_code = school_code
        self.use_api = use_api
        self.soup = BeautifulSoup(html, "html.parser")
        self._html_parse_of_score()

    def _html_parse_of_score(self):
        table = self.soup.find("table", {"id": re.compile("Datagrid1", re.IGNORECASE)})
        if not table:
            raise ScoreException(self.school_code, '获取成绩信息失败')
        rows = table.find_all('tr')
        rows.pop(0)
        self.score_info = {}
        for row in rows:
            cells = row.find_all("td")
            # TODO: 检查补考成绩 重修成绩 备注 重修标记是否有用
            # 学年 学期 课程代码、名称、性质
            year = cells[0].text
            term = cells[1].text
            lesson_identifier = cells[2].text
            lesson_name = cells[3].text.strip()
            lesson_type = cells[4].text
            # 学分 绩点
            credit = cells[6].text.strip() or 0
            point = cells[7].text.strip() or 0
            # 开课学院
            college = cells[16].text.strip()
            score_dict = {
                "name": lesson_name,
                "identifier": lesson_identifier,
                "type": lesson_type,
                "credit": float(credit),
                "point": float(point),
                "college": college
            }

            # 输出不为空的成绩
            dict_keys = ['daily', 'mid', 'end', 'exp', 'score']
            for cells_num in range(8,13):
                if cells[cells_num].text != '\xa0':
                    # 列表起始索引为0
                    score_dict[dict_keys[cells_num-8]] = self.handle_data(cells[cells_num].text)

            # 组装数组格式的数据备用
            self.score_info[year] = self.score_info.get(year, {})
            self.score_info[year][term] = self.score_info[year].get(term, [])
            self.score_info[year][term].append(score_dict)

    def get_score(self, year, term):
        ''' 返回成绩信息json格式 '''
        try:
            if not self.score_info:
                raise KeyError
            if year:
                if term:
                    return self.score_info[year][term]
                return self.score_info[year]
        except KeyError:
            raise ScoreException(self.school_code, '暂无成绩信息')

        return self.score_info

    @staticmethod
    def handle_data(data):
        try:
            return float(data)
        except ValueError:
            return data
