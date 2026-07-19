# Features/Favorites/favorites_panel.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from Features.Category.category_panel import CategoryPanel

class FavoritesPanel(QWidget):
    """즐겨찾기 전용 좌측 하단 패널입니다."""
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("FavoritesPanel")
        
        self.initUI()
        
    def initUI(self):
        lay_main = QVBoxLayout()
        lay_main.setContentsMargins(0, 0, 0, 0)
        
        # 💖 상단에 예쁜 타이틀 라벨 추가
        self.wgt_lbl_title = QLabel("Favorites")
        self.wgt_lbl_title.setStyleSheet("color: rgb(255, 150, 180); font-weight: bold; font-size: 12px; padding: 2px;")
        lay_main.addWidget(self.wgt_lbl_title)
        
        # 🌲 기존 CategoryPanel을 위젯 내부에 포함(Composition)하여 트리 기능 가져오기
        self.wgt_category_panel = CategoryPanel()
        
        lay_main.addWidget(self.wgt_category_panel)
        self.setLayout(lay_main)

    def updateFavoritesTree(self, _obj_root_node):
        """매니저가 완성한 트리를 UI(내부의 CategoryPanel)에 그리도록 전달합니다."""
        self.wgt_category_panel.updateCategoryTree(_obj_root_node)
