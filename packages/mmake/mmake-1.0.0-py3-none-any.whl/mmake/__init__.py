import os
from .args import get_args
from .parser import MMakeParser
from .Api import info, walk, error

def init():
    print("\033[1;33m[!] 本构建工具使用 Python MMake 库制作\033[0m\n")

def exists(file_path):
    if os.path.exists(file_path):
        print("\033[1;32m[!] 文件存在\033[0m\n")
        return True
    else:
        print("\033[1;31m[!] 文件不存在\033[0m")
        return False

def run():
    init()
    args = get_args()
    if len(args) < 2:
        print("\033[1;31m[!] 参数不足，请提供命令和文件目录路径。\033[0m")
        print("示例：python -m mmake <命令> <文件目录>")
        return

    command, directory = args[0], args[1]
    file_path = os.path.join(directory, f"{command}.mmake")
    if exists(file_path):
        parser = MMakeParser(file_path)
        parser.register_plugin("info", info)
        parser.register_plugin("walk", walk)
        parser.register_plugin("error", error)
        parser.parse()
