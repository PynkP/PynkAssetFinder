# Features/TopMenu/top_bar.py
from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Qt # (선택) Qt 정렬 상수를 사용하기 위해 추가할 수 있습니다.

from Features.TopMenu.scan_button import ScanButton

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: rgb(40, 40, 40);")
        
        lay_main = QHBoxLayout()
        
        # (선택 사항) 버튼이 창 모서리에 너무 바짝 붙지 않도록 좌우 여백을 약간 줍니다.
        # setContentsMargins(좌, 상, 우, 하)
        lay_main.setContentsMargins(10, 0, 10, 0)
        
        # 똑똑해진 스캔 버튼을 생성해서 레이아웃에 추가
        self.btn_scan = ScanButton("Folder Scan")
        lay_main.addWidget(self.btn_scan)
        
        # 💡 [핵심 추가] 레이아웃 끝에 '스프링'을 달아서 버튼을 왼쪽으로 쫙 밀어줍니다!
        lay_main.addStretch() 
        
        # 나중에 다른 버튼이나 검색창이 추가된다면 addStretch() 코드의 앞이나 뒤에 추가하여 
        # 위치를 유연하게 제어할 수 있습니다.
        
        self.setLayout(lay_main)