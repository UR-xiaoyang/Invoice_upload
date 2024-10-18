
class Arrange_invoice:
    @staticmethod
    def get_invoice_info(txt):
        发票号码 = ""
        发票代码 = ""
        价税合计 = ""
        效验码 = ""
        发票类型 = ""
        开票日期 = ""
        交易内容 = ""
        for i in range(len(txt)):
            try:
                if "发票代码" in txt[i]:
                    发票代码 = txt[i].split("：")[1]
                    if 发票代码 == "":
                        发票代码 = txt[i].split(": ")[1]
                if "发票号码" in txt[i]:
                    发票号码 = txt[i].split("：")[1]
                    if 发票号码 == "":
                        发票号码 = txt[i].split(": ")[1]
                if "开票日期" in txt[i]:
                    开票日期 = txt[i].split("：")[1]
                    if 开票日期 == "":
                        开票日期 = txt[i].split(": ")[1]
                if "校验码" in txt[i]:
                    效验码 = txt[i].split("：")[1]
                    if 效验码 == "":
                        效验码 = txt[i].split(": ")[1]
                if txt[i].count("*") >= 2 and "<" not in txt[i] and ">" not in txt[i] and 交易内容 == "" :
                    交易内容 = txt[i]
                if "小写" in txt[i]:
                    价税合计 = txt[i][5:]

            except IndexError:
                if "发票代码" in txt[i] and 发票代码 == "":
                    发票代码 = txt[i + 1]
                elif "发票号码" in txt[i] and 发票号码 == "":
                    发票号码 = txt[i + 1]
                elif "开票日期" in txt[i] and 开票日期 == "":
                    开票日期 = txt[i + 1]
                elif "校验码" in txt[i] and 效验码 == "":
                    效验码 = txt[i + 1]
                elif "小写" in txt[i] and 价税合计 == "":
                    价税合计 = txt[i + 1][1:]
        for i in range(len(txt)):
            if "发票代码" in txt[i] and 发票代码 == "":
                发票代码 = txt[i + 1]
            elif "发票号码" in txt[i] and 发票号码 == "":
                发票号码 = txt[i + 1]
            elif "开票日期" in txt[i] and 开票日期 == "":
                开票日期 = txt[i + 1]
            elif "校验码" in txt[i][0] and 效验码 == "":
                效验码 = txt[i + 1]
            elif "小写" in txt[i] and 价税合计 == "":
                价税合计 = txt[i + 1][1:]
        if 发票代码 == "":
            发票代码 = "电子发票"
        if 效验码 == "":
            效验码 = None
        if 发票类型 == "" and 发票代码 == "电子发票":
            发票类型 = "电子发票"
        elif 发票代码 != "电子发票":
            发票类型 = "增值税发票"
        结果 = [发票号码, 发票代码, str(价税合计), 效验码, 发票类型, 开票日期, 交易内容]
        for i in range(len(结果)):
            if "：" in str(结果[i]):
                结果[i] = 结果[i].replace("：", "")
            if "\n" in str(结果[i]):
                结果[i] = str(结果[i].split("\n")[1:])
        # 检查发票号码是否存在非数字的字符
        if any(i.isdigit() for i in 结果[0]) == False:
            for i in range(len(txt[-1])):
                if txt[-1][i] == "年":
                    结果[0] = txt[-1][i-4-20:i-4]
        # 检查发票发票日期是否不存在数字
        if any(i.isdigit() for i in 结果[5]) == False:
            for i in range(len(txt[-1])):
                if txt[-1][i] == "年":
                    结果[5] = txt[-1][i-4:i+6]

        # 检查是否有数字
        if any(i.isdigit() for i in 结果[2]) == False:
            for i in range(len(txt[-1])):
                前 = 0
                后 = 0
                if txt[-1][i] == "¥":
                    结果[2] = txt[-1][i-4:i]
                    前 = i
                if txt[-1][i] == ".":
                    后 = i
                结果[2] = txt[-1][前:后]
        if "¥" in 结果[2]:
            结果[2] = 结果[2].split("¥")[1]

        return 结果