# 语言本土化区域
class en_us:
    # Enghish
    # util.tools.py
    tools_help = """
    add { IP } { Community } { OID }\tAdd network device config.\n
    snmp_log\tGet log info from snmp.\n
    shutdown\tExit script.\n
    """
    service_stop = "Script was stopped."

    # util.cfg.read.py
    cfg_read_success = "Configuration file read completed."

    # util.excel_read.py
    read_devices_head = "Network device info："
    not_find_devices = "Device configuration not found, please manually add configuration."
    success_add_device = "Successfully add device:"

    # main.py
    not_exec = "Command error, you can use 'help' to query the command."
    ip_not_connect = "Unable to connect directly through IP, attempting to connect using SSH."
    try_ip_connect = "Connect the device now..."
    select_now = "Querying now..."


class zh_cn:
    # 简体中文
    # util.tools.py
    tools_help = """
    add { IP } { Community } { OID }\t添加设备配置\n
    snmp_log\t通过snmp获取设备log信息\n
    shutdown\t退出脚本\n
    """
    service_stop = "程序已停止运行"

    # util.cfg.read.py
    cfg_read_success = "配置文件读取完毕"

    # util.excel_read.py
    read_devices_head = "设备表信息："
    not_find_devices = "没有找到设备配置，清手动添加配置"
    success_add_device = "成功添加配置:"

    # main.py
    not_exec = "命令错误，可以使用help来查询命令"
    ip_not_connect = "无法直接通过IP进行连接，尝试使用SSH进行连接"
    try_ip_connect = "正在连接设备"
    select_now = "正在查询"