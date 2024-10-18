from 发票处理.数据识别.结果整理 import Arrange_invoice


class PDFReader:
    def __init__(self, file_path):
        self.file_path = file_path
    def 读取器(self):

        from pdfminer.high_level import extract_text

        文本内容 = extract_text(self.file_path)
        return 文本内容


def Debug():
    #PDF读取实例 = PDFReader('data_upload_invoice/报销人1_20241006204925110312.pdf')

    PDF读取实例 = PDFReader('data_upload_invoice/报销人1_20241013001026062593.pdf')

    读取内容 = PDF读取实例.读取器()
    print(读取内容)
    结果 = Arrange_invoice.get_invoice_info(读取内容)
    print(结果)

