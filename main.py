from pysnmp.hlapi import *
import netmiko
from ping3 import ping
from util.log import _log
from util.cfg_read import cfg
from util.excel_read import devices
from util.tools import tool
from util.list import list_oid
from os import path, makedirs, listdir

from importlib import import_module
language = getattr(import_module("lang.language", package="lang"), cfg.app_language)

class Mainapp:
    def __init__(self):
        if not path.exists("script"):
            makedirs("script")
    
    ##
    ## NETMIKO SELECT
    ##

    def netmiko_script(self, cmd):
        try:
            module = import_module(f'script.{cmd.split()[1]}')
            for device in devices.devices:
                if not device['ip'] == cmd.split()[2]:
                    continue
                ssh_setting = {
                    'device_type': 'huawei',
                    'ip': device['ip'],
                    'username': device['ssh_name'],
                    'password': device['ssh_password'],
                    'secret': device['secret'],
                    }
                break
            
        except:
            _log._ERROR(language.not_find_script)
        try:
            module.main(ssh_setting, cmd)
        except TypeError:
            _log._ERROR("参数输入错误")
        except Exception as error:
            _log._ERROR(error)

    ##
    ## PYSNMP SELECT
    ##

    def snmp_all(self, cpu_utilization_oid):
        # 查询所有设备
        try:
            for device in devices.devices:
                device_ip = device['ip']
                read_community = device['read_community']
                self.snmp_select(device_ip, read_community, cpu_utilization_oid)
                
        except Exception as error:
            _log._ERROR(str(error))
    
    def snmp_select(self, ip, read_community, cpu_utilization_oid):
        # 使用snmp时查询是否可以直接通过ip连接设备
        _log._RUNNING(cpu_utilization_oid, f"IP: {ip}, Read Community: {read_community}")
        
        result = check_ip_reachability(ip)
        if result:
            self.query_device(ip, read_community, cpu_utilization_oid)
        else:
            # IP不可达，提示用户使用ssh查询
            _log._WARN(language.ip_not_connect)
    
    def query_device(self, device_ip, read_community, cpu_utilization_oid):
        # 查询流程
        try:
            _log._INFO(language.select_now)
            
            oid = cpu_utilization_oid
            down_num = 0 
            
            while True:

                error_indication, error_status, error_index, var_binds = next(
                    getCmd(SnmpEngine(),
                        CommunityData(read_community),
                        UdpTransportTarget((device_ip, 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid))
                    )
                )
                
                if error_indication:
                    _log._ERROR(f"{language.SNMP_select_error}: {error_indication}")
                    break
                else:
                    if error_status:
                        _log._ERROR(f"{language.SNMP_error_info}: {error_status.prettyPrint()}")
                        break
                    else:
                        for var_bind in var_binds:
                            out_var = var_bind[1]
                            
                        if out_var:
                            _log._RUNNING(oid, var_bind[1])
                        # 设置空白超时项
                        elif down_num < 2:
                            down_num += 1
                        else:
                            break
                    
                oid = oid.rsplit('.', 1)[0] + '.' + str(int(oid.rsplit('.', 1)[1]) + 1)
            
        except Exception as error:
            _log._ERROR(str(error))
    


def check_ip_reachability(ip):
    # 查询ip是否可达
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
    # 前端交互界面
    while True:
        cmd = tool.terminal().lower()
        if cmd == "":
            continue
        elif cmd == "help":
            tool.help()
        elif cmd.split()[0] == "net":
            if len(cmd.split()) > 2:
                app.netmiko_script(cmd)
            elif len(cmd.split()) == 2:
                module = import_module(f'script.{cmd.split()[1]}')
                module.help_note()
            elif len(cmd.split()) == 1:
                for filename in listdir("script"):
                    try:
                        if filename.split(".")[1] == "py":
                            print(filename.split(".")[0])
                    except:
                        pass
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
    