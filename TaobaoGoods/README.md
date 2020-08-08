# 淘宝商品爬虫

### 项目结构

|--项目文件

 	  |--src

	  |--main.py

	  |--reqiurements.txt

  	  |--README.md

`src`: 额外支撑程序

`main.py`: 主程序

`reqiurements.txt`: 程序所依赖的第三方库

`README.md`: 项目描述文件

###  准备工作

* 程序依赖于`Chrome`浏览器，请确保您已安装`Chrome`浏览器
* 此项目的`src`目录下已经有了与`84.0.4147`版本`Chrome`浏览器对应的`chromedriver`，如果您的`Chrome`浏览器为此版本（如何查看`Chrome`版本？在`Chrome`地址栏输入`Chrome://version`，第一行即为浏览器版本），则可以使用该`chromedriver`
* 如果您需要另下载`chromedriver`，可以参考这篇博客：[https://blog.csdn.net/weixin_42508908/article/details/85986029](https://blog.csdn.net/weixin_42508908/article/details/85986029)（不需要配置环境变量），然后将其放在`src`目录下
* 在主程序中的`keyword_list`列表（`137`行左右）中添加您想搜索的商品关键词

### 实现思路

```flow
st=>start: 开始
e=>end: 结束
op1=>operation: 启动浏览器
op2=>operation: 访问登陆链接
op3=>operation: 点击支付宝登录
op4=>operation: 支付宝扫码登录
op5=>operation: 重新登录
op6=>operation: 访问淘宝首页
op7=>operation: 传入指定商品名并搜索
op8=>operation: 获取搜索结果的最大页数
op9=>operation: 跳转至指定页数
op10=>operation: 获取商品信息
op11=>operation: 写入 csv 文件
cond1=>condition: 是否登录成功？
cond2=>condition: 指定页数是否在最大页数范围内？
st->op1->op2->op3->op4->cond1
cond1(yes)->op6->op7->op8->cond2
cond1(no)->op5->op2
cond2(yes)->op9->op10->op11(left)->cond2
cond2(no)->e
```

### 写在最后

* 为什么要用支付宝扫码登录这样相对麻烦的方法？

  因为在采用用户名、密码的方式进行登录时，测试发现会出现验证滑块，这个解决倒也不难，网上有很多现成的解决方法，但是手动滑动滑块也验证不了，具体的原因我也搞不明白，所以干脆用扫码登录的方式。

### 参考链接

[1]  https://mp.weixin.qq.com/s/QvN-vBQbQGwsZifrLR5Thg 
