# Features/Register/category_tag.py

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

class CategoryTag(QFrame):
    """
    동적으로 추가되는 개별 카테고리 태그(블록) UI 위젯입니다.
    예: [ nature (x) ]
    """
    sig_remove_requested = Signal(str) # 삭제 요청 시 자신의 텍스트를 담아 보냅니다

    def __init__(self, _str_text):
        super().__init__()
        self.str_text = _str_text
        
        # 태그 디자인 설정
        self.setObjectName("CategoryTag")
        self.setStyleSheet("""
            #CategoryTag {
                background-color: #555555;
                border-radius: 12px;
                border: 1px solid #777777;
            }
        """)
        
        lay_main = QHBoxLayout()
        lay_main.setContentsMargins(10, 5, 5, 5) # 좌, 상, 우, 하 여백
        lay_main.setSpacing(5)
        
        # 카테고리 이름 라벨
        lbl_text = QLabel(self.str_text)
        lbl_text.setStyleSheet("color: white; font-weight: bold;")
        
        # 'X' 삭제 버튼
        self.btn_remove = QPushButton("✕")
        self.btn_remove.setFixedSize(20, 20)
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #dddddd;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4444;
                color: white;
            }
        """)
        self.btn_remove.clicked.connect(self._onRemoveClicked)
        
        lay_main.addWidget(lbl_text)
        lay_main.addWidget(self.btn_remove)
        self.setLayout(lay_main)
        
    def _onRemoveClicked(self):
        self.sig_remove_requested.emit(self.str_text)
