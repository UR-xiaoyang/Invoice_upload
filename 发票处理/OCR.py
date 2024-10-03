from paddleocr import PaddleOCR

class OCR_PaddleOCR:
    def ocr_image(img_path):
        结果 = []
        # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
        # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        result = ocr.ocr(img_path, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                结果.append(line[1][0])
        return 结果

    def ocr_pdf(pdf_path):
        结果 = []
        PAGE_NUM = 1  # 将识别页码前置作为全局，防止后续打开pdf的参数和前文识别参数不一致 / Set the recognition page number
        # ocr = PaddleOCR(use_angle_cls=True, lang="ch", page_num=PAGE_NUM)  # need to run only once to download and load model into memory
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", page_num=PAGE_NUM,
                        use_gpu=0)  # 如果需要使用GPU，请取消此行的注释 并注释上一行 / To Use GPU,uncomment this line and comment the above one.
        result = ocr.ocr(pdf_path, cls=True)

        for idx in range(len(result)):
            res = result[idx]
            if res == None:  # 识别到空页就跳过，防止程序报错 / Skip when empty result detected to avoid TypeError:NoneType

                continue
            for line in res:
                结果.append(line[1][0])
        return 结果
