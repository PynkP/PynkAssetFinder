# Core/main_controller.py
from PySide6.QtCore import QObject
from Core.folder_scanner import FolderScanner
from Core.asset_manager import AssetManager
from Core.category_manager import CategoryManager # 💡 1. 카테고리 매니저 임포트 추가!

class MainController(QObject):
    def __init__(self, _wgt_main_window):
        super().__init__()
        self.wgt_main = _wgt_main_window
        self.thr_scanner = None
        
        self.obj_asset_manager = AssetManager()
        self.obj_category_manager = CategoryManager() 
        
        self.initConnections()

    def initConnections(self):
        """UI에서 발생하는 이벤트들을 컨트롤러에 연결합니다."""
        
        # 1. 탑 바의 스캔 버튼 클릭 연결
        obj_top_bar = self.wgt_main.wgt_top_bar
        obj_top_bar.btn_scan.sig_scan_requested.connect(self.handleScanProcess)
        
        # 💡 2. 썸네일 그리드 뷰에서 썸네일이 클릭되었다는 신호(경로)를 받도록 연결
        obj_grid_view = self.wgt_main.wgt_main_panel.getGridView()
        obj_grid_view.sig_asset_clicked.connect(self.handleAssetClicked)

    def handleScanProcess(self):
        self.wgt_main.wgt_top_bar.btn_scan.setDisabled(True)
        self.wgt_main.wgt_top_bar.btn_scan.setText("Scanning...")
        
        str_directory = self.wgt_main.openFolderDialog()
        if not str_directory:
            self.wgt_main.wgt_top_bar.btn_scan.setEnabled(True)
            self.wgt_main.wgt_top_bar.btn_scan.setText("Folder Scan")
            return

        self.thr_scanner = FolderScanner(_str_target_path=str_directory)
        self.thr_scanner.sig_finished.connect(self._onScanCompleted)
        self.thr_scanner.start()

    def _onScanCompleted(self, _b_success):
        if _b_success:
            # 1. 썸네일 데이터 업데이트
            list_all_assets = self.obj_asset_manager.getAllAssets()
            self.wgt_main.obj_chunk_loader.reloadAssets(list_all_assets)
            
            # 2. 카테고리 데이터 업데이트 💡 (이제 에러 없이 잘 작동합니다!)
            list_categories = self.obj_category_manager.getAllCategories()
            self.wgt_main.wgt_category_panel.updateCategoryList(list_categories)
            
        self.wgt_main.wgt_top_bar.btn_scan.setEnabled(True)
        self.wgt_main.wgt_top_bar.btn_scan.setText("Folder Scan")

    # 💡 [새로 추가된 함수] 썸네일이 눌렸을 때 폴더를 여는 지휘
    def handleAssetClicked(self, _str_path):
        """
        그리드 뷰에서 썸네일 클릭 신호가 오면 이 함수가 실행됩니다.
        직접 폴더를 열지 않고, AssetManager 전문가에게 넘깁니다!
        """
        self.obj_asset_manager.openAssetFolder(_str_path)