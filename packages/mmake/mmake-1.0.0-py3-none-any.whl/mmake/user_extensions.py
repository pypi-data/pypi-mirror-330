from mmake.parser import MMakeParser
from mmake.api import info, walk, error
import sys

# 定义用户自定义命令
def custom_greet(name):
    print(f"\033[1;33m[Custom] Hello, {name.strip('\"')}! Welcome to MMake.\033[0m")

def custom_list_files(directory):
    import os
    print(f"\033[1;33m[ListFiles] 列出目录中的文件：{directory.strip('\"')}\033[0m")
    for file in os.listdir(directory.strip('\"')):
        print(f"  - {file}")

# 创建解析器实例
parser = MMakeParser(sys.argv[1] + ".mmake")

# 注册内置命令
parser.register_plugin("info", info)
parser.register_plugin("walk", walk)
parser.register_plugin("error", error)

# 注册用户自定义命令
parser.register_plugin("greet", custom_greet)
parser.register_plugin("list_files", custom_list_files)

# 解析并执行文件
parser.parse()
