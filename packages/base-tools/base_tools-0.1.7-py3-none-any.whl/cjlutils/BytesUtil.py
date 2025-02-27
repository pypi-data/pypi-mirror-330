def to_list(b: None | bytes) -> None | list[int]:
    """
    字节流转整数列表
    :param b: 字节流
    :return: 整数列表
    """
    if b is None:
        return None
    return [i for i in b]


def from_list(l: None | list[int]) -> None | bytes:
    """
    整数列表转字节流
    :param l: 整数列表
    :return: 字节流
    """
    if l is None:
        return None
    for i in l:
        if i < 0 or i > 255:
            return None
    return bytes(l)
