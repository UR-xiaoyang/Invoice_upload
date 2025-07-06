#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR结果解析器模块
负责从OCR识别出的原始文本中提取结构化的发票信息。
"""

import re
from datetime import datetime

class OcrParser:
    """
    一个用于从OCR文本中解析增值税发票信息的类。
    """
    def __init__(self, ocr_text_lines):
        """
        初始化解析器。
        :param ocr_text_lines: 一个包含OCR识别出的所有文本行的列表。
        """
        self.text_lines = ocr_text_lines
        self.full_text = "\n".join(ocr_text_lines)
        self.parsed_data = {}

        # 定义正则表达式
        self.patterns = {
            # 启发式: 发票号码是一长串数字，不依赖标签
            'invoice_number': re.compile(r'\b(\d{20})\b|\b(\d{18})\b'), # 优先匹配20位，然后18位
            # 发票代码: 10或12位数字，通常有明确标签
            'invoice_code': re.compile(r'(?:发票代码|代码)\s*[:：\s]\s*(\d{10,12})\b'),
            # 启发式: 直接查找日期格式，保持严格匹配，依赖预处理
            'issue_date': re.compile(r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'),
            # 允许跨行匹配的金额
            'total_amount_lower': re.compile(r'(?:价税合计|小写|金额)[\s\S]*?([¥￥\s]*[\d,]+\.\d{2})'),
        }

    def _pre_process_text(self, text):
        """预处理文本，清理常见的格式问题。"""
        # 移除行间的空格，方便正则匹配
        return re.sub(r'\s*\n\s*', '\n', text)

    def parse(self):
        """
        执行解析过程。
        """
        # 发票号码 - Heuristic: Find a long standalone number
        match = self.patterns['invoice_number'].search(self.full_text)
        if match:
            self.parsed_data['invoice_number'] = match.group(1) or match.group(2)

        # 发票代码
        match = self.patterns['invoice_code'].search(self.full_text)
        if match:
            self.parsed_data['invoice_code'] = match.group(1)

        # 开票日期 - Heuristic: Find the date format directly
        # 预处理: 修正常见的OCR错误, 如 `2024年01月158` -> `2024年01月15日`
        # 这个正则表达式寻找一个日期模式，该模式以一个数字结尾，并且这个数字是一个独立的"单词"
        date_fix_pattern = re.compile(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2})\d\b')
        fixed_text_for_date = date_fix_pattern.sub(r'\1日', self.full_text)
        
        match = self.patterns['issue_date'].search(fixed_text_for_date)
        if match:
            year, month, day = match.groups()
            self.parsed_data['issue_date'] = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

        # 金额 (小写) - 采用多策略查找以提高准确性
        amount_str = None

        # 策略1: 查找最明确的"(小写)"标签后的金额, 对OCR错误有一定容忍度
        # 匹配模式: `(小写)` 后跟任意非数字字符, 直到找到金额
        # 更新: 支持全角(（）)和半角(())括号, 并使用非贪婪匹配, 允许货币符号
        match = re.search(r'[\(（]小写[\)）][\s\S]*?([¥￥\s]*[\d,]+\.\d{2})', self.full_text)
        if match:
            amount_str = match.group(1)

        # 策略2: 如果策略1失败，查找"价税合计"后的金额
        if not amount_str:
            context_search = re.search(r'价\s*税\s*合计(.*)', self.full_text, re.IGNORECASE | re.DOTALL)
            if context_search:
                context = context_search.group(1)
                # 在'价税合计'后的文本里，查找所有数字金额
                amounts = re.findall(r'([\d,]+\.\d{2})', context)
                if amounts:
                    # 更新: 不再取最后一个金额，而是取找到的最大值，因为总额通常是最大的。
                    try:
                        cleaned_amounts = [float(a.replace(',', '')) for a in amounts]
                        if cleaned_amounts:
                            amount_str = f"{max(cleaned_amounts):.2f}"
                    except (ValueError, IndexError):
                        pass # 忽略转换或索引错误

        # 策略3: 如果前两种策略都失败，则在全文中查找所有可能的金额并取最大值
        if not amount_str:
            all_amounts = re.findall(r'([\d,]+\.\d{2})', self.full_text)
            if all_amounts:
                try:
                    cleaned_amounts = [float(a.replace(',', '')) for a in all_amounts]
                    if cleaned_amounts:
                        amount_str = str(max(cleaned_amounts))
                except (ValueError, IndexError):
                    pass # 忽略转换或索引错误

        if amount_str:
            cleaned_amount_str = amount_str.replace(',', '').replace('¥', '').replace('￥', '').strip()
            try:
                self.parsed_data['amount'] = float(cleaned_amount_str)
            except ValueError:
                print(f"无法解析最终确定的金额: {cleaned_amount_str}")
        
        # --- 购买方和销售方信息 (基于OCR读取顺序的启发式方法) ---
        # 假设：OCR工具通常按从左到右、从上到下的顺序读取文本。
        # 在大多数发票布局中，购买方信息位于销售方信息之前或之上。
        # 因此，我们假设找到的第一个公司名称是购买方，第二个是销售方（供应商）。
        
        # 查找所有可能是公司名称的行
        company_name_candidates = [
            line.strip().replace('名称:', '').replace('名称：', '') 
            for line in self.text_lines 
            if ("公司" in line or "有限" in line or "中心" in line or "大学" in line) 
            and "代码" not in line and len(line.strip()) > 5
        ]
        
        # 增加调试信息
        print(f"DEBUG: 找到 {len(company_name_candidates)} 个候选公司名称")
        if company_name_candidates:
            print(f"DEBUG: 候选列表 = {company_name_candidates}")
        
        # 根据候选公司的数量分配购买方和销售方
        if len(company_name_candidates) >= 2:
            self.parsed_data['purchaser'] = company_name_candidates[0]
            self.parsed_data['supplier'] = company_name_candidates[1]
            print(f"分配结果: 购买方='{self.parsed_data['purchaser']}', 销售方='{self.parsed_data['supplier']}'")
        elif len(company_name_candidates) == 1:
            # 如果只找到一个公司，我们无法确定它是购买方还是销售方。
            # 作为一个合理的默认值，我们将其分配给销售方，因为这通常是更关键的信息。
            # 用户可能需要在界面上进行手动更正。
            self.parsed_data['supplier'] = company_name_candidates[0]
            self.parsed_data['purchaser'] = '' # 留空
            print(f"警告: 只找到一个候选公司，已默认分配给销售方: '{company_name_candidates[0]}'")
        else:
            self.parsed_data['supplier'] = ''
            self.parsed_data['purchaser'] = ''
            print("警告: 未找到任何有效的候选公司名称。")
        
        # 发票类型
        self.parsed_data['invoice_type'] = '未知'
        if '电子' in self.full_text and '普通' in self.full_text:
            self.parsed_data['invoice_type'] = '电子普通发票'
        elif '电子' in self.full_text:
            self.parsed_data['invoice_type'] = '电子发票'
        elif '专用' in self.full_text:
            self.parsed_data['invoice_type'] = '增值税专用发票'
        elif '普通' in self.full_text:
            self.parsed_data['invoice_type'] = '增值税普通发票'

        # 项目名称 (启发式) - 查找第一个包含 '*' 的行
        self.parsed_data['item_name'] = ''
        for line in self.text_lines:
            if '*' in line:
                item_name = line.strip()
                # 简单的清理逻辑，移除一些常见的OCR错误前缀
                if item_name.startswith('尽'):
                    item_name = item_name[1:]
                self.parsed_data['item_name'] = item_name
                break

        # 为调试添加原始文本
        self.parsed_data['_raw_text'] = self.full_text

        # 为调试打印最终解析出的JSON
        import json
        print("--- Parsed Data ---")
        print(json.dumps(self.parsed_data, indent=2, ensure_ascii=False))
        print("-------------------")

        return self.parsed_data


if __name__ == '__main__':
    # 用于测试的伪造OCR文本
    fake_ocr_result = [
        "电子发瓢 (晋通发票)",
        "发票代码: 012345678910",
        "发票号码:  '25312000000131858850",
        "开票日期:  2025年05月048",
        "8海市税务扃",
        "名称:海南新清文化科技有限公司",
        "名称:上海荟选供应链管理有限公司",
        "琴",
        "隽",
        "统社会信用代码/纳税人识别号:91460108M4A948HC6",
        "信",
        "统-社会倍用代码/纳税人识别号:91310118M1JP9MG8卫",
        "项目名称",
        "规袼型号",
        "单  位",
        "数",
        "量",
        "金",
        "额",
        "税率/征收率",
        "税",
        "尽纸制品*打印纸",
        "件",
        "92.4557522123894",
        "184.91",
        "13%",
        "24.04",
        "垩184.91",
        "圣24.04",
        "价税合计 (大写)",
        ")贰佰零捌圆玖角伍分",
        "(小写)垩208.95",
        "开票人:  廖惠斌"
    ]
    parser = OcrParser(fake_ocr_result)
    data = parser.parse()
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False)) 