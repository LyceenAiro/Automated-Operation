# Script Name   port_monitor
# Version       1.0.0
# Author        LyceenAiro
# Dependent     0.0.5 
#
# 这是一个脚本实例
# 它将持续监控端口并在端口异常时关闭端口

from netmiko import ConnectHandler
from util.log import _log
from util.cfg_read import cfg
import time, math

def help_note():
    # 演示如何在脚本中接入全局语言设置
    if cfg.app_language == "zh_cn":
        help_note = "port_monitor { ip } { interface } { threshold }\n使用这个脚本来持续监控端口并在端口异常时关闭端口"
    else:
        help_note = "port_monitor { ip } { interface } { threshold }\nUse this script to continuously monitor ports and close them in case of port exceptions"
    print(help_note)

def main(device, cmd):
    threshold = int(cmd.split()[4])
    interface = cmd.split()[3]
    try:
        connection = ConnectHandler(**device)
        _log._INFO("开始端口监视脚本，使用Ctrl+C退出")

        # 检测这个端口是否是开启状态
        connection.send_command(f'display interface {interface}')
        if 'Administratively DOWN' in output:
            open_bool = input("该接口已经关闭，无法侦测其流量，是否将其开启(y/N)")
            if open_bool in ("y", "Y", "yes", "YES"):
                command = (f'interface {interface}', 'undo shutdown')
                connection.send_config_set(command)

        while True:
            # 发送命令获取接口的流量信息
            command = f'display interface {interface} | include input rate|output rate'
            output = connection.send_command(command)

            # 解析流量信息
            lines = output.split('\n')
            input_rate = int(lines[0].split()[5])
            output_rate = int(lines[1].split()[5])
            
            # 处理命令输出
            if input_rate >= output_rate:
                progress = input_rate / threshold
            else:
                progress = output_rate / threshold
            progress_str = f' {int(progress * 100)}%'
            progress = math.floor(progress * 10)
            if progress > 10:
                progress = 10
            progress_bar = '■' * progress + ' ' * (10 - progress) + progress_str
            _log._INFO(f"{progress_bar}\tinput {input_rate} bit/s | output {output_rate} bit/s")

            # 检测流量是否异常
            if input_rate > threshold or output_rate > threshold:
                # 流量异常，发送命令关闭接口
                shutdown_command = (f'interface {interface}', 'shutdown')
                connection.send_config_set(shutdown_command)
                connection.disconnect()
                _log._WARN(f'接口 {interface} 因为流量转发太大已经关闭了')
                _log._INFO("已经退出了监视脚本")
                break

            time.sleep(5)  # 间隔时间

    except KeyboardInterrupt:
        connection.disconnect()
        _log._INFO("已经退出了监视脚本")
    except TypeError:
        _log._ERROR("参数输入错误")
        connection.disconnect()
    except Exception as error:
        _log._ERROR(error)
        connection.disconnect()
        





