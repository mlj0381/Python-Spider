#!usr/bin/ebv python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import threading
import random
import csv
import traceback


class Anjuke(object):
    def __init__(self):
        self.url = "https://cityname.anjuke.com/sale/p{}/#filtersort"  # cityname 是城市的名字，请自行更改
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "max-age=0",
            "cookie": "",
            "upgrade-insecure-requests": "1",
            "user-agent": UserAgent().random,
        }
        self.proxies = []

    def reader(self):
        f = open(r"proxies.txt", "r", encoding="utf-8")
        lines = f.readlines()
        for line in lines:
            # print(line)
            self.proxies.append({"http": line.strip()})

    def add_proxies(self):
        threads = []
        for i in range(5):
            t = threading.Thread(target=self.reader, args=())
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def get_max_page_number(self):
        i = 1
        while requests.get(self.url.format(str(i)), headers=self.headers, proxies=random.choice(self.proxies), timeout=3).url != "https://neijiang.anjuke.com/sale/#filtersort":
            response = requests.get(self.url.format(str(i)), headers=self.headers, proxies=random.choice(self.proxies), timeout=3)
            # print("当前测试链接：", response.url)
            i += 2
        max_page = i - 2
        return max_page

    def get_home_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies=random.choice(self.proxies), timeout=10)
            # print(response.url)
            response.raise_for_status()
            html = response.text
            return html
        except:
            traceback.print_exc()

    @staticmethod
    def get_secondary_url(html):
        try:
            soup = BeautifulSoup(html, "lxml")
            ul = soup.select("ul#houselist-mod-new")[0]
            # print(ul)
            urls = ul.find_all("a", class_="houseListTitle")
            for each in urls:
                url = each.get("href")
                yield url
        except:
            traceback.print_exc()

    def get_house_info(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies=random.choice(self.proxies), timeout=10)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, "lxml")
        except:
            traceback.print_exc()
        else:
            if len(soup.select("div.basic-info.clearfix span")) != 0:
                price = soup.select("div.basic-info.clearfix span")[0].text.strip().strip("万")
            else:
                price = "null"
            if len(soup.select("ul.houseInfo-detail-list.clearfix li")) != 0:
                lis = soup.select("ul.houseInfo-detail-list.clearfix li")
                if len(lis[0].select("div")) != 0:
                    community = lis[0].select("div")[1].text.strip()
                else:
                    community = "null"
                if len(lis[1].select("div")) != 0:
                    house_type = lis[1].select("div")[1].text.replace("\n", "").replace("\t", "")
                else:
                    house_type = "null"
                if len(lis[2].select("div")) != 0:
                    unit_price = lis[2].select("div")[1].text.strip(" 元/m²")
                else:
                    unit_price = "null"
                if len(lis[3].select("div.houseInfo-content > p")) != 0:
                    address = lis[3].select("div.houseInfo-content > p")[0].text.replace("\n", "").replace(" ", "")
                else:
                    address = "null"
                if len(lis[4].select("div")) != 0:
                    area = lis[4].select("div")[1].text.strip("平方米")
                else:
                    area = "null"
                if len(lis[5].select("div")) != 0:
                    down_payment = lis[5].select("div")[1].text.strip().strip("万")
                else:
                    down_payment = "null"
                if len(lis[6].select("div")) != 0:
                    year = lis[6].select("div")[1].text.strip().strip("年")
                else:
                    year = "null"
                if len(lis[7].select("div")) != 0:
                    orientation = lis[7].select("div")[1].text
                else:
                    orientation = "null"
                if len(lis[8].select("div.houseInfo-content > span")) != 0:
                    monthly_payments = lis[8].select("div.houseInfo-content > span")[0].text.strip().strip("元")
                else:
                    monthly_payments = "null"
                if len(lis[9].select("div")) != 0:
                    property_type = lis[9].select("div")[1].text
                else:
                    property_type = "null"
                if len(lis[10].select("div")) != 0:
                    floor = lis[10].select("div")[1].text
                else:
                    floor = "null"
                if len(lis[11].select("div")) != 0:
                    decoration = lis[11].select("div")[1].text
                else:
                    decoration = "null"
                if len(lis[13].select("div")) != 0:
                    elevator = lis[13].select("div")[1].text
                else:
                    elevator = "null"
                if len(lis[15].select("div")) != 0:
                    house_property = lis[15].select("div")[1].text
                else:
                    house_property = "null"
            else:
                community = "null"
                house_type = "null"
                unit_price = "null"
                address = "null"
                area = "null"
                down_payment = "null"
                year = "null"
                orientation = "null"
                monthly_payments = "null"
                property_type = "null"
                floor = "null"
                decoration = "null"
                elevator = "null"
                house_property = "null"

            house_info = {
                "价格": price,
                "小区": community,
                "房屋户型": house_type,
                "房屋单价": unit_price,
                "所在位置": address,
                "建筑面积": area,
                "参考首付": down_payment,
                "建造年代": year,
                "房屋朝向": orientation,
                "参考月供": monthly_payments,
                "房屋类型": property_type,
                "所在楼层": floor,
                "装修程度": decoration,
                "配套电梯": elevator,
                "产权性质": house_property
            }
            print(house_info)
            self.save_data([value for value in house_info.values()])

    @staticmethod
    def save_data(data):
        header = ["价格（万）", "小区", "房屋户型", "房屋单价（元/m²）", "所在位置", "建筑面积（平方米）", "参考首付（万）", "建造年代（年）", "房屋朝向", "参考月供",
                  "房屋类型", "所在楼层", "装修程度", "配套电梯", "产权性质"]
        # 编码格式设置为 utf-8-sig 可以防止写入中文时产生乱码
        with open(r"results.csv", "a", encoding="utf-8-sig", newline="") as f1:
            writer = csv.writer(f1)
            with open(r"results.csv", "r", encoding="utf-8", newline="") as f2:
                rows = csv.reader(f2)
                # 判断文件中是否存在表头，如果存在就只写入数据，如果不存在则先写入表头再写入数据
                if not [row for row in rows]:
                    writer.writerow(header)
                    writer.writerow(data)
                else:
                    writer.writerow(data)

    def run(self):
        print("============从文本获取代理============")
        self.add_proxies()
        print("=============代理获取完毕============")
        # print(self.proxies)
        start_page = 1
        end_page = input("请输入您想爬取的页数，输入后请回车：")
        if end_page == "":
            print("您没有输入页数，程序将自动获取最大的页数，请稍等片刻")
            print("=================================================")
            end_page = self.get_max_page_number()
            print("程序获取到的最大页数为：", end_page)

        for page in range(start_page, int(end_page) + 1):
            print("============正在爬取第 %s 页数据============" % page)
            url = self.url.format(str(page))
            home_page = self.get_home_page(url)
            for detail_url in self.get_secondary_url(home_page):
                # print(detail_url)
                self.get_house_info(detail_url)
                time.sleep(random.randint(3, 5))  # 限制爬取速度
            print("============第 %s 页数据爬取完成============" % page)
        time.sleep(random.randint(10, 15))    # 限制爬取速度


if __name__ == "__main__":
    anjuke = Anjuke()
    t = threading.Thread(target=anjuke.run, args=())
    t.start()
    t.join()
