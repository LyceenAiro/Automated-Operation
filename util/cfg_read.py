from os import path
from configparser import ConfigParser
import sys
from .log import _log


# Read config.cfg
class Config:

    def __init__(self):
        self.cfg = ConfigParser()
        if not path.exists('config.cfg'):
            self._create()
            print('[ERROR]config.cfg not found, the program will try to generate a new one.\n')
            input('Press enter to continue.')
            sys.exit(1)

        self.device_ip, self.snmp_community, self.cpu_utilization_oid, = self._read()
        
        _log._INFO('配置文件读取完毕')


    def _create(self):
        _cfg = open('config.cfg', 'w', encoding='utf-8')
        _cfg.write(
            '[path]\n'
            'device_ip = \n'
            'snmp_community = \n'
            'cpu_utilization_oid = \n'
        )
        _cfg.close()

    def _read(self):
        self.cfg.read('config.cfg', encoding='utf-8')
        device_ip = self.cfg.get('path', 'device_ip')
        snmp_community = self.cfg.get('path', 'snmp_community')
        cpu_utilization_oid = self.cfg.get('path', 'cpu_utilization_oid')

        return device_ip, snmp_community, cpu_utilization_oid


cfg = Config()
