import sys

def get_args():
    """获取命令行参数"""
    args = sys.argv[1:]
    if len(args) < 2:
        print("\033[1;31m[!] 参数不足，请提供命令和文件目录路径。\033[0m")
        print("示例：python -m mmake <命令> <文件目录>")
        sys.exit(1)
    return args
