# Core/main_controller.py

from PySide6.QtCore import QObject
from Core.asset_manager import AssetManager
from Core.category_manager import CategoryManager

# 💡 고용한 팀장들을 수입해옵니다
from Core.Controllers.scan_controller import ScanController
from Core.Controllers.view_controller import ViewController
from Core.Controllers.cache_controller import CacheController # 💡 신규 채용!
from Features.RegisterWindow.register_controller import RegisterController
from Features.SearchBar.search_controller import SearchController

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
        self.ctrl_register = RegisterController(self.wgt_main, self.obj_asset_manager, self.obj_category_manager)
        self.ctrl_search = SearchController(self.wgt_main.wgt_top_bar.wgt_search, self.obj_asset_manager)

        # 3. 부서 간 소통 연결망 구축
        self.initConnections()

    def initConnections(self):
        # 💡 1. 썸네일(그리드뷰) 갱신 신호들
        self.ctrl_scan.sig_scan_all_finished.connect(self.ctrl_view.refreshGridView)
        self.ctrl_cache.sig_cache_loaded.connect(self.ctrl_view.refreshGridView)
        self.ctrl_register.sig_asset_registered.connect(self.ctrl_view.refreshGridView)
        self.ctrl_search.sig_search_completed.connect(self.ctrl_view.refreshGridView)

        # ==========================================
        # 💡 2. [수정] 카테고리 트리 구축 지시 (메모리 증발을 막기 위해 정식 함수 연결!)
        # ==========================================
        self.ctrl_scan.sig_scan_all_finished.connect(self.handleRebuildCategoryTree)
        self.ctrl_cache.sig_cache_loaded.connect(self.handleRebuildCategoryTree)
        self.ctrl_register.sig_asset_registered.connect(self.handleRebuildCategoryTree)

        # 3. 매니저가 트리 완성을 보고하면 화면에 그리도록 지시
        self.obj_category_manager.sig_categories_updated.connect(
            self.wgt_main.wgt_category_panel.updateCategoryTree
        )

        # 4. 좌측 패널 클릭 필터링
        self.wgt_main.wgt_category_panel.sig_category_clicked.connect(self.handleCategoryFilter)

    # ==========================================
    # 💡 [신규 함수] 메모리에서 지워지지 않는 정식 전담 지시 함수
    # ==========================================
    def handleRebuildCategoryTree(self):
        """에셋이 갱신되었을 때 카테고리 트리를 다시 구축하도록 매니저에게 지시합니다."""
        print("👔 [MainController] 에셋 변동 감지! 카테고리 트리를 다시 짓습니다.")
        self.obj_category_manager.buildCategoryTree(self.obj_asset_manager.getAllAssets())

    #[신규 함수] 사장님의 필터링 지휘 전담 함수
    def handleCategoryFilter(self, _list_category_path):
        """카테고리 클릭 보고를 받고 필터링된 화면 갱신을 지시합니다."""
        print(f"👔 [MainController] '{_list_category_path}' 필터링 지시 접수!")
        
        # 1. 창고장에게 해당 경로로 필터링해오라고 지시
        list_filtered = self.obj_asset_manager.getFilteredAssets(_list_category_path)
        print(f"🔍 [MainController] 창고 검색 완료: 총 {len(list_filtered)}개 발견됨.")
        
        # 2. 화면 팀장에게 걸러진 리스트만 새로 그리라고 지시
        self.ctrl_view.refreshGridView(list_filtered)