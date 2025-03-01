import re
import threading

import regex
import unicodedata
from html.parser import HTMLParser


def bj2qj(src):
    if src is None:
        return src

    DBC_SPACE = ' '
    SBC_SPACE = '　'
    DBC_CHAR_START = 33
    DBC_CHAR_END = 126
    CONVERT_STEP = 65248

    buf = []
    for char in src:
        if char == DBC_SPACE:
            buf.append(SBC_SPACE)
        elif DBC_CHAR_START <= ord(char) <= DBC_CHAR_END:
            buf.append(chr(ord(char) + CONVERT_STEP))
        else:
            buf.append(char)

    return ''.join(buf)


def qj2bj(src):
    """
    全角转半角
    :param src:
    :return:
    """
    if src is None:
        return src

    SBC_CHAR_START = 0xFF01
    SBC_CHAR_END = 0xFF5E
    CONVERT_STEP = 0xFEE0
    DBC_SPACE = ' '
    SBC_SPACE = '　'

    buf = []
    for char in src:
        if SBC_CHAR_START <= ord(char) <= SBC_CHAR_END:
            buf.append(chr(ord(char) - CONVERT_STEP))
        elif char == SBC_SPACE:
            buf.append(DBC_SPACE)
        else:
            buf.append(char)

    return ''.join(buf)


def get_diacritic_variant(char1):
    # 将字符转换为标准的 Unicode 形式
    normalized_char1 = unicodedata.normalize('NFD', char1)

    # 获取基本字符（去掉变音符号）
    base_char1 = ''.join(c for c in normalized_char1 if unicodedata.category(c) != 'Mn')

    # 判断基本字符是否相同
    return base_char1


def get_alphabetic_ratio(text: str) -> float:
    # 返回字母型字符所占比例
    if not text:
        return 0

    text = re.sub(r'\d+', '', text)

    # 正则表达式匹配字母型文字（包括拉丁字母、希腊字母、西里尔字母、阿拉伯字母等）
    alphabetic_pattern = (
        r"[\u0041-\u005A\u0061-\u007A"  # 拉丁字母 (A-Z, a-z)
        r"\u00C0-\u00FF"  # 带重音符号的拉丁字母 (À-ÿ)
        r"\u0080–\u00FF"  # 拉丁字母补充1
        r"\u0100–\u017F"  # 拉丁字母扩展A
        r"\u1E00-\u1EFF"  # 拉丁扩展 (Latin Extended Additional)
        r"\u0180-\u024F"  # 拉丁扩展-B (Latin Extended-B)
        r"\u2C60-\u2C7F"  # 拉丁扩展-C (Latin Extended Additional)
        r"\uA720-\uA7FF"  # 拉丁扩展-D (Latin Extended Additional)
        r"\uAB30-\uAB6F"  # 拉丁扩展-E (Latin Extended Additional)
        r"]"
    )

    # 使用正则表达式过滤出语言文字
    clean_text = regex.sub(r"[^\p{L}]", "", text)

    if len(clean_text) == 0:
        return 1.0

    # 匹配所有字母型字符
    alphabetic_chars = re.findall(alphabetic_pattern, clean_text)

    # 返回字母型字符所占比例
    return len(alphabetic_chars) / len(clean_text)


class HTMLTextExtractor(HTMLParser):
    _thread_local = threading.local()  # 线程局部存储

    def __init__(self):
        super().__init__()
        self.reset_state()

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data)

    def reset_state(self):
        self.reset()
        self.text = []
        self.skip = False

    def get_text(self):
        return ''.join(self.text).strip()

    @classmethod
    def get_parser(cls):
        # 每个线程获取独立实例
        if not hasattr(cls._thread_local, 'parser'):
            cls._thread_local.parser = cls()
        return cls._thread_local.parser


def clean_html(html):
    parser = HTMLTextExtractor.get_parser()
    parser.reset_state()
    parser.feed(html)
    parser.close()
    return parser.get_text()



