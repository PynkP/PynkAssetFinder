# Features/TopMenu/top_bar.py
from PySide6.QtWidgets import QFrame, QHBoxLayout

from Features.TopMenu.scan_button import ScanButton

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        
        lay_main = QHBoxLayout()
        
        # 똑똑해진 스캔 버튼을 생성해서 레이아웃에 추가
        self.btn_scan = ScanButton("Folder Scan")
        lay_main.addWidget(self.btn_scan)
        
        # 나중에 버튼이 추가되면 여기에 그냥 addWidget만 하면 됩니다.
        
        self.setLayout(lay_main)