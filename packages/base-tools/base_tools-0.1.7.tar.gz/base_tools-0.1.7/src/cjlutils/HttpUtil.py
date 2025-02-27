import requests
from requests import Response


def request(url, method='GET', headers=None, params=None, data=None, json=None) -> Response:
    """
    发送HTTP请求的通用方法
    :param url: 请求的URL
    :param method: 请求方法，默认为GET
    :param headers: 请求头
    :param params: URL参数
    :param data: 请求体数据
    :param json: 请求体JSON数据
    :return: 响应对象
    """
    # 构造请求
    req = requests.Request(method, url, headers=headers, params=params, data=data, json=json)
    # 发送请求
    session = requests.Session()
    resp = session.send(req.prepare())
    # 返回响应
    return resp
