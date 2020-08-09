"""
Function:
    获取穷游网的景点信息，并将数据写入 csv 文档
Author:
    leishufei
"""
import requests
import time
from bs4 import BeautifulSoup
import re
import csv


class Travel(object):
    def __init__(self):
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
            "Origin": "https://place.qyer.com"
        }

    def get_city_urls(self, pageUrl):
        resp = requests.get(pageUrl, headers=self.headers, timeout=20)
        html = resp.text
        city_content = re.findall(r"<ul class=\"plcCitylist\">(.*?)</ul>", html, re.S)[0]
        city_urls = re.findall(r"<li.*?>.*?<h3 .*?>.*?href=\"(.*?)\".*?</h3>.*?</li>", city_content, re.S)

        for city_url in city_urls:
            yield "https:" + city_url

    def get_items(self, city_url):
        items = ["sight", "food", "shopping", "activity", "mguide"]
        for item in items:
            url = city_url + item
            resp = requests.get(url, headers=self.headers, timeout=20)
            html = resp.text
            soup = BeautifulSoup(html, "lxml")
            item_list = soup.find("ul", class_="plcPoiList").find_all("li", class_="clearfix")
            for i in item_list:
                detail_url = "https:" + i.find("h3", class_="title fontYaHei").a.get("href")
                try:
                    resp = requests.get(detail_url,headers=self.headers, timeout=20)
                    html = resp.text
                    soup = BeautifulSoup(html, "lxml")
                    item_name = soup.select("div.compo-large-tit > .qyWrap > .poi-largeTit h1")[1].text.strip()
                    item_rank = soup.select("div.compo-main > div.poi-placeinfo.clearfix > div.infos > div:nth-child(1) > p.points > span.number")[0].text.strip()
                    address = soup.select("ul.poi-tips li")[0].select("div.content p")[0].text.strip("(查看地图)")
                    print("景点名称：{}\n评分：{}\n地址：{}\n".format(item_name, item_rank, address))
                    self.save_to_csv([item_name, item_rank, address])
                except:
                    pass

    def save_to_csv(self, content):
        headers = ["景点名称", "评分", "地址"]
        with open(r"data.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)

            with open(r"data.csv", "r", encoding="utf-8", newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    writer.writerow(headers)
                    writer.writerow(content)
                else:
                    writer.writerow(content)

    def run(self):
        base_url = "https://place.qyer.com/china/citylist-0-0-"
        urls = [base_url + str(i) for i in range(1, 10)]
        for url in urls:
            for i in self.get_city_urls(url):
                self.get_items(i)
            time.sleep(10)
        

if __name__ == "__main__":
    travel = Travel()
    travel.run()
