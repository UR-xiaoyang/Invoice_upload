from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import bcrypt
import datetime

# 生成随机密钥
def 生成随机密钥():
    # 生成随机密钥
    import random
    import string
    # 随机长度10-15位
    长度 = random.randint(10, 15)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=长度))

def 注册写入数据库(用户名, 密码, 邮箱, 银行卡号, 开户行, 真实姓名, 部门名称, IP):
    try:
        # 连接到数据库
        数据库连接, cursor = 连接数据库()

        # 对密码进行哈希处理
        hash加密密码 = bcrypt.hashpw(密码.encode('utf-8'), bcrypt.gensalt())

        # 获取当前日期
        register_date = datetime.datetime.now().date()

        # 预生成2FA密钥
        随机密钥 = 生成随机密钥()

        # 执行SQL插入操作
        cursor.execute(
            "INSERT INTO user (username, password, register_date, email, bank_card_number, bank_name, real_name, department_name, 2fa_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (用户名, hash加密密码, register_date, 邮箱, 银行卡号, 开户行, 真实姓名, 部门名称, 随机密钥))

        # 提交事务
        数据库连接.commit()
        记录日志("注册成功", IP, 用户名)
    except Exception as e:
        # 如果发生错误，打印错误信息
        print(f"注册写入数据库时发生错误: {e}")
    finally:
        # 关闭数据库连接
        关闭数据库(数据库连接, cursor)


# 调用函数示例
#def debug():
#    注册写入数据库("Debug", "123456", "test@test.com", "666", "天地银行", "测试用户", "测试部门", "127.0.0.1")
#debug()
