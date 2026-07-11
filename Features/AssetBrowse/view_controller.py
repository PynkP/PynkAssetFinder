# Features/AssetBrowse/view_controller.py

import os
from PySide6.QtCore import QObject, Signal
from Features.AssetBrowse.asset_context_menu import AssetContextMenu  # 💡 새 경로

class ViewController(QObject):
    sig_asset_deleted = Signal() # 💡 삭제 완료를 앱 컨트롤러에 알리는 신호

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.initConnections()

    def initConnections(self):
        """메인 패널(그리드 뷰)의 클릭 이벤트만 전담 마크합니다."""
        obj_grid_view = self.wgt_main.wgt_main_panel.getGridView()
        obj_grid_view.sig_asset_clicked.connect(self.handleAssetClicked)
        obj_grid_view.sig_asset_right_clicked.connect(self.showContextMenu)

    def refreshGridView(self, _list_all_assets=None):
        """사장님이 화면을 갱신하라고 지시할 때 호출됩니다."""
        # 💡 [핵심] 사장님이 특정 리스트를 넘겨줬으면 그걸 쓰고, 아니면 창고 전체 털어오기!
        list_target = _list_all_assets if _list_all_assets is not None else self.obj_asset_manager.getAllAssets()
        
        # 💡 이전처럼 한 번에 다 그려서 UI가 멈추는 것을 방지하기 위해 로더(ThumbnailLoader)에게 넘깁니다!
        # 로더가 알아서 기존 그리드를 비우고(clearGrid) 청크 단위로 나누어서 천천히 그리라고 지시합니다.
        self.wgt_main.obj_chunk_loader.reloadAssets(list_target)

    def handleAssetClicked(self, _str_path, _str_id):
        """썸네일이 클릭되었을 때의 액션을 처리합니다."""
        # 💡 경로 하나만 받아서 똑똑하게 이름을 알아냅니다
        str_name = os.path.splitext(os.path.basename(_str_path))[0]
        print(f"🖱️ [ViewController] 에셋 클릭 감지됨: {str_name} (ID: {_str_id})")
        
        # 💡 폴더 열기 기능 실행!
        self.obj_asset_manager.openAssetFolder(_str_path, _str_id)

    def showContextMenu(self, _str_id, _str_path, _pos):
        """에셋 우클릭 시 전용 컨텍스트 메뉴 객체를 생성하고 화면에 띄웁니다."""
        # 1. 독립된 메뉴 객체 생성
        self.obj_context_menu = AssetContextMenu(_str_id, _str_path)
        
        # 2. 메뉴의 버튼 신호를 컨트롤러의 실제 실행 함수에 연결
        self.obj_context_menu.sig_goToFiles.connect(self.handleGoToFiles)
        self.obj_context_menu.sig_deleteList.connect(self.handleDeleteList)
        
        # 3. 마우스 위치에 메뉴 표시
        self.obj_context_menu.exec(_pos)

    def handleGoToFiles(self, _str_path, _str_id):
        """우클릭 'Go to Files' 메뉴가 눌렸을 때 파일이 있는 폴더를 엽니다."""
        print(f"📂 [ViewController] Go to Files 요청: {_str_path} (ID: {_str_id})")
        self.obj_asset_manager.openAssetFolder(_str_path, _str_id)

    def handleDeleteList(self, _str_id):
        """우클릭 'Delete List' 메뉴가 눌렸을 때 처리를 담당합니다."""
        print(f"🗑️ [ViewController] Delete List 요청: {_str_id}")
        
        # 1. 창고장(AssetManager)에게 삭제 지시
        bool_deleted = self.obj_asset_manager.deleteAssetById(_str_id)
        
        if bool_deleted:
            # 2. 삭제 성공 시, 화면 갱신을 위해 앱 컨트롤러에 신호 전송
            self.sig_asset_deleted.emit()
