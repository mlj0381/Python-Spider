#!usr/bin/ env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import os
import time
from PIL import Image


class BaiduWenku(object):
    def __init__(self, url):
        # self.url = "https://wenku.baidu.com/view/005622f51611cc7931b765ce050876323112749d.html"  # 测试用
        self.url = url
        self.headers = {"user-agent": "Baiduspider"}  # 把请求头伪装成 Baiduspider

    @staticmethod
    def get_document_type(html):
        """获取文档类型"""
        # 很少写正则表达式，写起来还真费劲 $_$
        return re.findall(r"'docType'.*?'(.*?)'.*?", html, re.S)[0]

    def get_html(self):
        """获取页面"""
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        html = response.text
        return html

    @staticmethod
    def parse_doc(html):
        """解析页面，获取文本内容"""
        plist = []  # 定义列表，用于存储文本内容
        soup = BeautifulSoup(html, "lxml")
        plist.append(soup.title.string.strip("_百度文库"))  # 获取标题并去除百度文库的文字水印

        for div in soup.find_all("div", attrs={"class": "bd doc-reader"}):
            plist.extend(div.get_text().split("\n"))  # extend 可以一次性添加多个元素到列表中

        # # 去除 plist 中的空元素
        # while "" in plist:
        #     plist.remove("")
        #
        # # 去除空格或无意义字符
        # plist = [each.replace(" ", "") for each in plist]
        # plist = [each.replace("\x0c", "") for each in plist]
        return plist

    @staticmethod
    def save_to_doc(content):
        """将本文内容保存到 doc 文档中"""
        timestamp = str(int(time.time()))
        file_path = "results/doc/" + timestamp + "/"
        os.makedirs(file_path)
        with open(file_path + content[0] + ".doc", "w", encoding="utf-8") as f:
            for each in content:
                f.write(each)
                f.write("\n")

    def start_driver(self):
        """启动 webdriver"""
        # driver = webdriver.Chrome(r"src/chromedriver.exe")  # 如果没有将 webdriver.exe 添加到环境变量，就需要引用外部程序
        driver = webdriver.Chrome()  # 如果已经将 webdriver.exe 添加到环境变量了，就可以用这种方式
        # driver.maximize_window()  # 最大化窗口
        driver.get(self.url)
        return driver

    @staticmethod
    def get_total_page_number(driver):
        """获取页面的总页数"""
        pattern = re.compile(r'<span class="page-count">/(.*?)</span>')
        total_page_number = int(re.findall(pattern, driver.page_source)[0])  # 正则表达式获取总页数
        return total_page_number

    def parse_pdf(self, driver):
        """解析页面，获取 pdf 图片链接"""
        pic_urls = []  # 定义列表，用于存放图片的 url
        # 找到“继续阅读”按钮
        button = driver.find_element_by_xpath('//*[@id="html-reader-go-more"]/div[2]/div[1]/span')
        # 点击“继续阅读”按钮
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        # 获取总页数
        total_page_number = self.get_total_page_number(driver)
        # 找到输入框
        _input = driver.find_element_by_css_selector("input.page-input")
        time.sleep(1)
        for page in range(2, total_page_number):
            _input.clear()  # 先清除已有的内容
            _input.send_keys(f"{page}")  # 输入页数
            _input.send_keys(Keys.ENTER)  # 按下回车键
            time.sleep(0.2)
            divs = driver.find_elements_by_css_selector("div.reader-pic-item")
            if page == 2:
                for i in range(3):
                    print(">>> 正在爬取第 %d 页内容" % (i + 1))
                    url = re.findall('url[(]"(.*?)"[)]', divs[i].get_attribute("style"))  # 获取标签 style 属性中的 URL
                    pic_urls.append(url)
            else:
                print(">>> 正在爬取第 %d 页内容" % (page + 1))
                url = re.findall('url[(]"(.*?)"[)]', divs[2].get_attribute("style"))
                pic_urls.append(url)
            # time.sleep(1)
        driver.quit()
        return pic_urls

    def parse_ppt(self, driver):
        """解析页面，获取 ppt 图片链接"""
        # 获取 ppt 和获取 pdf 的逻辑是一样的，不过在获取链接的时候有一点改变，详情见 for 循环中的 if else 处
        pic_urls = []  # 定义列表，用于存放图片的 URL
        # 找到“继续阅读”按钮
        button = driver.find_element_by_xpath('//*[@id="html-reader-go-more"]/div[2]/div[1]/span')
        # 点击“继续阅读”按钮
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        # 获取总页数
        total_page_number = self.get_total_page_number(driver)
        # 找到输入框
        _input = driver.find_element_by_css_selector("input.page-input")
        time.sleep(1)
        for page in range(2, total_page_number):
            _input.clear()  # 先清除已有的内容
            _input.send_keys(f"{page}")  # 输入页数
            _input.send_keys(Keys.ENTER)  # 按下回车键
            time.sleep(0.2)
            divs = driver.find_elements_by_xpath('//div[@class="ppt-image-wrap"]/img')
            if page == 2:
                for i in range(3):
                    print(">>> 正在爬取第 %d 页内容" % (i + 1))
                    url = divs[i].get_attribute("src")  # 获取图片 url
                    pic_urls.append(url)
            else:
                print(">>> 正在爬取第 %d 页内容" % (page + 1))
                url = divs[page].get_attribute("src")
                pic_urls.append(url)
            # time.sleep(1)
        driver.quit()
        return pic_urls

    def save_to_pdf(self, urls, doc_type):
        """访问、下载、保存图片并打印为 pdf文件"""
        timestamp = str(int(time.time()))
        if doc_type == "pdf":
            file_path = "results/pdf/" + timestamp + "/"
        else:
            file_path = "results/ppt/" + timestamp + "/"
        os.makedirs(file_path)  # 自动创建目录，不用判断目录是否已经存在
        for index, url in enumerate(urls):
            with open(file_path + str(index + 1) + ".jpg", "wb") as f:
                f.write(requests.get(url, headers=self.headers).content)
        # 转换为 pdf 文件
        files = os.listdir(file_path)
        jpg_files = [file for file in files]
        jpg_files = [int(each.split(".")[0]) for each in jpg_files]  # 去掉后缀名，为排序做准备
        jpg_files.sort()  # 按从小到大的顺序排序
        jpg_files = [file_path + str(each) + ".jpg" for each in jpg_files]  # 重选添加后缀名，并添加上前面的相对路径
        output = Image.open(jpg_files[0])
        jpg_files.pop(0)
        sources = []
        for each in jpg_files:
            img = Image.open(each)
            img.convert("P")
            sources.append(img)
        output.save(file_path + "result.pdf", "PDF", save_all=True, append_images=sources)
        sources.clear()  # 清除列表数据

    def run(self):
        """运行函数"""
        html = self.get_html()
        print(">>> 分析目标文档格式")
        doc_type = self.get_document_type(html)
        if doc_type == "doc":
            # 如果文档类型为 doc，则用 requests 进行抓取
            print(">>> 目标文档为 doc 格式")
            print(">>> 开始抓取内容")
            content = self.parse_doc(html)
            print(">>> 内容抓取完毕")
            print(">>> 写入文档内容")
            self.save_to_doc(content)
            print(">>> 写入完成")
        elif doc_type == "pdf":
            # 如果文档类型为 pdf，则用 selenium 进行抓取
            print(">>> 目标文档为 pdf 格式")
            print(">>> 开始抓取内容")
            driver = self.start_driver()
            pic_urls = self.parse_pdf(driver)
            print(">>> 内容抓取完毕")
            print(">>> 写入文档内容")
            self.save_to_pdf(pic_urls, doc_type)
            print(">>> 写入完成")
        elif doc_type == "ppt":
            # 如果文档类型为 pdf，也用 selenium 进行抓取
            print(">>> 目标文档为 ppt 格式")
            print(">>> 开始抓取内容")
            driver = self.start_driver()
            pic_urls = self.parse_ppt(driver)
            print(">>> 内容抓取完毕")
            print(">>> 写入文档内容")
            self.save_to_pdf(pic_urls, doc_type)
            print(">>> 写入完成")
        else:
            print("抱歉，目标文档暂时无法爬取！")


if __name__ == "__main__":
    doc_url = ""
    wenku = BaiduWenku(doc_url)
    wenku.run()
