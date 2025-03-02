import re

class MMakeParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.plugins = {}  # 用户自定义插件

    def register_plugin(self, name, func):
        """注册用户自定义插件"""
        self.plugins[name] = func

    def parse(self):
        """解析 .mmake 文件"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    match = re.match(r"(\w+)\((.*)\)", line)
                    if match:
                        command, args = match.groups()
                        args = args.strip()
                        if command in self.plugins:
                            self.plugins[command](args)
                        else:
                            print(f"\033[1;31m[!] 未知指令：{line}\033[0m")
                    else:
                        print(line)
        except FileNotFoundError:
            print(f"\033[1;31m[!] 文件不存在：{self.file_path}\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] 解析文件时出错：{e}\033[0m")
