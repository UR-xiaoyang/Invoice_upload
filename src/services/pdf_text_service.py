#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Text Extraction Service Module
Handles quick text extraction from text-based PDF files.
"""

import multiprocessing
from PySide6.QtCore import QObject, Signal, QTimer

def pdf_text_process_worker(file_path, result_queue):
    """
    This function runs in a separate process to perform quick text extraction.
    """
    try:
        import fitz  # PyMuPDF
        from src.ocr_parser import OcrParser

        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        if not full_text.strip():
            raise ValueError("PDF文件为空或不包含任何文本内容。")

        parser = OcrParser(full_text.split('\n'))
        parsed_data = parser.parse()
        
        result_queue.put({'status': 'success', 'data': parsed_data})

    except Exception as e:
        result_queue.put({'status': 'error', 'message': str(e)})


class PdfTextService(QObject):
    """
    A service to run quick text extraction in a separate process.
    """
    extraction_finished = Signal(dict, str)
    extraction_error = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_process = None
        self.result_queue = None
        self.current_file = None
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_extraction_result)

    def start_extraction(self, file_path):
        """
        Starts the PDF text extraction process.
        """
        self.current_file = file_path
        self._run_process(pdf_text_process_worker, file_path)

    def _run_process(self, worker_func, file_path):
        """
        Runs the worker function in a separate process.
        """
        try:
            multiprocessing.set_start_method('spawn', force=True)
        except RuntimeError:
            pass  # Already set

        self.result_queue = multiprocessing.Queue()
        self.current_process = multiprocessing.Process(
            target=worker_func,
            args=(file_path, self.result_queue)
        )
        self.current_process.start()
        self.check_timer.start(100)

    def check_extraction_result(self):
        """
        Checks the queue for a result and emits signals.
        """
        if self.result_queue and not self.result_queue.empty():
            self.check_timer.stop()
            result = self.result_queue.get()
            
            self.stop_process()

            if result['status'] == 'success':
                self.extraction_finished.emit(result['data'], self.current_file)
            else:
                self.extraction_error.emit(result['message'], self.current_file)

    def stop_process(self):
        """
        Stops the timer and terminates the background process if it's running.
        """
        self.check_timer.stop()
        if self.current_process and self.current_process.is_alive():
            self.current_process.terminate()
            self.current_process.join()
        self.current_process = None 