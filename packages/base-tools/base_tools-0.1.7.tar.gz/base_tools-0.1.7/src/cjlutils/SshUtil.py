import sys

import paramiko


def ssh(host_name: str, account: str, password: str, cmd_list: list[str]) -> tuple:
    if cmd_list is None or len(cmd_list) <= 0:
        return tuple()
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    ssh.connect(host_name, username=account, port=22, password=password)

    sh_in = None
    out_str: str = ''
    err_str: str = ''
    for cmd in cmd_list:
        print(f'to execute: {cmd}')
        sh_in, sh_out, sh_err = ssh.exec_command(cmd)
        out_str = sh_out.read().decode('utf-8')
        err_str = sh_err.read().decode('utf-8')
        print('out: %s, error: %s' % (out_str, err_str))
    # 关闭连接
    if sh_in is not None:
        sh_in.close()
    ssh.close()
    return out_str, err_str


# ---------- 输入变量 ----------
if __name__ == '__main__':
    argv_len: int = len(sys.argv)
    print('此脚本仅支持输入立即生效的命令，不支持需要确认的命令，如密码确认')

    print('请输入远程连接')
    host_name = sys.argv[1] if argv_len > 1 else input()
    print(host_name)

    print('请输入账号')
    account = sys.argv[2] if argv_len > 2 else input()
    print(account)

    print('请输入密码')
    password = sys.argv[3] if argv_len > 3 else input()
    print(password)

    print('请输入一组命令，多个连续命令用分号隔开，如pwd;ls。空代表结束')
    cmd = input()
    while cmd is not None and len(cmd) > 0:
        print(cmd)
        ssh(host_name, account, password, [cmd])
        print('请输入命令，连续命令用分号隔开，如pwd;ls。空代表结束')
        cmd = input()
