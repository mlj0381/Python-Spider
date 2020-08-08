# 安居客爬虫

## 1 文件说明

main.py：程序文件

proxies.txt：存储代理 IP 的文件，考虑到代理 IP 存活的时间并不长，你可以选择自己爬取代理 IP 并写入该文件，可以参考我的另一个爬虫项目：GetProxies（[地址在这里](https://github.com/leishufei/PythonProjects/tree/master/PythonSpiders/GetProxies )）

requirements.txt：程序运行所需要的第三方库

results.csv：程序获取到的一部分数据

screenshots：存放程序运行截图的文件夹

## 2 环境配置

```python
pip install -r requirements.txt
```

## 3 运行

```python
# 通过命令行进入 main.py 所在的文件夹
# 然后输入以下命令
python main.py
```

## 4 运行截图

![1](screenshots/1.png)

## 5 运行结果

程序运行完成后，会在 main.py 的同级目录下生成一个 results.csv 文件，里面包含爬取的数据。

## 6 欠缺的地方

即便是加了请求头和代理 IP，并且设置了访问间隔（time.sleep），在访问一段时间后仍然会被安居客反爬虫。现在越来越多的网站对爬虫进行了限制，因此反反爬虫这方面的知识以后还得不断的学习。后续会用程序获取的数据进行数据分析，把爬虫和数据分析结合起来。

PS：令我费解的是，不加访问间隔的程序被反爬虫的几率却远比加了访问间隔的程序低得多，此程序只是为了学习和交流，所以还是尽量设置上访问间隔，以免对服务器造成太大的负担。