import os
from PySide6.QtCore import QThread, Signal
from Core.asset_manager import AssetManager
from Core.category_manager import CategoryManager

class FolderScanner(QThread):
    # 💡 1. bool이 아니라 list(딕셔너리들을 담은 리스트)를 던지도록 시그널 정의
    sig_finished = Signal(list)

    def __init__(self, _str_target_path, _set_valid_extensions=None):
        super().__init__()
        self.str_target_path = _str_target_path
        
        if _set_valid_extensions is None:
            self.set_valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        else:
            self.set_valid_extensions = _set_valid_extensions

    def run(self):
        """os.scandir를 이용한 초고속 스캔 로직 수행"""
        print(f"📁 [FolderScanner] 스캔 시작: {self.str_target_path}")
        print(f"🔍 찾는 확장자: {self.set_valid_extensions}")
        
        list_info = []

        def _scanDirectoryFast(_str_current_path):
            try:
                for obj_entry in os.scandir(_str_current_path):
                    if obj_entry.is_dir(follow_symlinks=False):
                        _scanDirectoryFast(obj_entry.path)
                        
                    elif obj_entry.is_file(follow_symlinks=False):
                        # 💡 [핵심 추가] 파일 이름에 우리가 만든 캐시 이름이 포함되어 있으면 통과!
                        if "_pynk_asset_cache.json" in obj_entry.name:
                            continue 

                        # 기존 스캔 로직 진행
                        str_ext = os.path.splitext(obj_entry.name)[1].lower()
                        if str_ext in self.set_valid_extensions:
                            list_info.append({
                                "name": obj_entry.name,
                                "path": obj_entry.path,
                                "ext": str_ext
                            })
            except PermissionError:
                pass

        # 1. 파일 초고속 스캔 실행
        _scanDirectoryFast(self.str_target_path)

        # 2. 💡 [수정] 스캐너는 스스로 업데이트하지 않고, 지휘관에게 찾은 딕셔너리 리스트를 그대로 바칩니다!
        self.sig_finished.emit(list_info)

    # ==========================================
    # 🛠️ [내부 전용 함수 구역]
    # ==========================================
    def _updateAssetData(self, _list_info):
        """중앙 에셋 창고의 데이터를 최신화합니다."""
        obj_asset_manager = AssetManager()
        obj_asset_manager.clearAssets()
        obj_asset_manager.addAssets(_list_info)

    def _updateCategoryData(self, _list_info):
        """카테고리(좌측 패널) 창고의 데이터를 최신화합니다."""
        obj_category_manager = CategoryManager()
        obj_category_manager.clearCategories()

        # 💡 [수정] 경로 끝에 '/'가 붙어있어도 안전하게 이름만 쏙 빼내는 마법의 코드
        str_clean_path = os.path.normpath(self.str_target_path)
        str_folder_name = os.path.basename(str_clean_path)
        
        int_file_count = len(_list_info)
        obj_category_manager.addCategory(str_folder_name, int_file_count)