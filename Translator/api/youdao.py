import requests
import js2py


class YoudaoTranslator(object):
    def __init__(self):
        # self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        # 带上 _o 会出错，去掉就可以正常获取内容了，表示很不解
        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
            # Cookie 可加可不加
        }
        self.data = {
            "i": None,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": None,
            "sign": None,
            "lts": None,
            "bv": None,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }

    def get_translation(self, content):
        """
        获取翻译内容
        :param content: 翻译前的内容
        :return: 翻译后的内容
        """
        params = self.get_params(content)
        self.data["i"] = content
        self.data["salt"] = params["salt"]
        self.data["sign"] = params["sign"]
        self.data["lts"] = params["ts"]
        self.data["bv"] = params["bv"]
        response = requests.post(self.url, data=self.data, headers=self.headers)
        translation = response.json()["translateResult"][0][0]["tgt"]
        return translation

    def get_params(self, content):
        """
        获取表单中的加密参数。
        也可以通过 python 的 md5 生成加密参数，不过既然谷歌和百度都是采用执行 js 的方法，有道也没有必要搞特殊了
        :param content: 要翻译的内容
        :return: salt, sign, ts, bv 四个参数
        """
        js_code = open("./javascript/youdao.js", "r", encoding="utf-8").read()
        eval_js = js2py.EvalJs()
        eval_js.execute(js_code)
        params = eval_js.x(content, self.headers["User-agent"])
        return params

    def run(self):
        content = input("请输入你想翻译的内容：")
        translation = self.get_translation(content)
        print("原文：{}\n译文：{}\n".format(content, translation))


if __name__ == "__main__":
    youdao = YoudaoTranslator()
    youdao.run()
