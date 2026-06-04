# Core/main_controller.py

from PySide6.QtCore import QObject
from Core.asset_manager import AssetManager
from Core.category_manager import CategoryManager

# 💡 고용한 팀장들을 수입해옵니다
from Core.Controllers.scan_controller import ScanController
from Core.Controllers.view_controller import ViewController
from Core.Controllers.cache_controller import CacheController # 💡 신규 채용!

class MainController(QObject):
    """최상위 지휘관: 팀장들을 고용하고, 부서 간의 소통 창구만 연결해 줍니다."""
    def __init__(self, _wgt_main):
        super().__init__()
        self.wgt_main = _wgt_main
        
        # 1. 공용 데이터 창고(Manager) 개설
        self.obj_asset_manager = AssetManager()
        self.obj_category_manager = CategoryManager()
        
        # 2. 부서별 전담 팀장 고용 (사장님의 권한인 UI와 창고를 공유해 줍니다)
        self.ctrl_scan = ScanController(self.wgt_main, self.obj_asset_manager)
        self.ctrl_view = ViewController(self.wgt_main, self.obj_asset_manager)
        self.ctrl_cache = CacheController(self.wgt_main, self.obj_asset_manager)

        # 3. 부서 간 소통 연결망 구축
        self.initConnections()

    def initConnections(self):
        # 💡 [핵심] 수집 팀장이 "스캔 다 끝났습니다!" 하고 신호를 보내면
        # 사장님이 화면 팀장에게 "새로고침 해!" 라고 지시를 내립니다.
        self.ctrl_scan.sig_scan_all_finished.connect(self.ctrl_view.refreshGridView)

        # 💡 캐시 로드 끝 -> 화면 갱신
        self.ctrl_cache.sig_cache_loaded.connect(self.ctrl_view.refreshGridView)