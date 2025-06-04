from util.cfg_read import cfg
from datetime import datetime, timedelta
import ntplib
from uuid import uuid4

class ThreadManagerClass():
    ## 线程管理器
    ## 支持管理线程类的运行状态

    ## 需要在脚本中导入pin中已经创建的线程管理器，你也可以自己使用该类创建线程管理器
    ## from util.pin import ThreadManager -> 使用全局线程管理器
    ## from util.pin import ThreadManagerClass -> 创建一个新的线程管理器，用于多类型线程项目管理

    ## 线程管理器API
    ## self.add_thread({线程类}) -> 添加一个新的线程类到线程管理器，会给该线程绑定一个uuid
    ## self.remove_thread({uuid}) -> 通过uuid检索，关闭一个正在运行的线程
    ## self.remove_all_thread() -> 关闭该线程管理器中所有的线程
    ## self.get_running_threads() -> 查询线程管理器中所有线程的状态
    ## self.get_running_script() -> 检查某个脚本name是否在运行，会返回一个bool值
    ## self.remove_thread_name({name}) -> 关闭所有该名称的线程
    ## self. get_running_script({name}) -> 查询是否有该名称的线程运行


    def __init__(self, manager_name="None Name"):
        self.threads = {}
        self.manager_name = manager_name

    def add_thread(self, task_class):
        thread_id = str(uuid4())
        while thread_id in self.threads:
            thread_id = str(uuid4())
        thread = task_class(thread_id)
        self.threads[thread_id] = thread
        thread.start()
        return thread

    def remove_thread(self, thread_id):
        try:
            thread_info = self.threads.pop(thread_id)
            thread = thread_info
            thread.stop()
        except:
            pass

    def remove_thread_name(self, script_name: str):
        removeing_id = []
        for thread_id, thread_info in self.threads.items():
            if thread_info.name == script_name:
                removeing_id.append(thread_id)
        if removeing_id:
            for id in removeing_id:
                self.remove_thread(id)
                
    def remove_all_thread(self):
        for thread_id in list(self.threads.keys()):
            self.remove_thread(thread_id)

    def get_running_threads(self):
        print(f"{self.manager_name}\n")
        for thread_id, thread_info in dict(self.threads).items():
            try:
                running_time = datetime.now() - thread_info.create_time
                print(f"UUID: {thread_id}, 程序名: {thread_info.name}, 运行时长: {running_time}")
            except Exception as error:
                print(error)
                self.remove_thread(thread_id)

    def get_running_script(self, script_name: str):
        for thread_id, thread_info in self.threads.items():
            if thread_info.name == script_name:
                return True
        return False

def mysql_config(HOST=cfg.sql_ip, PORT=cfg.sql_port, DB=cfg.sql_database, USER=cfg.sql_user, PWD=cfg.sql_password, TIMEOUT=5):
    db_config = {
        'host': HOST,
        'port': PORT,
        'database': DB,
        'user': USER,
        'password': PWD,
        'connection_timeout': TIMEOUT
    }
    return db_config

def get_ntp_time(server: str, port: int = 123, reconnect: int = 2, timeout: int = 3):
    if reconnect >= 1:
        for _ in range(reconnect): # 重新连接来过滤丢包问题
            try:
                Client = ntplib.NTPClient()
                result = Client.request(server, port=port, version=3, timeout=timeout)
                return (datetime.utcfromtimestamp(result.tx_time) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') # +8h
            except:
                continue
    try:
        Client = ntplib.NTPClient()
        result = Client.request(server, port=port, version=3)
        return (datetime.utcfromtimestamp(result.tx_time) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') # +8h
    except:
        return None

class VersionLowError(Exception):
    # 低版本错误
    def __init__(self, message="version is too low, you must updata."):
        self.message = message
        super().__init__(self.message)

class FilterError(Exception):
    # 过滤触发错误
    def __init__(self, message="You data was filter."):
        self.message = message
        super().__init__(self.message)

ThreadManager = ThreadManagerClass("全局线程")