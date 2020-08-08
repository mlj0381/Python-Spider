"""
爬取 58 同城上的招聘信息
"""
#!usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
import random
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery as pq
import os
import csv
import time


class Zhaopin(object):
    def __init__(self):
        # 第一页的 URL，用于获取最大页数
        self.url = "https://gz.58.com/job/pn1/?param7503=1&from=yjz2_zhaopin&PGTID=0d302408-0000-30bb-587d-5aed5ac6bb8d&ClickID=3"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61",
            "Referer": "https://gz.58.com/job/pn4/?param7503=1&from=yjz2_zhaopin&PGTID=0d302408-0000-39b8-0e4c-675b4ed1fa98&ClickID=3",
            "Accept": "*/*"
        }
        # 其实把访问频率降低点，完全不需要使用代理
        # self.proxy = self.get_proxy()
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.session.keep_alive = False

    def get_proxy(self):
        """
        @崔庆才 提供的开源项目，以获取随机可用的代理
        地址：https://github.com/Python3WebSpider/ProxyPool
        """
        proxy_url = "http://localhost:5555/random"
        response = requests.get(proxy_url)
        proxy = response.text
        return {"http": "http://" + proxy}

    def get_max_page_number(self):
        # response = requests.get(self.url, headers=self.headers, timeout=5)
        response = self.session.get(self.url, headers=self.headers, timeout=5)
        html = response.text
        max_page_number = int(re.findall(r'<i class="total_page">(.*?)</i>', html)[0])
        return max_page_number

    def get_page(self, url):
        try:
            # response = requests.get(url, headers=self.headers, proxies=self.proxy, timeout=5)
            response = self.session.get(url, headers=self.headers, timeout=10)
            html = response.text
            return html
        except Exception as e:
            print("Meeting an error: ", e)

    def get_detailed_urls(self, html):
        soup = BeautifulSoup(html, "lxml")
        divs = soup.find_all("div", attrs={"class": "job_name clearfix"})
        detailed_urls = []
        for div in divs:
            detailed_url = div.a.get("href")
            detailed_urls.append(detailed_url)
        return detailed_urls

    def get_info(self, url):
        html = self.get_page(url)
        soup = BeautifulSoup(html, "lxml")

        # 职位信息
        if soup.select("span.pos_title"):
            pos_title = soup.select("span.pos_title")[0].text.strip()
        else:
            pos_title = ""
        if soup.select("span.pos_salary"):
            pos_salary = soup.select("span.pos_salary")[0].text.strip()
        else:
            pos_salary = ""
        if soup.select("div.pos_welfare > span"):
            pos_welfare = ";".join([each.text.strip() for each in soup.select("div.pos_welfare > span")])
        else:
            pos_welfare = ""
        if soup.select("div.pos_base_condition > span"):
            pos_condition = ";".join([each.text.strip() for each in soup.select("div.pos_base_condition > span")])
        else:
            pos_condition = ""
        if soup.select("div.pos-area > span"):
            pos_address = " ".join([each.text.strip().replace(" ", "") for each in soup.select("div.pos-area > span")[:-1]])
        else:
            pos_address = ""
        doc = pq(html)
        if doc("div.subitem_con.pos_description div.des").html():
            pos_description = doc("div.subitem_con.pos_description div.des").html().strip().replace("\n", "").replace(" ", "").replace("<br/>", "\n")
        else:
            pos_description = ""
        if doc("div.txt div.shiji p").html():
            company_introduction = doc("div.txt div.shiji p").html().strip().replace("\n", "").replace(" ", "").replace("<br/>", "\n")
        else:
            company_introduction = ""
        if soup.select("div.item_con.px-intro span"):
            course_introduction = ";".join([each.text for each in soup.select("div.item_con.px-intro span")[:-2]])
        else:
            course_introduction = ""
        if soup.select("div.subitem_con.comp_intro_daipei div.shiji"):
            institution_introduction = soup.select("div.subitem_con.comp_intro_daipei div.shiji")[0].text.strip().replace("\n", "").replace(" ", "")
        else:
            institution_introduction = ""

        # 公司信息
        if soup.select("div.baseInfo_link"):
            company_name = soup.select("div.baseInfo_link")[0].text.strip()
        else:
            company_name = ""
        if soup.select("a.comp_baseInfo_link"):
            company_business = soup.select("a.comp_baseInfo_link")[0].text.strip()
        else:
            company_business = ""
        if soup.select("p.comp_baseInfo_scale"):
            company_scale = soup.select("p.comp_baseInfo_scale")[0].text.strip()
        else:
            company_scale = ""
        if soup.select("div.com_statistics p"):
            # 简历查看率和招聘职位个数是通过 js 生成的，无法从源代码中获取
            a = soup.select("div.rightCon div.comp_baseInfo_title a")[0].get("href")
            userid, postid = re.findall(r'com/(.*?)/\?[entinfo=]?(.*?)_.*?', a)[0]
            # 除了 infoId (和 postid 值一样）和 userid 有用以外，其他的参数都没有意义
            resume_read_data_url = "https://statisticszp.58.com/position/totalcount/?infoId=%s&userId=%s&local=&" \
                                   "cateID=&referUrl=&callback=&_=" % (postid, userid)
            resume_feedback_data_url = "https://jianli.58.com/ajax/getefrate/%s?callback=&_=" % userid
            response1 = requests.get(resume_read_data_url, headers=self.headers)
            response2 = requests.get(resume_feedback_data_url, headers=self.headers)
            resume_read_num = re.findall(r'"infoCount":(.*?),', response1.text)[0]
            resume_feedback_rate = re.findall(r'"efrate":(.*?)}', response2.text)[0]
            join_time = soup.select("div.com_statistics p")[2].text.strip().split(" ")[0]
            # recruitment_condition = [each.text.strip().split(" ")[0] for each in soup.select("div.com_statistics p")]
            recruitment_condition = [resume_feedback_rate, resume_read_num, join_time]
        else:
            recruitment_condition = ["", "", ""]

        content = [pos_title, pos_salary, pos_welfare, pos_condition, pos_address, pos_description, company_introduction,
                   course_introduction, institution_introduction, company_name, company_business, company_scale,
                   recruitment_condition[0], recruitment_condition[1], recruitment_condition[2]]

        self.save_info(content)
        content.clear()
        recruitment_condition.clear()

    def save_info(self, content):
        if not os.path.exists(r"results/"):
            os.makedirs("results/")
        with open(r"results/58.csv", "a", encoding="utf-8-sig", newline="") as f1:
            writer = csv.writer(f1)
            with open(r"results/58.csv", "r", encoding="utf-8-sig") as f2:
                rows = csv.reader(f2)
                # 判断是否要写入表头
                if not [row for row in rows]:
                    writer.writerow(["职位名称", "职位薪资", "员工福利", "招聘条件", "公司位置", "职位描述", "公司介绍",
                                     "课程介绍", "培训机构介绍", "公司名称", "公司业务", "公司规模", "简历查看率",
                                     "招聘职位", "加入58"])
                    writer.writerow(content)
                else:
                    writer.writerow(content)

    def run(self):
        print("========================START========================")
        start_page = 1
        end_page = input("请输入您想爬取的页数（不输入表示爬取所有页）：")
        max_page_number = self.get_max_page_number()
        if end_page == "":
            print("检测到您未输入页数，将爬取所有页（%s）" % max_page_number)
            end_page = max_page_number
        else:
            end_page = int(end_page)
            if end_page > max_page_number:
                print("抱歉，您输入的页数超出了最大页数")
                end_page = max_page_number

        for page in range(start_page, end_page + 1):
            url = "https://gz.58.com/job/pn{}/?param7503=1&from=yjz2_zhaopin&PGTID=0d302408-0000-30bb-587d-5aed5ac6b" \
                  "b8d&ClickID=3".format(str(page))
            home_page = self.get_page(url)
            urls = self.get_detailed_urls(home_page)
            for index, url in enumerate(urls):
                print("正在爬取第 %d 页第 %d 条信息" % (page, index + 1))
                # print("目标链接：", url)
                self.get_info(url)
                time.sleep(random.randint(10, 15))
        print("========================END========================")


if __name__ == "__main__":
    zhaopin = Zhaopin()
    zhaopin.run()
