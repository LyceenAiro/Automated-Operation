from pysnmp.hlapi import *
from util.cfg_read import cfg
from util.log import _log

class Mainapp:

    try:
        _log._INFO("正在创建SNMP请求")
        # 设备信息
        device_ip = cfg.device_ip
        snmp_community = cfg.snmp_community

        # SNMP OID
        cpu_utilization_oid = cfg.cpu_utilization_oid  # 根据设备类型和MIB库进行调整

        # 创建SNMP请求
        snmp_object = ObjectIdentity(cpu_utilization_oid)
        snmp_target = ObjectIdentity(device_ip, snmp_community)
        snmp_varbind = ObjectType(snmp_object)

        _log._INFO("正在发送SNMP请求并获取响应")
        # 发送SNMP请求并获取响应
        snmp_response = getCmd(SnmpEngine(), CommunityData(snmp_community), UdpTransportTarget((device_ip, 161)),
                           ContextData(), snmp_varbind)

        # 处理SNMP响应
        errorIndication, errorStatus, errorIndex, varBinds = next(snmp_response)
        if errorIndication:
            print('SNMP请求错误:', errorIndication)
        elif errorStatus:
            print('SNMP错误状态:', errorStatus.prettyPrint())
        else:
            for varBind in varBinds:
                print('CPU利用率:', varBind.prettyPrint())

    except Exception as error:
        _log._ERROR(str(error))



if __name__ == "__main__":
    Mainapp()
    _log._INFO("程序已停止运行")