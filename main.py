# main.py (일부 수정)
import sys
import os # 파일 경로 확인용
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog

from Features.TopMenu.top_bar import TopBar
from Features.CategoryView.category_panel import CategoryPanel
from Features.ThumbnailView.main_panel import MainPanel
from Features.ThumbnailView.thumbnail_loader import ThumbnailLoader 
from Features.BottomBar.bottom_bar import BottomBar

from Core.main_controller import MainController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pynk Asset Finder")
        self.resize(1200, 800)
        
        # 1. UI 위젯 배치
        self._initUI()
        
        # 💡 2. 로더 생성 및 시그널 연결 (콜백 방식 제거)
        self.obj_chunk_loader = ThumbnailLoader()
        obj_grid_view = self.wgt_main_panel.getGridView()
        
        # 로더가 소리치면(Signal), 그리드 뷰가 행동(Slot)하도록 직통 전화선 연결!
        self.obj_chunk_loader.sig_clear_requested.connect(obj_grid_view.clearGrid)
        self.obj_chunk_loader.sig_chunk_ready.connect(obj_grid_view.addThumbnailChunk)
        # (필요하다면 sig_load_completed 도 연결할 수 있습니다)
        
        # 3. 컨트롤러 고용
        self.obj_controller = MainController(_wgt_main=self)
    
    def _initUI(self):
        wgt_central = QWidget()
        lay_main = QVBoxLayout()
        lay_main.setContentsMargins(0, 0, 0, 0)
        lay_main.setSpacing(0)
        
        self.wgt_top_bar = TopBar()
        lay_main.addWidget(self.wgt_top_bar)
        
        lay_content = QHBoxLayout()
        lay_content.setContentsMargins(0, 0, 0, 0)
        lay_content.setSpacing(0)
        
        self.wgt_category_panel = CategoryPanel()
        lay_content.addWidget(self.wgt_category_panel, 1)
        
        self.wgt_main_panel = MainPanel()
        lay_content.addWidget(self.wgt_main_panel, 4)
        
        # (기존 코드) 중앙 패널들을 메인 레이아웃에 추가합니다.
        lay_main.addLayout(lay_content)
        
        # 💡 2. 가장 마지막(화면 맨 아래)에 바텀 바를 장착합니다!
        self.wgt_bottom_bar = BottomBar()
        lay_main.addWidget(self.wgt_bottom_bar)
        
        wgt_central.setLayout(lay_main)
        self.setCentralWidget(wgt_central)

    def openFolderDialog(self):
        str_path = QFileDialog.getExistingDirectory(self, "Select Asset Folder")
        return str_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 💡 1. 스타일 시트 파일 읽어서 프로그램 전체(app)에 적용하기!
    str_qss_path = "Resources/style.qss"
    if os.path.exists(str_qss_path):
        with open(str_qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            print("🎨 스타일 시트 로드 완료!")
    else:
        print("⚠️ 경고: Resources/style.qss 파일을 찾을 수 없습니다.")

    # 2. 메인 윈도우 실행
    window = MainWindow()
    window.show()
    sys.exit(app.exec())