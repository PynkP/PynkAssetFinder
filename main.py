# main.py (일부 수정)
import sys
import os # 파일 경로 확인용
import ctypes
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog

from PySide6.QtGui import QIcon

from Features.TopMenu.top_bar import TopBar
from Features.CategoryView.category_panel import CategoryPanel
from Features.ThumbnailView.main_panel import MainPanel
from Features.ThumbnailView.thumbnail_loader import ThumbnailLoader 
from Features.BottomBar.bottom_bar import BottomBar
from Features.LogView.log_window import LogWindow

from Core.main_controller import MainController


# 💡 [추가] exe 파일로 만들었을 때도 리소스(아이콘, qss) 위치를 완벽하게 찾아주는 마법의 함수!
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller가 만든 임시 폴더 경로를 찾습니다.
        base_path = sys._MEIPASS
    except Exception:
        # 일반 파이썬 실행일 때는 현재 폴더를 기준으로 합니다.
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 💡 프로그램 시작과 동시에 로그 창을 생성하여 백그라운드 수집을 시작합니다.
        self.wgt_log_window = LogWindow(self)
        
        self.setWindowTitle("Pynk Asset Finder")
        self.setMinimumWidth(1280)  # ✅ 최소 너비 1280 고정
        self.setMinimumHeight(400)
        self.resize(1280, 800)

        self.setWindowIcon(QIcon(resource_path("Resources/icons/app_icon.ico")))

        # 1. UI 위젯 배치
        self._initUI()
        
        # 💡 2. 로더 생성 및 시그널 연결 (콜백 방식 제거)
        self.obj_chunk_loader = ThumbnailLoader()
        obj_grid_view = self.wgt_main_panel.getGridView()
        
        # 로더가 소리치면(Signal), 그리드 뷰가 행동(Slot)하도록 직통 전화선 연결!
        self.obj_chunk_loader.sig_clear_requested.connect(obj_grid_view.clearGrid)
        self.obj_chunk_loader.sig_chunk_ready.connect(obj_grid_view.addThumbnailChunk)
        
        # 💡 [추가] 무한 스크롤 연동! 스크롤이 바닥에 닿으면 로더에게 다음 청크를 가져오라고 지시
        obj_grid_view.sig_scroll_bottom_reached.connect(self.obj_chunk_loader.loadNextChunk)
        
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
        
        # 💡 바텀 바의 로그 버튼 클릭 시그널을 로그 창 띄우기와 연결합니다.
        self.wgt_bottom_bar.sig_log_clicked.connect(self.wgt_log_window.show)
        
        lay_main.addWidget(self.wgt_bottom_bar)
        
        wgt_central.setLayout(lay_main)
        self.setCentralWidget(wgt_central)

    def openFolderDialog(self):
        str_path = QFileDialog.getExistingDirectory(self, "Select Asset Folder")
        return str_path
    

if __name__ == "__main__":

    try:
        # 💡 [핵심 마법] 윈도우 작업표시줄 아이콘 분리 독립 선언!
        try:
            # 나만의 고유한 프로그램 ID를 만듭니다 (이름은 마음대로 하셔도 됩니다)
            myappid = 'pynkp.assetfinder.version_1' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            pass # (혹시라도 Mac이나 Linux에서 실행될 때 에러가 나지 않도록 하는 안전장치)

        app = QApplication(sys.argv)
        
        # 💡 [수정 2] 프로그램 전체 아이콘에도 resource_path 마법 적용!
        app.setWindowIcon(QIcon(resource_path("Resources/icons/app_icon.ico")))

        # 💡 [수정 3] 기능별로 나뉜 여러 개의 스타일 시트를 차례대로 읽어 합칩니다.
        list_qss_files = [
            "Resources/Styles/main_style.qss",
            "Resources/Styles/topbar_style.qss",
            "Resources/Styles/category_style.qss",
            "Resources/Styles/thumbnail_style.qss",
            "Resources/Styles/register_style.qss",
            "Resources/Styles/bottombar_style.qss",
        ]

        str_combined_qss = ""
        for str_file in list_qss_files:
            str_qss_path = resource_path(str_file)
            if os.path.exists(str_qss_path):
                with open(str_qss_path, "r", encoding="utf-8") as f:
                    str_combined_qss += f.read() + "\n"
            else:
                print(f"⚠️ 경고: {str_file} 파일을 찾을 수 없습니다.")

        app.setStyleSheet(str_combined_qss)
        print("🎨 분할된 스타일 시트 로드 및 병합 완료!")

        # 2. 메인 윈도우 실행
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        traceback.print_exc()