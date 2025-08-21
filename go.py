import paramiko
import os
import json


 


URL="gulf.moneroocean.stream:10128"
ADDRESS="4A1sCcmWh3vMuRX4WAs43JFp9ZDL7FnpQBQhdCrL9pTBdRLCZVFh59ATi3kYhebUvGXoBWvBgDCywj8v9zVhzuPAPSFR8tM"

ip_dict = [
    {'ip': '192.168.1.170', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.171', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.172', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.173', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.190', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.191', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.192', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.193', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.194', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.195', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.196', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.197', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.198', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.199', 'username': 'root', 'password': 'Yousa@290',
        'put_path': '/mnt/disk1/project1', 'threads': 12, 'cuda': False},
    {'ip': '192.168.1.151', 'username': 'root', 'password': 'Boguan@360',
        'put_path': '/home', 'threads': 3, 'cuda': False},
    {'ip': '192.168.1.153', 'username': 'root', 'password': 'Boguan@360',
        'put_path': '/home', 'threads': 3, 'cuda': False},
    {'ip': '192.168.1.155', 'username': 'root', 'password': 'Boguan@360',
        'put_path': '/home', 'threads': 12, 'cuda': True}
]

def writeSh(worker_value, threads,cuda):
    pass_name = fmtIp(worker_value)
    # 写入 shell 脚本
    sh_template_path = os.path.join(os.getcwd(), "sh.tpl")
    sh_output_path = os.path.join(os.getcwd(), "server", "server.sh")
    with open(sh_template_path, "r", encoding="utf-8") as f:
        sh_content = f.read()
    sh_content = sh_content.replace("{THREADS}", str(threads)).replace('\r\n', '\n')
    sh_content = sh_content.replace("{URL}", str(URL)).replace('\r\n', '\n')
    sh_content = sh_content.replace("{ADDRESS}", str(ADDRESS)).replace('\r\n', '\n')
   
    sh_content = sh_content.replace("{WORKERNAME}", str(pass_name)).replace('\r\n', '\n')
    
  
    sh_content = sh_content.replace('\r\n', '\n')
    with open(sh_output_path, "w", encoding="utf-8", newline='\n') as f:
        f.write(sh_content)

    # 处理 config.json
    config_template_path = os.path.join(os.getcwd(), "config.json")
    config_output_path = os.path.join(os.getcwd(), "server", "config.json")
    

    with open(config_template_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    # 替换 pass
    if "pools" in config_data and isinstance(config_data["pools"], list) and len(config_data["pools"]) > 0:
        config_data["pools"][0]["pass"] = pass_name
    else:
        raise ValueError("config.json 中没有有效的 pools 配置")
    
    config_data["cuda"]["enabled"] = cuda
 
    # 保存 config.json
    with open(config_output_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)



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
    threads=row.get('threads')
    cuda=row.get('cuda')
    writeSh(ip,threads,cuda)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        sftp = ssh.open_sftp()
        put_server_path=os.path.join(put_path, "server")
        sftp_mkdir_p(sftp,  put_server_path)
        upload_dir(sftp, os.path.join(os.getcwd(), "server"),  put_server_path)


        local_clear_login_ip_script = os.path.join(os.getcwd(), "clear_login_ip.sh")
        remote_clear_login_ip_script = put_path.rstrip("/") + "/clear_login_ip.sh"

        local_clean_keywords_script = os.path.join(os.getcwd(), "clen_keywords.sh")
        remote_clean_keywords_script = put_path.rstrip("/") + "/clean_keywords.sh"
   
        sftp.put(local_clear_login_ip_script, remote_clear_login_ip_script)
        sftp.put(local_clean_keywords_script, remote_clean_keywords_script)




        sftp.close()

        # 远程执行命令部分
        commands = [
            f"cd {put_server_path} && chmod +x server.sh && sh server.sh stop",
              f"rm -f  {put_server_path}",
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
