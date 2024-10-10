import json

from 数据库.数据库配置 import Config
from 数据库.联系数据库 import 连接数据库, 关闭数据库


def 获取版本号():
    print("v20241011")

def 加载配置():
    with open('config.json') as f:
        return json.load(f)

def 初始化():
    print(">启动SERVER")
    获取版本号()
    配置 = 加载配置()
    print("服务器启动在:",配置["host"]+":"+str(配置["port"]))
    print("工作进程数量:", 配置["workers"])
    print("数据库服务器地址:", 配置["SQL_config"]["db_host"])
    print("数据库名称:", 配置["SQL_config"]["db_name"])
    Config.HOST = 配置["SQL_config"]["db_host"]
    Config.NAME = 配置["SQL_config"]["db_name"]
    Config.USER = 配置["SQL_config"]["db_user"]
    Config.PASSWORD = 配置["SQL_config"]["db_password"]
    Config.PORT = 配置["SQL_config"]["db_port"]
    try:
        连接, 光标 = 连接数据库()
        print("数据库连接成功")
        关闭数据库(连接, 光标)
    except:
        print("数据库连接失败")
        exit()

    return 配置




