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
            
            # 💡 [신규 추가] 현재 사용자가 선택한 카테고리 경로를 기억하는 변수
            self.list_current_category_path = [] 
            
            # 초기화 완료 처리
            self.bool_initialized = True

    def addAssets(self, _list_new_assets, _already_sorted=False):
        """스캐너가 찾아온 새로운 에셋 리스트를 중앙 저장소에 추가합니다."""
        self.list_all_assets.extend(_list_new_assets)
        
        # ✅ 이미 정렬된 데이터(캐시 로드 시)는 정렬 생략
        if not _already_sorted:
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
        # 💡 [추가] 방금 클릭한 카테고리 경로를 기억해둡니다! (검색할 때 사용)
        self.list_current_category_path = _list_category_path
        
        # 만약 최상위 "Root"를 클릭했다면? (경로가 비어있음)
        if not _list_category_path:
            return self.list_all_assets
            
        list_filtered = []
        # ✅ [최적화 A] 검색 경로만 소문자로 변환 (에셋 측은 미리 캐싱된 값 사용)
        list_lower_path = [cat.lower() for cat in _list_category_path]
        int_path_len = len(list_lower_path)
        
        for asset in self.list_all_assets:
            # 1. 카테고리가 아예 없는 파일들 처리 ("Uncategorized" 클릭 시)
            if not asset.list_categories:
                if int_path_len == 1 and list_lower_path[0] == "uncategorized":
                    list_filtered.append(asset)
                continue
                
            # 2. 미리 캐싱된 소문자 카테고리로 바로 비교 (변환 비용 없음)
            if len(asset.list_categories_lower) >= int_path_len:
                if asset.list_categories_lower[:int_path_len] == list_lower_path:
                    list_filtered.append(asset)
                
        return list_filtered

    # ==========================================
    # 💡 [신규 추가] 검색 필터링 함수
    # ==========================================
    def searchAssets(self, _str_keyword):
        """현재 선택된 카테고리 내에서 키워드가 포함된 에셋을 필터링하여 반환합니다."""
        
        # 💡 [핵심 변경] 전체 에셋이 아닌, '현재 선택된 카테고리의 에셋들'만 먼저 가져옵니다.
        list_base_assets = self.getFilteredAssets(self.list_current_category_path)
        
        if not _str_keyword:
            return list_base_assets # 검색어가 없으면 현재 카테고리 전체 반환
            
        list_result = []
        str_lower_keyword = _str_keyword.lower()
        
        # 💡 [핵심 변경] list_all_assets 대신 list_base_assets 안에서만 검색합니다!
        for asset in list_base_assets:
            # 1. 이름 또는 ID에서 검색
            str_name = asset.str_asset_name.lower()
            str_id = asset.str_id.lower()
            
            if (str_lower_keyword in str_name) or (str_lower_keyword in str_id):
                list_result.append(asset)
                continue
                
            # 2. 태그(카테고리 경로)에서 검색
            for str_tag in asset.list_categories_lower:
                if str_lower_keyword in str_tag:
                    list_result.append(asset)
                    break # 이 에셋은 중복 추가되지 않도록 루프 탈출
                    
        return list_result