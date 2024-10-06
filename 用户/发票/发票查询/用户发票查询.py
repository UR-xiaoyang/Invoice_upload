from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库

def 发票查询(用户, IP):
    try:
        连接, 光标 = 连接数据库()

        # 去除分页逻辑，只保留基本的查询
        命令 = "SELECT * FROM invoice WHERE upload_user = %s AND is_used = 0 ORDER BY is_used DESC"
        光标.execute(命令, (用户,))

        # 获取查询结果
        结果 = 光标.fetchall()

        记录日志(f"{用户}成功请求所有发票", IP, 用户)
        # 返回查询结果
        return 结果

    except Exception as e:
        # 异常处理逻辑，例如记录日志或抛出特定错误

        记录日志(f"{用户}请求发票时出错", IP, 用户)
        print(f"发票查询出错: {e}")
        return None

    finally:
        # 确保数据库连接和光标被关闭
        关闭数据库(连接, 光标)
