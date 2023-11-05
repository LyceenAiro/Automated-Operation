from os import path
import openpyxl

from util.log import _log
from util.cfg_read import cfg

import importlib
language = getattr(importlib.import_module("lang.language", package="lang"), cfg.app_language)

class Devices:
    def __init__(self):
        # 从Excel表格中读取配置
        if path.exists('devices.xlsx'):
            # 从Excel表格中读取配置
            devices = self.read()
            log_message = f"\n{language.read_devices_head}"
            for device in devices:
                log_message += f"\nIP: {device['ip']}, SNMP Community: {device['snmp_community']}, CPU Utilization OID: {device['cpu_utilization_oid']}"
            _log._INFO(log_message)
        else:
            devices = []
            _log._INFO(language.not_find_devices)

    
    def read(self):
        # 从Excel表格中读取配置
        workbook = openpyxl.load_workbook('devices.xlsx')
        sheet = workbook.active

        devices = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            device = {
                'ip': row[0],
                'snmp_community': row[1],
                'cpu_utilization_oid': row[2]
            }
            devices.append(device)

        return devices

    
    def write(self, devices):
        # 将配置写入Excel表格
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        sheet.append(['IP', 'SNMP Community', 'CPU Utilization OID'])
        for device in devices:
            sheet.append([device['ip'], device['snmp_community'], device['cpu_utilization_oid']])

        workbook.save('devices.xlsx')

devices = Devices()


    
