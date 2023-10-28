# 这是一个示例 Python 脚本。
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import message_handler
import asyncio

import os
import importlib


def import_plugins(plugin_folder=os.path.join(os.path.dirname(__file__), 'plugin')):
    # 获取插件文件夹的绝对路径

    # 遍历插件文件夹下的所有子文件夹
    for folder_name in os.listdir(plugin_folder):
        plugin_path = os.path.join(plugin_folder, folder_name)

        # 检查子文件夹是否是一个包（包含 __init__.py 文件）
        if os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, '__init__.py')):
            # 动态导入子文件夹下的所有模块
            for filename in os.listdir(plugin_path):
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = f'plugin.{folder_name}.{filename[:-3]}'  # 构建模块名称
                    importlib.import_module(module_name)
                    print(f"已导入{module_name}")

            # 导入子文件夹本身并执行其 __init__.py 文件
            importlib.import_module(f'plugin.{folder_name}')
            print(f"已导入{folder_name}")
