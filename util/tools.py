from os import path, listdir, rename
import datetime

from util.cfg_read import cfg
from util.log import _log

import importlib
language = getattr(importlib.import_module("lang.language", package="lang"), cfg.app_language)

class AppTool:
    def terminal(self):
        date = datetime.datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        cmd = input(f"\033[1;36m{date}Terminal>\033[0m")
        _log._WRITE(cmd, "input")
        return cmd
    
    def help(self):
        print(language.tools_help)

    def shutdown(self):
        _log._INFO(language.service_stop)
        if path.exists(f"log/timmer.log"):
            # 日志文件命名
            file_list = listdir("log")
            date = datetime.datetime.now().strftime('%y%m%d')
            prefix = f"timmer{date}"

            suffixes = []
            for filename in file_list:
                if filename.startswith(prefix):
                    suffix = filename[len(prefix): -4]
                    suffixes.append(suffix)
            
            if not suffixes:
                new_suffix = "000"
            else:
                max_suffix = max(suffixes)
                new_suffix = str(int(max_suffix) + 1).zfill(len(max_suffix))
            new_filename = prefix + new_suffix + ".log"
            
            rename(f"log/timmer.log", f"log/{new_filename}")

tool = AppTool()