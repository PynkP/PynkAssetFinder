# Core/folder_scanner.py

import os
from PySide6.QtCore import QThread, Signal
from Core.Models.asset_factory import AssetFactory

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
                        str_ext = os.path.splitext(obj_entry.name)[1].lower()
                        if str_ext in self.set_valid_extensions:
                            if str_ext == ".json":
                                # 💡 파일 내용물의 앞부분만 살짝 읽어서 캐시 파일인지 확인합니다.
                                is_cache = False
                                try:
                                    with open(obj_entry.path, 'r', encoding='utf-8') as f:
                                        if "_pynk_cache_signature" in f.read(256):
                                            is_cache = True
                                except Exception:
                                    pass # 읽기 실패 시 무시하고 진행
                                    
                                if is_cache:
                                    continue # 서명이 발견되면 캐시이므로 스캔 건너뜀!
                                    
                                obj_metadata = AssetFactory.create_from_json(obj_entry.path)
                            else:
                                obj_metadata = AssetFactory.create_from_image(obj_entry.path)
                                
                            if obj_metadata:
                                list_info.append(obj_metadata)
                                
            except PermissionError:
                pass

        print(f"🚀 [FolderScanner] 탐색 시작: {self.str_directory}")
        _scanDirectoryFast(self.str_directory)
        
        self.sig_finished.emit(list_info)