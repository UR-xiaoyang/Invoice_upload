#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自定义发票对话框模块
用于添加或编辑发票信息
"""
import os
from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QDateEdit, QDoubleSpinBox,
                               QComboBox, QTextEdit, QWidget, QPushButton, QFileDialog,
                               QHBoxLayout, QMessageBox, QFormLayout, QScrollArea, QFrame)
from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtGui import QIcon

from src.services.ocr_service import OcrService
from src.services.pdf_text_service import PdfTextService

class InvoiceDialog(QDialog):
    """添加或编辑发票的对话框"""
    # Signal to indicate that OCR processing is complete
    ocr_finished = Signal(dict)

    def __init__(self, parent=None, invoice_data=None):
        super().__init__(parent)
        self.setWindowTitle("编辑发票" if invoice_data else "添加新发票")

        self.invoice_data = invoice_data
        self.original_file_path = invoice_data.get('file_path') if invoice_data else None
        
        self.setup_ui()
        if self.invoice_data:
            self.load_data()
        
        # Initialize Services
        self.ocr_service = OcrService()
        self.ocr_service.ocr_finished.connect(self.on_process_finished)
        self.ocr_service.ocr_error.connect(self.on_process_error)
        
        self.pdf_text_service = PdfTextService()
        self.pdf_text_service.extraction_finished.connect(self.on_process_finished)
        self.pdf_text_service.extraction_error.connect(self.on_process_error)

    def setup_ui(self):
        """设置用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 创建一个可滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # 创建用于滚动区域内容的容器
        content_widget = QWidget()
        content_widget.setObjectName("dialogContent")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        # --- OCR Section ---
        ocr_widget = QWidget()
        ocr_layout = QHBoxLayout(ocr_widget)
        ocr_layout.setContentsMargins(0,0,0,0)
        
        self.upload_button = QPushButton("📄 上传并识别(OCR)")
        self.upload_button.setIcon(QIcon.fromTheme("document-open"))
        self.upload_button.setFixedHeight(40)
        self.upload_button.setToolTip("适用于扫描件或图片格式的发票，速度较慢。")
        
        self.quick_extract_button = QPushButton("⚡️ 从PDF快速提取")
        self.quick_extract_button.setIcon(QIcon.fromTheme("text-x-generic"))
        self.quick_extract_button.setFixedHeight(40)
        self.quick_extract_button.setToolTip("仅适用于包含文本的PDF文件，速度快，准确率高。")

        self.ocr_status_label = QLabel("")
        self.ocr_status_label.setProperty("class", "caption")

        ocr_layout.addWidget(self.upload_button)
        ocr_layout.addWidget(self.quick_extract_button)
        ocr_layout.addWidget(self.ocr_status_label)
        ocr_layout.addStretch()
        
        content_layout.addWidget(ocr_widget)

        # --- Form Section ---
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(12)
        
        self.invoice_code_input = QLineEdit()
        self.invoice_number_input = QLineEdit()
        self.supplier_input = QLineEdit()
        self.issue_date_input = QDateEdit(QDate.currentDate())
        self.issue_date_input.setCalendarPopup(True)
        self.issue_date_input.setDisplayFormat("yyyy-MM-dd")
        
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 9999999.99)
        self.amount_input.setPrefix("¥ ")

        self.invoice_type_input = QLineEdit()
        self.item_name_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["办公用品", "差旅交通", "餐饮招待", "技术服务", "其他"])
        self.category_input.setEditable(True)
        
        self.status_input = QComboBox()
        self.status_input.addItems(["未使用", "已使用"])
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("添加备注信息...")
        self.notes_input.setMinimumHeight(80)

        form_layout.addRow("发票代码:", self.invoice_code_input)
        form_layout.addRow("发票号码:", self.invoice_number_input)
        form_layout.addRow("供应商:", self.supplier_input)
        form_layout.addRow("开票日期:", self.issue_date_input)
        form_layout.addRow("金额:", self.amount_input)
        form_layout.addRow("发票类型:", self.invoice_type_input)
        form_layout.addRow("项目名称:", self.item_name_input)
        form_layout.addRow("分类:", self.category_input)
        form_layout.addRow("状态:", self.status_input)
        form_layout.addRow("备注:", self.notes_input)
        
        content_layout.addLayout(form_layout)
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(content_widget)
        
        # 将滚动区域添加到主布局
        main_layout.addWidget(scroll_area)
        
        # --- Dialog Buttons ---
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.on_accept)
        button_box.rejected.connect(self.reject)
        
        self.upload_button.clicked.connect(self.run_ocr)
        self.quick_extract_button.clicked.connect(self.run_quick_extract)
        
        main_layout.addWidget(button_box)
        
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)

    def run_ocr(self):
        """Handle the OCR process."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择发票文件", "", "发票文件 (*.png *.jpg *.jpeg *.bmp *.pdf)")

        if file_path:
            self.upload_button.setEnabled(False)
            self.quick_extract_button.setEnabled(False)
            self.ocr_status_label.setText("... 识别中 ...")
            self.ocr_service.start_ocr(file_path)

    def run_quick_extract(self):
        """Handle the quick text extraction from PDF."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择PDF发票文件", "", "PDF文件 (*.pdf)")
        
        if file_path:
            self.upload_button.setEnabled(False)
            self.quick_extract_button.setEnabled(False)
            self.ocr_status_label.setText("... 快速提取中 ...")
            self.pdf_text_service.start_extraction(file_path)

    def on_process_finished(self, parsed_data, file_path):
        """通用插槽，用于处理任何后台服务成功完成的情况。"""
        self.upload_button.setEnabled(True)
        self.quick_extract_button.setEnabled(True)
        self.ocr_status_label.setText("✅ 处理完成")
        self.load_data(parsed_data)
        # 保存文件路径以备后用
        self.original_file_path = file_path

    def on_process_error(self, error_message, file_path):
        """通用插槽，用于处理任何后台服务失败的情况。"""
        self.upload_button.setEnabled(True)
        self.quick_extract_button.setEnabled(True)
        self.ocr_status_label.setText(f"❌ 操作失败")
        QMessageBox.critical(self, "处理错误", f"处理文件 '{os.path.basename(file_path)}' 时发生错误:\n{error_message}")

    def on_accept(self):
        """Validate input and accept the dialog."""
        if not self.invoice_number_input.text().strip():
            QMessageBox.warning(self, "输入错误", "发票号码不能为空。")
            self.invoice_number_input.setFocus()
            return

        if not self.supplier_input.text().strip():
            QMessageBox.warning(self, "输入错误", "供应商不能为空。")
            self.supplier_input.setFocus()
            return
            
        self.accept()

    def closeEvent(self, event):
        self.ocr_service.stop_process()
        self.pdf_text_service.stop_process()
        super().closeEvent(event)
        
    def load_data(self, data=None):
        """加载数据到表单。如果未提供数据，则使用 self.invoice_data。"""
        source_data = data or self.invoice_data
        if not source_data:
            return

        self.invoice_code_input.setText(source_data.get('invoice_code', ''))
        self.invoice_number_input.setText(source_data.get('invoice_number', ''))
        self.supplier_input.setText(source_data.get('supplier', ''))
        
        date_str = source_data.get('issue_date', '')
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        self.issue_date_input.setDate(date if date.isValid() else QDate.currentDate())
        
        self.amount_input.setValue(float(source_data.get('amount', 0.0)))
        self.status_input.setCurrentText(source_data.get('status', '未使用'))
        self.notes_input.setText(source_data.get('notes', ''))
        self.invoice_type_input.setText(source_data.get('invoice_type', ''))
        self.item_name_input.setText(source_data.get('item_name', ''))
        self.category_input.setCurrentText(source_data.get('category', ''))

    def get_data(self):
        """获取对话框中的数据"""
        data = {
            "invoice_code": self.invoice_code_input.text(),
            "invoice_number": self.invoice_number_input.text(),
            "supplier": self.supplier_input.text(),
            "issue_date": self.issue_date_input.date().toString("yyyy-MM-dd"),
            "amount": self.amount_input.value(),
            "notes": self.notes_input.toPlainText(),
            "invoice_type": self.invoice_type_input.text(),
            "item_name": self.item_name_input.text(),
            "category": self.category_input.currentText(),
            "status": self.status_input.currentText()
        }
        if self.invoice_data and 'id' in self.invoice_data:
            data['id'] = self.invoice_data['id']
        
        # 包含原始文件路径
        if self.original_file_path:
            data['file_path'] = self.original_file_path
        
        return data