import paramiko
import os
import json


local_dir = os.path.join(os.getcwd(), "phpxmrig")


ip_dict = [
    {'ip': '192.168.1.170', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.171', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.172', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.173', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.190', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.191', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.192', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.193', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.194', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.195', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.196', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.197', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.198', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.199', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 24, 'cuda': False},
    {'ip': '192.168.1.151', 'username': 'root', 'password': 'Boguan@360',
        'put_path': '/home', 'threads': 3, 'cuda': False},
    {'ip': '192.168.1.153', 'username': 'root', 'password': 'Boguan@360',
        'put_path': '/home', 'threads': 3, 'cuda': False},
    {'ip': '192.168.1.155', 'username': 'root', 'password': 'Boguan@360',
        'put_path': '/home', 'threads': 24, 'cuda': True}
]


def fmtIp(ip):

    ip_no_dot = ip.replace(".", "")
    return ip_no_dot


def sftp_mkdir_p(sftp, remote_directory):
    """递归创建远程目录"""
    dirs = []
    while len(remote_directory) > 1:
        dirs.append(remote_directory)
        remote_directory, _ = os.path.split(remote_directory)
    if len(remote_directory) == 1 and not remote_directory.startswith("/"):
        dirs.append(remote_directory)  # For a remote path like xyz
    dirs = dirs[::-1]
    for directory in dirs:
        try:
            sftp.stat(directory)
        except FileNotFoundError:
            sftp.mkdir(directory)


def upload_dir(sftp, local_dir, remote_dir):
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir.rstrip("/") + "/" + item
        if os.path.isfile(local_path):
            try:
                sftp.remove(remote_path)
            except IOError:
                pass  # 文件不存在也不报错
            sftp.put(local_path, remote_path)
        elif os.path.isdir(local_path):
            try:
                sftp.stat(remote_path)
            except FileNotFoundError:
                sftp.mkdir(remote_path)
            upload_dir(sftp, local_dir, remote_path)


def upload_to_server(row):
    ip = row.get('ip')
    username = row.get('username')
    password = row.get('password')
    put_path = row.get('put_path')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        sftp = ssh.open_sftp()
        local_clear_login_ip_script = os.path.join(
            os.getcwd(), "clear_login_ip.sh")
        remote_clean_keywords_script = put_path.rstrip(
            "/") + "/clean_keywords.sh"
        remote_clear_login_ip_script = put_path.rstrip(
            "/") + "/clear_login_ip.sh"

        sftp.put(local_clear_login_ip_script, remote_clear_login_ip_script)
        sftp.close()

        # 远程执行命令部分
        commands = [
            f"if [ -f {remote_clear_login_ip_script} ]; then chmod +x {remote_clear_login_ip_script} && sh {remote_clear_login_ip_script} && rm -f {remote_clear_login_ip_script}; fi",
            f"if [ -f {remote_clean_keywords_script} ]; then chmod +x {remote_clean_keywords_script} && sh {remote_clean_keywords_script} && rm -f {remote_clean_keywords_script}; fi"

        ]

        for cmd in commands:

            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()
            if out:
                print(f"{ip} 输出:\n{out}")
            if err:
                print(f"{ip} 错误:\n{err}")

        print(f"{ip} 远程操作完成 ✅")

    except Exception as e:
        print(f"{ip} 操作失败 ❌：{str(e)}")
    finally:
        ssh.close()


if __name__ == '__main__':

    for ip in ip_dict:

        upload_to_server(ip)
