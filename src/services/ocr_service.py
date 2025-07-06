#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR Service Module
Handles all OCR-related tasks in a separate process to avoid blocking the GUI.
"""

import multiprocessing
import os
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QMessageBox
from pdf2image import convert_from_path
import numpy as np


def ocr_process_worker(file_path, result_queue):
    """
    This function runs in a separate process to perform OCR.
    """
    try:
        import easyocr
        from src.ocr_parser import OcrParser

        # Check file type
        _, extension = os.path.splitext(file_path.lower())

        reader = easyocr.Reader(['ch_sim', 'en'])
        
        if extension == '.pdf':
            images = convert_from_path(file_path, first_page=1, last_page=1)
            if not images:
                raise ValueError("无法从PDF文件中提取图像。")
            image_np = np.array(images[0])
            text_list = reader.readtext(image_np, detail=0)
        else:
            text_list = reader.readtext(file_path, detail=0)

        parser = OcrParser(text_list)
        parsed_data = parser.parse()
        
        result_queue.put({'status': 'success', 'data': parsed_data})

    except Exception as e:
        result_queue.put({'status': 'error', 'message': str(e)})


class OcrService(QObject):
    """
    A service to run OCR in a separate process and communicate with the main
    GUI thread via signals.
    """
    ocr_finished = Signal(dict, str)
    ocr_error = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_process = None
        self.result_queue = None
        self.current_file = None
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_ocr_result)

    def start_ocr(self, file_path):
        """
        Starts the OCR process for a single file.
        """
        self.current_file = file_path
        
        model_dir = os.path.join(os.path.expanduser('~'), '.EasyOCR', 'model')
        needs_download = not os.path.exists(model_dir)

        if needs_download:
            reply = QMessageBox.question(None, '需要下载模型',
                                         "首次使用OCR功能需要下载语言模型文件(约80MB)。\n"
                                         "这是一个一次性的设置步骤。是否继续？",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.No:
                self.ocr_error.emit("用户取消了模型下载。", self.current_file)
                return
        
        self._run_process(ocr_process_worker, file_path)

    def _run_process(self, worker_func, file_path):
        """
        Runs the OCR worker in a separate process.
        """
        try:
            multiprocessing.set_start_method('spawn', force=True)
        except RuntimeError:
            pass # Already set

        self.result_queue = multiprocessing.Queue()
        self.current_process = multiprocessing.Process(
            target=worker_func,
            args=(file_path, self.result_queue)
        )
        self.current_process.start()
        self.check_timer.start(100)

    def check_ocr_result(self):
        """
        Checks the queue for a result from the OCR process and emits signals.
        """
        if self.result_queue and not self.result_queue.empty():
            self.check_timer.stop()
            result = self.result_queue.get()
            
            self.stop_process()

            if result['status'] == 'success':
                self.ocr_finished.emit(result['data'], self.current_file)
            else:
                self.ocr_error.emit(result['message'], self.current_file)

    def stop_process(self):
        """
        Stops the timer and terminates the background process if it's running.
        """
        self.check_timer.stop()
        if self.current_process and self.current_process.is_alive():
            self.current_process.terminate()
            self.current_process.join()
        self.current_process = None
        
    def is_running(self):
        """Check if a scan process is currently active."""
        return self.current_process is not None and self.current_process.is_alive() 