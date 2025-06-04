import mysql.connector
from util.pin import *
from util.log import _log
from util.cfg_read import cfg
from util.tools import tool
from util.register_module import script_dict
from util.pin import VersionLowError
from util.install_data import install_data

from os import system
import logging

from importlib import import_module
language = getattr(import_module("lang.language", package="lang"), cfg.app_language)

from ctypes import *

import logging
import readline
readline.set_completer_delims('')
readline.parse_and_bind("tab: complete")

from tqdm import TqdmExperimentalWarning
import warnings
import traceback

class Mainapp:
    def __init__(self):
        try:
            sql_test = mysql.connector.connect(**mysql_config(TIMEOUT=1))
            sql_cur = sql_test.cursor()
            sql_cur.execute("SHOW TABLES")
            _log._INFO("Mysql服务已连接")
        except Exception as error:
            _log._WRITE(error, "ERROR")
            _log._WARN(language.sql_not_connect)
        finally:
            try: sql_test.close()
            except: pass
        if cfg.app_debug:
            _log._WARN("开发者模式已启用")

    def script_packed_debug(self, cmd:str):
        try:
            module = script_dict[cmd.split()[0]]
            script_mode = module.api_import()
            if len(cmd.split()) > 1:
                if "sql" in script_mode:
                    app.script_api_sql(cmd, module)
                else:    
                    app.script_api(cmd, module)
            elif len(cmd.split()) == 1:
                module.help_note()
        except KeyboardInterrupt:
            _log._INFO(language.exit_script)
        except Exception as error:
            _log._WRITE(error, "ERROR")
            traceback.print_exc()

    def script_packed(self, cmd:str):
        # 打包获取函数的API接口，附加必要纠错功能
        try:
            module = script_dict[cmd.split()[0]]
            script_mode = module.api_import()
        except KeyError:
            _log._WARN(language.not_find_script)
            return
        except AttributeError:
            _log._WARN("脚本格式已经过时或无效，请更新脚本的格式")
            return
        if len(cmd.split()) > 1:
            try:
                if "sql" in script_mode:
                    app.script_api_sql(cmd, module)
                else:    
                    app.script_api(cmd, module)
            except TypeError:
                module.help_note()
            except ValueError as error:
                _log._ERROR(f"输入的参数错误了: {error}")
            except KeyboardInterrupt:
                _log._INFO(language.exit_script)
            except IndexError as error:
                _log._ERROR(f"输入的参数有误, 或数据库出现错误: {error}")
            except Exception as error:
                _log._ERROR(error)

        elif len(cmd.split()) == 1:
            module.help_note()

    def thread_kill(self, cmd:str):
        if len(cmd.split()) == 1: return
        elif cmd.split()[1] == "all" and tool.yes_or_no("确定关闭所有后台程序吗?"):
            ThreadManager.remove_all_thread()
        else:
            ThreadManager.remove_thread(cmd.split()[1])

    ##
    ## SCRIPT API
    ##

    def script_api(self, cmd:str, module):
        # 默认的API
        module.main(cmd)
    
    def script_api_sql(self, cmd:str, module):
        # 数据库专用接口，可以处理数据库常见错误
        # 附带一个数据库指针和提交接口
        # 自动销毁因为错误跳出而无法操作的指针
        try:
            with mysql.connector.connect(**mysql_config()) as sql_connect:
                sql_cursor = sql_connect.cursor()
                module.main(cmd, sql_connect, sql_cursor)
        except mysql.connector.Error as error:
            traceback.print_exc()
            if error.errno == 1146:
                _log._ERROR("数据库未初始化，请先初始化数据库再操作")
            elif error.errno == 1062:
                _log._ERROR("设备ip已经存在，无法添加该设备")
            else:
                _log._ERROR(error)
        except VersionLowError as error:
            _log._ERROR(error)
        
def service_while():
    # 前端交互界面
    while True:
        readline.set_completer(tool.input_complete())
        cmd = tool.terminal()
        try:
            cmd.split()[0]
        except IndexError:
            continue
        if cmd == "help":
            tool.help()
        elif cmd == "cfg_read":
            cfg._read()
        elif cmd == "cls":
            system("cls")
        elif cmd == "system":
            tool.system_info()
        elif cmd == "log_clear":
            tool.clear_log()
        elif cmd == "debug":
            if cfg.app_debug:
                _log._WARN("你已经处于开发者模式")
                continue
            opendebug = tool.yes_or_no("你确定要开启开发者模式吗?")
            if opendebug:
                cfg.app_debug = True
                _log._WARN("开发者模式已启用")
        elif cmd == "shutdown":
            tool.shutdown()
            break
        elif cmd == "top":
            ThreadManager.get_running_threads()
        elif cmd.split()[0] == "kill":
            app.thread_kill(cmd)
        else:
            if cfg.app_debug: app.script_packed_debug(cmd)
            else: app.script_packed(cmd)



if __name__ == "__main__":
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    warnings.simplefilter("ignore", TqdmExperimentalWarning)
    warnings.filterwarnings("ignore", message="Setting an item of incompatible dtype is deprecated", category=FutureWarning)
    logging.getLogger("httpx").propagate = False
    if not cfg.app_debug: system("cls")
    print(f"{install_data.softname}  LyceenAiro@2025  v{install_data.version}")
    app = Mainapp()
    service_while()
    