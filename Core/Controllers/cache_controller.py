# Core/Controllers/cache_controller.py

import json
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox
from Core.Models.metadata import MetaData # 💡 우리가 만든 완벽한 규약 수입!

class CacheController(QObject):
    sig_cache_loaded = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.initConnections()

    def initConnections(self):
        obj_top_bar = self.wgt_main.wgt_top_bar
        obj_top_bar.btn_save.clicked.connect(self.handleSaveCache)
        obj_top_bar.btn_load.clicked.connect(self.handleLoadCache)

    # ========================================================
    # 💾 캐시 저장 로직 (Save)
    # ========================================================
    def handleSaveCache(self):
        if not self.obj_asset_manager.getAllAssets():
            QMessageBox.warning(self.wgt_main, "저장 불가", "스캔된 에셋이 없습니다!")
            return
            
        str_save_path, _ = QFileDialog.getSaveFileName(
            self.wgt_main, "에셋 캐시 저장", "_pynk_asset_cache.json", "JSON Cache (*.json)"
        )
        if not str_save_path: return 
            
        try:
            list_dict_assets = [asset.to_dict() for asset in self.obj_asset_manager.getAllAssets()]
            
            # 💡 [핵심] 캐시 파일임을 증명하는 서명(Signature) 문구를 맨 위에 박아줍니다!
            dict_cache_data = {
                "_pynk_cache_signature": "this is pynk asset finder cache",
                "assets": list_dict_assets
            }
            
            with open(str_save_path, 'w', encoding='utf-8') as f:
                json.dump(dict_cache_data, f, indent=4, ensure_ascii=False)
                
            print(f"💾 [CacheController] 캐시 저장 성공: {str_save_path}")
            QMessageBox.information(self.wgt_main, "저장 완료", "캐시 데이터가 성공적으로 저장되었습니다!")
            
        except Exception as e:
            QMessageBox.critical(self.wgt_main, "저장 에러", f"문제가 발생했습니다.\n{e}")

    # ========================================================
    # 📂 캐시 불러오기 로직 (Load)
    # ========================================================
    def handleLoadCache(self):
        str_load_path, _ = QFileDialog.getOpenFileName(
            self.wgt_main, "캐시 불러오기", "", "JSON Cache (*.json)"
        )
        if not str_load_path: return
            
        try:
            with open(str_load_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 💡 [핵심] 서명이 있는 새 버전인지, 리스트 형태의 옛날 버전인지 판별합니다 (하위 호환성)
            if isinstance(data, dict) and data.get("_pynk_cache_signature") == "this is pynk asset finder cache":
                list_raw_data = data.get("assets", [])
            elif isinstance(data, list):
                list_raw_data = data
            else:
                raise Exception("유효한 Pynk Asset Finder 캐시 파일이 아닙니다.")
            
            # 💡 [핵심 변경점] 읽어온 딕셔너리들을 다시 완벽한 MetaData 구조체로 해동(조립)합니다!
            # (** 문법을 쓰면 딕셔너리의 키워드를 구조체에 쏙쏙 알아서 매칭해 줍니다)
            list_metadata_assets = [MetaData(**dict_data) for dict_data in list_raw_data]
            
            # 창고 비우고 새로 적재
            self.obj_asset_manager.clearAssets()
            self.obj_asset_manager.addAssets(list_metadata_assets)
            
            # 사장님께 로드 완료 보고!
            self.sig_cache_loaded.emit() 
            print(f"📂 [CacheController] 캐시 로드 성공: 총 {self.obj_asset_manager.getAssetCount()}개")
            
        except Exception as e:
            print(f"❌ 캐시 로드 에러: {e}")
            QMessageBox.critical(self.wgt_main, "로드 에러", f"잘못된 캐시 파일입니다.\n{e}")