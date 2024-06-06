from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库

# 定义每页记录数
每页记录数 = 10

def 发票查询(用户, 页数, IP):
    try:
        连接, 光标 = 连接数据库()

        # 计算OFFSET值，注意页码通常从1开始，所以需要减1以得到正确的偏移量
        偏移量 = (页数 - 1) * 每页记录数

        # 调整SQL以包含分页逻辑
        命令 = "SELECT * FROM invoice WHERE upload_user = %s AND is_used = 0 ORDER BY is_used DESC LIMIT %s OFFSET %s"
        光标.execute(命令, (用户, 每页记录数, 偏移量))

        # 获取查询结果
        结果 = 光标.fetchall()

        记录日志(f"{用户}成功请求第{页数}页发票", IP, 用户)
        # 返回查询结果
        return 结果

    except Exception as e:
        # 异常处理逻辑，例如记录日志或抛出特定错误

        记录日志(f"{用户}请求第{页数}页发票出错", IP, 用户)
        print(f"发票查询出错: {e}")
        return None

    finally:
        # 确保数据库连接和光标被关闭
        关闭数据库(连接, 光标)
# def Debug():
#    # 调用发票查询函数
#    结果 = 发票查询("Debug", 2, "127.0.0.1")
#    # 打印查询结果
#    print(结果)
# Debug()