"""
Function:
    爬取中国高考在线的高校信息
Author:
    leishufei
"""
#!usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import csv
import time


class NCEESpider(object):
    def __init__(self):
        self.base_url = "https://api.eol.cn/gkcx/api/"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40",
            "Referer": "https://gkcx.eol.cn/school/search",
            "Host": "api.eol.cn"
        }

    def get_json(self, page):
        form_data = {
            "access_token": "",
            "admissions": "",
            "central": "",
            "department": "",
            "dual_class": "",
            "f211": "",
            "f985": "",
            "is_dual_class": "",
            "keyword": "",
            "page": page,  # 后面再调
            "province_id": "",
            "request_type": 1,
            "school_type": "",
            "signsafe": "",
            "size": 20,
            "sort": "view_total",
            "type": "",
            "uri": "apigkcx/api/school/hotlists"
        }
        try:
            response = requests.post(self.base_url, data=form_data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(e)

    def parse_json(self, json_data):
        if json_data["data"]:
            items = json_data["data"]["item"]
            for each in items:
                # 学校名
                school_name = each["name"]
                # 所属部门
                belong = each["belong"]
                # 高校层次
                dual_class_name = each["dual_class_name"]
                # 是否 985
                f985 = each["f985"]
                # 是否 211
                f211 = each["f211"]
                # 办学类型
                level_name = each["level_name"]
                # 院校类型
                type_name = each["type_name"]
                # 是否公办
                nature_name = each["nature_name"]
                # 人气值
                view_total = each["view_total"]
                # 所在省份
                province_name = each["province_name"]
                # 所在城市
                city_name = each["city_name"]
                # 地址
                address = each["address"]
                # 排名
                rank = each["rank"]
                self.save_data([school_name, belong, dual_class_name, f985, f211, level_name, type_name, nature_name,
                                view_total, province_name, city_name, address, rank])

    def save_data(self, school_content):
        with open(r"result.csv", "a", encoding="utf-8", newline="") as f1:
            writer = csv.writer(f1)
            with open(r"result.csv", "r", encoding="utf-8") as f2:
                rows = csv.reader(f2)
                # 判断表头是否存在
                if not [row for row in rows]:
                    writer.writerow(["school_name", "belong", "dual_class_name", "985", "211", "level", "type", "nature",
                                     "total_view", "province", "city", "address", "rank"])
                    writer.writerow(school_content)
                else:
                    writer.writerow(school_content)

    def run(self):
        # 最大页数为 148 页
        for page in range(1, 148 + 1):
            print("正在爬取第 %s 页" % page)
            json = self.get_json(page)
            self.parse_json(json)
            time.sleep(2)


if __name__ == "__main__":
    spider = NCEESpider()
    spider.run()
