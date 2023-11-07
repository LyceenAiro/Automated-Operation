from os import path, rename, makedirs, listdir
import datetime

class init_log:
    def __init__(self):
        if not path.exists("log"):
            makedirs("log")
        if path.exists(f"log/timmer.log"):
            # 将上一个未正常命名的日志文件重命名
            file_list = listdir("log")
            date = datetime.datetime.fromtimestamp(path.getmtime("log/timmer.log")).strftime('%y%m%d')
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
    
    def _RUNNING(self, app, string):
        # 操作信息
        INFO_Colors = "\033[1;32m"
        date = datetime.datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        with open(f"log/timmer.log", "a", encoding="utf-8") as file:
            file.write(f"{date}[{app}]\t{string}\n")
        print(f"{INFO_Colors}{date}[{app}]\033\t[0m{string}")
    
    def _INFO(self, string):
        # 日志信息
        INFO_Colors = "\033[1;36m"
        date = datetime.datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        with open(f"log/timmer.log", "a", encoding="utf-8") as file:
            file.write(f"{date}[INFO]\t{string}\n")
        print(f"{INFO_Colors}{date}[INFO]\033[0m\t{string}")

    def _WARN(self, string):
        # 警告信息
        INFO_Colors = "\033[1;33m"
        date = datetime.datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        with open(f"log/timmer.log", "a", encoding="utf-8") as file:
            file.write(f"{date}[WARN]\t{string}\n")
        print(f"{INFO_Colors}{date}[WARN]\033[0m\t{string}")

    def _ERROR(self, string):
        # 错误信息
        INFO_Colors = "\033[1;31m"
        date = datetime.datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        with open(f"log/timmer.log", "a", encoding="utf-8") as file:
            file.write(f"{date}[ERROR]\t{string}\n")
        print(f"{INFO_Colors}{date}[ERROR]\033[0m\t{string}")
    
    def _WRITE(self, string, type):
        # 静默写入
        if string == "":
            return
        elif "&" == string[0]:
            return
        date = datetime.datetime.now().strftime('[%y/%m/%d %H:%M:%S]')
        with open(f"log/timmer.log", "a", encoding="utf-8") as file:
            file.write(f"{date}[{type}]\t{string}\n")

_log = init_log()