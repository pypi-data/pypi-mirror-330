def sort_dict_by_key(d: dict, reverse=False) -> list[tuple]:
    items = list(d.items())
    items.sort(key=lambda x: x[0], reverse=reverse)
    return items


def sort_dict_by_value(d: dict, reverse=False) -> list[tuple]:
    items = list(d.items())
    items.sort(key=lambda x: x[1], reverse=reverse)
    return items


def get_distribution(d: dict[any, list]) -> dict[any, int]:
    result = dict()
    if d is None or d.__len__() == 0:
        return result
    for key in d.keys():
        if result.__contains__(key):
            result[key] += d[key].__len__()
        else:
            result[key] = d[key].__len__()
    return result


def find_all(d: dict, condition: callable) -> dict:
    result = dict()
    for key in d.keys():
        value = d[key]
        if condition(key, value):
            result[key] = value
    return result
