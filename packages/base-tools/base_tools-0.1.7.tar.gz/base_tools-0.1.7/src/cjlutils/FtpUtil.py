import os
from ftplib import FTP


def close(ftp: FTP) -> bool:
    """
    关闭连接
    :param ftp: FTP实例
    :return: 是否执行成功
    """
    try:
        ftp.close()
        return True
    except Exception as e:
        print(f"close with error: {str(e)}")
        return False


def connect_remote_computer(host: str, port: int, user: str, password: str) -> FTP | None:
    """
    连接远程主机，并获取FTP实例
    :param host: 远程主机域名
    :param port: 远程主机端口
    :param user: 登录远程主机使用的用户名
    :param password: 登录远程主机使用的密码
    :return: FTP实例
    """
    ftp = FTP()
    try:
        # 连接到服务器
        ftp.connect(host, port)

        # 登录
        ftp.login(user, password)
    except Exception as e:
        print(f"connect remote computer with error: {str(e)}")
        ftp.close()
        ftp = None
    return ftp


def create_directory_if_not_exists(ftp: FTP, remote_dir):
    """
    创建指定目录，如果目录已经存在，则忽略
    :param ftp: FTP实例
    :param remote_dir: 指定目录
    """
    try:
        current_dir = str(ftp.pwd())
        ftp.cwd(remote_dir)  # 如果目录存在，可以切换到该目录
        ftp.cwd(current_dir)
    except Exception:
        ftp.mkd(remote_dir)  # 如果目录不存在，创建它
    else:
        print(f"directory exists: {remote_dir}")


def cwd(ftp: FTP, remote_dir: str):
    """
    移动到指定路径
    :param ftp: FTP实例
    :param remote_dir: 指定目录
    :return:
    """
    try:
        ftp.cwd(remote_dir)
    except Exception as e:
        print(f"cwd to {remote_dir} with error: {str(e)}")


def delete_file(ftp: FTP, remote_file_path: str):
    """
    删除指定远程文件

    :param ftp: FTP实例
    :param remote_file_path: 文件路径
    """
    try:
        ftp.delete(remote_file_path)
    except Exception as e:
        print(f"delete file {remote_file_path} with error: {str(e)}")


def ls(ftp: FTP, remote_dir: str) -> str | None:
    """
    查看指定目录下的文件和文件夹名称列表
    :param ftp: FTP实例
    :param remote_dir: 指定目录
    :return: 文件和文件夹名称列表
    """
    result = None
    try:
        result = ftp.retrlines(f'LIST {remote_dir}')
    except Exception as e:
        print(f"ls {remote_dir} with error: {str(e)}")
    return result


def pwd(ftp: FTP) -> str | None:
    """
    获取当前所在远端路径
    :param ftp: FTP实例
    :return: 远端路径
    """
    path: str | None = None
    try:
        path = ftp.pwd()
    except Exception as e:
        print(f"pwd with error: {str(e)}")
    return path


def remove_dir(ftp: FTP, remote_path: str):
    """
    删除指定远端目录
    :param ftp: FTP对象，
    :param remote_path:
    :return:
    """
    try:
        ftp.rmd(remote_path)
    except Exception as e:
        print(f"remove dir {remote_path} with error: {str(e)}")


def upload_file_directly(ftp: FTP, local_file_path: str, remote_file_path: str):
    """
    使用FTP协议传输文件到远程主机
    直接传递整个文件，适合较小的文件

    :param ftp: FTP实例，通过connect_remote_computer获取
    :param local_file_path: 文件的本地路径，传输起点
    :param remote_file_path: 文件将要在远端主机上的路径，传输终点
    :return:
    """
    try:
        # 切换到远程目录（如果需要）
        remote_dir = os.path.dirname(remote_file_path)
        if remote_dir:
            ftp.cwd(remote_dir)

        # 设置二进制传输模式
        ftp.voidcmd('TYPE I')

        # 打开本地文件
        with open(local_file_path, 'rb') as file:
            # 上传文件
            remote_filename = os.path.basename(remote_file_path)
            ftp.storbinary(f'STOR {remote_filename}', file)

        print(f"upload file {local_file_path} to {remote_file_path} finished")
    except Exception as e:
        print(f"upload file with error: {str(e)}")
