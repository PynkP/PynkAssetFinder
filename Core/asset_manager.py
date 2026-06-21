import os
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


class AssetManager:
    # 💡 유일한 인스턴스를 저장할 공간과, 초기화 여부를 확인하는 변수입니다.
    obj_instance = None
    bool_initialized = False

    def __new__(cls, *args, **kwargs):
        """
        싱글턴(Singleton) 생성 로직:
        이미 만들어진 인스턴스가 없다면 새로 만들고, 있다면 기존 것을 반환합니다.
        """
        if cls.obj_instance is None:
            cls.obj_instance = super().__new__(cls, *args, **kwargs)
        return cls.obj_instance

    def __init__(self):
        """초기화 작업: 단 한 번만 실행되도록 bool_initialized 변수로 방어합니다."""
        if not self.bool_initialized:
            # 전체 에셋을 관리할 중앙 리스트
            self.list_all_assets = []
            
            # 초기화 완료 처리
            self.bool_initialized = True

    def addAssets(self, _list_new_assets):
        """스캐너가 찾아온 새로운 에셋 리스트를 중앙 저장소에 추가합니다."""
        self.list_all_assets.extend(_list_new_assets)
        
        # 💡 [핵심 수정] 추가될 때마다 전체 에셋을 이름(asset_name) 알파벳 오름차순으로 정렬합니다.
        # 소문자로 변환(.lower())하여 대소문자가 뒤죽박죽 섞이지 않고 깔끔하게 정렬되게 합니다.
        self.list_all_assets.sort(key=lambda asset: asset.str_asset_name.lower())

    def getAllAssets(self):
        """현재 관리 중인 모든 에셋 리스트를 반환합니다."""
        return self.list_all_assets

    def clearAssets(self):
        """기존에 저장된 에셋 리스트를 비워줍니다. (새로운 폴더 스캔 시 사용)"""
        self.list_all_assets.clear()

    def getAssetCount(self):
        """현재 보관 중인 에셋의 총 개수를 반환합니다."""
        return len(self.list_all_assets)
    
    def openAssetFolder(self, _str_file_path):
        """주어진 파일 경로의 부모 폴더를 운영체제의 기본 탐색기로 엽니다."""
        
        # 방어 로직: 파일이 실제로 존재하는지 한 번 더 확인합니다.
        if not os.path.exists(_str_file_path):
            print(f"경로를 찾을 수 없습니다: {_str_file_path}")
            return False

        # 1. 폴더 경로만 추출
        str_folder_path = os.path.dirname(_str_file_path)
        
        # 2. 운영체제 탐색기 열기
        QDesktopServices.openUrl(QUrl.fromLocalFile(str_folder_path))
        return True
    
    def getUniqueAssetTypes(self) -> list:
        """현재 보관 중인 에셋들의 고유한 Asset Type 목록을 반환합니다."""
        set_types = set()
        for asset in self.list_all_assets:
            if hasattr(asset, 'str_asset_type') and asset.str_asset_type and asset.str_asset_type != "Unknown":
                set_types.add(asset.str_asset_type)
        return sorted(list(set_types))

    def getFilteredAssets(self, _list_category_path: list) -> list:
        """
        특정 카테고리 경로와 앞부분이 완벽히 일치하는 에셋만 반환합니다.
        (예: ["AAA", "nature"] 클릭 시, ["AAA", "nature", "rock"]은 포함되지만 ["3D asset", "nature"]는 제외)
        """
        # 만약 최상위 "Root"를 클릭했다면? (경로가 비어있음)
        if not _list_category_path:
            return self.list_all_assets
            
        list_filtered = []
        list_lower_path = [cat.lower() for cat in _list_category_path]
        
        for asset in self.list_all_assets:
            # 1. 카테고리가 아예 없는 파일들 처리 ("Uncategorized" 클릭 시)
            if not asset.list_categories:
                if len(list_lower_path) == 1 and list_lower_path[0] == "uncategorized":
                    list_filtered.append(asset)
                continue
                
            # 2. 에셋이 가진 카테고리 앞부분이 클릭한 경로와 똑같은지 검사!
            list_lower_asset_cats = [cat.lower() for cat in asset.list_categories]
            
            if len(list_lower_asset_cats) >= len(list_lower_path):
                if list_lower_asset_cats[:len(list_lower_path)] == list_lower_path:
                    list_filtered.append(asset)
                
        return list_filtered