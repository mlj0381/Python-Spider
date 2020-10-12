"""
Function:
    Download wallpaper of Bing
Author:
    leishufei
"""
import re
import os
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool


class BingWallpaperSpider(object):
    def __init__(self):
        self.url = "https://bing.lylares.com/"
        self.api_url = "https://bing.lylares.com/web/api"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38",
            "Referer": "https://bing.lylares.com/",
            "Cookie": ""
        }
        self.post_data = {
            "append": "list-home",
            # "paged": 1,  # page 通过 update() 方法进行传递
            "token": "",
            "action": "ajax_load_posts",
            "page": "home"
        }
        self.update_()

    def update_(self):
        """
        更新 headers 和 post_data
        :return: none
        """
        response = requests.get(self.url)
        cookie = "PHPSESSID" + "=" + response.cookies["PHPSESSID"]
        soup = BeautifulSoup(response.text, "lxml")
        load_more_button = soup.select(".container > nav > div > button")[0]
        token = load_more_button.get("data-token")
        self.headers.update({"Cookie": cookie})
        self.post_data.update({"token": token})

    def get_new_page(self, page):
        """
        通过 post 方法获取新页面
        :param page: 页数
        :return: 页面 html
        """
        self.post_data.update({"paged": page})
        response = requests.post(self.api_url, data=self.post_data, headers=self.headers)
        html = response.text
        return html

    def parse_page(self, page):
        """
        解析页面
        :param page: 页数
        :return: none
        """
        html = self.get_new_page(page)
        soup = BeautifulSoup(html, "lxml")
        divs = soup.select("div.list-item.custom-hover")
        for div in divs:
            title = div.select(".list-content > .list-body > a")[0].text.strip()
            # small_img_url = re.findall(".*?\((.*?)\)", div.select(".media.media-16x9 > a")[0].get("style"))[0]
            detailed_url = "https://bing.lylares.com/" + div.select(".media.media-16x9 > a")[0].get("href")
            large_img_url = self.get_large_picture_url(detailed_url)
            print("title:", title)
            print("img_url:", large_img_url)
            yield title, large_img_url

    def get_large_picture_url(self, detailed_url):
        """
        获取大图的下载链接
        :param detailed_url: 详情页的 url
        :return: 大图的下载链接
        """
        response = requests.get(detailed_url, headers=self.headers)
        regex = r"background-image: url\((.*?)\);"
        large_picture_url = re.search(regex, response.text).group(1)
        return large_picture_url

    def save_picture(self, page):
        """
        保存图片
        :param page: 页数
        :return: none
        """
        for title, img_url in self.parse_page(page):
            title = re.sub(r"[/\\.*?'\"<>]", "", title)
            with open("pics/" + title + ".jpg", "wb") as f:
                f.write(requests.get(img_url).content)

    def run(self):
        """
        运行函数
        :return: none
        """
        pages = [page for page in range(1, 100)]
        if not os.path.exists("pics/"):
            os.mkdir("pics/")
        pool = Pool(10)
        pool.map(self.save_picture, pages)
        pool.close()
        pool.join()


if __name__ == "__main__":
    spider = BingWallpaperSpider()
    spider.run()
