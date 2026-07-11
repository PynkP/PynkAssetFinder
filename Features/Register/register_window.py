# Features/Register/register_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit
from PySide6.QtCore import Qt
from Features.Register.make_data_form import MakeDataForm  # 💡 새 경로

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
        lay_top.addStretch()  # 💡 왼쪽을 스프링으로 꽉 채워서 버튼을 오른쪽 끝으로 밉니다!
        
        # 헝가리안 표기법 적용
        self.btn_load_data = QPushButton("Load Data")
        self.btn_load_data.setMinimumHeight(35)
        self.btn_load_data.setMinimumWidth(100)
        lay_top.addWidget(self.btn_load_data)
        
        lay_main.addLayout(lay_top)
        
        # ==========================================
        # 2. 중앙: Make Data 폼이 들어갈 영역
        # ==========================================
        self.frm_make_data_area = QFrame()
        self.frm_make_data_area.setObjectName("MakeDataArea") # 💡 고유 이름표 지정
        
        lay_frame = QVBoxLayout()
        lay_frame.setAlignment(Qt.AlignTop) # 💡 요소들을 위에서부터 차곡차곡 쌓도록 설정
        
        # 💡 [추가] Asset Name 입력 영역 (통일성 있는 디자인)
        lay_name_row = QHBoxLayout()
        
        lbl_name = QLabel("Asset Name")
        lbl_name.setMinimumWidth(80) # 아래쪽 라벨들과 동일한 너비 유지
        
        self.let_asset_name = QLineEdit()
        self.let_asset_name.setPlaceholderText("에셋 이름을 입력하세요")
        self.let_asset_name.setMinimumHeight(30)
        
        # 왼쪽 라벨, 오른쪽 텍스트박스 배치
        lay_name_row.addWidget(lbl_name)
        lay_name_row.addWidget(self.let_asset_name)
        
        lay_frame.addLayout(lay_name_row)
        
        # 💡 [추가] ID 발급 영역 (가로 배치)
        lay_id_row = QHBoxLayout()
        
        self.btn_make_id = QPushButton("Make ID")
        self.btn_make_id.setMinimumHeight(30)
        self.btn_make_id.setMinimumWidth(80)
        
        self.let_id = QLineEdit()
        self.let_id.setReadOnly(True) # 유저가 마음대로 수정해서 중복을 만들지 못하게 읽기 전용으로 설정!
        self.let_id.setPlaceholderText("버튼을 눌러 고유 ID를 발급받으세요")
        self.let_id.setMinimumHeight(30)
        
        lay_id_row.addWidget(self.btn_make_id)
        lay_id_row.addWidget(self.let_id)
        
        lay_frame.addLayout(lay_id_row)
        
        # 💡 [추가] 동적으로 작동하는 Make Data 폼
        self.wgt_make_data_form = MakeDataForm()
        lay_frame.addWidget(self.wgt_make_data_form)
        
        lay_frame.addStretch()

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
