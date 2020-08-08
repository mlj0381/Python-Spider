#!usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue


class Proxy(object):

    """初始化参数"""
    def __init__(self):
        self.url = "https://www.kuaidaili.com/free/inha/"  # 代理网址
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54",
            "Referer": "https://www.kuaidaili.com/",
            "Host": "www.kuaidaili.com"
        }
        self.all_proxies = []
        self.available_proxies = []
        self.available_proxies_queue = Queue()

    """获取网页上所列出来的代理，这里只爬取第一页的代理"""
    def get_proxies(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        trs = soup.select("table.table.table-bordered.table-striped > tbody tr")
        for each in trs:
            tds = each.select("td")
            ip_address = tds[0].text.strip()
            ip_port = tds[1].text.strip()
            ip_type = "http" if tds[3].text.strip() == "HTTP" else "https"
            proxy = ip_type + "://" + ip_address + ":" + ip_port
            self.all_proxies.append(proxy)

    """获取有效的代理"""
    def get_available_proxies(self):
        self.get_proxies()
        # 创建线程，加快检查代理有效性的速度
        threads = []
        for each in self.all_proxies:
            t = threading.Thread(target=self.check, args=(each, ))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        while not self.available_proxies_queue.empty():
            proxy = self.available_proxies_queue.get()
            self.available_proxies.append(proxy)

        for each in self.available_proxies:
            self.save_proxies(each)

    """检查获取的代理是否有效"""
    def check(self, proxy):
        proxies = {"https": proxy}
        response = requests.get("http://icanhazip.com", proxies=proxies)
        if response.status_code == 200:
            print("测试成功 -> ", proxy)
            self.available_proxies_queue.put(proxy)
        else:
            print("测试失败 -> ", proxy)

    """保存有效的代理"""
    @staticmethod
    def save_proxies(proxy):
        with open(r"proxies.txt", "a", encoding="utf-8") as f:
            f.write(proxy + "\n")

    def run(self):
        self.get_available_proxies()


if __name__ == "__main__":
    proxy = Proxy()
    proxy.run()
