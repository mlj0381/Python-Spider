import requests
import js2py


class BaiduTranslator(object):
    def __init__(self):
        self.url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
            # 必须加 Cookie，否则会出错
            "Cookie": "BAIDUID=AAC94C02DA58A6E1A6FC363502E36DCD:FG=1; BDUSS=FkfmZRMjlFRTk0VTlXd2p4QTZmYjZnZ1psYzhMWm1MSmVuVH5YZjI2cU5pVEJmRVFBQUFBJCQAAAAAAAAAAAEAAAD0IdV7d2~SqmppZd-jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI38CF-N~AhfdF; BIDUPSID=AAC94C02DA58A6E1A6FC363502E36DCD; PSTM=1594798231; BDRCVFR[FhauBQh29_R]=mbxnW11j9Dfmh7GuZR8mvqV; delPer=0; PSINO=7; cflag=13%3A3; ZD_ENTRY=bing; BDUSS_BFESS=FkfmZRMjlFRTk0VTlXd2p4QTZmYjZnZ1psYzhMWm1MSmVuVH5YZjI2cU5pVEJmRVFBQUFBJCQAAAAAAAAAAAEAAAD0IdV7d2~SqmppZd-jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI38CF-N~AhfdF; H_PS_PSSID=32294_1452_31672_32379_32357_31660_32351_32046_32398_32429_2453_32117_31708_26350_31640; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1596800480,1596802679,1596803053; yjs_js_security_passport=720ed866bd70e328f6bddcaf2d9550b1b5bf2f67_1596803053_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1596804291"
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
