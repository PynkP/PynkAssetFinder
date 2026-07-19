# Features/Register/register_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from Features.Register.make_data_form import MakeDataForm  

class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register Data")
        
        # 창 크기 설정 (이미지 비율에 맞춰 세로로 약간 길게 잡았습니다)
        self.setMinimumSize(400, 400) 
        
        # 전체를 아우르는 메인 수직 레이아웃
        lay_main = QVBoxLayout()
        
        # ==========================================
        # 1. 상단: Load Data 버튼 영역 (오른쪽 정렬)
        # ==========================================
        lay_top = QHBoxLayout()
        lay_top.addStretch()  
        
        self.btn_load_data = QPushButton("Load Data")
        self.btn_load_data.setMinimumHeight(35)
        self.btn_load_data.setMinimumWidth(100)
        lay_top.addWidget(self.btn_load_data)
        
        lay_main.addLayout(lay_top)
        
        # ==========================================
        # 2. 중앙: Make Data 폼이 들어갈 영역
        # ==========================================
        self.frm_make_data_area = QFrame()
        self.frm_make_data_area.setObjectName("MakeDataArea") 
        
        lay_frame = QVBoxLayout()
        lay_frame.setAlignment(Qt.AlignTop) 
        
        # 💡 [수정] 동적으로 작동하는 Make Data 폼에 모든 입력 UI를 위임합니다!
        self.wgt_make_data_form = MakeDataForm()
        lay_frame.addWidget(self.wgt_make_data_form)
        
        lay_frame.addStretch()

        self.frm_make_data_area.setLayout(lay_frame)
        
        lay_main.addWidget(self.frm_make_data_area, stretch=1) 
        
        # ==========================================
        # 3. 하단: Make Data 버튼 영역 (왼쪽 정렬)
        # ==========================================
        lay_bottom = QHBoxLayout()
        
        self.btn_make_data = QPushButton("Make Data")
        self.btn_make_data.setMinimumHeight(35)
        self.btn_make_data.setMinimumWidth(100)
        lay_bottom.addWidget(self.btn_make_data)
        
        lay_bottom.addStretch() 
        
        lay_main.addLayout(lay_bottom)
        
        # 최종 레이아웃 적용
        self.setLayout(lay_main)
