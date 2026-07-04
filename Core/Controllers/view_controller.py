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
        # 💡 [핵심] 사장님이 특정 리스트를 넘겨줬으면 그걸 쓰고, 아니면 창고 전체 털어오기!
        list_target = _list_all_assets if _list_all_assets is not None else self.obj_asset_manager.getAllAssets()
        
        # 💡 이전처럼 한 번에 다 그려서 UI가 멈추는 것을 방지하기 위해 로더(ThumbnailLoader)에게 넘깁니다!
        # 로더가 알아서 기존 그리드를 비우고(clearGrid) 청크 단위로 나누어서 천천히 그리라고 지시합니다.
        self.wgt_main.obj_chunk_loader.reloadAssets(list_target)

    def handleAssetClicked(self, _str_path):
        """썸네일이 클릭되었을 때의 액션을 처리합니다."""
        # 💡 경로 하나만 받아서 똑똑하게 이름을 알아냅니다
        str_name = os.path.splitext(os.path.basename(_str_path))[0]
        print(f"🖱️ [ViewController] 에셋 클릭 감지됨: {str_name}")
        
        # 💡 PynkP님이 추가하신 폴더 열기 기능 실행!
        self.obj_asset_manager.openAssetFolder(_str_path)