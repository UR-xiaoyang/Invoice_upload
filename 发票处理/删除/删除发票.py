from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库


class DeleteInvoice:
    @staticmethod
    def Delete(ID, IP, 操作人):

        try:
            连接, 光标 = 连接数据库()

            # 将is_used设置为1
            光标.execute("UPDATE invoice SET is_used=1 WHERE ID=%s", (ID,))
            连接.commit()
            关闭数据库(连接, 光标)
            记录日志(f"发票{ID}已删除", IP, 操作人)
            return f"发票{ID}已删除"
        except:
            记录日志(f"发票{ID}删除失败", IP, 操作人)
            return None

def Debug():
    debug = DeleteInvoice()
    debug.Delete(1, "127.0.0.1", "Debug")
# Debug()

