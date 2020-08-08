#!usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv


class WebsitesSpider(object):

    def __init__(self):
        self.url = "https://theporndude.com/zh"  # 只做学习交流用途，可不是传播那啥
        self.headers = {
            # 网站似乎没有反爬措施，不过还是加个 UA 好了
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }
        self.clist = []

    def get_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = response.text
            return html
        except Exception as e:
            raise e

    def get_category_list(self):
        html = self.get_page(self.url)
        soup = BeautifulSoup(html, "lxml")
        categories = soup.find(id="main_container").find_all("div", class_="category-header")

        for category in categories:
            url = "https://theporndude.com" + category.h2.a.get("href")
            name = category.h2.a.text.strip()
            self.clist.append(
                {
                    "类别名": name,
                    "链接": url
                }
            )

    def get_urls(self):
        self.get_category_list()  # 先将所有类别页面的链接添加到列表中，以备下面的调用
        for each in self.clist:
            category_name = each["类别名"]
            category_url = each["链接"]
            html = self.get_page(category_url)
            soup = BeautifulSoup(html, "lxml")
            contents = soup.find("div", class_="url_links_wrapper url_links_hover").find_all("div", class_="url_link_container")
            count = 0
            for each in contents:
                count += 1
                website_name = each.find("div", class_="url_link_title").a.text.split()[0]
                website_url = each.find("div", class_="url_link_title").a.get("data-site-link")
                self.save_to_csv([category_name, count, website_name, website_url])
                print("\r当前正在爬取<-%s->类别链接\t爬取进度：%.2f%%" % (category_name, count * 100 / 100), end="")

    def save_to_csv(self, data):
        header = ["类别名", "序号", "网站名", "链接"]
        # 防止写入中文时乱码
        with open(r"results.csv", "a", encoding="utf-8-sig", newline="") as f1:
            writer = csv.writer(f1)
            with open(r"results.csv", "r", encoding="utf-8") as f2:
                rows = csv.reader(f2)
                if not [row for row in rows]:
                    f1.writerow(header)
                    f1.writerow(data)
                else:
                    f1.writerow(data)

    def run():
        self.get_urls()


if __name__ == "__main__":
    spider = WebsitesSpider()
    spider.run()
