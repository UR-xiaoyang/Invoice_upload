from PySide6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel
from PySide6.QtCore import Qt

class ProgressDialog(QDialog):
    """一个用于显示批量处理进度的对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量处理中...")
        self.setMinimumWidth(400)
        self.setModal(True) # 设置为模态对话框，阻止与其他窗口交互
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False) # 禁用关闭按钮
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)


        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        self.status_label = QLabel("正在准备...", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        self.detail_label = QLabel("处理文件: ", self)

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.detail_label)
        
    def update_progress(self, value: int, total: int, current_file: str):
        """
        更新进度
        :param value: 当前已处理的数量
        :param total: 总数量
        :param current_file: 当前正在处理的文件名
        """
        if total > 0:
            percent = int((value / total) * 100)
            self.progress_bar.setValue(percent)
            self.status_label.setText(f"进度: {value} / {total} ({percent}%)")
            self.detail_label.setText(f"正在处理: {current_file}")
        else:
            self.progress_bar.setValue(0)
            self.status_label.setText("正在准备...")
            self.detail_label.setText("") 