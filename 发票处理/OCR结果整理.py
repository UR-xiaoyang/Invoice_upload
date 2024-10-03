import re
from typing import List, Dict

class Arrange_invoice:
    @staticmethod
    def get_invoice_info(txt: List[str]) -> List[str]:
        # 初始化结果字典
        result = {
            '发票号码': '',
            '发票代码': '',
            '价税合计': '',
            '效验码': '',
            '发票类型': '',
            '开票日期': '',
            '交易内容': ''
        }

        # 定义正则表达式模式
        patterns = {
            '发票号码': r'发票号码[:：]\s*(\S+)',
            '发票代码': r'发票代码[:：]\s*(\S+)',
            '开票日期': r'开票日期[:：]\s*(\S+)',
            '校验码': r'校验码[:：]\s*(\S+)',
            '价税合计': r'[（(]小写[)）]\s*[:：￥¥]\s*(\S+)'
        }

        # 合并所有文本行
        full_text = ' '.join(line if isinstance(line, str) else line[0] for line in txt)

        # 使用正则表达式提取信息
        for key, pattern in patterns.items():
            match = re.search(pattern, full_text)
            if match:
                result[key if key != '校验码' else '效验码'] = match.group(1)

        # 处理特殊情况
        result['发票代码'] = result['发票代码'] or '电子发票'
        result['效验码'] = result['效验码'] or None
        result['发票类型'] = '电子发票' if result['发票代码'] == '电子发票' else '增值税发票'

        # 查找交易内容（包含多个 * 的行）
        result['交易内容'] = next((line for line in txt if isinstance(line, str) and line.count('*') > 1), '')

        # 返回结果列表
        return [result['发票号码'], result['发票代码'], result['价税合计'],
                result['效验码'], result['发票类型'], result['开票日期'], result['交易内容']]
