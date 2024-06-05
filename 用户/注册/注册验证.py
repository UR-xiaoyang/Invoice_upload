from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库
from 用户.注册.写入数据库 import 注册写入数据库

def 注册验证(用户名, 密码, 邮箱, 银行卡号, 开户行, 真实姓名, 部门名称, IP):
    # 检验邮箱是否注册
    try:
        # 连接到数据库
        数据库连接请求, cursor = 连接数据库()

        # 使用参数化查询来防止SQL注入
        # 查询用户名是否存在
        cursor.execute("SELECT * FROM user WHERE username = %s", (用户名))
        用户名存在 = cursor.fetchone() is not None

        # 根据查询结果进行后续处理
        if 用户名存在:
            记录日志(f"{IP}在试图注册已经注册的用户“{用户名}”", IP, "Login")
            return "用户存在"
        else:
            注册写入数据库(用户名, 密码, 邮箱, 银行卡号, 开户行, 真实姓名, 部门名称, IP)

    except Exception as e:
        # 如果发生错误，打印错误信息
        print(f"注册验证过程中发生错误: {e}")
        return "注册验证过程中发生错误，请稍后再试。"
    finally:
        # 关闭数据库连接
        关闭数据库(数据库连接请求, cursor)
