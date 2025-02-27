def classify(l: list, classifier: callable) -> dict:
    """
    按照指定逻辑分类
    :param l: 原始列表
    :param classifier: 分类规则器，输入列表中的元素，返回分类类型
    :return: 一个字典，key为分类类型，value为对应的元素列表
    """
    result = dict()
    for data in l:
        data_type = classifier(data)
        if result.__contains__(data_type):
            result[data_type].append(data)
        else:
            result[data_type] = [data]
    return result


def find_all(l: list, predicate: callable) -> list:
    """
    查找所有符合条件的元素
    :param l: 原始列表
    :param predicate: 查找条件，输入列表中的元素，返回是否符合条件
    :return: 符合条件的元素列表
    """
    result = list()
    for data in l:
        if predicate(data):
            result.append(data)
    return result


def firstElement(l: list) -> any:
    """
    获取列表的第一个元素
    :param l: 列表
    :return: 第一个元素
    """
    if l is None or len(l) == 0:
        return None
    return l[0]


def get_distribution(l: list[tuple[any, any]]) -> dict[any, int]:
    """
    获取列表中元素的分布情况
    :param l: 列表，元素需要是一个长度为2的元组，否则被忽略
    :return:
    """
    result = dict()
    if l is None or l.__len__() == 0:
        return result
    for entry in l:
        if entry.__len__() != 2:
            continue
        key = entry[0]
        if result.__contains__(key):
            result[key] += 1
        else:
            result[key] = 1
    return result


def lastElement(l: list) -> any:
    """
    获取列表的最后一个元素
    :param l:  列表
    :return: 最后一个元素
    """
    if l is None or len(l) == 0:
        return None
    return l[-1]


def random_order(l: list) -> list:
    """
    随机打乱列表
    :param l: 原始列表
    :return: 新列表，为原列表的乱序
    """
    import random
    random.shuffle(l)
    return l


def to_string(l: list, separator: str = ',', prefix: str = '', suffix: str = '', transformer: callable = None) -> str:
    """
    将列表转换为字符串
    :param l: 列表
    :param separator: 元素之间的分隔符
    :param prefix: 前缀
    :param suffix: 后缀
    :param transformer: 元素转换为字符串的逻辑：输入元素，返回字符串
    :return: 字符串
    """
    if l is None or l.__len__() == 0:
        return ''
    separator = '' if separator is None else separator
    prefix = '' if prefix is None else prefix
    suffix = '' if suffix is None else suffix

    result = ''
    for data in l:
        result += separator + str(transformer(data) if transformer is not None else data)
    return f'{prefix}{result[len(separator):]}{suffix}'


def transform(l: list, transformer: callable) -> list:
    """
    对列表中的每个元素进行转换
    :param l: 列表
    :param transformer: 转换逻辑，输入列表中的元素，返回转换后的元素
    :return: 转换后的元素组成的新列表
    """
    result = list()
    for data in l:
        result.append(transformer(data))
    return result