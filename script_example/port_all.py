# Script Name   port_all
# Version       0.1.2
# Author        LyceenAiro
# Dependent     0.0.6
#
# 它将持续监控所有端口的数据

# 在这里可以调用util中的函数
from util.log import _log
import time

def help_note():
    help_note = "port_all { ip } { cmd }\ncmd | -t\t持续监控接口"
    print(help_note)

def main(connection, cmd):

    cmd_t = False

    # 参数配置示例
    if "-t" in cmd:
        cmd_t = True
        _log._RUNNING(cmd.split()[2], "开始端口监视脚本，使用Ctrl+C退出")

    while True:
        # 发送命令获取接口的流量信息
        command = f'display interface brief'
        output = connection.send_command(command)

        # 解析流量信息
        lines = output.split('\n')
        end_list = "所有接口的信息\n"
        
        for line, string in enumerate(lines):
            if line >= 9:
                end_list = end_list + string + "\n"
        _log._RUNNING(cmd.split()[2], end_list)

        if cmd_t == False:
            break

        time.sleep(5)  # 间隔时间


    





