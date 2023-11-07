from pysnmp.hlapi import *
import paramiko
from ping3 import ping
from util.log import _log
from util.cfg_read import cfg
from util.excel_read import devices
from util.tools import tool
from util.list import list_oid

import importlib
language = getattr(importlib.import_module("lang.language", package="lang"), cfg.app_language)

class Mainapp:
    def __init__(self):
        self.ssh_username = cfg.ssh_username
        self.ssh_password = cfg.ssh_password

    def snmp_all(self, cpu_utilization_oid):
        try:
            for device in devices.devices:
                device_ip = device['ip']
                read_community = device['read_community']
                self.snmp_select(device_ip, read_community, cpu_utilization_oid)
                
        except Exception as error:
            _log._ERROR(str(error))
    
    def snmp_select(self, ip, read_community, cpu_utilization_oid):
        _log._RUNNING(cpu_utilization_oid, f"IP: {ip}, Read Community: {read_community}")
        
        result = check_ip_reachability(ip)
        if result:
            self.query_device(ip, read_community, cpu_utilization_oid)
        else:
            # IP不可达，尝试使用SSH连接查询设备
            _log._WARN(language.ip_not_connect)
            self.ssh_query_device(ip, read_community, cpu_utilization_oid)
    
    def query_device(self, device_ip, read_community, cpu_utilization_oid):
        try:
            _log._INFO(language.select_now)
            
            error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   CommunityData(read_community),
                   UdpTransportTarget((device_ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(cpu_utilization_oid)))
            )
            
            if error_indication:
                _log._ERROR(f"{language.SNMP_select_error}: {error_indication}")
            else:
                if error_status:
                    _log._ERROR(f"{language.SNMP_error_info}: {error_status.prettyPrint()}")
                else:
                    # return info
                    for var_bind in var_binds:
                        _log._INFO({var_bind[1]})
            
        except Exception as error:
            _log._ERROR(str(error))
    
    def ssh_query_device(self, device_ip, read_community, cpu_utilization_oid):
        try:
            # 创建SSH连接
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(device_ip, username=self.ssh_username, password=self.ssh_password, timeout=3)
            
            # 执行SNMP查询命令
            stdin, stdout, stderr = ssh_client.exec_command('snmpwalk -v 2c -c {} {} {}'.format(read_community, device_ip, cpu_utilization_oid))
            
            # return info
            for line in stdout:
                _log._INFO(line.strip())
            
            ssh_client.close()
            
        except Exception as error:
            _log._ERROR(str(error))


def check_ip_reachability(ip):
    try:
        _log._INFO(language.try_ip_connect)
        response_time = ping(ip, timeout=0.5)
        if response_time is not None:
            return True
        else:
            return False
    except Exception:
        return False
            
        
def service_while():
    while True:
        cmd = tool.terminal().lower()
        if cmd == "":
            continue
        elif cmd == "help":
            tool.help()
        elif cmd.split()[0] == "snmp" and len(cmd.split()) > 1:
            try:
                if cmd.split()[1] == "add":
                    try:
                        if len(cmd.split()) == 5:
                            devices.write([{"ip": str(cmd.split()[2]), "Read Community": str(cmd.split()[3]), "Write Community": str(cmd.split()[4])}])
                        elif len(cmd.split()) == 4:
                            devices.write([{"ip": str(cmd.split()[2]), "Read Community": str(cmd.split()[3]), "Write Community": str(cmd.split()[3])}])
                        else:
                            print("snmp add { IP } { Read Community } { Write Community }")
                    except Exception as error:
                            _log._ERROR(str(error))
                elif cmd.split()[1] == "delete":
                    devices.delete(cmd.split()[2])
                elif cmd.split()[1] == "reload":
                    _log._RUNNING("reload", language.reload_device)
                    devices.read()
                elif cmd.split()[2] == "all":
                    app.snmp_all(list_oid[cmd.split()[1]])
                else:
                    app.snmp_select(list_oid[cmd.split()[1]], cmd.split()[2])
            except:
                print("snmp { cmd } { ip }")
        elif cmd == "log clear":
            tool.clear_log()
        elif cmd == "shutdown":
            tool.shutdown()
            break
        else:
            print(language.not_exec)

if __name__ == "__main__":
    app = Mainapp()
    service_while()
    