from 发票处理.数据识别.PDF.PDF import PDFReader
from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库
from 发票处理.数据识别.OCR.OCR import OCR_PaddleOCR
from 发票处理.数据识别.结果整理 import Arrange_invoice
class 发票处理:

    def __init__(self, IP, 操作人):
        self.IP = IP
        self.操作人 = 操作人
    @staticmethod
    def 发票文件处理(发票ID, use_OCR):
        # 数据库查找对应ID的数据
        连接, 光标 = 连接数据库()

        光标.execute("SELECT * FROM invoice WHERE ID=%s", (发票ID,))
        查询的数据 = 光标.fetchall()
        关闭数据库(连接, 光标)
        识别结果 = None
        if ".pdf" in 查询的数据[0][4] and use_OCR == False:
            实例化发票 = PDFReader(f"data_upload_invoice/{查询的数据[0][4]}")
            读取结果 = 实例化发票.读取器()
            识别结果 = 读取结果.split("\n\n")
        elif use_OCR == True and ".pdf" in 查询的数据[0][4]:
            try:
                识别结果 = OCR_PaddleOCR.ocr_pdf(f"data_upload_invoice/{查询的数据[0][4]}")
            except:
                print("警告：未检测到OCR,无法进行OCR识别")
                return None
        else:
            try:
                识别结果 = OCR_PaddleOCR.ocr_image(f"data_upload_invoice/{查询的数据[0][4]}")
            except:
                print("警告：未检测到OCR,无法进行OCR识别")
                return None
        发票结果 = Arrange_invoice.get_invoice_info(识别结果)

        return 发票结果
    def 发票数据存入数据库(self, 发票结果, 发票ID):
        try:
            连接, 光标 = 连接数据库()
            sql = """
            INSERT INTO Invoice_Info (发票ID, 发票号码, 发票代码, 价税合计, 效验码, 发票类型, 开票日期, 交易内容)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            执行数据 = (发票ID, *发票结果)
            光标.execute(sql, 执行数据)
            连接.commit()
            关闭数据库(连接, 光标)
            记录日志(f"{发票ID}完成识别并写入数据库", self.IP, self.操作人)
        except:
            记录日志(f"{发票ID} 识别失败", self.IP, self.操作人)

    # def 处理(self):
    #     发票ID = 76
    #     数据 = self.发票文件处理(发票ID)
    #     self.发票数据存入数据库(数据, 发票ID)


# if __name__ == "__main__":
#     发票 = 发票处理("127.0.0.1", "Debug")
#     发票.Debug()
