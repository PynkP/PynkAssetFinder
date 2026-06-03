import os
from PySide6.QtCore import QThread, Signal
from Core.asset_manager import AssetManager
from Core.category_manager import CategoryManager

class FolderScanner(QThread):
    sig_finished = Signal(bool)

    def __init__(self, _str_target_path):
        super().__init__()
        self.str_target_path = _str_target_path
        self.set_valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

    def run(self):
        if not os.path.exists(self.str_target_path):
            self.sig_finished.emit(False)
            return

        list_image_info = []

        def _scanDirectoryFast(_str_current_path):
            try:
                for obj_entry in os.scandir(_str_current_path):
                    if obj_entry.is_dir(follow_symlinks=False):
                        _scanDirectoryFast(obj_entry.path)
                    elif obj_entry.is_file(follow_symlinks=False):
                        str_ext = os.path.splitext(obj_entry.name)[1].lower()
                        if str_ext in self.set_valid_extensions:
                            list_image_info.append({
                                "name": obj_entry.name,
                                "path": obj_entry.path,
                                "ext": str_ext
                            })
            except PermissionError:
                pass

        # 1. 파일 스캔 실행
        _scanDirectoryFast(self.str_target_path)

        # 2. 💡 [리팩토링] 분리된 함수들을 호출하여 데이터를 깔끔하게 넘겨줍니다.
        self._updateAssetData(list_image_info)
        self._updateCategoryData(list_image_info)
        
        self.sig_finished.emit(True)

    # ==========================================
    # 🛠️ [내부 전용 함수 구역]
    # ==========================================
    def _updateAssetData(self, _list_image_info):
        """중앙 에셋 창고의 데이터를 최신화합니다."""
        obj_asset_manager = AssetManager()
        obj_asset_manager.clearAssets()
        obj_asset_manager.addAssets(_list_image_info)

    def _updateCategoryData(self, _list_image_info):
        """카테고리(좌측 패널) 창고의 데이터를 최신화합니다."""
        obj_category_manager = CategoryManager()
        obj_category_manager.clearCategories()

        # 💡 [수정] 경로 끝에 '/'가 붙어있어도 안전하게 이름만 쏙 빼내는 마법의 코드
        str_clean_path = os.path.normpath(self.str_target_path)
        str_folder_name = os.path.basename(str_clean_path)
        
        int_file_count = len(_list_image_info)
        obj_category_manager.addCategory(str_folder_name, int_file_count)