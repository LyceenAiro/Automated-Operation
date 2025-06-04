import script
from util.log import _log
from util.tools import tool

def get_module():
    _log._INFO(f"正在导入模块...")
    module_dict = {}
    module_names = []
    for module_name in dir(script):
        if not module_name.startswith('__') and not '_module' in module_name:
            module_dict[module_name] = getattr(script, module_name)
            module_names.append(module_name)
            _log._INFO(f"模块 {module_name} 导入成功")
    _log._INFO("正在生成模块索引...")
    tool.script_names = module_names
    _log._INFO("模块导入完毕")
    return module_dict

script_dict = get_module()

