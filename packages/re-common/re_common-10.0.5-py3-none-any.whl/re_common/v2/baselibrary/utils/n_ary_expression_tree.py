class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"Node(value={self.value}, children={self.children})"


def tokenize(expression):
    """将表达式分解为标记（token），仅以 and, or, not 和括号作为分界符

    Args:
        expression (str): 输入的字符串表达式，例如 'a = 3 + (b > 2) and c'

    Returns:
        list: 分解后的标记列表，例如 ['a = 3 + (b > 2)', 'and', 'c']
    """
    tokens = []  # 存储最终的标记列表
    current = ""  # 当前正在构建的标记字符串
    i = 0  # 当前字符的索引
    length = len(expression)  # 输入表达式的长度

    def is_delimiter_match(expression, i, delimiter_len=3, delimiter="and"):
        """检查当前位置是否匹配指定的分隔符（and, or, not）

        Args:
            expression (str): 输入的表达式字符串
            i (int): 当前检查的起始索引
            delimiter_len (int): 分隔符的长度，默认为 3（适用于 'and' 和 'not'）
            delimiter (str): 要检查的分隔符，默认为 'and'

        Returns:
            bool: 如果当前位置匹配分隔符且前后有空格，返回 True，否则返回 False
        """
        # 检查索引是否超出范围
        if not i + delimiter_len <= length:
            return False
        # 检查当前位置是否匹配指定分隔符（忽略大小写）
        if not expression[i:i + delimiter_len].lower() == delimiter:
            return False

        # 检查分隔符前是否有一个空格（如果不是字符串开头）
        if i - 1 >= 0:
            if not expression[i - 1].lower() == ' ':
                return False

        # 检查分隔符后是否有一个空格（如果不是字符串结尾）
        if i + delimiter_len + 1 <= length:
            if not expression[i + delimiter_len].lower() == ' ':
                return False
        return True

    # 遍历表达式的每个字符
    while i < length:
        char = expression[i]  # 当前处理的字符

        # 处理括号
        if char in "()":
            if current.strip():  # 如果当前标记有内容，先将其添加到 tokens
                tokens.append(current.strip())
                current = ""  # 重置当前标记
            tokens.append(char)  # 将括号作为独立标记添加
            i += 1  # 移动到下一个字符
            continue

        # 检查是否遇到 and, or, not 分隔符
        if is_delimiter_match(expression, i, delimiter_len=3, delimiter="and"):
            if current.strip():  # 如果当前标记有内容，先添加
                tokens.append(current.strip())
                current = ""  # 重置当前标记
            tokens.append("and")  # 添加 'and' 标记
            i += 3  # 跳过 'and' 的长度
            continue
        elif is_delimiter_match(expression, i, delimiter_len=2, delimiter="or"):
            if current.strip():  # 如果当前标记有内容，先添加
                tokens.append(current.strip())
                current = ""  # 重置当前标记
            tokens.append("or")  # 添加 'or' 标记
            i += 2  # 跳过 'or' 的长度
            continue
        elif is_delimiter_match(expression, i, delimiter_len=3, delimiter="not"):
            if current.strip():  # 如果当前标记有内容，先添加
                tokens.append(current.strip())
                current = ""  # 重置当前标记
            tokens.append("not")  # 添加 'not' 标记
            i += 3  # 跳过 'not' 的长度
            continue

        # 将非分隔符字符追加到当前标记中，包括空格
        current += char
        i += 1  # 移动到下一个字符

    # 处理最后一个标记（如果有内容）
    if current.strip():
        tokens.append(current.strip())

    return tokens  # 返回标记列表




def parse_expression(tokens):
    """递归下降解析表达式"""

    def parse_or(tokens, pos):
        """解析 OR 级别（最低优先级）"""
        left, pos = parse_and(tokens, pos)
        while pos < len(tokens) and tokens[pos] == 'or':
            pos += 1
            if pos >= len(tokens):
                raise ValueError("Incomplete expression after 'or'")
            right, pos = parse_and(tokens, pos)
            left = Node('or', [left, right])
        return left, pos

    def parse_and(tokens, pos):
        """解析 AND 级别（次高优先级）"""
        left, pos = parse_not(tokens, pos)
        while pos < len(tokens) and tokens[pos] == 'and':
            pos += 1
            if pos >= len(tokens):
                raise ValueError("Incomplete expression after 'and'")
            right, pos = parse_not(tokens, pos)
            left = Node('and', [left, right])
        return left, pos

    def parse_not(tokens, pos):
        """解析 NOT 级别（最高优先级）"""
        if pos < len(tokens) and tokens[pos] == 'not':
            pos += 1
            if pos >= len(tokens):
                raise ValueError("Incomplete expression after 'not'")
            child, pos = parse_primary(tokens, pos)
            return Node('not', [child]), pos
        return parse_primary(tokens, pos)

    def parse_primary(tokens, pos):
        """解析基本单元（条件或括号表达式）"""
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")

        if tokens[pos] == '(':
            pos += 1
            subtree, pos = parse_or(tokens, pos)
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            return subtree, pos + 1
        else:
            # 假设这是一个条件（如 A=1）
            return Node(tokens[pos]), pos + 1

    # 从头开始解析
    tree, pos = parse_or(tokens, 0)
    if pos < len(tokens):
        raise ValueError(f"Extra tokens after expression: {tokens[pos:]}")
    return tree


# 测试代码
expressions = [
    "not A=1 and B= 2",
    "A=1 and (not B=2 or (C=3 or D=4))",
    "A=1 and not (B=2 or C=3 and D=4 or E=5)",
    "(A=1 and not (B=2 or C=3 or D=4))",
    "A=1 and",  # 不完整表达式
    "and A=1",  # 不完整表达式
]

for expr in expressions:
    try:
        print(f"\nExpression: {expr}")
        tokens = tokenize(expr)
        print("Tokens:", tokens)
        tree = parse_expression(tokens)
        print("Tree:", tree)
    except ValueError as e:
        print(f"Error: {e}")