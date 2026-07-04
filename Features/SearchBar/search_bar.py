# Features/SearchBar/search_bar.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

class SearchBar(QWidget):
    """상단 메뉴 중앙에 들어갈 검색 UI 뷰입니다."""
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        lay_main = QHBoxLayout()
        # 기존 top_bar와 어울리도록 여백을 최소화합니다.
        lay_main.setContentsMargins(0, 0, 0, 0)
        
        # 1. 텍스트 입력창
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Search assets...")
        self.input_search.setMinimumWidth(350)
        self.input_search.setMinimumHeight(37)
        
        # 2. 검색 버튼
        self.btn_search = QPushButton("Search")
        self.btn_search.setMinimumHeight(35)
        
        lay_main.addWidget(self.input_search)
        lay_main.addWidget(self.btn_search)
        
        self.setLayout(lay_main)
