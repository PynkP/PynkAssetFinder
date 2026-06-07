# Core/Controllers/view_controller.py

import os
from PySide6.QtCore import QObject

class ViewController(QObject):
    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.initConnections()

    def initConnections(self):
        """메인 패널(그리드 뷰)의 클릭 이벤트만 전담 마크합니다."""
        obj_grid_view = self.wgt_main.wgt_main_panel.getGridView()
        obj_grid_view.sig_asset_clicked.connect(self.handleAssetClicked)

    def refreshGridView(self, _list_all_assets=None):
        """사장님이 화면을 갱신하라고 지시할 때 호출됩니다."""
        obj_grid_view = self.wgt_main.wgt_main_panel.getGridView()
        obj_grid_view.clearGrid() # 화면 싹 비우기!
        
        # 💡 [핵심] 사장님이 특정 리스트를 넘겨줬으면 그걸 쓰고, 아니면 창고 전체 털어오기!
        list_target = _list_all_assets if _list_all_assets is not None else self.obj_asset_manager.getAllAssets()
        
        if list_target:
            obj_grid_view.addThumbnailChunk(list_target)

    def handleAssetClicked(self, _str_path):
        """썸네일이 클릭되었을 때의 액션을 처리합니다."""
        # 💡 경로 하나만 받아서 똑똑하게 이름을 알아냅니다
        str_name = os.path.splitext(os.path.basename(_str_path))[0]
        print(f"🖱️ [ViewController] 에셋 클릭 감지됨: {str_name}")
        
        # 💡 PynkP님이 추가하신 폴더 열기 기능 실행!
        self.obj_asset_manager.openAssetFolder(_str_path)