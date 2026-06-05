# Core/folder_scanner.py

import os
from PySide6.QtCore import QThread, Signal
from Core.Models.metadata import MetaData # 💡 우리가 만든 구조체 수입!

class FolderScanner(QThread):
    sig_finished = Signal(list)

    def __init__(self, _str_directory, _set_valid_extensions=None):
        super().__init__()
        self.str_directory = _str_directory
        
        # 확장자 세팅
        if _set_valid_extensions is None:
            self.set_valid_extensions = {'.png', '.jpg', '.jpeg', '.tga', '.exr'}
        else:
            self.set_valid_extensions = _set_valid_extensions

    def run(self):
        list_info = []

        def _scanDirectoryFast(_str_current_path):
            try:
                for obj_entry in os.scandir(_str_current_path):
                    if obj_entry.is_dir(follow_symlinks=False):
                        _scanDirectoryFast(obj_entry.path)
                        
                    elif obj_entry.is_file(follow_symlinks=False):
                        # 💡 캐시 파일은 건너뛰기
                        if "_pynk_asset_cache.json" in obj_entry.name:
                            continue 

                        str_ext = os.path.splitext(obj_entry.name)[1].lower()
                        if str_ext in self.set_valid_extensions:
                            
                            # 💡 함수화된 로직으로 깔끔하게 장바구니에 담기!
                            if str_ext == ".json":
                                list_info.append(self._jsonScan(obj_entry, str_ext))
                            else:
                                list_info.append(self._imgScan(obj_entry))
                                
            except PermissionError:
                pass

        print(f"🚀 [FolderScanner] 탐색 시작: {self.str_directory}")
        _scanDirectoryFast(self.str_directory)
        
        self.sig_finished.emit(list_info)

    # ========================================================
    # 📦 분리된 포장(Parsing) 전담 함수들
    # ========================================================
    def _jsonScan(self, _obj_entry, _str_ext):
        """메가스캔 JSON 파일은 번역가를 위해 날것(Raw) 딕셔너리로 넘깁니다."""
        return {
            "name": _obj_entry.name,
            "path": _obj_entry.path,
            "ext": _str_ext
        }

    def _imgScan(self, _obj_entry):
        """일반 이미지는 PynkAsset 구조체(MetaData)에 완벽하게 맞춰서 포장합니다."""
        str_pure_name = os.path.splitext(_obj_entry.name)[0]
        
        return MetaData(
            str_id=str_pure_name,            # 파일 이름
            str_path_preview=_obj_entry.path,  # 파일 절대 경로
            str_asset_type="Image",          # 고정값
            list_categories=["2d"]           # 고정값
        )