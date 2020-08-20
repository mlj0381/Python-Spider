#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function:
    爬取电视剧《以家人之名》的评论
Author:
    leishufei
"""
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import csv


def get_video_id():
    """
    获取每一集视频的 id
    :return: id 列表
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.mgtv.com/b/333900/9578912.html?cxid=9571sxdjy")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.episode-items.clearfix")))
    # print(driver.page_source)
    lis = driver.find_elements(By.CSS_SELECTOR, "ul.episode-items.clearfix > li")
    ids = []
    for li in lis:
        all_ = li.find_elements(By.CSS_SELECTOR, "*")  # 获取父节点下的所有子节点
        # 排除掉预告片或者需要 VIP 才能看的视频的 id
        if len(all_) == 1:
            ids.append(li.get_attribute("data-vid"))
    # print(ids)
    return ids


def get_comments(vid, page):
    """
    获取评论内容
    :param vid: 视频 id
    :param page: 评论的页数
    :return:
    """
    base_url = "https://comment.mgtv.com/v4/comment/getCommentList"
    params = {
        "page": page,
        "subjectType": "hunantv2014",
        "subjectId": vid,
        "callback": "jQuery18202275527241633104_1597910771827",
        "_support": "10000000",
        "_": time.time() * 1000
    }
    # url = "https://comment.mgtv.com/v4/comment/getCommentList?page=70&subjectType=hunantv2014&subjectId=9578912&callback=jQuery18202275527241633104_1597910771827&_support=10000000&_=1597910775464"
    response = requests.get(base_url, params=params)
    # print(response.text)
    # 正则表达式提取评论内容
    comments = re.findall('"content":"(.*?)"', response.text)
    if len(comments) != 0:
        comments = [[i] for i in comments]
        # print(comments)
        save_comments(comments)
    

def save_comments(comments):
    """
    将评论内容存储到 csv 文件中
    :param comments: 评论内容
    :return:
    """
    if not os.path.exists("result/"):
        os.mkdir("result/")
    # utf-8-sig 保证能将中文正确写入到 csv 文件
    with open("result/comments.csv", "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(comments)


if __name__ == "__main__":
    # video_ids = ['9578912', '9578925', '9589845', '9589868', '9599379', '9599455', '9608463', '9608488', '9617493', '9624745', '9630948', '9630963', '9638581', '9638597']
    video_ids = get_video_id()
    for index, id_ in enumerate(video_ids):
        for page in range(70, 100):
            print("[INFO] 正在获取第 %s 集第 %s 页评论评论" % (index + 1, page))
            get_comments(id_, page)
            time.sleep(2)