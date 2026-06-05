"""프로그램 하단에 제작자 정보와 깃허브 링크를 보여주는 하단 바(Footer) UI입니다."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class BottomBar(QWidget):
    def __init__(self):
        super().__init__()
        # 하단 바의 고정 높이와 배경색을 지정합니다 (탑 바보다 살짝 어둡게)
        self.setFixedHeight(30) 
        self.setStyleSheet("background-color: rgb(25, 25, 25); color: gray; font-size: 12px;")
        self.initUI()

    def initUI(self):
        lay_main = QHBoxLayout()
        lay_main.setContentsMargins(10, 0, 10, 0)
        

        self.wgt_ver_info = QLabel()
        str_version_text = "※ Version_0.3.0"
        self.wgt_ver_info.setText(str_version_text)
        self.wgt_ver_info.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lay_main.addWidget(self.wgt_ver_info)
        

        self.wgt_lbl_info = QLabel()
        # 💡 [핵심] HTML 태그를 사용해서 링크에 색상을 넣고, 클릭 가능하게 만듭니다.
        str_html_text = 'Copy Left @ <a href="https://github.com/PynkP/PynkAssetFinder" style="color: rgb(100, 200, 255); text-decoration: none;">https://github.com/PynkP/PynkAssetFinder</a> Made by PynkP'
        
        self.wgt_lbl_info.setText(str_html_text)
        
        # 💡 이 옵션을 켜주면 사용자가 링크를 클릭했을 때 윈도우 기본 웹 브라우저가 자동으로 열립니다!
        self.wgt_lbl_info.setOpenExternalLinks(True) 
        
        # 글자를 화면 가운데에 오른쪽 정렬합니다.
        self.wgt_lbl_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.wgt_ver_info

        lay_main.addWidget(self.wgt_lbl_info)
        self.setLayout(lay_main)