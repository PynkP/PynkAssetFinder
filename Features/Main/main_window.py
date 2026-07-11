# Features/Main/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtGui import QIcon

from Core.Utils.resource_helper import resource_path
from Features.SharedUI.top_bar import TopBar
from Features.Category.category_panel import CategoryPanel
from Features.AssetBrowse.main_panel import MainPanel
from Features.AssetBrowse.thumbnail_loader import ThumbnailLoader
from Features.SharedUI.bottom_bar import BottomBar
from Features.SharedUI.log_window import LogWindow

from Core.app_controller import AppController
from Features.Main.shortcut_action import ShortcutAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 프로그램 시작과 동시에 로그 창을 생성하여 백그라운드 수집을 시작합니다.
        self.wgt_log_window = LogWindow(self)
        
        self.setWindowTitle("Pynk Asset Finder")
        self.setMinimumWidth(1280)
        self.setMinimumHeight(400)
        self.resize(1280, 800)

        self.setWindowIcon(QIcon(resource_path("Resources/icons/app_icon.ico")))

        # 1. UI 위젯 배치
        self._initUI()
        
        # 2. 로더 생성 및 시그널 연결
        self.obj_chunk_loader = ThumbnailLoader()
        obj_grid_view = self.wgt_main_panel.getGridView()
        
        self.obj_chunk_loader.sig_clear_requested.connect(obj_grid_view.clearGrid)
        self.obj_chunk_loader.sig_chunk_ready.connect(obj_grid_view.addThumbnailChunk)
        
        # 무한 스크롤 연동!
        obj_grid_view.sig_scroll_bottom_reached.connect(self.obj_chunk_loader.loadNextChunk)
        
        # 3. 앱 컨트롤러 고용
        self.obj_controller = AppController(_wgt_main=self)
        
        # 4. 단축키 전담반 고용 (UI와 컨트롤러가 준비된 후 호출)
        self.obj_shortcut_action = ShortcutAction(self, self.obj_controller)
    
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
        
        lay_main.addLayout(lay_content)
        
        self.wgt_bottom_bar = BottomBar()
        self.wgt_bottom_bar.sig_log_clicked.connect(self.wgt_log_window.show)
        lay_main.addWidget(self.wgt_bottom_bar)
        
        wgt_central.setLayout(lay_main)
        self.setCentralWidget(wgt_central)

    def openFolderDialog(self):
        str_path = QFileDialog.getExistingDirectory(self, "Select Asset Folder")
        return str_path
