import os
import sys

def info(message):
    print(f"\033[1;34m[INFO] {message.strip('\"')}\033[0m")

def walk(directory):
    print(f"\033[1;32m[Walk] 遍历目录：{directory.strip('\"')}\033[0m")
    for root, dirs, files in os.walk(directory.strip('\"')):
        print(f"目录：{root}")
        for file in files:
            print(f"  文件：{file}")

def error(message):
    print(f"\033[1;31m[ERROR] {message.strip('\"')}\033[0m")
    sys.exit(1)
