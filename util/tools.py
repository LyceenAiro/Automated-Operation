from os import path, listdir, remove, makedirs
from datetime import datetime
import ipaddress

from util.cfg_read import cfg
from util.log import _log
from util.pin import ThreadManager
from util.install_data import install_data

from openpyxl import load_workbook
from openpyxl.styles import Alignment

from importlib import import_module
language = getattr(import_module("lang.language", package="lang"), cfg.app_language)

now_time = datetime.now().strftime("%Y-%m-%d")

class AppTool:
    def __init__(self):
        self.script_names = []

    def terminal(self):
        date = datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        try:
            cmd = input(f"\033[1;36m{date}Terminal>\033[0m")
        except KeyboardInterrupt:
            print("Ctrl + C")
            self.shutdown()
        except EOFError:
            print("Ctrl + D")
            self.shutdown()
        _log._WRITE(cmd, "input")
        return cmd
    
    def help(self):
        print(language.tools_help)

    def system_info(self):
        print(f"{install_data.softname}  LyceenAiro@2025  v{install_data.version}")

    def shutdown(self):
        _log._INFO(language.service_stop)
        ThreadManager.remove_all_thread()
        exit()
    
    def clear_log(self):
        # 清理log文件
        about = input(language.clear_log_about).lower()
        if about == "y" or about == "yes":
            clear_num = 0
            for file_name in listdir("log"):
                file_path = path.join("log", file_name)
                if path.isfile(file_path) and file_name != _log.path:
                    remove(file_path)
                    clear_num +=1
            _log._INFO(f"{language.clear_log_num[0]} {clear_num} {language.clear_log_num[1]}")

    def input_complete(self):
        # 获取对应词（触发器）
        completions = self.completions_get()
        def complete(text, state):
            options = [i for i in completions if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None
        return complete
    
    def is_valid_ipv4_address(self, address):
        try:
            ipaddress.IPv4Address(address)
            return True
        except ipaddress.AddressValueError:
            return False
    
    def completions_get(self):
        # 获取模块
        util_module = ["help", "shutdown", "cfg_read", "cls", "log_clear", "debug", "system", "top", "kill"]

        return util_module + self.script_names
    
    def yes_or_no(self, tell_str:str):
        # 询问是否确认
        input_str = input(tell_str)
        if input_str.lower() in ["y", "yes", "true", "iknow", "是", "对", "确认", "我知道了"]:
            return True
        else:
            return False
        
    def default_excel_index(self, file_path):
        book = load_workbook(file_path)
        sheet = book.active
        for cell in sheet['1']:
            cell.alignment = Alignment(horizontal='left')
            cell.border = None
            cell.font = None
        book.save(file_path)

    def QuickAccess(self, cmd: str, user_index: int, password_index: int):
        try: user = cmd.split()[user_index]
        except: 
            if cfg.qa_user == "0": raise TypeError("获取user字段时发生了错误")
            else: user = cfg.qa_user
        try: password = cmd.split()[password_index]
        except: 
            if cfg.qa_password == "0": raise TypeError("获取passowrd字段时发生了错误")
            else: password = cfg.qa_password
        return user, password
    
    def type_regiest(self, type: str, regiest_list: list):
        result_str = ""
        for i in regiest_list:
            if result_str != "":
                regiest_list += " OR "
            regiest_list += f"{type} = '{i}'"
        return regiest_list

tool = AppTool()