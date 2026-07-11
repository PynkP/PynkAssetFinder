# Features/SharedUI/log_window.py

import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QTextCursor

class StreamInterceptor(QObject):
    sig_text_written = Signal(str)

    def write(self, _str_text):
        self.sig_text_written.emit(str(_str_text))
        
    def flush(self):
        pass

class LogWindow(QDialog):
    def __init__(self, _parent=None):
        super().__init__(_parent)
        self.setWindowTitle("Pynk Log Console")
        self.resize(800, 400)
        
        self._initUI()
        self._connectStream()
        
    def _initUI(self):
        lay_main = QVBoxLayout()
        
        self.wgt_txt_log = QPlainTextEdit()
        self.wgt_txt_log.setReadOnly(True)
        # 콘솔 느낌을 주기 위한 스타일
        self.wgt_txt_log.setStyleSheet(
            "background-color: #1E1E1E; color: #D4D4D4; font-family: Consolas, monospace; font-size: 13px;"
        )
        lay_main.addWidget(self.wgt_txt_log)
        
        lay_btn = QHBoxLayout()
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.wgt_txt_log.clear)
        
        lay_btn.addStretch(1)
        lay_btn.addWidget(self.btn_clear)
        
        lay_main.addLayout(lay_btn)
        self.setLayout(lay_main)
        
    def _connectStream(self):
        self.obj_original_stdout = sys.stdout
        self.obj_original_stderr = sys.stderr
        
        self.obj_stream = StreamInterceptor()
        self.obj_stream.sig_text_written.connect(self._appendLog)
        
        sys.stdout = self.obj_stream
        sys.stderr = self.obj_stream
        
    def _appendLog(self, _str_text):
        self.wgt_txt_log.moveCursor(QTextCursor.End)
        self.wgt_txt_log.insertPlainText(_str_text)
        self.wgt_txt_log.moveCursor(QTextCursor.End)

    def closeEvent(self, _event):
        # 창이 닫혀도 메모리에서 지우지 않고 숨기기만 합니다. (백그라운드 로깅 유지)
        _event.ignore()
        self.hide()
