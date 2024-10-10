import zipfile
import os

from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库


class 发票下载:
    def __init__(self, 操作人, IP):
        self.操作人 = 操作人
        self.IP = IP

    def 打包器(self, 文件列表):
        # 创建一个压缩文件
        with zipfile.ZipFile(f"临时文件/{self.操作人}.zip", 'w') as zipf:
            for 文件 in 文件列表:
                zipf.write(文件, os.path.basename(文件))
                记录日志(f"{文件}已打包发票", self.IP, self.操作人)
        return f"临时文件/{self.操作人}.zip"
    def 文件列表整理(self, ID列表):
        文件列表 = []

        连接, 光标 = 连接数据库()

        for ID in ID列表:
            # 查询对应的file_name
            光标.execute("SELECT file_name FROM invoice WHERE ID=%s", (ID,))
            结果 = 光标.fetchone()  # 获取单条结果
            if 结果:  # 确保查询到结果
                文件名 = 结果[0]  # 因为 fetchone() 返回一个元组，取第一项
                if os.path.exists(f"data_upload_invoice/{文件名}"):
                    文件列表.append(f"data_upload_invoice/{文件名}")
                else:
                    记录日志(f"{文件名} 文件不存在，跳过", self.IP, self.操作人)
            else:
                记录日志(f"ID为 {ID} 的发票记录未找到", self.IP, self.操作人)

        return 文件列表


def Debug():
    测试下载实例 = 发票下载("Debug", "127.0.0.1")
    文件列表 = 测试下载实例.文件列表整理([77,78,79])
    测试下载实例.打包器(文件列表)