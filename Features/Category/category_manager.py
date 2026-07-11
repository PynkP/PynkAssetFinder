# Features/Category/category_manager.py

from PySide6.QtCore import QObject, Signal

class CategoryNode:
    """트리 구조를 만들기 위한 개별 폴더(노드) 구조체입니다."""
    def __init__(self, _str_name):
        self.str_name = _str_name   # 폴더 이름 (예: "3d", "nature")
        self.int_count = 0          # 이 폴더(하위 포함)에 속한 에셋 개수
        self.dict_children = {}     # 하위 폴더들 (이름: CategoryNode)


class CategoryManager(QObject):
    # 💡 트리가 완성되면 화면 팀장에게 "트리 완성됐으니 그려라!" 라고 알려줄 신호
    sig_categories_updated = Signal(object) 

    def __init__(self):
        super().__init__()
        # 가상의 "최상위(Root) 폴더"를 하나 만듭니다. (모든 폴더의 시작점)
        self.obj_root_node = CategoryNode("Root")

    def clearCategories(self):
        """기존 트리를 싹 비우고 초기화합니다."""
        self.obj_root_node = CategoryNode("Root")

    def buildCategoryTree(self, _list_metadata_assets):
        """
        창고(AssetManager)에 있는 모든 데이터를 받아서 깊이 있는 트리를 구축합니다.
        구조: Root (All) → assetCategories 순서대로 뎁스 생성
        """
        self.clearCategories()
        
        # 💡 [버그 예방] 나중에 카테고리 클릭 시 필터링할 때 쓸 수 있도록 데이터를 들고 있습니다.
        self.list_assets = _list_metadata_assets

        for asset in _list_metadata_assets:
            list_categories = asset.list_categories

            # 카테고리가 아예 없는 파일은 Uncategorized로
            if not list_categories:
                list_categories = ["Uncategorized"]

            # Root 전체 카운트 +1
            self.obj_root_node.int_count += 1

            # assetCategories 순서대로 파고 내려가며 트리 구축
            current_node = self.obj_root_node
            for str_category_name in list_categories:

                # 하위 노드가 없으면 새로 생성
                if str_category_name not in current_node.dict_children:
                    current_node.dict_children[str_category_name] = CategoryNode(str_category_name)

                # 하위 노드로 한 칸 내려감
                current_node = current_node.dict_children[str_category_name]
                current_node.int_count += 1

        print(f"🌲 [CategoryManager] 트리 구축 완료! (총 {self.obj_root_node.int_count}개 에셋 분류됨)")
        
        # 💡 [핵심 수정] 트리를 화면에 그리기 직전에, 모든 뎁스의 폴더들을 오름차순 정렬합니다.
        self._sortNode(self.obj_root_node)
        
        # 구축된 트리의 최상위(Root) 노드를 신호에 실어서 보냅니다.
        self.sig_categories_updated.emit(self.obj_root_node)

    # ========================================================
    # 💡 [신규 함수] 트리 정렬 재귀 함수
    # ========================================================
    def _sortNode(self, _node):
        """노드의 자식들을 이름(알파벳 오름차순, 대소문자 무시) 기준으로 정렬합니다."""
        # 현재 뎁스의 딕셔너리를 이름(키값) 기준으로 정렬해서 새로 끼워 넣습니다.
        _node.dict_children = dict(sorted(_node.dict_children.items(), key=lambda item: item[0].lower()))
        
        # 끝까지 파고들면서 하위 뎁스의 자식들도 전부 똑같이 정렬시킵니다. (재귀)
        for child_node in _node.dict_children.values():
            self._sortNode(child_node)

    def getChildrenOfPath(self, _list_path: list) -> list:
        """
        주어진 카테고리 경로(예: ["3D asset", "nature"])에 속하는
        바로 다음 뎁스의 자식 카테고리 이름 목록을 반환합니다.
        경로가 비어있으면 Root의 자식들을 반환합니다.
        """
        current_node = self.obj_root_node
        for str_name in _list_path:
            if str_name in current_node.dict_children:
                current_node = current_node.dict_children[str_name]
            else:
                return [] # 경로가 잘못되었거나 자식이 없으면 빈 리스트 반환
        
        # 자식 노드들의 이름을 리스트로 반환
        return list(current_node.dict_children.keys())

    def getFilteredAssets(self, _str_category_name: str) -> list:
        """
        특정 카테고리 이름이 포함된 에셋만 쏙쏙 골라서 반환합니다.
        """
        # 만약 최상위 "Root"를 클릭했다면? 필터링 없이 전체 데이터를 다 줍니다.
        if _str_category_name == "Root":
            return self.list_assets
            
        list_filtered = []
        str_target = _str_category_name.lower() # 검색할 단어를 소문자로 통일
        
        for asset in self.list_assets:
            # 1. 카테고리가 아예 없는 파일들 처리 ("Uncategorized" 클릭 시)
            if not asset.list_categories:
                if str_target == "uncategorized":
                    list_filtered.append(asset)
                continue
                
            # 2. 에셋이 가진 카테고리들을 전부 소문자로 바꿔서 타겟이 있는지 검사!
            # (UI는 "Nature"지만 데이터는 "nature"일 수 있으니 안전하게 대소문자 무시)
            list_lower_cats = [cat.lower() for cat in asset.list_categories]
            if str_target in list_lower_cats:
                list_filtered.append(asset)
                
        return list_filtered
