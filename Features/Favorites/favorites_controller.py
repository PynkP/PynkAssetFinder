# Features/Favorites/favorites_controller.py

from PySide6.QtCore import QObject
from Features.Favorites.favorites_manager import FavoritesManager
from Features.Favorites.favorites_panel import FavoritesPanel

class FavoritesController(QObject):
    """
    즐겨찾기 부서를 총괄하는 컨트롤러입니다.
    데이터(Manager)와 화면(Panel)을 연결해주는 중재자(Mediator) 역할을 합니다.
    """
    def __init__(self, _wgt_favorites_panel: FavoritesPanel, _obj_asset_manager):
        super().__init__()
        self.wgt_favorites_panel = _wgt_favorites_panel
        self.obj_asset_manager = _obj_asset_manager
        
        # 전용 매니저 고용
        self.obj_favorites_manager = FavoritesManager()
        
        self.initConnections()
        
    def initConnections(self):
        # 1. 매니저가 트리를 다 지으면 패널에게 그리라고 지시
        self.obj_favorites_manager.sig_categories_updated.connect(
            self.wgt_favorites_panel.updateFavoritesTree
        )
        
    def handleRebuildFavoritesTree(self):
        """즐겨찾기 데이터가 변동되었을 때 트리를 다시 그리도록 지시합니다."""
        print("👔 [FavoritesController] 즐겨찾기 변동 감지! 트리를 다시 짓습니다.")
        
        # 💡 [최적화!] Pynk님이 제안하신 고속 반환 함수를 사용! (O(1) 속도)
        list_favorites = self.obj_asset_manager.getFavoriteAssets()
        self.obj_favorites_manager.buildCategoryTree(list_favorites)
