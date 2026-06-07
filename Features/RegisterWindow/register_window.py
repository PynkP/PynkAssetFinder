# Features/RegisterWindow/register_window.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt

class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register Data")
        
        # 창 크기 설정 (이미지 비율에 맞춰 세로로 약간 길게 잡았습니다)
        self.setMinimumSize(400, 600) 
        
        # 전체를 아우르는 메인 수직 레이아웃
        lay_main = QVBoxLayout()
        
        # ==========================================
        # 1. 상단: Load Data 버튼 영역 (오른쪽 정렬)
        # ==========================================
        lay_top = QHBoxLayout()
        lay_top.addStretch()  # 💡 왼쪽을 스프링으로 꽉 채워서 버튼을 오른쪽 끝으로 밉니다!
        
        # 헝가리안 표기법 적용
        self.btn_load_data = QPushButton("Load Data")
        self.btn_load_data.setMinimumHeight(35)
        self.btn_load_data.setMinimumWidth(100)
        lay_top.addWidget(self.btn_load_data)
        
        lay_main.addLayout(lay_top)
        
        # ==========================================
        # 2. 중앙: Make Data 폼이 들어갈 임시 영역 (QFrame)
        # ==========================================
        self.frm_make_data_area = QFrame()
        
        # 이미지처럼 어두운 배경색을 주어 영역을 확실히 구분합니다
        self.frm_make_data_area.setStyleSheet("background-color: #444444; border-radius: 5px;") 
        
        # 프레임 내부 텍스트 레이아웃
        lay_frame = QVBoxLayout()
        lbl_placeholder = QLabel("Make Data를 만드는 곳\n나중에 만들 UI 영역")
        lbl_placeholder.setAlignment(Qt.AlignCenter) # 텍스트 중앙 정렬
        lbl_placeholder.setStyleSheet("color: white; font-size: 16px;") 
        
        lay_frame.addWidget(lbl_placeholder)
        self.frm_make_data_area.setLayout(lay_frame)
        
        # 💡 남는 공간을 모두 중앙 영역이 차지하도록 stretch=1 옵션을 줍니다!
        lay_main.addWidget(self.frm_make_data_area, stretch=1) 
        
        # ==========================================
        # 3. 하단: Make Data 버튼 영역 (왼쪽 정렬)
        # ==========================================
        lay_bottom = QHBoxLayout()
        
        self.btn_make_data = QPushButton("Make Data")
        self.btn_make_data.setMinimumHeight(35)
        self.btn_make_data.setMinimumWidth(100)
        lay_bottom.addWidget(self.btn_make_data)
        
        lay_bottom.addStretch() # 💡 오른쪽을 스프링으로 밀어서 버튼을 왼쪽 끝으로 고정합니다!
        
        lay_main.addLayout(lay_bottom)
        
        # 최종 레이아웃 적용
        self.setLayout(lay_main)
