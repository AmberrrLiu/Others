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
    gpu_message = f"��ǰ���ܿ��еĿ���Ϊ��{str(free_gpu_memory)}," \
                    f"ĿǰGPUռ�����{mem}."
    content = f"{user_name}, ���ã� " \
              f"IP Ϊ {ip_addr} �ķ��������Կ�����, " \
              f"{gpu_message}"

    return content, flag #True if len(free_gpu_memory) > 0 else False


def send_email(content, msg_from, passwd, msg_to):
    msg = MIMEText(content)
    msg['Subject'] = "GPU �п�ȱ��ʾ!"
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # �ʼ����������˿ں�
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("���ͳɹ�")
    except Exception as e:
        print(f"����ʧ��: {e}")
    finally:
        quit()
if __name__ == "__main__":
    msg_from = '444683639@qq.com' # ���ͷ�����
    passwd = 'sesgnuzldcpdbjhj'  # ���뷢�ͷ��������Ȩ��
    msg_to = '444683639@qq.com'  # �ռ�������
    while True:
        content, flag = gather_info()
        if flag:
            send_email(content, msg_from, passwd, msg_to)
            break
        time.sleep(30)
