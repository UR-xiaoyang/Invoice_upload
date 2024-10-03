from datetime import datetime
from pathlib import Path
from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库

def 存储发票(上传文件, 用户名, IP):
    """
    直接保存上传的文件到本地，并在数据库记录基本信息。
    """
    try:
        # 创建或确认“上传的发票”目录存在
        上传目录 = Path("data_upload_invoice")
        上传目录.mkdir(parents=True, exist_ok=True)

        # 生成一个唯一的文件名
        文件名 = f"{用户名}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}{Path(上传文件.filename).suffix}"
        文件路径 = 上传目录 / 文件名

        # 保存文件到服务器
        with open(文件路径, 'wb') as f:
            f.write(上传文件.file.read())

        # 记录数据库
        try:
                数据库连接, cursor = 连接数据库()
                # 准备SQL语句
                sql = """
                INSERT INTO invoice (upload_user, is_used, upload_time, file_name)
                VALUES (%s, %s, %s, %s);
                """
                参数 = (用户名, 0, datetime.now(), 文件名)
                # 执行SQL插入
                cursor.execute(sql, 参数)
                数据库连接.commit()

                # 记录日志
                记录日志(f"发票图片上传成功：{文件名}", IP, 用户名)
        except Exception as e:
            记录日志(f"数据库操作错误：{e}", IP, 用户名)
            return False

        return 文件路径
    except Exception as e:
        记录日志(f"发票上传处理错误：{e}", IP, 用户名)
        return False
