#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
现代化样式管理模块
负责管理应用程序的所有样式定义
采用现代化设计语言，提供更好的用户体验
"""


class AppStyles:
    """应用程序样式管理类"""
    
    # 颜色调色板
    COLORS = {
        'primary': '#2563eb',           # 主色调 - 蓝色
        'primary_hover': '#1d4ed8',     # 主色调悬停
        'primary_pressed': '#1e40af',   # 主色调按下
        'secondary': '#64748b',         # 次要色调 - 灰蓝
        'success': '#10b981',           # 成功色 - 绿色
        'success_hover': '#059669',     # 成功色悬停
        'warning': '#f59e0b',           # 警告色 - 橙色
        'warning_hover': '#d97706',     # 警告色悬停
        'danger': '#ef4444',            # 危险色 - 红色
        'danger_hover': '#dc2626',      # 危险色悬停
        'background': '#f1f5f9',        # 背景色 - 浅灰
        'surface': '#ffffff',           # 表面色
        'surface_alt': '#f8fafc',       # 替代表面色 (更亮的灰色)
        'border': '#e2e8f0',            # 边框色
        'border_focus': '#3b82f6',      # 焦点边框色
        'text_primary': '#1e293b',      # 主要文本色
        'text_secondary': '#64748b',    # 次要文本色
        'text_muted': '#94a3b8',        # 静音文本色
        'shadow': 'rgba(0, 0, 0, 0.1)', # 阴影色
        'shadow_hover': 'rgba(0, 0, 0, 0.15)', # 悬停阴影色
        'white': '#ffffff',
    }
    
    @staticmethod
    def get_main_window_style():
        """获取主窗口样式"""
        return f"""
            QMainWindow {{
                background-color: {AppStyles.COLORS['background']};
                color: {AppStyles.COLORS['text_primary']};
                font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
                font-size: 14px;
            }}
        """
    
    @staticmethod
    def get_dialog_style():
        """获取对话框样式"""
        return f"""
            QDialog {{
                background-color: {AppStyles.COLORS['surface']};
                color: {AppStyles.COLORS['text_primary']};
                font-size: 14px;
            }}
            #dialogContent {{
                background-color: {AppStyles.COLORS['surface']};
            }}
        """
    
    @staticmethod
    def get_group_box_style():
        """获取分组框样式"""
        return f"""
            QGroupBox {{
                font-weight: 600;
                font-size: 16px;
                color: {AppStyles.COLORS['text_primary']};
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: 12px;
                margin: 15px 0;
                padding-top: 20px;
                background-color: {AppStyles.COLORS['surface']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                background-color: {AppStyles.COLORS['surface']};
                border-radius: 6px;
            }}
        """
    
    @staticmethod
    def get_button_style():
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {AppStyles.COLORS['primary']};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-width: 100px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {AppStyles.COLORS['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {AppStyles.COLORS['primary_pressed']};
            }}
            QPushButton:disabled {{
                background-color: {AppStyles.COLORS['text_muted']};
                color: {AppStyles.COLORS['surface']};
            }}
            
            /* 成功按钮样式 */
            QPushButton[buttonType="success"] {{
                background-color: {AppStyles.COLORS['success']};
            }}
            QPushButton[buttonType="success"]:hover {{
                background-color: {AppStyles.COLORS['success_hover']};
            }}
            
            /* 警告按钮样式 */
            QPushButton[buttonType="warning"] {{
                background-color: {AppStyles.COLORS['warning']};
            }}
            QPushButton[buttonType="warning"]:hover {{
                background-color: {AppStyles.COLORS['warning_hover']};
            }}
            
            /* 危险按钮样式 */
            QPushButton[buttonType="danger"] {{
                background-color: {AppStyles.COLORS['danger']};
            }}
            QPushButton[buttonType="danger"]:hover {{
                background-color: {AppStyles.COLORS['danger_hover']};
            }}
            
            /* 次要按钮样式 */
            QPushButton[buttonType="secondary"] {{
                background-color: {AppStyles.COLORS['surface']};
                color: {AppStyles.COLORS['text_primary']};
                border: 2px solid {AppStyles.COLORS['border']};
            }}
            QPushButton[buttonType="secondary"]:hover {{
                background-color: {AppStyles.COLORS['surface_alt']};
                border-color: {AppStyles.COLORS['primary']};
            }}

            /* 自定义关闭按钮 */
            QPushButton[isCloseButton="true"] {{
                background-color: transparent;
                border: none;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
                padding: 0;
                border-radius: 16px;
            }}
            QPushButton[isCloseButton="true"]:hover {{
                background-color: rgba(0,0,0, 0.1);
            }}
            QPushButton[isCloseButton="true"]:pressed {{
                background-color: rgba(0,0,0, 0.2);
            }}
        """
    
    @staticmethod
    def get_input_style():
        """获取输入框样式"""
        return f"""
            QLineEdit {{
                padding: 12px 16px;
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                background-color: {AppStyles.COLORS['surface']};
                color: {AppStyles.COLORS['text_primary']};
                selection-background-color: {AppStyles.COLORS['primary']};
                selection-color: white;
            }}
            QLineEdit:focus {{
                border-color: {AppStyles.COLORS['border_focus']};
                outline: none;
            }}
            QLineEdit:hover {{
                border-color: {AppStyles.COLORS['text_secondary']};
            }}
            
            QComboBox {{
                padding: 12px 16px;
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                background-color: {AppStyles.COLORS['surface']};
                color: {AppStyles.COLORS['text_primary']};
                min-height: 20px;
            }}
            QComboBox:focus {{
                border-color: {AppStyles.COLORS['border_focus']};
            }}
            QComboBox:hover {{
                border-color: {AppStyles.COLORS['text_secondary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: 5px solid transparent;
                border-top: 5px solid {AppStyles.COLORS['text_secondary']};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: 8px;
                background-color: {AppStyles.COLORS['surface']};
                selection-background-color: {AppStyles.COLORS['primary']};
                selection-color: white;
                padding: 4px;
            }}
            
            QDateEdit {{
                padding: 12px 16px;
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                background-color: {AppStyles.COLORS['surface']};
                color: {AppStyles.COLORS['text_primary']};
                min-height: 20px;
            }}
            QDateEdit:focus {{
                border-color: {AppStyles.COLORS['border_focus']};
            }}
            QDateEdit:hover {{
                border-color: {AppStyles.COLORS['text_secondary']};
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 30px;
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: 5px solid transparent;
                border-top: 5px solid {AppStyles.COLORS['text_secondary']};
                margin-right: 10px;
            }}
        """
    
    @staticmethod
    def get_table_style():
        """获取表格样式"""
        return f"""
            QTableView {{
                background-color: {AppStyles.COLORS['surface']};
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: 12px;
                gridline-color: {AppStyles.COLORS['border']};
                font-size: 14px;
                color: {AppStyles.COLORS['text_primary']};
                selection-background-color: {AppStyles.COLORS['primary']};
                selection-color: white;
                alternate-background-color: {AppStyles.COLORS['surface_alt']};
            }}
            QTableView::item {{
                padding: 12px 16px;
                border: none;
                border-bottom: 1px solid {AppStyles.COLORS['border']};
            }}
            QTableView::item:selected {{
                background-color: {AppStyles.COLORS['primary']};
                color: white;
            }}
            QTableView::item:hover {{
                background-color: rgba(37, 99, 235, 0.1);
            }}
            QHeaderView::section {{
                background-color: {AppStyles.COLORS['surface_alt']};
                color: {AppStyles.COLORS['text_primary']};
                padding: 16px;
                border: none;
                border-bottom: 2px solid {AppStyles.COLORS['border']};
                font-weight: 600;
                font-size: 14px;
                text-align: left;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 10px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 10px;
            }}
            QTableView::corner {{
                background-color: {AppStyles.COLORS['surface_alt']};
                border: none;
            }}
            
            /* 滚动条样式 (暂时禁用以排查光标问题)
            QScrollBar:vertical {{
                background-color: 
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background-color: {AppStyles.COLORS['text_muted']};
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {AppStyles.COLORS['text_secondary']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar:horizontal {{
                background-color: {AppStyles.COLORS['surface_alt']};
                height: 12px;
                border-radius: 6px;
                margin: 0;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {AppStyles.COLORS['text_muted']};
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {AppStyles.COLORS['text_secondary']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0;
            }}
            */
        """
    
    @staticmethod
    def get_status_bar_style():
        """获取状态栏样式"""
        return f"""
            QStatusBar {{
                background-color: {AppStyles.COLORS['surface']};
                color: {AppStyles.COLORS['text_secondary']};
                border-top: 1px solid {AppStyles.COLORS['border']};
                padding: 8px 16px;
                font-size: 13px;
            }}
        """
    
    @staticmethod
    def get_label_style():
        """获取标签样式"""
        return f"""
            QLabel {{
                color: {AppStyles.COLORS['text_primary']};
                font-size: 14px;
                font-weight: 500;
                padding: 4px 0;
            }}
            QLabel[labelType="title"] {{
                font-size: 18px;
                font-weight: 700;
                color: {AppStyles.COLORS['text_primary']};
            }}
            QLabel[labelType="subtitle"] {{
                font-size: 16px;
                font-weight: 600;
                color: {AppStyles.COLORS['text_secondary']};
            }}
            QLabel[labelType="caption"] {{
                font-size: 12px;
                color: {AppStyles.COLORS['text_muted']};
            }}
        """
    
    @staticmethod
    def get_sidebar_style():
        """获取侧栏样式"""
        return f"""
            SidebarWidget {{
                background-color: {AppStyles.COLORS['surface']};
                border-right: 1px solid {AppStyles.COLORS['border']};
            }}

            /* 侧栏内部分区标题 */
            QLabel[labelType="section_title"] {{
                color: {AppStyles.COLORS['text_secondary']};
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
                margin: 10px 0 5px 10px;
            }}

            /* 侧栏菜单和工具按钮的通用样式 */
            QPushButton[buttonType="sidebar_menu"],
            QPushButton[buttonType="sidebar_tool"] {{
                background-color: transparent;
                color: {AppStyles.COLORS['text_secondary']};
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                text-align: left;
                font-weight: 500;
                font-size: 14px;
                min-height: auto;
            }}
            QPushButton[buttonType="sidebar_menu"]:hover,
            QPushButton[buttonType="sidebar_tool"]:hover {{
                background-color: {AppStyles.COLORS['surface_alt']};
                color: {AppStyles.COLORS['text_primary']};
            }}
            QPushButton[buttonType="sidebar_menu"]:checked {{
                background-color: {AppStyles.COLORS['primary']};
                color: {AppStyles.COLORS['white']};
                font-weight: 600;
            }}

            /* 侧栏动作按钮 (如添加用户) */
            QPushButton[buttonType="action"] {{
                background-color: transparent;
                color: {AppStyles.COLORS['text_secondary']};
                border: 1px dashed {AppStyles.COLORS['border']};
                border-radius: 6px;
                font-weight: 600;
                padding: 0;
                min-width: 0;
                min-height: 0;
            }}
            QPushButton[buttonType="action"]:hover {{
                background-color: {AppStyles.COLORS['primary']};
                color: {AppStyles.COLORS['white']};
                border-style: solid;
            }}

            /* 侧栏切换按钮 */
            QPushButton[buttonType="sidebar_toggle"] {{
                background-color: {AppStyles.COLORS['surface_alt']};
                color: {AppStyles.COLORS['text_secondary']};
                border: none;
                border-radius: 20px;
                padding: 0;
                min-width: 40px;
                min-height: 40px;
            }}
            QPushButton[buttonType="sidebar_toggle"]:hover {{
                background-color: {AppStyles.COLORS['primary']};
                color: {AppStyles.COLORS['white']};
            }}
        """
    
    @staticmethod
    def get_message_box_style():
        """获取消息框样式"""
        return f"""
            QMessageBox {{
                background-color: {AppStyles.COLORS['surface']};
            }}
            QMessageBox QLabel {{
                color: {AppStyles.COLORS['text_primary']};
                font-size: 16px;
                padding: 20px;
            }}
            QMessageBox QPushButton {{
                background-color: {AppStyles.COLORS['primary']};
                color: {AppStyles.COLORS['white']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {AppStyles.COLORS['primary_hover']};
            }}
            QMessageBox QPushButton:pressed {{
                background-color: {AppStyles.COLORS['primary_pressed']};
            }}
        """
    
    @staticmethod
    def get_complete_style():
        """获取完整的应用程序样式"""
        return (
            AppStyles.get_main_window_style() +
            AppStyles.get_dialog_style() +
            AppStyles.get_group_box_style() +
            AppStyles.get_button_style() +
            AppStyles.get_input_style() +
            AppStyles.get_table_style() +
            AppStyles.get_status_bar_style() +
            AppStyles.get_label_style() +
            AppStyles.get_sidebar_style() +
            AppStyles.get_message_box_style()
        ) 