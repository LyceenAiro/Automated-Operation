from os import path
import sys
from configparser import ConfigParser

from util.log import _log

from importlib import import_module


# Read config.cfg
class Config:

    def __init__(self):
        self.cfg = ConfigParser()
        if not path.exists('config.cfg'):
            _log._INFO('配置文件未找到，正在初始化配置文件\n')
            self._create()

        self.app_language, self.app_debug,\
        self.log_max_size, self.log_level, \
        self.sql_ip, self.sql_port, self.sql_database, self.sql_user, self.sql_password \
        = self._read()
        
        language = getattr(import_module("lang.language", package="lang"), self.app_language)

        _log.max_file_size = self.log_max_size * 1024 * 1024
        _log.level = self.log_level

        _log._INFO(language.cfg_read_success)


    def _create(self):
        _cfg = open('config.cfg', 'w', encoding='utf-8')
        _cfg.write(
            '[app]\n'
            '# 配置前端语言(默认: zh_cn) [zh_cn: 中文, en_us: 英文]\n'
            'language = zh_cn\n'
            '# 是否启用开发者模式\n'
            'debug = false\n'
            '# 设置程序的最大递归长度, 线程维持运行需要\n'
            'setrecursionlimit = 1000\n'
            '\n'
            '\n'
            '[log]\n'
            '# 配置日志文件的最大大小(默认: 32, 单位: MB)\n'
            'max size = 32\n'
            '# 配置日志在前端显示的等级(默认: 3) [0: 关闭, 1: INFO, 2: WARN, 3: ERROR, 4: DEBUG]\n'
            'level = 3\n'
            '\n'
            '\n'
            '[sql]\n'
            '# 配置数据库IP地址\n'
            'ip = 127.0.0.1\n'
            '# 配置数据库端口\n'
            'port = 3306\n'
            '# 配置使用的数据库\n'
            'database = PyAoDHA\n'
            '# 配置数据库用户名\n'
            'user = PyAo_root\n'
            '# 配置数据库密码\n'
            'password = admin\n'
        )
        _cfg.close()

    def _read(self):
        try:
            self.cfg.read('config.cfg', encoding='utf-8')
            # app
            app_language = self.cfg.get('app', 'language')
            app_debug = self.cfg.getboolean('app', 'debug')
            app_setrecursionlimit = self.cfg.getint('app', 'setrecursionlimit')
            # log
            log_max_size = self.cfg.getint('log', 'max size')
            log_level = self.cfg.getint('log', 'level')
            # sql
            sql_ip = self.cfg.get('sql', 'ip')
            sql_port = self.cfg.get('sql', 'port')
            sql_database = self.cfg.get('sql', 'database')
            sql_user = self.cfg.get('sql', 'user')
            sql_password = self.cfg.get('sql', 'password')
        except Exception as error:
            _log._ERROR('读取配置文件出错，请检查配置或删除配置文件重新生成\n')
            _log._ERROR(error)
            input('Press enter to continue.')
            sys.exit(1)

        if not len(app_language) == 5 and not '_' in app_language:
            _log._ERROR('Language setting error.\n')
            input('Press enter to continue.')
            sys.exit(1)

        if app_setrecursionlimit >= 1:
            sys.setrecursionlimit(app_setrecursionlimit)
            _log._INFO(f"setrecursionlimit: {app_setrecursionlimit}")
        else:
            sys.setrecursionlimit(1000000)
            _log._ERROR("cfg.app_setrecursionlimit 的值设置的太小, 不生效")
            _log._INFO("setrecursionlimit: 1000000")

        return app_language, app_debug,\
        log_max_size, log_level,\
        sql_ip, sql_port, sql_database, sql_user, sql_password

cfg = Config()
