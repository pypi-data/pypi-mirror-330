def get_greatest_common_divisor(a: int, b: int) -> int:
    """
    求最大公约数
    :param a: 整数a
    :param b: 整数b
    :return: 最大公约数
    """
    if a <= 0 or b <= 0:
        return -1
    while b != 0:
        a, b = b, a % b
    return a


def get_least_common_multiple(a: int, b: int) -> int:
    """
    求最小公倍数
    :param a: 整数a
    :param b: 整数b
    :return: 最小公倍数
    """
    if a <= 0 or b <= 0:
        return -1
    return a * b // get_greatest_common_divisor(a, b)


def get_union_of_line_segment_int(l: list[tuple[int, int]]) -> tuple[int, int]:
    """
    获取线段的并集
    :param l: 线段列表，线段的首尾分别由一个整数表示，为半必半开区间
    :return: 线段的并集，半必半开区间
    """
    if l is None or len(l) == 0:
        return tuple()
    start = l[0][0]
    stop = l[0][1]
    for i in range(1, len(l)):
        if l[i][0] < start:
            start = l[i][0]
        if l[i][1] > stop:
            stop = l[i][1]
    return start, stop


def get_intersection_of_line_segment_int(l: list[tuple[int, int]]) -> tuple[int, int]:
    """
    获取线段的交集
    :param l: 线段列表，线段的首尾分别由一个整数表示，为半必半开区间
    :return: 线段的交集，半必半开区间
    """
    if l is None or len(l) == 0:
        return tuple()
    start = l[0][0]
    stop = l[0][1]
    for i in range(1, len(l)):
        if l[i][0] > start:
            start = l[i][0]
        if l[i][1] < stop:
            stop = l[i][1]
        if start >= stop:
            return tuple()
    return start, stop
