# Core/main_controller.py

from PySide6.QtCore import QObject
from Core.asset_manager import AssetManager
from Core.category_manager import CategoryManager

# 💡 고용한 팀장들을 수입해옵니다
from Core.Controllers.scan_controller import ScanController
from Core.Controllers.view_controller import ViewController
from Core.Controllers.cache_controller import CacheController # 💡 신규 채용!
from Features.RegisterWindow.register_controller import RegisterController

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
        self.ctrl_register = RegisterController(self.wgt_main, self.obj_asset_manager)

        # 3. 부서 간 소통 연결망 구축
        self.initConnections()

    def initConnections(self):
        # 💡 [핵심] 수집 팀장이 "스캔 다 끝났습니다!" 하고 신호를 보내면
        # 사장님이 화면 팀장에게 "새로고침 해!" 라고 지시를 내립니다.
        self.ctrl_scan.sig_scan_all_finished.connect(self.ctrl_view.refreshGridView)

        # 💡 캐시 로드 끝 -> 화면 갱신
        self.ctrl_cache.sig_cache_loaded.connect(self.ctrl_view.refreshGridView)

        # 💡 에셋 개별 등록 완료 -> 화면 갱신
        self.ctrl_register.sig_asset_registered.connect(self.ctrl_view.refreshGridView)

        # ==========================================
        # 💡 2. [추가] 카테고리 트리 구축 지시
        # ==========================================
        # 스캔이나 로드가 끝났을 때, 카테고리 매니저를 호출해서 트리를 갱신하라고 지시합니다.
        # (람다를 써서 창고의 리스트를 통째로 넘겨줍니다)
        self.ctrl_scan.sig_scan_all_finished.connect(
            lambda: self.obj_category_manager.buildCategoryTree(self.obj_asset_manager.getAllAssets())
        )
        self.ctrl_cache.sig_cache_loaded.connect(
            lambda: self.obj_category_manager.buildCategoryTree(self.obj_asset_manager.getAllAssets())
        )
        self.ctrl_register.sig_asset_registered.connect(
            lambda: self.obj_category_manager.buildCategoryTree(self.obj_asset_manager.getAllAssets())
        )
        # ==========================================
        # 💡 [추가] 매니저가 "트리 완성했다!" 하고 신호를 보내면, 
        # 화면 팀장(또는 좌측 패널)에게 "받아서 그려라!" 라고 전달합니다.
        # ==========================================
        # (주의: self.wgt_main.wgt_category_panel 등 실제 사용하시는 변수명에 맞게 적어주세요!)
        self.obj_category_manager.sig_categories_updated.connect(
            self.wgt_main.wgt_category_panel.updateCategoryTree
        )

        # ==========================================
        # 💡 [필터링 마법 연결] 좌측 패널 클릭 -> 사장님 호출
        # ==========================================
        # (wgt_category_panel 등 실제 변수명에 맞게 조정해 주세요)
        self.wgt_main.wgt_category_panel.sig_category_clicked.connect(self.handleCategoryFilter)

    #[신규 함수] 사장님의 필터링 지휘 전담 함수
    def handleCategoryFilter(self, _str_category_name):
        """카테고리 클릭 보고를 받고 필터링된 화면 갱신을 지시합니다."""
        print(f"👔 [MainController] '{_str_category_name}' 필터링 지시 접수!")
        
        # 1. 창고장에게 해당 카테고리만 가져오라고 지시 (아까 만든 함수 사용!)
        list_filtered = self.obj_asset_manager.getFilteredAssets(_str_category_name)
        print(f"🔍 [MainController] 창고 검색 완료: 총 {len(list_filtered)}개 발견됨.")
        
        # 2. 화면 팀장에게 걸러진 리스트만 새로 그리라고 지시
        self.ctrl_view.refreshGridView(list_filtered)