from pysnmp.hlapi import *
import paramiko
import socket


from util.log import _log
from util.cfg_read import cfg
from util.excel_read import devices
from util.tools import tool

import importlib
language = getattr(importlib.import_module("lang.language", package="lang"), cfg.app_language)

class Mainapp:
    def __init__(self):
        self.ssh_username = cfg.ssh_username
        self.ssh_password = cfg.ssh_password

    def snmp_log(self):
        try:
            for device in devices:
                device_ip = device['ip']
                snmp_community = device['snmp_community']
                cpu_utilization_oid = device['cpu_utilization_oid']
                
                # 检查IP是否可达
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((device_ip, 22))
                if result == 0:
                    # IP可达，直接查询设备
                    self.query_device(device_ip, snmp_community, cpu_utilization_oid)
                else:
                    # IP不可达，尝试使用SSH连接查询设备
                    _log._WARN(language.ip_not_connect)
                    self.ssh_query_device(device_ip, snmp_community, cpu_utilization_oid)
                
        except Exception as error:
            _log._ERROR(str(error))
    
    def query_device(self, device_ip, snmp_community, cpu_utilization_oid):
        try:
            # 构建SNMP命令
            snmp_object = ObjectIdentity(cpu_utilization_oid)
            snmp_varbind = ObjectType(snmp_object)
            
            # 构建SNMP请求
            snmp_request = getCmd(SnmpEngine(), CommunityData(snmp_community), UdpTransportTarget((device_ip, 161)),
                                ContextData(), snmp_varbind)
            
            # 执行SNMP查询命令
            # ...
            
        except Exception as error:
            _log._ERROR(str(error))
    
    def ssh_query_device(self, device_ip, snmp_community, cpu_utilization_oid):
        try:
            # 创建SSH客户端
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 连接SSH服务器
            ssh_client.connect(device_ip, username=self.ssh_username, password=self.ssh_password)
            
            # 使用SSH执行SNMP查询命令
            stdin, stdout, stderr = ssh_client.exec_command('snmpwalk -v 2c -c {} {} {}'.format(snmp_community, device_ip, cpu_utilization_oid))
            
            # 处理SNMP响应
            for line in stdout:
                _log._INFO(line.strip())
            
            # 关闭SSH连接
            ssh_client.close()
            
        except Exception as error:
            _log._ERROR(str(error))
            
        
def service_while():
    while True:
        cmd = tool.terminal().lower()
        if cmd == "help":
            tool.help()
        elif cmd == "snmp_log":
            app.snmp_log()
        elif "add" in cmd:
            if len(cmd.split()) == 4:
                try:
                    devices.write([{"ip": str(cmd.split()[1]), "snmp_community": str(cmd.split()[2]), "cpu_utilization_oid": str(cmd.split()[3])}])
                except Exception as error:
                    _log._ERROR(str(error))
        elif cmd == "shutdown":
            tool.shutdown()
            break
        elif cmd == "":
            continue
        else:
            print(language.not_exec)

if __name__ == "__main__":
    app = Mainapp()
    service_while()
    