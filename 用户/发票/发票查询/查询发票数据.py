from 数据库.联系数据库 import 连接数据库
import datetime

class 发票数据查询:

    @staticmethod
    def 获取数据(发票信息):
        数据 = []
        for i in 发票信息:
            # 查询数据库
            连接, 光标 = 连接数据库()
            光标.execute('SELECT * FROM Invoice_Info WHERE 发票ID = %s LIMIT 1', (i[0],))
            查询数据 = 光标.fetchone()

            数据.append([i[0], 查询数据])
        return 数据

# txt = ((75, '报销人1', 0, datetime.datetime(2024, 10, 2, 15, 3), '报销人1_20241002150300566172.pdf'), (76, '报销人1', 0, datetime.datetime(2024, 10, 2, 15, 3), '报销人1_20241002150300568682.pdf'), (77, '报销人1', 0, datetime.datetime(2024, 10, 2, 15, 3), '报销人1_20241002150300570242.pdf'), (78, '报销人1', 0, datetime.datetime(2024, 10, 2, 15, 3), '报销人1_20241002150300571663.pdf'), (79, '报销人1', 0, datetime.datetime(2024, 10, 4, 9, 50, 17), '报销人1_20241004095017314135.pdf'))
#
# 发票数据查询 = 发票数据查询()
# 发票数据查询.获取数据(txt)
