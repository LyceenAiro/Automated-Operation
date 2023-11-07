# 语言本土化区域
class en_us:
    # Enghish
    # util.tools.py
    tools_help = """
    add { IP } { Community } { OID }\tAdd device configuration.\n
    snmp { cmd } { ip }\tRetrieve device log information via SNMP.\n
        cmd ---
            | add\tAdd device to device table
            | delete\tDelete device in device table
            | reload\tReload device table
            | sysdesc\tQuery system information
            | systime\tQuery system time
            | sysname\tQuery system name
            | ifnum\tQuery interface count
            | ifdesc\tQuery interface information
            | cpu \tQuery CPU information
            | cpu+\tQuery individual CPU information
            | ram\tQuery memory information
            | rom\tQuery storage information
        ip  ---
            | all\tQuery information filled in device table
            | { ip } { community }\tQuery specific device information\n
    log clear\tClear all log files
    shutdown\tExit program
    """
    service_stop = "Script was stopped."
    clear_log_about = "\033[0;31mAre you sure you want to clear all log files?(y/N)\033[0m"
    clear_log_num = ["Cleared in total", "log files"]

    # util.cfg.read.py
    cfg_read_success = "Configuration file read completed."

    # util.excel_read.py
    read_devices_head = "Network device info："
    not_find_devices = "Device configuration not found, please manually add configuration."
    success_add_device = "Successfully add device"
    was_delete = "Successfully deleted device"
    not_find = "Device not found."

    # main.py
    not_exec = "Command error, you can use 'help' to query the command."
    ip_not_connect = "Unable to connect directly through IP, attempting to connect using SSH."
    try_ip_connect = "Connect the device now..."
    select_now = "Querying now..."
    SNMP_select_error = "SNMP select error"
    SNMP_sekect_info = "SNMP error info"
    reload_device = "Reloading device table..."


class zh_cn:
    # 简体中文
    # util.tools.py
    tools_help = """
    add { IP } { Community } { OID }\t添加设备配置
    snmp { cmd } { ip }\t通过snmp获取设备log信息
        cmd ---
            | add\t添加设备到设备表中
            | delete\t从设备表中删除设备
            | reload\t重载设备表
            | sysdesc\t查询系统信息
            | systime\t查询系统时间
            | sysname\t查询系统名
            | ifnum\t查询接口数量
            | ifdesc\t查询接口信息
            | cpu \t查询cpu信息
            | cpu+\t查询每个cpu信息
            | ram\t查询内存信息
            | rom\t查询存储信息
        ip  ---
            | all\t查询设备表填写的信息
            | { ip } { community }\t 查询特定设备信息\n
    log clear\t清除所有log文件
    shutdown\t退出程序
    """
    service_stop = "程序已停止运行"
    clear_log_about = "\033[0;31m你确定要清除所有log文件吗?(y/N)\033[0m"
    clear_log_num = ["一共清除","个log文件"]

    # util.cfg.read.py
    cfg_read_success = "配置文件读取完毕"

    # util.excel_read.py
    read_devices_head = "设备表信息："
    not_find_devices = "没有找到设备配置，清手动添加配置"
    success_add_device = "成功添加配置"
    was_delete = "成功删除设备"
    not_find = "没有找到设备"

    # main.py
    not_exec = "命令错误，可以使用help来查询命令"
    ip_not_connect = "无法直接通过IP进行连接，尝试使用SSH进行连接"
    try_ip_connect = "正在连接设备"
    select_now = "正在查询"
    SNMP_select_error = "SNMP查询错误"
    SNMP_sekect_info = "SNMP错误状态"
    reload_device = "正在重新载入设备表"