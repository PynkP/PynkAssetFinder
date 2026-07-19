# Features/Modify/modify_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from Features.Register.make_data_form import MakeDataForm

class ModifyWindow(QDialog):
    """
    에셋의 이름, 타입, 썸네일, 카테고리를 수정하는 다이얼로그 창입니다.
    RegisterWindow를 참고하여 만들었으며, MakeDataForm을 재사용합니다.
    Make ID / Load Data 버튼 없이 Modify 전용 구성으로 운영됩니다.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modify Asset Data")
        self.setMinimumSize(400, 400)
        self.setFixedWidth(400)  # 💡 RegisterWindow와 동일한 너비로 고정

        lay_main = QVBoxLayout()

        # ==========================================
        # 중앙: MakeDataForm 폼 영역
        # ==========================================
        self.frm_data_area = QFrame()
        self.frm_data_area.setObjectName("MakeDataArea")

        lay_frame = QVBoxLayout()
        lay_frame.setAlignment(Qt.AlignTop)

        # 💡 MakeDataForm 통 재사용 후 Modify 모드 적용 (Make ID 행 숨김)
        self.wgt_make_data_form = MakeDataForm()
        self.wgt_make_data_form.setModifyMode()
        lay_frame.addWidget(self.wgt_make_data_form)

        lay_frame.addStretch()
        self.frm_data_area.setLayout(lay_frame)

        lay_main.addWidget(self.frm_data_area, stretch=1)

        # ==========================================
        # 하단: Modify Data 버튼 (왼쪽 정렬)
        # ==========================================
        lay_bottom = QHBoxLayout()

        self.btn_modify_data = QPushButton("Modify Data")
        self.btn_modify_data.setMinimumHeight(35)
        self.btn_modify_data.setMinimumWidth(100)
        lay_bottom.addWidget(self.btn_modify_data)

        lay_bottom.addStretch()
        lay_main.addLayout(lay_bottom)

        self.setLayout(lay_main)
