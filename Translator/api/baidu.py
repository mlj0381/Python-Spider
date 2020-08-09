import requests
import js2py


class BaiduTranslator(object):
    def __init__(self):
        self.url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
            # 必须加 Cookie，否则会出错
            "Cookie": ""
        }
        self.data = {
            "from": None,  # 原文语言
            "to": None,  # 译文语言
            "query": None,  # 待翻译内容
            "transtype": "realtime",
            "simple_means_flag": 3,
            "sign": None,  # 加密参数
            "token": "86a6cdd72051161d3e2015316343e721",
            "domain": "common"
        }

    def get_translation(self, content):
        """
        获取翻译内容
        :param content: 待翻译的原文
        :return: 译文
        """
        languages = ["zh", "en"]
        if self.is_Chinese(content):
            source_language, target_language = languages
        else:
            source_language, target_language = reversed(languages)
        self.data["from"] = source_language
        self.data["to"] = target_language
        self.data["query"] = content
        self.data["sign"] = self.get_sign(content)

        response = requests.post(self.url, data=self.data, headers=self.headers)
        translation = response.json()["trans_result"]["data"][0]["dst"]
        return translation

    def is_Chinese(self, content):
        """
        判断待翻译内容是否含有中文
        :param content: 待翻译内容
        :return: True or False
        """
        for w in content:
            if "\u4e00" <= w <= "\u9fa5":
                return True
        return False

    def get_sign(self, content):
        """
        获取 js 加密后的参数 sign
        :param content: 待翻译的文本
        :return: 加密的参数 sign
        """
        js_code = open("./javascript/baidu.js", "r", encoding="utf-8").read()
        eval_js = js2py.EvalJs()
        eval_js.execute(js_code)
        sign = eval_js.e(content)
        # print(sign)
        return sign

    def run(self):
        content = input("请输入您想翻译的内容：")
        translation = self.get_translation(content)
        print("原文：{}\n译文：{}".format(content, translation))


if __name__ == "__main__":
    baidu = BaiduTranslator()
    baidu.run()
