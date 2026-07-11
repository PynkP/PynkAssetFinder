# Core/FileSystem/folder_scanner.py

import os
import concurrent.futures
from PySide6.QtCore import QThread, Signal
from Core.Models.asset_factory import AssetFactory  # Core/Models 유지

class FolderScanner(QThread):
    sig_finished = Signal(list)

    def __init__(self, _str_directory):
        super().__init__()
        self.str_directory = _str_directory

    def run(self):
        list_json_paths = []

        def _collectJsonPathsFast(_str_current_path):
            try:
                for obj_entry in os.scandir(_str_current_path):
                    if obj_entry.is_dir(follow_symlinks=False):
                        _collectJsonPathsFast(obj_entry.path)

                    elif obj_entry.is_file(follow_symlinks=False):
                        if obj_entry.name.lower().endswith('.json'):
                            list_json_paths.append(obj_entry.path)

            except PermissionError:
                pass

        print(f"🚀 [FolderScanner] 파일 탐색 시작: {self.str_directory}")
        _collectJsonPathsFast(self.str_directory)
        
        list_info = []
        print(f"⚡ [FolderScanner] JSON 파싱 병렬 처리 시작 (총 {len(list_json_paths)}개)")
        
        # ✅ 멀티스레딩을 활용하여 I/O 대기 시간을 최소화하고 병렬로 분석합니다.
        # max_workers를 지정하지 않으면 시스템 코어 수에 맞게 자동으로 최적화됩니다.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # map 함수를 통해 리스트의 모든 경로를 AssetFactory에 동시에 던져줍니다.
            results = executor.map(AssetFactory.create_from_json, list_json_paths)
            
            for obj_metadata in results:
                if obj_metadata:
                    list_info.append(obj_metadata)
        
        print(f"🏁 [FolderScanner] 탐색 및 파싱 완료: {len(list_info)}개 에셋 로드됨")
        self.sig_finished.emit(list_info)
