def fancy_print(message, symbol="*", padding=2):
    """
    打印带装饰框的字符串

    :param message: 要打印的消息
    :param symbol: 用来装饰的符号，默认为 "*"
    :param padding: 字符串左右的填充宽度，默认为 2
    """
    message = str(message)
    length = len(message) + padding * 2
    border = symbol * (length + 2)

    print(border)
    print(f"{symbol}{' ' * padding}{message}{' ' * padding}{symbol}")
    print(border)
