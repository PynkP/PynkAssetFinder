import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtGui import QColor, QPalette

from Features.TopMenu.top_bar import TopBar
from Features.ThumbnailView.main_panel import MainPanel
from Features.ThumbnailView.thumbnail_loader import ThumbnailLoader
from Features.CategoryView.category_panel import CategoryPanel
from Core.asset_manager import AssetManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 1. 윈도우 기본 설정
        self.initWindow()

        # 2. 뼈대가 되는 기본 레이아웃 생성
        self.initBaseLayout()

        # 3. 각 구역별 UI 생성 및 배치
        self.initTopBarUI()
        self.initCategoryPanelUI()
        self.initMainPanelUI()

        # 4. 최종 레이아웃 적용
        self.setLayout(self.lay_main)

    def initWindow(self):
        """윈도우 자체의 속성(크기, 배경색 등) 설정"""
        self.setWindowTitle("Pynk Asset Finder")
        self.resize(1280, 720)

        # 변수: 헝가리안(obj) + 뱀표기법(palette)
        obj_palette = self.palette()
        obj_palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(obj_palette)
        self.setAutoFillBackground(True)

    def initBaseLayout(self):
        """각 패널을 담을 메인 레이아웃들만 미리 생성"""
        # 변수: 헝가리안(lay) + 뱀표기법(main, content)
        self.lay_main = QVBoxLayout()
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.lay_main.setSpacing(0)

        self.lay_content = QHBoxLayout()
        self.lay_content.setContentsMargins(0, 0, 0, 0)
        self.lay_content.setSpacing(0)

    def initTopBarUI(self):
        """상단 바 생성 및 메인 레이아웃에 추가"""
        # 변수: 헝가리안(wgt) + 뱀표기법(top_bar)
        self.wgt_top_bar = TopBar()
        self.lay_main.addWidget(self.wgt_top_bar)

    def initCategoryPanelUI(self):
        """카테고리 패널 생성 및 컨텐츠(가로) 레이아웃에 추가"""
        self.wgt_category_panel = CategoryPanel()
        self.lay_content.addWidget(self.wgt_category_panel)

    def initMainPanelUI(self):
        self.wgt_main_panel = MainPanel()
        self.lay_content.addWidget(self.wgt_main_panel)
        self.lay_main.addLayout(self.lay_content)

        self.obj_chunk_loader = ThumbnailLoader()
        obj_grid_view = self.wgt_main_panel.getGridView()
        
        # 💡 3개의 스위치를 로더에게 몽땅 쥐여줍니다.
        self.obj_chunk_loader.setCallbacks(
            _func_clear=obj_grid_view.clearGrid,                # 화면 청소 스위치
            _func_chunk=obj_grid_view.addThumbnailChunk,        # 화면 그리기 스위치
            _func_completed=None                          # 💡 에러 원인 제거! 당장 필요 없는 스위치는 None으로 뺍니다.
            #_func_completed=self.wgt_top_bar.onDrawCompleted    # 상단바 복구 스위치 (필요시 ScanButton의 함수로 변경 가능)
        )

        # 💡 [핵심 변경] TopBar의 '스마트 버튼(btn_scan)'이 쏘는 완료 신호를 마스터 함수에 연결합니다!
        self.wgt_top_bar.btn_scan.sig_scan_completed.connect(self.onScanCompleted)

    # ==========================================
    # 🔗 [콜백 (이벤트) 관리 구역]
    # ==========================================
    def onScanCompleted(self):
        """스캔 버튼에서 폴더 스캔을 성공적으로 마쳤다는 신호가 오면 실행됩니다."""
        # 1. 썸네일 쪽 로더 가동! (오른쪽 바둑판 그리기)
        self.obj_chunk_loader.reloadAssets()
        
        # 2. 왼쪽 카테고리 패널에 새 데이터 새로고침!
        self.wgt_category_panel.updateCategoryList()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())