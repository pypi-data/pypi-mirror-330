import sys

import os
import paramiko
from paramiko.sftp_client import SFTPClient


# ---------- 定义函数 ----------
def _is_empty(s: str) -> bool:
    return s is None or len(s) <= 0


def _run_with_sftp_client(hostname: str, account: str, password: str, handler: callable, port: int = 22):
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    ssh.connect(hostname, username=account, port=port, password=password)

    transport = paramiko.Transport((hostname, port))
    transport.connect(username=account, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    result = None
    try:
        result = handler(sftp)
    except Exception as e:
        print(f'caught error: {e}')
    finally:
        sftp.close()
        ssh.close()
    return result


def transport_files(hostname: str, account: str, password: str, push_file_path_list: list[list[str]] = None,
                    pull_file_path_list: list[list[str]] = None) -> bool:
    if push_file_path_list is None and pull_file_path_list is None:
        print('transport_files: nothing to be done')
        return True
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    ssh.connect(hostname, username=account, port=22, password=password)

    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=account, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    caught_exception = False
    if push_file_path_list is not None:
        for push_file_pair in push_file_path_list:
            try:
                if push_file_pair is None or len(push_file_pair) < 2:
                    continue
                print(f'pushing file from {push_file_pair[0]} to {push_file_pair[1]}')
                sftp.put(push_file_pair[0], push_file_pair[1])
            except Exception as e:
                print(f'push file error: {e}')
                caught_exception = True

    if pull_file_path_list is not None:
        for pull_file_pair in pull_file_path_list:
            try:
                if pull_file_pair is None or len(pull_file_pair) < 2:
                    continue
                print(f'pulling file from {pull_file_pair[0]} to {pull_file_pair[1]}')
                sftp.get(pull_file_pair[0], pull_file_pair[1])
            except Exception as e:
                print(f'pull file error: {e}')
                caught_exception = True

    transport.close()
    return not caught_exception


def transport_dir(hostname: str, account: str, password: str, remote_dir: str, local_dir: str) -> bool:
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到远程主机
        ssh.connect(hostname, username=account, port=22, password=password)

        # 创建SFTP客户端
        sftp: SFTPClient = ssh.open_sftp()

        # 递归下载文件夹
        def download_dir(remote_path, local_path):
            # 确保本地目录存在
            os.makedirs(local_path, exist_ok=True)

            # 列出远程目录内容
            for item in sftp.listdir_attr(remote_path):
                remote_item_path = os.path.join(remote_path, item.filename)
                local_item_path = os.path.join(local_path, item.filename)

                if item.st_mode & 0o4000:  # 检查是否为目录
                    download_dir(remote_item_path, local_item_path)
                else:
                    sftp.get(remote_item_path, local_item_path)

        # 开始下载
        download_dir(remote_dir, local_dir)

        print(f"Successfully pulled folder from {remote_dir} to {local_dir}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

    finally:
        # 关闭连接
        sftp.close()
        ssh.close()
    return True


# ---------- 输入变量 ----------
if __name__ == '__main__':
    argv_len: int = len(sys.argv)
    print('请输入远程连接')
    host_name = sys.argv[1] if argv_len > 1 else input()
    print(host_name)

    print('请输入账号')
    account = sys.argv[2] if argv_len > 2 else input()
    print(account)

    print('请输入密码')
    password = sys.argv[3] if argv_len > 3 else input()
    print(password)

    print('请输入要上传文件的本地路径，需要包括文件名，空代表不上传。路径包括空格，可用双引号包裹空格')
    push_local_path = sys.argv[4] if argv_len > 4 else input()
    print(push_local_path)

    push_path_list = None
    if not _is_empty(push_local_path):
        print('请输入要上传文件的远端路径，需要包括文件名，空代表不上传')
        push_remote_path = sys.argv[5] if argv_len > 5 else input()
        print(push_remote_path)
        push_path_list = None if _is_empty(push_remote_path) else [
            [push_local_path, push_remote_path]
        ]
    print('上传参数：%s' % push_path_list)

    print('请输入要下载文件的远端路径，需要包括文件名，空代表不下载')
    pull_remote_path = sys.argv[6] if argv_len > 6 else input()
    print(pull_remote_path)

    pull_path_list = None
    if not _is_empty(pull_remote_path):
        print('请输入要下载文件的本地路径，需要包括文件名，空代表不下载')
        pull_local_path = sys.argv[7] if argv_len > 7 else input()
        print(pull_local_path)
        pull_path_list = None if _is_empty(pull_local_path) else [
            [pull_remote_path, pull_local_path]
        ]

    print('下载参数：%s' % pull_path_list)

    transport_files(host_name, account, password, push_path_list, pull_path_list)
