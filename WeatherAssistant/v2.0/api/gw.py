import requests
from bs4 import BeautifulSoup
import time
import json
import re
from pyecharts.charts import Line, Scatter
from pyecharts.globals import ThemeType
from pyecharts import options as opts


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
    text_ = "温度：{}\n风向：{}\n风速：{}\n湿度：{}\n天气：{}\n能见度：{}\n降雨：{}\n空气质量：{}\n日期：{}\n更新时间：{}"\
        .format(temp, wd, ws, sd, weather, njd, rain, aqi, date_, time_)
    # print(text_)
    return text_


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
    text_ = "{}\n天气：{}\n温度：{}\n风速：{}\n\n{}\n天气：{}\n温度：{}\n风速：{}"\
        .format(type1, weather1, temp1, ws1, type2, weather2, temp2, ws2)
    # print(text_)
    return text_


def plot_1d_weather(cip):
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
    weather_list = []
    for i in range(len(data)):
        time_ = data[i].split(",")[0]
        wind = data[i].split(",")[2]
        temp = data[i].split(",")[3]
        time_list.append(time_)
        weather_list.append(wind)
        temp_list.append(temp)
    # time_list = [re.findall("\d+", i)[0] + "-" + re.findall("\d+", i)[1] for i in time_list]
    time_list = time_list[:-1]
    temp_list = [int(i.strip("℃")) for i in temp_list][:-1]
    weather_list = weather_list[:-1]

    line = Line(init_opts=opts.InitOpts(width="450px", height="170px", theme=ThemeType.MACARONS))
    # line = Line(init_opts=opts.InitOpts(width="1000px", height="500px", theme=ThemeType.MACARONS))
    line.add_xaxis(xaxis_data=time_list)
    line.add_yaxis(
        series_name="",
        y_axis=temp_list,
        symbol_size=8,
        is_hover_animation=False
    )
    line.set_global_opts(
        title_opts=opts.TitleOpts(
            subtitle="数据来源于中国天气网",
            # pos_left="10px",
            pos_left="center",
            pos_top="-5px"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=True,
            axislabel_opts=opts.LabelOpts(
                rotate=30,
                font_size=12
            ),
            axistick_opts=opts.AxisTickOpts(is_align_with_label=False)
        ),
        yaxis_opts=opts.AxisOpts(
            # is_scale=False,
            min_=min(temp_list)-10,
            max_=max(temp_list)+2,
            interval=5,
            name="温度(°C)",
            name_location="center",
            # name_gap=25,
            name_gap=5,
            name_textstyle_opts=opts.TextStyleOpts(
                font_size=13,
                color="black"
            ),
            type_="value",
            axislabel_opts=opts.LabelOpts(
                font_size=12,
                is_show=False
            ),
            # axistick_opts=opts.AxisTickOpts(length=5)
            axistick_opts=opts.AxisTickOpts(length=0)
        ),
    )
    line.set_series_opts(
        label_opts=opts.LabelOpts(
            font_size=15,
            position="bottom",
            color="#f68227"
        ),
        linestyle_opts=opts.LineStyleOpts(width=2.5),
        markpoint_opts=opts.MarkPointOpts(
            symbol_size=1,
            data=[
                opts.MarkPointItem(name="天气", coord=[time_list[i], temp_list[i]], value=weather_list[i]) for i in range(len(time_list))
            ],
            label_opts=opts.LabelOpts(
                color="black",
                font_size=14,
                distance=10
            )
        )
    )
    line.render("time-temp-curve.html")


def plot_7d_weather(cip):
    url = "http://www.weather.com.cn/weather/{}.shtml".format(cip)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    html = response.text

    # 解析数据
    soup = BeautifulSoup(html, "lxml")
    lis = soup.select("div.c7d > ul > li")
    date_list = []
    weather_list = []
    lowest_temp_list = []
    highest_temp_list = []
    for li in lis:
        date_ = re.findall("(.*?)（.*?）", li.select("h1")[0].text)[0]
        if len(date_) == 2:
            date_ = "0" + date_
        which_day = re.findall(".*?（(.*?)）", li.select("h1")[0].text)[0]
        weather = li.select("p")[0].text
        temp = li.select("p")[1].text.strip().replace("℃", "")
        if "/" in temp:
            highest_temp = temp.split("/")[0]
            lowest_temp = temp.split("/")[1]
        else:
            highest_temp = temp
            lowest_temp = temp
        date_list.append(f"{date_}\n({which_day})")
        weather_list.append(weather)
        lowest_temp_list.append(int(lowest_temp))
        highest_temp_list.append(int(highest_temp))

    line = Line(init_opts=opts.InitOpts(width="450px", height="170px", theme=ThemeType.MACARONS))
    line.add_xaxis(
        xaxis_data=date_list
    )
    line.add_yaxis(
        series_name="最高温度",
        y_axis=highest_temp_list,
        symbol_size=8,
        is_hover_animation=False,
        label_opts=opts.LabelOpts(font_size=15)
    )
    line.add_yaxis(
        series_name="最低温度",
        y_axis=lowest_temp_list,
        symbol_size=8,
        is_hover_animation=False,
        label_opts=opts.LabelOpts(
            position="bottom",
            font_size=15
        )
    )
    line.set_global_opts(
        title_opts=opts.TitleOpts(
            # subtitle="数据来源于中国天气网",
            # pos_top="-5px"
        ),
        legend_opts=opts.LegendOpts(pos_right="30px"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axislabel_opts=opts.LabelOpts(font_size=13)
        ),
        yaxis_opts=opts.AxisOpts(
            # is_scale=True,
            min_=min(lowest_temp_list)-10 if min(lowest_temp_list)-10 > 0 else 0,
            max_=max(highest_temp_list)+5,
            interval=10,
            name="温度(°C)",
            name_location="center",
            # name_gap=25,
            name_gap=5,
            name_textstyle_opts=opts.TextStyleOpts(
                font_size=13,
                color="black"
            ),
            type_="value",
            axislabel_opts=opts.LabelOpts(is_show=False),
            # axistick_opts=opts.AxisTickOpts(length=5)
            axistick_opts=opts.AxisTickOpts(length=0)
        )
    )
    line.set_series_opts(
        linestyle_opts=opts.LineStyleOpts(width=2.5),
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(coord=[z[0], z[1]], value=z[2]) for z in zip(date_list, highest_temp_list, weather_list)],
            symbol_size=1,
            label_opts=opts.LabelOpts(
                color="black",
                rotate=25,
                distance=28,
                font_size=11
            )
        )
    )
    line.render("time-temp-curve.html")


if __name__ == "__main__":
    city_name = "哈尔滨"
    # city_name = input("请输入您想查询的城市：")
    city_ip = get_city_ip(city_name)
    # get_base_weather(city_ip)
    # get_additional_weather(city_ip)
    # plot_1d_weather(city_ip)
    plot_7d_weather(city_ip)