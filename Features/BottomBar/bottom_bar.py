"""프로그램 하단에 제작자 정보와 깃허브 링크를 보여주는 하단 바(Footer) UI입니다."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

class BottomBar(QWidget):
    # 💡 로그 버튼이 눌렸음을 외부에 알리는 시그널
    sig_log_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("bottomBarWidget")
        self.setFixedHeight(30) 
        self.initUI()

    def initUI(self):
        lay_main = QHBoxLayout()
        lay_main.setContentsMargins(10, 0, 10, 0)
        
        self.wgt_ver_info = QLabel()
        str_version_text = "※ Version_0.7.0"
        self.wgt_ver_info.setText(str_version_text)
        self.wgt_ver_info.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lay_main.addWidget(self.wgt_ver_info)
        
        # 💡 로그 창을 띄우는 버튼 생성
        self.btn_log = QPushButton("📜 Log")
        self.btn_log.setCursor(Qt.PointingHandCursor)
        # 버튼이 클릭되면 시그널을 발사합니다.
        self.btn_log.clicked.connect(self.sig_log_clicked.emit)
        
        lay_main.addWidget(self.btn_log)
        
        # 💡 1. 좌측 여백 추가 (왼쪽 요소들과 가운데 요소 사이 공간)
        lay_main.addStretch(1)

        # 💡 2. 가운데 "How to Use" 추가
        self.wgt_lbl_how_to_use = QLabel()
        # TODO: 실제 연결할 URL을 넣어주세요! (예: 노션 링크, 깃허브 위키 등)
        str_how_to_use_html = 'How to Use : <a href="https://docs.google.com/document/d/13ckMc8KbkGt6T9giIYvtM7x5aSBHUNil0dmfvk-EyVc/edit?tab=t.0" style="color: rgb(100, 200, 255); text-decoration: none;">Document URL</a>'
        self.wgt_lbl_how_to_use.setText(str_how_to_use_html)
        self.wgt_lbl_how_to_use.setOpenExternalLinks(True) 
        self.wgt_lbl_how_to_use.setAlignment(Qt.AlignCenter)
        
        lay_main.addWidget(self.wgt_lbl_how_to_use)

        # 💡 3. 우측 여백 추가 (가운데 요소와 오른쪽 요소 사이 공간)
        lay_main.addStretch(1)

        self.wgt_lbl_info = QLabel()
        str_html_text = 'Copy Left @ <a href="https://github.com/PynkP/PynkAssetFinder" style="color: rgb(100, 200, 255); text-decoration: none;">https://github.com/PynkP/PynkAssetFinder</a> Made by PynkP'
        
        self.wgt_lbl_info.setText(str_html_text)
        self.wgt_lbl_info.setOpenExternalLinks(True) 
        self.wgt_lbl_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        lay_main.addWidget(self.wgt_lbl_info)
        self.setLayout(lay_main)