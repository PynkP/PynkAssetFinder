# Core/Controllers/scan_controller.py

from PySide6.QtCore import QObject, Signal
from Core.folder_scanner import FolderScanner
from Core.json_parser import JsonParser

class ScanController(QObject):
    # 💡 스캔과 파싱이 완벽하게 끝났을 때 사장님께 보고할 신호
    sig_scan_all_finished = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.thr_scanner = None
        self.thr_parser = None
        
        self.initConnections()

    def initConnections(self):
        """탑 바의 스캔 버튼들만 전담 마크합니다."""
        obj_top_bar = self.wgt_main.wgt_top_bar
        obj_top_bar.btn_scan.sig_scan_requested.connect(self.handleScanProcess)
        obj_top_bar.btn_scan_mega.sig_scan_requested.connect(self.handleJsonScanProcess)

    # --------------------------------------------------------
    # 📁 일반 폴더 스캔
    # --------------------------------------------------------
    def handleScanProcess(self):
        str_directory = self.wgt_main.openFolderDialog()
        if not str_directory: return
            
        print(f"🚀 [ScanController] 일반 탐색가 고용 중... 대상: {str_directory}")
        self.thr_scanner = FolderScanner(str_directory)
        self.thr_scanner.sig_finished.connect(self._onScanCompleted)
        self.thr_scanner.start()

    def _onScanCompleted(self, _list_info):
        self.obj_asset_manager.clearAssets()
        self.obj_asset_manager.addAssets(_list_info)
        self.sig_scan_all_finished.emit() # 사장님께 보고!

    # --------------------------------------------------------
    # 🚀 메가스캔 JSON 스캔 & 파싱
    # --------------------------------------------------------
    def handleJsonScanProcess(self):
        str_directory = self.wgt_main.openFolderDialog()
        if not str_directory: return
            
        print(f"🚀 [ScanController] JSON 탐색가 고용 중... 대상: {str_directory}")
        self.thr_scanner = FolderScanner(str_directory, {'.json'})
        self.thr_scanner.sig_finished.connect(self._onJsonFilesFound)
        self.thr_scanner.start()

    def _onJsonFilesFound(self, _list_json_info):
        self.thr_parser = JsonParser(_list_json_info)
        self.thr_parser.sig_parse_finished.connect(self._onJsonParseCompleted)
        self.thr_parser.start()

    def _onJsonParseCompleted(self, _list_parsed_assets):
        self.obj_asset_manager.clearAssets()
        self.obj_asset_manager.addAssets(_list_parsed_assets)
        self.sig_scan_all_finished.emit() # 사장님께 보고!