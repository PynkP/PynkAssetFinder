# Core/Controllers/cache_controller.py

import json
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox

class CacheController(QObject):
    # 💡 로드가 끝났을 때 사장님(MainController)에게 화면 갱신을 요청할 신호
    sig_cache_loaded = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.initConnections()

    def initConnections(self):
        obj_top_bar = self.wgt_main.wgt_top_bar
        # 오직 Save / Load 버튼만 전담 마크!
        obj_top_bar.btn_save.clicked.connect(self.handleSaveCache)
        obj_top_bar.btn_load.clicked.connect(self.handleLoadCache)

    def handleSaveCache(self):
        if not self.obj_asset_manager.list_assets:
            QMessageBox.warning(self.wgt_main, "저장 불가", "스캔된 에셋이 없습니다!")
            return
            
        str_save_path, _ = QFileDialog.getSaveFileName(
            self.wgt_main, "에셋 캐시 저장", "_pynk_asset_cache.json", "JSON Cache (*.json)"
        )
        if not str_save_path: return 
            
        try:
            with open(str_save_path, 'w', encoding='utf-8') as f:
                json.dump(self.obj_asset_manager.list_assets, f, indent=4, ensure_ascii=False)
            print(f"💾 [CacheController] 캐시 저장 성공: {str_save_path}")
            QMessageBox.information(self.wgt_main, "저장 완료", "캐시 데이터가 성공적으로 저장되었습니다!")
        except Exception as e:
            QMessageBox.critical(self.wgt_main, "저장 에러", f"문제가 발생했습니다.\n{e}")

    def handleLoadCache(self):
        str_load_path, _ = QFileDialog.getOpenFileName(
            self.wgt_main, "캐시 불러오기", "", "JSON Cache (*.json)"
        )
        if not str_load_path: return
            
        try:
            with open(str_load_path, 'r', encoding='utf-8') as f:
                self.obj_asset_manager.list_assets = json.load(f)
            
            # 사장님께 로드 완료 보고!
            self.sig_cache_loaded.emit() 
            print(f"📂 [CacheController] 캐시 로드 성공: 총 {len(self.obj_asset_manager.list_assets)}개")
            
        except Exception as e:
            QMessageBox.critical(self.wgt_main, "로드 에러", f"잘못된 캐시 파일입니다.\n{e}")