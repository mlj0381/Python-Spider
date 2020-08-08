"""
selenium 爬取淘宝商品数据
"""
#!usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import parsel
import time
import re
import csv
import os


class TaobaoGoods(object):
    def __init__(self):
        self.login_url = "https://login.taobao.com/member/login.jhtml"
        self.home_page_url = "https://www.taobao.com"
        self.driver = webdriver.Chrome("src/chromedriver.exe")
        self.driver.set_page_load_timeout(5)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        """
        通过支付宝扫码方式登陆淘宝
        :return:
        """
        print("[INFO] 正在启动浏览器，准备登陆淘宝")
        try:
            self.driver.get(self.login_url)
        except TimeoutException:
            self.driver.execute_script('window.stop()')
        time.sleep(1)
        # 使用支付宝登陆方式
        login = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form >  div.login-blocks.sns-login-links > a.alipay-login"))
        )
        login.click()
        print("[INFO] 请使用支付宝扫码以进行登陆")
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#layout-center"))
            )
            print("[INFO] 登陆成功")
        except NoSuchElementException:
            print("[INFO] 登录失败")
            print("[INFO] 请在 5 秒后尝试重新登陆")
            time.sleep(5)
            self.login()

    def get_total_page_number(self, keyword):
        """
        获取指定商品关键词的搜索结果的最大页数
        :param keyword: 商品关键词
        :return: 搜索结果的最大页数
        """
        print("[INFO] 正在获取最大页数")
        try:
            self.driver.get(self.home_page_url)
            # 输入框
            _input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#q"))
            )
            # 确定按钮
            submit = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-search.tb-bg"))
            )
            _input.send_keys(keyword)
            time.sleep(1)
            submit.click()
            # 获取页数
            _text = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#mainsrp-pager > div > div > div > div.total"))
            ).text
            total_page_number = int(re.findall(r"(\d+)", _text)[0])
            return total_page_number
        except TimeoutException:
            self.get_total_page_number(keyword)

    def jump_to_next_page(self, page_number):
        """
        跳转到指定页
        :param page_number: 商品所在页
        :return:
        """
        print("[INFO] 跳转至第 %s 页" % page_number)
        try:
            # 页数输入框
            _input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#mainsrp-pager > div > div > div > div > input.input.J_Input"))
            )
            # 确定按钮
            submit = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div#mainsrp-pager > div > div > div > div > span.btn.J_Submit"))
            )
            _input.clear()
            _input.send_keys(str(page_number))
            time.sleep(1)
            submit.click()
        except TimeoutException:
            self.jump_to_next_page(page_number)

    def get_products_info(self, keyword):
        """
        获取商品数据
        :param keyword: 商品关键词
        :return:
        """
        print("[INFO] 正在获取商品信息")
        # 等待商品信息加载完成
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#mainsrp-itemlist > div > div > div.items"))
        )
        html = parsel.Selector(self.driver.page_source)

        goods_name = html.xpath('//div[@class="grid g-clearfix"]//img/@alt').extract()
        shop_name = html.xpath('//div[@class="grid g-clearfix"]//div[@class="row row-3 g-clearfix"]/div/a/span[2]/text()').extract()
        price = html.xpath('//div[@class="grid g-clearfix"]//div[@class="row row-1 g-clearfix"]/div/strong/text()').extract()
        purchase_num = html.xpath('//div[@class="grid g-clearfix"]//div[@class="row row-1 g-clearfix"]/div[2]/text()').extract()
        location = html.xpath('//div[@class="grid g-clearfix"]//div[@class="row row-3 g-clearfix"]/div[2]/text()').extract()

        if not os.path.exists("data/"):
            os.mkdir("data/")
        with open(r"data/result.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for i in range(len(goods_name)):
                writer.writerow([keyword, goods_name[i], shop_name[i], price[i], purchase_num[i], location[i]])

    def run(self):
        print("=========================START=========================")
        self.login()
        keyword_list = ["", ]  # 添加您想搜索的关键词
        for keyword in keyword_list:
            print("[INFO] 指定商品关键词---->%s" % keyword)
            total_page_number = self.get_total_page_number(keyword)
            for i in range(1, total_page_number + 1):
                self.jump_to_next_page(i)
                self.get_products_info(keyword)
                time.sleep(15)
        print("[INFO] 执行完毕，退出程序")
        print("=========================END=========================")
        self.driver.quit()


if __name__ == "__main__":
    taobao = TaobaoGoods()
    taobao.run()
