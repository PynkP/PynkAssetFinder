# Features/Scan/scan_controller.py

from PySide6.QtCore import QObject, Signal
from Core.FileSystem.folder_scanner import FolderScanner  # 💡 새 경로

class ScanController(QObject):
    sig_scan_all_finished = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.thr_scanner = None
        self.btn_active = None
        
        # 💡 bool 플래그 제거됨!
        
        self.initConnections()

    def initConnections(self):
        obj_top_bar = self.wgt_main.wgt_top_bar
        
        # 1. 메가스캔: 완전 덮어쓰기 로직으로 연결
        obj_top_bar.btn_scan_mega.sig_scan_requested.connect(self.handleJsonScanProcess)
        
        # 2. 추가 스캔: 중복 제외 이어붙이기 로직으로 연결
        obj_top_bar.btn_add_scan.sig_scan_requested.connect(self.handleAddScanProcess)

    # --------------------------------------------------------
    # 🚀 메가스캔 JSON 스캔 (덮어쓰기 모드)
    # --------------------------------------------------------
    def handleJsonScanProcess(self):
        str_directory = self.wgt_main.openFolderDialog()
        if not str_directory: return
            
        self.btn_active = self.wgt_main.wgt_top_bar.btn_scan_mega
        self.btn_active.setScanningState(True)
        
        print(f"🚀 [ScanController] JSON 탐색... 대상: {str_directory}")
        
        self.thr_scanner = FolderScanner(str_directory)
        self.thr_scanner.sig_finished.connect(self._onMegaScanCompleted) 
        self.thr_scanner.start()

    # --------------------------------------------------------
    # ➕ 추가 스캔 (이어붙이기 모드)
    # --------------------------------------------------------
    def handleAddScanProcess(self):
        str_directory = self.wgt_main.openFolderDialog()
        if not str_directory: return
            
        self.btn_active = self.wgt_main.wgt_top_bar.btn_add_scan
        self.btn_active.setScanningState(True)
        
        print(f"🚀 [ScanController] JSON 추가 탐색... 대상: {str_directory}")
        
        self.thr_scanner = FolderScanner(str_directory)
        self.thr_scanner.sig_finished.connect(self._onAddScanCompleted) 
        self.thr_scanner.start()

    # --------------------------------------------------------
    # ✅ 완료 처리 (메가스캔 - 초기화)
    # --------------------------------------------------------
    def _onMegaScanCompleted(self, _list_info):
        self._resetButtonState()
        
        # 기존 데이터를 비우고 채웁니다
        self.obj_asset_manager.clearAssets()
        self.obj_asset_manager.addAssets(_list_info)
        
        self.sig_scan_all_finished.emit() # 사장님께 보고!

    # --------------------------------------------------------
    # ✅ 완료 처리 (추가 스캔 - 중복 검사)
    # --------------------------------------------------------
    def _onAddScanCompleted(self, _list_info):
        self._resetButtonState()
        
        # 💡 Manager의 새로운 함수를 이용해 중복(ID)을 거르고 이어 붙입니다!
        int_added_count = self.obj_asset_manager.addUniqueAssets(_list_info)
        print(f"➕ [ScanController] 스캔 완료: 총 {len(_list_info)}개 발견, 중복 제외 {int_added_count}개 추가됨.")
        
        self.sig_scan_all_finished.emit()

    # --------------------------------------------------------
    # 🔘 버튼 상태 복구 공통 함수
    # --------------------------------------------------------
    def _resetButtonState(self):
        if self.btn_active:
            self.btn_active.setScanningState(False)
            self.btn_active = None
