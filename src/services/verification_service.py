#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发票查验自动化服务
使用 Selenium 自动打开浏览器并填写发票信息
"""

import time
import os
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

class WorkerSignals(QObject):
    """定义工作线程可发出的信号"""
    finished = Signal(str)
    error = Signal(str)

class VerificationWorker(QRunnable):
    """在后台线程中运行Selenium的Worker"""
    def __init__(self, invoice_data: dict):
        super().__init__()
        self.invoice_data = invoice_data
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """执行浏览器自动化任务"""
        try:
            # 确定chromedriver的路径，优先使用项目根目录下的驱动
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            local_driver_path = os.path.join(project_root, 'chromedriver')

            if os.path.exists(local_driver_path):
                # 如果驱动文件在项目根目录，确保它是可执行的
                if not os.access(local_driver_path, os.X_OK):
                    os.chmod(local_driver_path, 0o755)
                service = ChromeService(executable_path=local_driver_path)
            else:
                # 否则，依赖系统PATH中的驱动
                service = ChromeService()

            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=service, options=options)

        except WebDriverException as e:
            if "executable needs to be in PATH" in str(e) or "cannot be found" in str(e):
                error_msg = "错误: 找不到 'chromedriver'。请下载并将其放置在项目根目录，或将其路径添加到系统环境变量中。"
            elif "session not created" in str(e):
                error_msg = "错误: 浏览器驱动版本与浏览器版本不兼容。请下载匹配的'chromedriver'。"
            else:
                error_msg = f"启动浏览器驱动时出错: {e}"
            self.signals.error.emit(error_msg)
            return
        except Exception as e:
            self.signals.error.emit(f"初始化浏览器时发生未知错误: {e}")
            return
            
        try:
            driver.get("https://inv-veri.chinatax.gov.cn/")
            time.sleep(1.5) # 等待页面加载

            # 填写发票代码
            fpdm_input = driver.find_element(By.ID, "fpdm")
            fpdm_input.send_keys(self.invoice_data.get("invoice_code", ""))

            # 填写发票号码
            fphm_input = driver.find_element(By.ID, "fphm")
            fphm_input.send_keys(self.invoice_data.get("invoice_number", ""))

            # 填写开票日期
            kprq_input = driver.find_element(By.ID, "kprq")
            date_str = self.invoice_data.get("issue_date", "").replace("-", "")
            kprq_input.send_keys(date_str)

            # 定位到金额输入框并聚焦
            kjje_input = driver.find_element(By.ID, "kjje")
            driver.execute_script("arguments[0].scrollIntoView(true);", kjje_input)
            kjje_input.click()

            self.signals.finished.emit("浏览器已打开，请手动完成查验。")

        except Exception as e:
            self.signals.error.emit(f"在页面上填写信息时出错: {e}")
        

class VerificationService(QObject):
    """处理发票查验的浏览器自动化服务"""
    verification_finished = Signal(str)
    verification_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def start_verification(self, invoice_data: dict):
        """创建并启动一个worker来执行查验任务"""
        worker = VerificationWorker(invoice_data)
        worker.signals.finished.connect(self.verification_finished)
        worker.signals.error.connect(self.verification_error)
        QThreadPool.globalInstance().start(worker)

if __name__ == '__main__':
    # 此部分仅用于直接测试，在应用中不会执行
    pass 