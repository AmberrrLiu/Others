# https://blog.csdn.net/huuuuuuuu/article/details/109851526
#coding=gbk
import getpass
import re
import smtplib
import socket
import subprocess
import time
from email.mime.text import MIMEText

import numpy as np



def gather_info():
    user_name = getpass.getuser()

    ip_addr = socket.gethostbyname(socket.gethostname())

    used_gpu_memory = np.array(list(map(int, re.findall("(\d+)", subprocess.getstatusoutput(
        'nvidia-smi -q -d Memory |grep -A4 GPU|grep Used')[1], flags=0))))
    free_gpu_memory = np.argwhere(used_gpu_memory < 100)
    mem = used_gpu_memory.tolist()
    flag = 1
    for idx in range(len(mem)):
        if int(mem[idx]) > 5000:
            flag = 0
    gpu_message = f"当前可能空闲的卡号为：{str(free_gpu_memory)}," \
                    f"目前GPU占用情况{mem}."
    content = f"{user_name}, 您好！ " \
              f"IP 为 {ip_addr} 的服务器有显卡空余, " \
              f"{gpu_message}"

    return content, flag #True if len(free_gpu_memory) > 0 else False


def send_email(content, msg_from, passwd, msg_to):
    msg = MIMEText(content)
    msg['Subject'] = "GPU 有空缺提示!"
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except Exception as e:
        print(f"发送失败: {e}")
    finally:
        quit()
if __name__ == "__main__":
    msg_from = '444xxxxxx@qq.com' # 发送方邮箱
    passwd = 'xxxxxxxxx'  # 填入发送方邮箱的授权码,POP3
    msg_to = '444xxxxxx@qq.com'  # 收件人邮箱
    while True:
        content, flag = gather_info()
        if flag:
            send_email(content, msg_from, passwd, msg_to)
            break
        time.sleep(30)
