import re


def is_all_english_chars(s):
    return bool(re.match(r'^[A-Za-z]+$', s))


def contains_chinese_chars(s):
    return bool(re.search(r'[\u3400-\u9fff]', s))


def is_empty(value):
    # 如果是 None，直接返回 True
    if value is None:
        return True

    # 如果是字符串，检查去除空白后是否为空
    if isinstance(value, str):
        return value.strip() == ""

    # 可选：处理其他可迭代类型（如列表、字典等）
    if hasattr(value, "__len__"):
        return len(value) == 0

    # 默认情况下，非 None、非空类型返回 False
    return False