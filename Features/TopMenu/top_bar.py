# Features/TopMenu/top_bar.py
from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Qt # (선택) Qt 정렬 상수를 사용하기 위해 추가할 수 있습니다.
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton

from Features.TopMenu.scan_button import ScanButton

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        lay_main = QHBoxLayout()
        
        # (선택 사항) 버튼이 창 모서리에 너무 바짝 붙지 않도록 좌우 여백을 약간 줍니다.
        # setContentsMargins(좌, 상, 우, 하)
        lay_main.setContentsMargins(10, 0, 10, 0)
        
        # ==========================================
        # 1. 🖼️ 일반 스캔 버튼 -> "Image Asset"
        # ==========================================
        # 💡 이름 변경
        self.btn_scan = ScanButton("Image Asset")
        
        # 💡 크기 및 폰트 키우기
        self.btn_scan.setMinimumHeight(30) # 세로 길이를 40픽셀로 넉넉하게!
        self.btn_scan.setMinimumWidth(100) # 가로 길이도 넉넉하게!


        # ==========================================
        # 2. 🚀 메가스캔 스캔 버튼 (Mega Scan Asset)
        # ==========================================
        # 💡 크기 및 폰트 키우기
        self.btn_scan_mega = ScanButton("Scan Mega Assets")

        self.btn_scan_mega.setMinimumHeight(30) 
        self.btn_scan_mega.setMinimumWidth(120)


        lay_main.addWidget(self.btn_scan)
        lay_main.addWidget(self.btn_scan_mega)

        # 💡 [핵심 추가] 레이아웃 끝에 '스프링'을 달아서 버튼을 왼쪽으로 쫙 밀어줍니다!
        lay_main.addStretch() 
        
        # 3. Register 버튼
        self.btn_register = QPushButton("Register")
        self.btn_register.setMinimumHeight(30)
        self.btn_register.setMinimumWidth(90)
        lay_main.addWidget(self.btn_register)
        
        self.btn_load = QPushButton("Load Cache")
        self.btn_load.setMinimumHeight(30)
        self.btn_load.setMinimumWidth(90)

        # 4. Save 버튼 (저장하기)
        self.btn_save = QPushButton("Save Cache")
        self.btn_save.setMinimumHeight(30)
        self.btn_save.setMinimumWidth(90)

        # 오른쪽 위젯들을 레이아웃에 추가
        lay_main.addWidget(self.btn_load)
        lay_main.addWidget(self.btn_save)

        self.setLayout(lay_main)