import requests
from bs4 import BeautifulSoup
import time
import json
import re
# import matplotlib.pyplot as plt


headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59",
    "Referer": "http://www.weather.com.cn/weather1d/101271201.shtml"  # 不加这个会出错（403 错误码）
}


def get_city_ip(cname):
    timestamp = int(time.time() * 1000)
    url = "http://toy1.weather.com.cn/search?cityname={}&callback=success_jsonpCallback&_={}".format(cname, timestamp)
    response = requests.get(url, headers=headers)
    city_ip = re.findall(r"\d{9}", response.text)[0]
    # print(city_ip)
    return city_ip


def get_base_weather(cip):
    timestamp = int(time.time() * 1000)
    # 异步加载的数据
    url = "http://d1.weather.com.cn/sk_2d/{}.html?_={}".format(cip, timestamp)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    content = response.text
    # print(content)

    # 解析数据
    # 温度
    temp = re.findall('"temp":"(.*?)"', content)[0] + "°C"
    # 风向
    wd = re.findall('"WD":"(.*?)"', content)[0]
    # 风速
    ws = re.findall('"WS":"(.*?)"', content)[0]
    # 湿度
    sd = re.findall('"SD":"(.*?)"', content)[0]
    # 时间
    time_ = re.findall('"time":"(.*?)"', content)[0]
    # 天气状况
    weather = re.findall('"weather":"(.*?)"', content)[0]
    # 能见度
    njd = re.findall('"njd":"(.*?)"', content)[0]
    # 降雨
    rain = re.findall('"rain":"(.*?)"', content)[0]
    # 空气质量
    aqi = re.findall('"aqi":"(.*?)"', content)[0]
    # 日期
    date_ = re.findall('"date":"(.*?)"', content)[0]
    # print("温度：{}\n风向：{}\n风速：{}\n湿度：{}\n天气：{}\n能见度：{}\n降雨：{}\n空气质量：{}\n日期：{}\n更新时间：{}"
    #       .format(temp, wd, ws, sd, weather, njd, rain, aqi, date_, time_))
    return "温度：{}\n风向：{}\n风速：{}\n湿度：{}\n天气：{}\n能见度：{}\n降雨：{}\n空气质量：{}\n日期：{}\n更新时间：{}".format(
        temp, wd, ws, sd, weather, njd, rain, aqi, date_, time_)


def get_additional_weather(cip):
    # 常规数据
    url = "http://www.weather.com.cn/weather1d/{}.shtml#input".format(cip)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    html = response.text
    # print(response.text)
    soup = BeautifulSoup(html, "lxml")

    # 第一列数据
    li1 = soup.select("div.t > ul.clearfix > li")[0]
    # 白天 or 夜间
    type1 = li1.select("h1")[0].text.strip()
    # 天气状况
    weather1 = li1.select("p.wea")[0].text.strip()
    # 温度
    temp1 = li1.select("p.tem")[0].text.strip()
    # 风速
    ws1 = li1.select("p.win > span")[0].text.strip()

    # 第二列数据
    li2 = soup.select("div.t > ul.clearfix > li")[1]
    type2 = li2.select("h1")[0].text.strip()
    weather2 = li2.select("p.wea")[0].text.strip()
    temp2 = li2.select("p.tem")[0].text.strip()
    ws2 = li2.select("p.win > span")[0].text.strip()

    # print("\n{}\n天气：{}\n温度：{}\n风速：{}\n{}\n天气：{}\n温度：{}\n风速：{}"
    #       .format(type1, weather1, temp1, ws1, type2, weather2, temp2, ws2))
    return "{}\n天气：{}\n温度：{}\n风速：{}\n\n{}\n天气：{}\n温度：{}\n风速：{}".format(
        type1, weather1, temp1, ws1, type2, weather2, temp2, ws2)


def get_1d_weather(cip):
    url = "http://www.weather.com.cn/weather1d/{}.shtml#input".format(cip)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    html = response.text
    # print(response.text)
    soup = BeautifulSoup(html, "lxml")
    script = soup.select("div#today > script")[1].text.strip().strip("var hour3data=")
    json_ = json.loads(script)
    # print(json_)
    data = json_["1d"]
    # print(data)
    time_list = []
    temp_list = []
    for i in range(len(data)):
        time_ = data[i].split(",")[0]
        temp = data[i].split(",")[3]
        time_list.append(time_)
        temp_list.append(temp)
    time_list = [re.findall("\d+", i)[0] + "-" + re.findall("\d+", i)[1] for i in time_list]
    temp_list = [int(i.strip("℃")) for i in temp_list]
    # plt.figure(figsize=(8, 4))
    # plt.plot(time_list, temp_list, "s-")
    # plt.xlabel("time (day-hour)")
    # plt.ylabel("temperature (°C)")
    # plt.show()
    return [time_list, temp_list]


def get_7d_weather():
    pass


if __name__ == "__main__":
    # city_name = "北京"
    city_name = input("请输入您想查询的城市：")
    city_ip = get_city_ip(city_name)
    get_base_weather(city_ip)
    get_additional_weather(city_ip)
    get_1d_weather(city_ip)
