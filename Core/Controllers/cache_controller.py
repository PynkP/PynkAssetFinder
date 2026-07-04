# Core/Controllers/cache_controller.py

import json
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox
from Core.Models.metadata import MetaData


# ========================================================
# 🧵 캐시 로드 전용 백그라운드 스레드
# UI 스레드를 막지 않고 파일 읽기 + 객체 생성을 처리합니다.
# ========================================================
class CacheLoaderThread(QThread):
    sig_loaded = Signal(list)   # 로드 성공 시 MetaData 리스트 전달
    sig_error  = Signal(str)    # 에러 발생 시 에러 메시지 전달

    def __init__(self, _str_path):
        super().__init__()
        self.str_path = _str_path

    def run(self):
        try:
            with open(self.str_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict) and data.get("_pynk_cache_signature") == "this is pynk asset finder cache":
                list_raw_data = data.get("assets", [])
            elif isinstance(data, list):
                list_raw_data = data
            else:
                self.sig_error.emit("유효한 Pynk Asset Finder 캐시 파일이 아닙니다.")
                return

            # 💡 MetaData 객체 생성 - 무거운 작업이므로 백그라운드에서 처리
            list_metadata_assets = [MetaData(**dict_data) for dict_data in list_raw_data]
            self.sig_loaded.emit(list_metadata_assets)

        except Exception as e:
            self.sig_error.emit(str(e))


class CacheController(QObject):
    sig_cache_loaded = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        self.obj_loader_thread = None  # 스레드 참조 보관 (GC 방지)

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

            # 💡 캐시 파일임을 증명하는 서명(Signature) 문구를 맨 위에 박아줍니다!
            dict_cache_data = {
                "_pynk_cache_signature": "this is pynk asset finder cache",
                "assets": list_dict_assets
            }

            with open(str_save_path, 'w', encoding='utf-8') as f:
                # ✅ [최적화] indent=4 제거 → separators로 최소 크기 저장 (파일 크기 대폭 감소)
                json.dump(dict_cache_data, f, separators=(',', ':'), ensure_ascii=False)

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

        # ✅ [최적화] 파일 읽기 + 객체 생성을 백그라운드 스레드에서 처리 → UI freeze 없음
        self.obj_loader_thread = CacheLoaderThread(str_load_path)
        self.obj_loader_thread.sig_loaded.connect(self._onCacheLoaded)
        self.obj_loader_thread.sig_error.connect(self._onCacheError)
        self.obj_loader_thread.start()

    def _onCacheLoaded(self, _list_metadata_assets):
        """스레드에서 로드 완료 시 호출 - UI 스레드에서 실행됨"""
        self.obj_asset_manager.clearAssets()
        # ✅ [최적화] 캐시는 저장 시 이미 정렬된 상태 → 재정렬 생략
        self.obj_asset_manager.addAssets(_list_metadata_assets, _already_sorted=True)

        self.sig_cache_loaded.emit()
        print(f"📂 [CacheController] 캐시 로드 성공: 총 {self.obj_asset_manager.getAssetCount()}개")

    def _onCacheError(self, _str_error):
        """스레드에서 에러 발생 시 호출"""
        print(f"❌ 캐시 로드 에러: {_str_error}")
        QMessageBox.critical(self.wgt_main, "로드 에러", f"잘못된 캐시 파일입니다.\n{_str_error}")