import re
import subprocess


def _adb_header(device_serial: str = None) -> str:
    """
    生成adb命令的头部
    :param device_serial: 设备序列号
    :return: adb命令的头部
    """
    return 'adb' if device_serial is None else f'adb -s {device_serial}'


def _adb_headers(device_serial: str = None) -> list:
    """
    生成adb命令的头部
    :param device_serial: 设备序列号
    :return: adb命令的头部
    """
    return ['adb'] if device_serial is None else ['adb', '-s', device_serial]


def click(x: float, y: float, device_serial: str = None) -> subprocess.CompletedProcess:
    """
    模拟在Android设备上点击屏幕的操作
    :param x: 点击点的x坐标值
    :param y: 点击点的y坐标值
    :param device_serial: 设备序列号
    :return: 无返回值
    """
    command = f'{_adb_header(device_serial)} shell input tap {x} {y}'
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def get_screen_size(device_serial: str = None) -> None | tuple:
    """
    获取Android设备的屏幕尺寸
    :return: 如果成功获取屏幕尺寸，则返回一个元组，包含屏幕宽度和高度；否则返回None
    """
    cmd = f"{_adb_header(device_serial)} shell wm size"
    output = subprocess.check_output(cmd, shell=True).decode()
    match = re.search(r"(\d+)x(\d+)", output)
    if match:
        width = int(match.group(1))
        height = int(match.group(2))
        return width, height
    else:
        return None


def input_text(text: str, device_serial: str = None) -> subprocess.CompletedProcess:
    """
    输入文本
    :param text: 文本内容
    :param device_serial: 设备序列号
    :return: 无返回值
    """
    text_bytes = text.encode('utf-8')
    command = _adb_headers(device_serial)
    command.extend(['shell', 'input', 'text', text_bytes])
    return subprocess.run(command, shell=False)


def install(apk_path: str, device_serial: str = None) -> subprocess.CompletedProcess:
    """
    在设备上安装应用程序
    :param apk_path: 安装包目录
    :param device_serial: 设备序列号
    :return: 执行结果
    """
    command = f'{_adb_header(device_serial)} install -r {apk_path}'
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def list_packages(device_serial: str = None) -> subprocess.CompletedProcess:
    """
    查看设备上的应用程序列表
    :param device_serial: 设备序列号
    :return: 执行结果
    """
    command = f"{_adb_header(device_serial)} shell pm list packages"
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def long_press(x: float, y: float, duration: int, device_serial: str = None):
    """
    模拟在Android设备上长按屏幕的操作
    :param x: 长按点的x坐标值
    :param y: 长按点的y坐标值
    :param duration: 长按的持续时间（单位为毫秒）
    :param device_serial: 设备序列号
    :return: 无返回值
    """
    cmd = f"{_adb_header(device_serial)} shell input touchscreen swipe {x} {y} {x} {y} {duration}"
    subprocess.run(cmd, shell=True)


def pull(device_path: str, local_path: str, device_serial: str = None) -> subprocess.CompletedProcess:
    """
    从设备上导出文件
    :param device_path: 文件在设备上的地址
    :param local_path: 文件导出到的地址，此处为执行命令的设备的地址
    :param device_serial: 设备序列号
    :return: 执行结果
    """
    command = f"{_adb_header(device_serial)} pull {device_path} {local_path}"
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def start_application(package_name: str, activity_name: str, device_serial: str = None) -> subprocess.CompletedProcess:
    """
    启动应用程序
    :param package_name: 应用包名，如com.example.app
    :param activity_name: 启动Activity完整名称，包括包名。如com.example.app.MainActivity
    :param device_serial: 设备序列号
    :return: 执行结果
    """
    command = f"{_adb_header(device_serial)} shell am start -n {package_name}/{activity_name}"
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def swipe(x1: float, y1: float, x2: float, y2: float, duration: int, device_serial: str = None):
    """
    模拟在Android设备上滑动屏幕的操作
    :param x1: 起始点的x坐标值
    :param y1: 起始点的y坐标值
    :param x2: 终止点的x坐标值
    :param y2: 终止点的y坐标值
    :param duration: 滑动的持续时间（单位为毫秒）
    :param device_serial: 设备序列号
    :return: 无返回值
    """
    cmd = f"{_adb_header(device_serial)} shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.run(cmd, shell=True)


def tap(x: float, y: float, device_serial: str = None) -> subprocess.CompletedProcess:
    """
    模拟在Android设备上点击屏幕的操作
    :param x: 点击点的x坐标值
    :param y: 点击点的y坐标值
    :param device_serial: 设备序列号
    :return: 无返回值
    """
    return click(x, y, device_serial)

