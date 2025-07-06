#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
现代化按钮组件模块
负责处理操作按钮的功能，采用现代化设计
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon


class ButtonWidget(QWidget):
    """现代化按钮组件"""
    
    # 定义信号
    add_clicked = Signal()      # 添加按钮点击信号
    edit_clicked = Signal()     # 编辑按钮点击信号
    delete_clicked = Signal()   # 删除按钮点击信号
    export_clicked = Signal()   # 导出按钮点击信号
    batch_scan_clicked = Signal()
    verify_clicked = Signal()   # 查验按钮点击信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局
        layout = QHBoxLayout(self)
        layout.setSpacing(12)  # 增加按钮间距
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建按钮 - 使用更现代的文本和图标
        self.add_btn = QPushButton("➕ 添加发票")
        self.add_btn.setIcon(QIcon.fromTheme("list-add"))
        
        self.batch_scan_btn = QPushButton("📂 批量扫描")
        self.batch_scan_btn.setIcon(QIcon.fromTheme("document-open-multiple"))
        self.batch_scan_btn.setToolTip("批量上传并识别多个发票文件 (图片或PDF)")
        
        self.edit_btn = QPushButton("✏️ 编辑")
        self.edit_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.delete_btn = QPushButton("🗑️ 删除发票")
        self.export_btn = QPushButton("📤 导出数据")
        self.verify_btn = QPushButton("🔍 发票查验")
        self.verify_btn.setIcon(QIcon.fromTheme("system-search"))
        
        # 设置按钮样式类型
        self.add_btn.setProperty("buttonType", "success")
        self.edit_btn.setProperty("buttonType", "warning")
        self.delete_btn.setProperty("buttonType", "danger")
        self.export_btn.setProperty("buttonType", "secondary")
        self.verify_btn.setProperty("buttonType", "secondary")
        
        # 设置按钮提示文本
        self.add_btn.setToolTip("添加新的发票记录")
        self.edit_btn.setToolTip("编辑选中的发票记录")
        self.verify_btn.setToolTip("打开网站查验选中的发票")
        self.delete_btn.setToolTip("删除选中的发票记录")
        self.export_btn.setToolTip("导出发票数据到文件")
        
        # 设置按钮最小宽度
        button_min_width = 120
        self.add_btn.setMinimumWidth(button_min_width)
        self.batch_scan_btn.setMinimumWidth(button_min_width)
        self.edit_btn.setMinimumWidth(button_min_width)
        self.verify_btn.setMinimumWidth(button_min_width)
        self.delete_btn.setMinimumWidth(button_min_width)
        self.export_btn.setMinimumWidth(button_min_width)
        
        # 添加按钮到布局
        layout.addWidget(self.add_btn)
        layout.addWidget(self.batch_scan_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.verify_btn)
        layout.addWidget(self.delete_btn)
        
        # 添加一个伸缩项，将导出按钮推到右侧
        layout.addStretch(1)
        
        # 导出按钮放在右侧
        layout.addWidget(self.export_btn)
        
        # 初始状态下禁用编辑和删除按钮
        self.set_selection_buttons_enabled(False)
    
    def connect_signals(self):
        """连接信号和槽"""
        self.add_btn.clicked.connect(self.add_clicked.emit)
        self.batch_scan_btn.clicked.connect(self.batch_scan_clicked.emit)
        self.edit_btn.clicked.connect(self.edit_clicked.emit)
        self.delete_btn.clicked.connect(self.delete_clicked.emit)
        self.export_btn.clicked.connect(self.export_clicked.emit)
        self.verify_btn.clicked.connect(self.verify_clicked.emit)
    
    def set_selection_buttons_enabled(self, enabled):
        """根据是否有选中项来启用/禁用编辑和删除按钮"""
        self.edit_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
        self.verify_btn.setEnabled(enabled)
        
        edit_tooltip = "编辑选中的发票记录" if enabled else "请先选择要编辑的发票"
        delete_tooltip = "删除选中的发票记录" if enabled else "请先选择要删除的发票"
        verify_tooltip = "打开网站查验选中的发票" if enabled else "请先选择要查验的发票"
        
        self.edit_btn.setToolTip(edit_tooltip)
        self.delete_btn.setToolTip(delete_tooltip)
        self.verify_btn.setToolTip(verify_tooltip) 