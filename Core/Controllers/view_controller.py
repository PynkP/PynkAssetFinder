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

    def refreshGridView(self):
        """사장님이 화면을 갱신하라고 지시할 때 호출됩니다."""
        obj_grid_view = self.wgt_main.wgt_main_panel.getGridView()
        obj_grid_view.clearGrid() 
        
        if self.obj_asset_manager.list_assets:
            obj_grid_view.addThumbnailChunk(self.obj_asset_manager.list_assets)

    def handleAssetClicked(self, _str_path):
        """썸네일이 클릭되었을 때의 액션을 처리합니다."""
        # 💡 경로 하나만 받아서 똑똑하게 이름을 알아냅니다
        str_name = os.path.splitext(os.path.basename(_str_path))[0]
        print(f"🖱️ [ViewController] 에셋 클릭 감지됨: {str_name}")
        
        # 💡 PynkP님이 추가하신 폴더 열기 기능 실행!
        self.obj_asset_manager.openAssetFolder(_str_path)