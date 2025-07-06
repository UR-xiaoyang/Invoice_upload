#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发票管理系统主程序入口
"""

import sys
import os

# 将项目根目录添加到Python路径中，以解决模块导入问题
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication

from src.main_window import InvoiceMainWindow


def main():
    """主程序入口函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("发票管理系统")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("发票管理系统开发团队")
    
    # 创建并显示主窗口
    window = InvoiceMainWindow()
    window.show()
    
    # 运行应用程序事件循环
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 