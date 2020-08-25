# 天气查询助手

## 项目结构

.  
├── README.md  
├── api  
│   ├── __init__.py  
│   └── gw.py  
├── assets  
│   ├── search.png  
│   └── weather.ico  
├── demo.py  
└── ui  
    ├── MainWindow.py  
    ├── MainWindow.ui  
    └── __init__.py  

`README.md`: 项目描述文件  
`api`: 获取天气信息的接口  
`assets`: 图标  
`demo.py`: 主程序  
`ui`: qt-designer 界面文件

## 第三方库依赖

`requests`
`BeautifulSoup`
`matplotlib`
`PyQt5`

## 运行

在终端运行命令：

```bash
python demo.py
```

## 效果

<center>
<img src="screenshots/s1.png" width="300" />
<img src="screenshots/s2.png" width="300" />
</center>

## 实现过程

后面再慢慢补吧

## 还需改进的地方

- [ ]  ​	没有写获取连续 7 天数据的接口
- [ ]  ​	使用 pyinstaller 打包项目时文件太大（180 M），故没有上传
- [ ]  ​    窗口中显示的图片白边太多、曲线没有添加数据标签、纵轴温度的刻度没有细分
