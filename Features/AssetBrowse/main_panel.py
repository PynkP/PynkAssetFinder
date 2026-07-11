# Features/AssetBrowse/main_panel.py

from PySide6.QtWidgets import QFrame, QVBoxLayout
# 💡 방금 분리한 바둑판 전용 뷰를 가져옵니다.

from Features.AssetBrowse.asset_grid_view import AssetGridView  # 💡 새 경로

class MainPanel(QFrame):
    def __init__(self):
        super().__init__()
        
        # 패널 기본 스타일 설정
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        
        self.initBaseLayout()
        self.initViews()

    def initBaseLayout(self):
        self.lay_main = QVBoxLayout()
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

    def initViews(self):
        """실제 에셋들이 그려질 그리드 뷰를 생성하고 배치합니다."""
        self.wgt_grid_view = AssetGridView()
        self.lay_main.addWidget(self.wgt_grid_view)

    def getGridView(self):
        """외부에서 그리드 뷰 객체에 접근할 수 있도록 인스턴스를 반환합니다."""
        return self.wgt_grid_view
