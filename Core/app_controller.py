# Core/app_controller.py

from PySide6.QtCore import QObject
from Core.Repositories.asset_manager import AssetManager       # 💡 새 경로
from Features.Category.category_manager import CategoryManager  # 💡 새 경로

# 💡 기능별로 분산된 컨트롤러들을 수입해옵니다
from Features.Scan.scan_controller import ScanController        # 💡 새 경로
from Features.AssetBrowse.view_controller import ViewController # 💡 새 경로
from Features.Cache.cache_controller import CacheController     # 💡 새 경로
from Features.Register.register_controller import RegisterController # 💡 새 경로
from Features.Search.search_controller import SearchController  # 💡 새 경로

class AppController(QObject):
    """최상위 지휘관: 기능별 컨트롤러들을 고용하고, 부서 간의 소통 창구만 연결해 줍니다."""
    def __init__(self, _wgt_main):
        super().__init__()
        self.wgt_main = _wgt_main
        
        # 1. 공용 데이터 창고(Manager) 개설
        self.obj_asset_manager = AssetManager()
        self.obj_category_manager = CategoryManager()
        
        # 2. 부서별 전담 컨트롤러 고용 (사장님의 권한인 UI와 창고를 공유해 줍니다)
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
        # 💡 2. 카테고리 트리 구축 지시 (메모리 증발을 막기 위해 정식 함수 연결!)
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

        # 💡 [추가] 뷰 컨트롤러에서 삭제되었다는 신호를 받으면 화면 갱신
        self.ctrl_view.sig_asset_deleted.connect(self.handleAssetDeleted)

    # ==========================================
    # 💡 [신규 함수] 메모리에서 지워지지 않는 정식 전담 지시 함수
    # ==========================================
    def handleRebuildCategoryTree(self):
        """에셋이 갱신되었을 때 카테고리 트리를 다시 구축하도록 매니저에게 지시합니다."""
        print("👔 [AppController] 에셋 변동 감지! 카테고리 트리를 다시 짓습니다.")
        self.obj_category_manager.buildCategoryTree(self.obj_asset_manager.getAllAssets())

    def handleAssetDeleted(self):
        """에셋이 리스트에서 삭제되었을 때 후속 조치를 합니다."""
        # 1. 카테고리 트리 재구축 (해당 에셋이 속했던 카테고리가 비어버렸을 수도 있으므로)
        self.handleRebuildCategoryTree()
        
        # 2. 현재 선택된 카테고리를 기준으로 화면(그리드 뷰) 갱신
        list_filtered = self.obj_asset_manager.getFilteredAssets(self.obj_asset_manager.list_current_category_path)
        self.ctrl_view.refreshGridView(list_filtered)

    # [신규 함수] 사장님의 필터링 지휘 전담 함수
    def handleCategoryFilter(self, _list_category_path):
        """카테고리 클릭 보고를 받고 필터링된 화면 갱신을 지시합니다."""
        print(f"👔 [AppController] '{_list_category_path}' 필터링 지시 접수!")
        
        # 1. 창고장에게 해당 경로로 필터링해오라고 지시
        list_filtered = self.obj_asset_manager.getFilteredAssets(_list_category_path)
        print(f"🔍 [AppController] 창고 검색 완료: 총 {len(list_filtered)}개 발견됨.")
        
        # 2. 화면 팀장에게 걸러진 리스트만 새로 그리라고 지시
        self.ctrl_view.refreshGridView(list_filtered)
