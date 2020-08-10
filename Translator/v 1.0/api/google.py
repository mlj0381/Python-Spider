import js2py
import requests


class WordsLengthError(Exception):
    def __init__(self, err="The length of input is out of limit (4891)"):
        Exception.__init__(self, err)


class GoogleTranslator(object):
    def __init__(self):
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
        }
        self.url = "https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl={}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&dt=gt&clearbtn=1&otf=1&ssel=3&tsel=0&xid=45662847&kc=2&tk={}&q={}"

    def get_translation(self, words):
        """
        翻译输入的内容
        :param words: 输入的内容
        :return: 译文
        """
        # 判断是否超出最大长度限制
        if len(words) > 4891:
            raise WordsLengthError

        languages = ["zh-CN", "en"]
        if self.is_Chinese(words):
            # 指定翻译后的语种
            target_language = languages[1]
        else:
            target_language = languages[0]
        response = requests.get(self.url.format(target_language, self.get_tk(words), words), headers=self.headers)
        translation = response.json()[0][0][0]
        return translation

    def get_tk(self, words):
        """
        获取 js 加密的参数 tk
        :param words: 待翻译的内容
        :return: 参数 tk
        """
        # 已经有大佬将生成 tk 的算法提取出来了，地址：https://github.com/cocoa520/Google_TK
        # 不过我还是自己提取了一下生成 tk 的算法
        js_code = open("./javascript/google.js", "r", encoding="utf-8").read()
        evaljs = js2py.EvalJs()
        evaljs.execute(js_code)
        tk = evaljs.Au(words)
        return tk

    def is_Chinese(self, words):
        """
        判断输入的内容是否为中文
        :param words: 用户输入的文本
        :return: True or False
        """
        for w in words:
            # 只要有一个字符是中文就认定为是中译英（返回 True）
            if "\u4e00" <= w <= "\u9fa5":
                return True
        return False

    def run(self):
        words = input("请输入您想翻译的内容：")
        translation = self.get_translation(words)
        print("原文：{}\n译文：{}".format(words, translation))


if __name__ == "__main__":
    google = GoogleTranslator()
    google.run()