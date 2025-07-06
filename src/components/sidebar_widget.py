#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
现代化侧栏组件模块
负责提供用户导航和管理功能
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QScrollArea, QListView,
                               QMessageBox, QInputDialog, QMenu)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QStringListModel
from PySide6.QtGui import QAction

from src.data_manager import data_manager

class SidebarWidget(QWidget):
    """现代化侧栏组件"""
    
    # 定义信号
    user_selected = Signal(str)      # 用户选择信号
    user_list_changed = Signal()     # 用户列表变化信号
    toggle_requested = Signal()      # 切换请求信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_expanded = True
        self.expanded_width = 250
        self.collapsed_width = 80
        self.current_selection = None
        self.setup_ui()
        self.connect_signals()
        self.load_users()
    
    def setup_ui(self):
        """设置用户界面"""
        self.setFixedWidth(self.expanded_width)
        
        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Define Widgets ---
        self.title_label = QLabel("发票管理")
        self.title_label.setProperty("labelType", "title")
        self.version_label = QLabel("v2.0 Multi-User")
        self.version_label.setProperty("labelType", "caption")
        self.user_list_title = QLabel("用户列表")
        self.user_list_title.setProperty("labelType", "section_title")
        self.add_user_button = QPushButton("+")
        self.add_user_button.setFixedSize(24, 24)
        self.add_user_button.setToolTip("添加新用户")
        self.add_user_button.setProperty("buttonType", "action")
        self.user_list_view = QListView()
        self.user_list_model = QStringListModel()
        self.user_list_view.setModel(self.user_list_model)
        self.user_list_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self.user_list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.toggle_button = QPushButton("◀")
        self.toggle_button.setProperty("buttonType", "sidebar_toggle")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.setToolTip("收起/展开侧栏")

        # --- Header ---
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 25, 20, 25)
        title_container = QHBoxLayout()
        icon_label = QLabel("💼")
        icon_label.setProperty("iconType", "large")
        title_container.addWidget(icon_label)
        title_container.addWidget(self.title_label)
        title_container.addStretch()
        header_layout.addLayout(title_container)
        header_layout.addWidget(self.version_label)
        
        # --- User Management ---
        user_section_widget = QWidget()
        user_section_layout = QVBoxLayout(user_section_widget)
        user_section_layout.setContentsMargins(15, 20, 15, 20)
        user_section_layout.setSpacing(8)
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.user_list_title)
        title_layout.addStretch()
        title_layout.addWidget(self.add_user_button)
        user_section_layout.addLayout(title_layout)
        user_section_layout.addWidget(self.user_list_view)

        # --- Footer ---
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(20, 20, 20, 25)
        footer_layout.addStretch()
        footer_layout.addWidget(self.toggle_button)

        # --- Assemble Layout ---
        main_layout.addWidget(header_widget)
        main_layout.addWidget(self.create_separator())
        main_layout.addWidget(user_section_widget, 1)
        main_layout.addWidget(footer_widget)

    def create_separator(self):
        """创建分隔线"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator

    def connect_signals(self):
        """连接信号和槽"""
        self.add_user_button.clicked.connect(self.add_user)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.user_list_view.clicked.connect(self.on_user_selected)
        self.user_list_view.customContextMenuRequested.connect(self.show_user_context_menu)

    def load_users(self):
        """从数据管理器加载用户并更新UI"""
        users = data_manager.get_users()
        self.user_list_model.setStringList(users)

        if not users:
            self.current_selection = None
            self.user_selected.emit(None)
            return

        # 默认选中第一个用户
        if self.current_selection is None or self.current_selection not in users:
            self.current_selection = users[0]

        self.set_current_selection(self.current_selection)

    def on_user_selected(self, index):
        """处理用户选择事件"""
        user_name = self.user_list_model.data(index, Qt.ItemDataRole.DisplayRole)
        if self.current_selection != user_name:
            self.current_selection = user_name
            self.user_selected.emit(user_name)

    def show_user_context_menu(self, pos):
        """显示用户按钮的右键菜单"""
        index = self.user_list_view.indexAt(pos)
        if not index.isValid():
            return

        user_name = self.user_list_model.data(index, Qt.ItemDataRole.DisplayRole)

        context_menu = QMenu(self)
        rename_action = QAction("重命名", self)
        delete_action = QAction("删除", self)
        context_menu.addAction(rename_action)
        context_menu.addAction(delete_action)

        if len(data_manager.get_users()) <= 1:
            delete_action.setEnabled(False)

        action = context_menu.exec(self.user_list_view.mapToGlobal(pos))
        if action == rename_action:
            self.rename_user(user_name)
        elif action == delete_action:
            self.delete_user(user_name)

    def add_user(self):
        """添加新用户"""
        text, ok = QInputDialog.getText(self, "添加新用户", "请输入用户名:")
        if ok and text:
            if data_manager.add_user(text):
                self.current_selection = text
                self.load_users()
                self.user_list_changed.emit()
            else:
                QMessageBox.warning(self, "添加失败", "用户名已存在或无效。")

    def rename_user(self, old_name):
        """重命名用户"""
        new_name, ok = QInputDialog.getText(self, "重命名用户", f"为 '{old_name}' 输入新名称:", text=old_name)
        if ok and new_name and new_name != old_name:
            if data_manager.rename_user(old_name, new_name):
                if self.current_selection == old_name:
                    self.current_selection = new_name
                self.load_users()
                self.user_list_changed.emit()
            else:
                QMessageBox.warning(self, "重命名失败", "新用户名已存在或无效。")

    def delete_user(self, user_name):
        """删除用户"""
        reply = QMessageBox.question(self, "确认删除", 
                                     f"确定要删除用户 '{user_name}' 吗？\n该用户的所有发票数据将被永久删除。",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if data_manager.delete_user(user_name):
                if self.current_selection == user_name:
                    self.current_selection = None
                self.load_users()
                self.user_list_changed.emit()
            else:
                QMessageBox.warning(self, "删除失败", "无法删除最后一个用户。")
    
    def toggle_sidebar(self):
        """切换侧栏的展开/收起状态"""
        self.is_expanded = not self.is_expanded
        
        target_width = self.expanded_width if self.is_expanded else self.collapsed_width
        self.toggle_button.setText("◀" if self.is_expanded else "▶")

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.valueChanged.connect(self.update_text_visibility)
        self.animation.start()
        
    def update_text_visibility(self):
        """根据侧栏宽度更新文本标签的可见性"""
        show_text = self.width() > self.collapsed_width + 20
        self.title_label.setVisible(show_text)
        self.version_label.setVisible(show_text)
        self.user_list_title.setVisible(show_text)
        self.add_user_button.setVisible(show_text)
        
    def set_current_selection(self, user_name):
        """设置当前选中的用户"""
        if not user_name:
            self.user_list_view.clearSelection()
            return
            
        try:
            row = self.user_list_model.stringList().index(user_name)
            index = self.user_list_model.index(row)
            self.user_list_view.setCurrentIndex(index)
            self.current_selection = user_name
        except ValueError:
            # User not in list, clear selection
            self.user_list_view.clearSelection()
            self.current_selection = None

    def get_current_selection(self):
        """获取当前选中的用户"""
        return self.current_selection

    def set_expanded(self, expanded):
        """设置侧栏的展开状态"""
        self.is_expanded = expanded
        self.setFixedWidth(self.expanded_width if expanded else self.collapsed_width)
        self.update_text_visibility() 