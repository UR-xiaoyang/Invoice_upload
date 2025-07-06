#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
现代化主窗口模块
负责整合所有组件并管理主要的应用程序逻辑
采用现代化设计，提供更好的用户体验
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar, QMessageBox, QSplitter, QFileDialog, QPushButton
from PySide6.QtCore import QDate, QTimer, QUrl, Qt
from PySide6.QtGui import QIcon, QTextDocument, QPainter, QImage, QDesktopServices, QPageLayout
from PySide6 import QtCore
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
import uuid
import os

from components.table_widget import InvoiceTableWidget
from components.button_widget import ButtonWidget
from components.sidebar_widget import SidebarWidget
from components.invoice_dialog import InvoiceDialog
from components.progress_dialog import ProgressDialog
from styles.styles import AppStyles
from src.data_manager import data_manager
from src.services.ocr_service import OcrService
from src.services.pdf_text_service import PdfTextService
from src.services.verification_service import VerificationService


class InvoiceMainWindow(QMainWindow):
    """现代化发票管理主窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.ocr_service = OcrService()
        self.pdf_text_service = PdfTextService()
        self.verification_service = VerificationService()
        
        self.ocr_queue = []
        self.pdf_queue = []
        self.batch_total_count = 0
        self.batch_processed_count = 0
        self.progress_dialog = None
        self.on_batch_finished_called = False
        
        self.setup_ui()
        self.connect_signals()
        # self.update_status_bar() # Will be called after loading data
        self.setup_window_properties()
        # Initial load
        initial_user = self.sidebar_widget.get_current_selection()
        if initial_user:
            self.on_user_selected(initial_user)
    
    def setup_ui(self):
        """设置用户界面"""
        # 设置窗口属性
        self.setWindowTitle("💼 发票管理系统 - 现代化版本")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # 应用样式
        self.setStyleSheet(AppStyles.get_complete_style())
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 使用QSplitter作为主布局
        main_splitter = QSplitter(QtCore.Qt.Orientation.Horizontal, self)
        
        # 创建侧栏
        self.sidebar_widget = SidebarWidget(self)
        
        # 创建主内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        # --- Start: Custom Title Bar ---
        title_bar_layout = QHBoxLayout()
        title_bar_layout.addStretch()

        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon.fromTheme("window-close"))
        self.close_button.setProperty("isCloseButton", True)
        self.close_button.setFixedSize(32, 32)
        self.close_button.setToolTip("关闭程序")
        
        title_bar_layout.addWidget(self.close_button)
        content_layout.addLayout(title_bar_layout)
        # --- End: Custom Title Bar ---
        
        # 创建组件
        self.table_widget = InvoiceTableWidget()
        self.button_widget = ButtonWidget()
        
        # 添加组件到内容布局
        content_layout.addWidget(self.table_widget, 1)
        content_layout.addWidget(self.button_widget)
        
        # 将侧边栏和主内容区域添加到QSplitter
        main_splitter.addWidget(self.sidebar_widget)
        main_splitter.addWidget(content_widget)
        main_splitter.setStretchFactor(1, 1) # 主内容区拉伸
        main_splitter.setSizes([250, 1150]) # 初始大小

        # 将QSplitter设置为主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_splitter)
        
        # 创建状态栏
        # self.status_bar = QStatusBar()
        # self.setStatusBar(self.status_bar)
        # self.status_bar.showMessage("系统就绪")
        
        # 添加状态栏永久小部件
        self.setup_status_bar()
    
    def setup_status_bar(self):
        """设置状态栏"""
        from PySide6.QtWidgets import QLabel
        
        # 添加版本信息
        version_label = QLabel("v1.0.0")
        version_label.setProperty("labelType", "caption")
        # self.status_bar.addPermanentWidget(version_label)
        
        # 添加时间显示
        self.time_label = QLabel()
        self.time_label.setProperty("labelType", "caption")
        # self.status_bar.addPermanentWidget(self.time_label)
        
        # 更新时间显示
        self.update_time_display()
        
        # 设置定时器更新时间
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time_display)
        self.time_timer.start(1000)  # 每秒更新一次
    
    def setup_window_properties(self):
        """设置窗口属性"""
        # 设置窗口图标（如果有的话）
        self.setWindowIcon(QIcon.fromTheme("document-properties"))
        
        # 此处暂时留空，恢复到Qt的默认行为
        pass
    
    def update_time_display(self):
        """更新时间显示"""
        from PySide6.QtCore import QDateTime
        current_time = QDateTime.currentDateTime()
        time_text = current_time.toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(time_text)
    
    def connect_signals(self):
        """连接信号和槽"""
        # 侧栏组件信号
        self.sidebar_widget.user_selected.connect(self.on_user_selected)
        self.sidebar_widget.user_list_changed.connect(self.load_invoice_data) # 用户列表变化时重新加载
        
        # 表格组件信号
        self.table_widget.selection_changed.connect(self.on_table_selection_changed)
        self.table_widget.row_double_clicked.connect(self.on_table_row_double_clicked)
        self.table_widget.data_changed.connect(self.on_table_data_changed)
        self.table_widget.edit_requested.connect(self.on_edit_invoice)
        self.table_widget.delete_requested.connect(self.on_delete_invoices_by_rows)
        self.table_widget.status_change_requested.connect(self.on_status_change_requested)
        self.table_widget.print_requested.connect(self.on_print_requested)
        
        # 按钮组件信号
        self.button_widget.add_clicked.connect(self.on_add_invoice)
        self.button_widget.edit_clicked.connect(self.on_edit_invoice)
        self.button_widget.delete_clicked.connect(self.on_delete_invoice)
        self.button_widget.export_clicked.connect(self.on_export_data)
        self.button_widget.batch_scan_clicked.connect(self.on_batch_scan)
        self.button_widget.verify_clicked.connect(self.on_verify_invoice)

        # 自定义关闭按钮
        self.close_button.clicked.connect(self.close)

        # 服务信号
        self.ocr_service.ocr_finished.connect(self.on_batch_item_finished)
        self.ocr_service.ocr_error.connect(self.on_batch_item_error)
        self.pdf_text_service.extraction_finished.connect(self.on_batch_item_finished)
        self.pdf_text_service.extraction_error.connect(self.on_batch_item_error)
        self.verification_service.verification_finished.connect(self.on_verification_finished)
        self.verification_service.verification_error.connect(self.on_verification_error)
    
    def on_user_selected(self, user_name):
        """处理用户选择变化事件"""
        self.current_user = user_name
        self.setWindowTitle(f"💼 发票管理系统 - {self.current_user}")
        self.load_invoice_data()
    
    def load_invoice_data(self):
        """加载当前用户的发票数据到表格"""
        if not self.current_user:
            self.table_widget.set_table_data([])
            # self.update_status_bar()
            return

        invoices = data_manager.get_invoices(self.current_user)
        
        # 将数据转换为表格需要的格式 (列表的列表)
        table_data = []
        for inv in invoices:
            table_data.append([
                inv.get('id', ''),
                inv.get('invoice_code', ''),
                inv.get('invoice_number', ''),
                inv.get('supplier', ''),
                inv.get('issue_date', ''),
                inv.get('amount', 0),  # Pass raw amount
                inv.get('invoice_type', ''),
                inv.get('item_name', ''),
                inv.get('category', ''),
                inv.get('notes', ''),
                inv.get('status', '未使用'),
            ])
        
        self.table_widget.set_table_data(table_data)
        # self.update_status_bar()
    
    def on_table_selection_changed(self, current_row, current_column):
        """处理表格选择变化"""
        has_selection = current_row >= 0
        self.button_widget.set_selection_buttons_enabled(has_selection)
        
        if has_selection:
            # 获取选中行的信息
            row_data = self.table_widget.get_row_data(current_row)
            if row_data and len(row_data) > 2:
                invoice_number = row_data[2] # index 2 is invoice number now
                # self.status_bar.showMessage(f"📋 已选择发票: {invoice_number}")
        else:
            # self.update_status_bar()
            pass
    
    def on_table_row_double_clicked(self, row):
        """处理表格行双击"""
        self.on_edit_invoice()
    
    def on_table_data_changed(self):
        """处理表格数据变化"""
        # self.update_status_bar()
    
    def on_add_invoice(self):
        """处理添加发票"""
        if not self.current_user:
            QMessageBox.warning(self, "⚠️ 警告", "请先选择一个用户。")
            return

        dialog = InvoiceDialog(self)
        if dialog.exec():
            new_data = dialog.get_data()
            invoice_id = str(uuid.uuid4())
            new_data['id'] = invoice_id  # 添加唯一ID

            # 检查是否有文件需要保存
            if 'file_path' in new_data and new_data['file_path']:
                cached_path = data_manager.save_source_file(new_data['file_path'], invoice_id)
                if cached_path:
                    new_data['source_file'] = cached_path
                del new_data['file_path']  # 删除临时路径

            data_manager.add_invoice(self.current_user, new_data)
            self.load_invoice_data()  # 重新加载数据
            # self.status_bar.showMessage(f"✅ 发票 {new_data.get('invoice_number', '')} 已成功添加", 3000)
    
    def on_edit_invoice(self):
        """处理编辑发票"""
        selected_row = self.table_widget.get_current_row()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ 警告", "请先选择要编辑的发票记录")
            return

        invoice_id = self.table_widget.get_cell_data(selected_row, 0)
        if not invoice_id:
            QMessageBox.critical(self, "❌ 错误", "无法获取发票ID，数据可能已损坏。")
            return
            
        # 从 data_manager 获取原始数据
        if not self.current_user:
            QMessageBox.critical(self, "❌ 错误", "没有选中的用户。")
            return
        all_invoices = data_manager.get_invoices(self.current_user)
        invoice_data = next((inv for inv in all_invoices if inv.get("id") == invoice_id), None)

        if not invoice_data:
            QMessageBox.critical(self, "❌ 错误", "在数据源中未找到所选发票。")
            return

        # 打开编辑对话框
        dialog = InvoiceDialog(self, invoice_data=invoice_data)
        if dialog.exec():
            updated_data = dialog.get_data()

            # 关键修复：从原始数据中保留 source_file 路径
            if 'source_file' in invoice_data:
                updated_data['source_file'] = invoice_data['source_file']

            # 如果在编辑时上传了新文件，则更新 source_file
            if 'file_path' in updated_data and updated_data['file_path']:
                 # The file path from dialog is a temp path, we need to save it to cache
                 cached_path = data_manager.save_source_file(updated_data['file_path'], invoice_id)
                 updated_data['source_file'] = cached_path
                 del updated_data['file_path'] # remove temp path

            data_manager.update_invoice(self.current_user, invoice_id, updated_data)
            self.load_invoice_data() # 重新加载数据
            # self.status_bar.showMessage(f"✅ 发票 {updated_data['invoice_number']} 已成功更新", 3000)
    
    def on_delete_invoices_by_rows(self, row_indices):
        """处理从右键菜单或按钮发出的多行删除请求"""
        if not self.current_user:
            return

        ids_to_delete = []
        for row_index in row_indices:
            invoice_id = self.table_widget.get_cell_data(row_index, 0)
            if invoice_id:
                ids_to_delete.append(invoice_id)

        if not ids_to_delete:
            return

        deleted_count = 0
        for invoice_id in ids_to_delete:
            if data_manager.delete_invoice(self.current_user, invoice_id):
                deleted_count += 1
        
        if deleted_count > 0:
            self.load_invoice_data()
            # self.status_bar.showMessage(f"��️ {deleted_count} 条发票已删除", 3000)

    def on_status_change_requested(self, row_indices, new_status):
        """处理多行状态更改请求"""
        if not self.current_user:
            return

        updated_count = 0
        for row_index in row_indices:
            invoice_id = self.table_widget.get_cell_data(row_index, 0)
            if not invoice_id:
                continue

            invoice_data = data_manager.get_invoice_by_id(self.current_user, invoice_id)
            if invoice_data:
                invoice_data['status'] = new_status
                if data_manager.update_invoice(self.current_user, invoice_id, invoice_data):
                    updated_count += 1

        if updated_count > 0:
            self.load_invoice_data()
            # self.status_bar.showMessage(f"✅ {updated_count} 条记录的状态已更新为 '{new_status}'", 3000)

    def on_print_requested(self, row_indices):
        """处理多行打印请求"""
        if not self.current_user:
            QMessageBox.warning(self, "无用户", "请先选择一个用户。")
            return
            
        if len(row_indices) > 1:
            QMessageBox.information(self, "多文件打印", "将为您逐一打开选中的文件以供打印。")

        for row_index in row_indices:
            invoice_id = self.table_widget.get_cell_data(row_index, 0)
            if not invoice_id:
                continue
                
            invoice_data = data_manager.get_invoice_by_id(self.current_user, invoice_id)
            if not invoice_data:
                continue # 如果没找到数据就跳过
                
            file_path = invoice_data.get("source_file")
            if not file_path or not os.path.exists(file_path):
                QMessageBox.warning(self, "文件未找到", f"未找到发票 {invoice_data.get('invoice_number', '')} 的源文件，已跳过。")
                continue
                
            self.print_original_file(file_path)

    def print_original_file(self, file_path):
        """根据文件类型打印原始文件（图片或PDF）"""
        _, extension = os.path.splitext(file_path.lower())

        if extension in ['.png', '.jpg', '.jpeg', '.bmp']:
            # 打印图片
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                painter = QPainter()
                painter.begin(printer)
                image = QImage(file_path)
                rect = painter.viewport()
                size = image.size()
                size.scale(rect.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(image.rect())
                painter.drawImage(0, 0, image)
                painter.end()
                # self.status_bar.showMessage(f"🖼️ 图片 {os.path.basename(file_path)} 已发送到打印机", 3000)

        elif extension == '.pdf':
            # 恢复为使用系统默认程序打开PDF进行打印
            absolute_path = os.path.abspath(file_path)
            if not QDesktopServices.openUrl(QUrl.fromLocalFile(absolute_path)):
                QMessageBox.critical(self, "打开失败", f"无法使用系统默认应用打开PDF文件: {absolute_path}")
            else:
                # self.status_bar.showMessage(f"📄 正在使用默认应用打开PDF以供打印...", 3000)
                pass
        else:
            QMessageBox.warning(self, "不支持的文件类型", f"不支持打印此文件类型: {extension}")

    def on_delete_invoice(self):
        """删除发票"""
        selected_rows = self.table_widget.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "无选中项", "请先在表格中选择要删除的发票。")
            return
        
        # 复用带有确认对话框的处理方法
        self.table_widget.handle_delete_request(selected_rows)

    def on_batch_scan(self):
        """处理批量扫描请求"""
        if not self.current_user:
            QMessageBox.warning(self, "⚠️ 警告", "请先选择一个用户以进行批量扫描。")
            return

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "选择要批量扫描的发票文件",
            "",
            "发票文件 (*.png *.jpg *.jpeg *.bmp *.pdf)"
        )

        if not file_paths:
            return
        
        # 分发任务到不同的队列
        self.ocr_queue = [p for p in file_paths if p.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.pdf_queue = [p for p in file_paths if p.lower().endswith('.pdf')]

        self.batch_total_count = len(self.ocr_queue) + len(self.pdf_queue)
        self.batch_processed_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        if self.batch_total_count == 0:
            return

        self.button_widget.setDisabled(True)
        # self.status_bar.showMessage(f"⏳ 开始批量处理 {self.batch_total_count} 个文件...")

        # 创建并显示进度对话框
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()

        self._start_next_batch_item()

    def _start_next_batch_item(self):
        """按顺序启动下一个批量处理任务"""
        file_path_to_process = None
        if self.pdf_queue:
            file_path_to_process = self.pdf_queue[0] 
        elif self.ocr_queue:
            file_path_to_process = self.ocr_queue[0]

        if file_path_to_process:
            # 更新进度对话框
            if self.progress_dialog:
                self.progress_dialog.update_progress(
                    self.batch_processed_count, 
                    self.batch_total_count, 
                    os.path.basename(file_path_to_process)
                )

            if file_path_to_process.lower().endswith('.pdf'):
                self.pdf_text_service.start_extraction(self.pdf_queue.pop(0))
            else:
                self.ocr_service.start_ocr(self.ocr_queue.pop(0))
        else:
            # 所有队列都已处理完毕，以防万一
            if not self.on_batch_finished_called:
                self.on_batch_finished()

    def on_batch_item_finished(self, parsed_data, file_path):
        """处理单个文件批处理完成后的逻辑"""
        self.batch_processed_count += 1
        
        if parsed_data and self.current_user:
            self.success_count += 1  # 增加成功计数
            # 为新发票生成唯一ID
            invoice_id = str(uuid.uuid4())
            parsed_data['id'] = invoice_id
            
            # 保存源文件并获取其缓存路径
            cached_file_path = data_manager.save_source_file(file_path, invoice_id)
            if cached_file_path:
                parsed_data['source_file'] = cached_file_path
            
            # 添加发票数据
            data_manager.add_invoice(self.current_user, parsed_data)
        else:
            self.failure_count += 1 # 如果没有解析出数据，也算作失败

        # 更新进度对话框
        if self.progress_dialog:
            self.progress_dialog.update_progress(self.batch_processed_count, self.batch_total_count, os.path.basename(file_path))

        if self.batch_processed_count == self.batch_total_count:
            self.on_batch_finished()
        else:
            self._start_next_batch_item()

    def on_batch_item_error(self, error_message, file_path):
        """当批量扫描中单个文件失败时调用（通用）"""
        self.failure_count += 1
        self.batch_processed_count += 1
        print(f"处理文件失败 '{file_path}': {error_message}") # 在后台打印错误
        
        # 更新进度对话框
        if self.progress_dialog:
            self.progress_dialog.update_progress(self.batch_processed_count, self.batch_total_count, f"失败: {os.path.basename(file_path)}")

        # 自动开始下一个
        QTimer.singleShot(50, self._start_next_batch_item)

    def on_batch_finished(self):
        """当所有批量任务完成时调用"""
        if self.on_batch_finished_called:
            return
        self.on_batch_finished_called = True

        self.button_widget.setDisabled(False)
        self.load_invoice_data() # 刷新表格
        
        # 关闭进度对话框
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        summary_message = (
            f"<h3>批量处理完成！</h3>"
            f"<p>✅ 成功处理: <b>{self.success_count}</b> 个文件</p>"
            f"<p>❌ 处理失败: <b>{self.failure_count}</b> 个文件</p>"
            f"<p>详情请查看程序运行的命令行窗口。</p>"
        )
        
        QMessageBox.information(self, "批量处理结果", summary_message)
        # self.update_status_bar()

    def on_export_data(self):
        """处理数据导出请求"""
        if not self.current_user:
            QMessageBox.warning(self, "无用户", "请先选择一个要导出数据的用户。")
            return

        invoices_to_export = data_manager.get_invoices(self.current_user)
        
        if not invoices_to_export:
            QMessageBox.information(self, "无数据", f"用户'{self.current_user}'没有任何发票可以导出。")
            return
            
        self.table_widget.export_to_excel(invoices_to_export)
    
    # def update_status_bar(self):
    #     """更新状态栏信息"""
    #     total_count = self.table_widget.get_row_count()
    #     if self.current_user:
    #         self.status_bar.showMessage(f"👤 当前用户: {self.current_user}  |  总计 {total_count} 条发票记录")
    #     else:
    #         self.status_bar.showMessage("请选择一个用户")
    
    def closeEvent(self, event):
        """处理窗口关闭事件"""
        reply = QMessageBox.question(
            self, "❓ 确认退出", 
            "您确定要关闭发票管理系统吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 停止后台服务
            self.ocr_service.stop_process()
            self.pdf_text_service.stop_process()
            # 停止定时器
            if hasattr(self, 'time_timer'):
                self.time_timer.stop()
            
            # self.status_bar.showMessage("正在退出系统...")
            event.accept()
        else:
            event.ignore()
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于发票管理系统",
            """
            <h3>💼 发票管理系统</h3>
            <p><b>版本:</b> 1.0.0</p>
            <p><b>开发:</b> 现代化UI重构版本</p>
            <p><b>技术:</b> PySide6 + 现代化设计</p>
            
            <p>功能特性:</p>
            <ul>
            <li>🔍 智能搜索和筛选</li>
            <li>📋 现代化表格显示</li>
            <li>📊 实时统计分析</li>
            <li>🎨 现代化UI设计</li>
            </ul>
            """
        )
    
    def on_sidebar_toggle(self):
        """处理侧栏切换"""
        # 这个逻辑现在由侧边栏自己处理，主窗口不再需要干预
        pass
    
    # The following methods are now obsolete or would need rethinking
    # in a multi-user context. For now, we can comment them out or remove them.
    # We are simplifying the UI to focus on per-user invoice management.

    # def on_sidebar_menu_clicked(self, item_id):
    #     ...
    
    # def get_menu_display_name(self, item_id):
    #     ...

    # def show_dashboard_view(self):
    #     ...

    # def show_invoices_view(self):
    #     ...

    # def show_search_view(self):
    #     ...
    
    # def show_reports_view(self):
    #     ...
        
    # def show_suppliers_view(self):
    #     ...
        
    # def handle_import_data(self):
    #     ...
        
    # def handle_backup_data(self):
    #     ...
        
    # def show_settings_view(self):
    #     ... 

    def on_verify_invoice(self):
        """处理发票查验，使用Selenium自动填写"""
        selected_row = self.table_widget.get_current_row()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ 警告", "请先选择要查验的发票记录")
            return

        row_data = self.table_widget.get_row_data(selected_row)
        if not row_data:
            return

        # 从表格数据中提取查验所需信息
        # 表头: "ID", "发票代码", "发票号码", "供应商", "开票日期", "金额", ...
        invoice_data = {
            "invoice_code": row_data[1],
            "invoice_number": row_data[2],
            "issue_date": row_data[4],
        }

        # 检查核心信息
        if not all([invoice_data["invoice_number"], invoice_data["issue_date"]]):
            QMessageBox.warning(self, "⚠️ 信息不全", "缺少必要的查验信息（发票号码或开票日期）。")
            return
            
        # self.status_bar.showMessage("正在启动浏览器以进行发票查验...", 3000)
        self.verification_service.start_verification(invoice_data)

    def on_verification_finished(self, message):
        """处理查验成功结束的信号"""
        # self.status_bar.showMessage(message, 5000)
        pass

    def on_verification_error(self, error_message):
        """处理查验过程中发生错误的信号"""
        # QMessageBox.critical(self, "❌ 查验出错", error_message)
        # self.status_bar.showMessage("查验功能启动失败。", 5000) 