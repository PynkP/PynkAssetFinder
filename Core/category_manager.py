# Core/category_manager.py

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
        창고(AssetManager)에 있는 모든 데이터를 받아서 평탄화된 트리를 구축합니다.
        구조: Root (All) → 2D / 3D / Uncategorized → 개별 카테고리들 (1단계만)
        """
        self.clearCategories()

        for asset in _list_metadata_assets:
            list_categories = asset.list_categories

            # 카테고리가 아예 없는 파일은 Uncategorized로
            if not list_categories:
                list_categories = ["Uncategorized"]

            # Root 전체 카운트 +1
            self.obj_root_node.int_count += 1

            # 첫 번째 요소(예: "3d", "2d")를 대분류로 사용
            str_top_category = list_categories[0].capitalize()

            # 대분류 노드가 없으면 새로 생성
            if str_top_category not in self.obj_root_node.dict_children:
                self.obj_root_node.dict_children[str_top_category] = CategoryNode(str_top_category)

            obj_top_node = self.obj_root_node.dict_children[str_top_category]
            obj_top_node.int_count += 1

            # 두 번째 요소부터는 대분류 바로 아래에 평탄하게 배치 (깊이 제한!)
            for str_sub_category in list_categories[1:]:
                str_display_name = str_sub_category.capitalize()

                if str_display_name not in obj_top_node.dict_children:
                    obj_top_node.dict_children[str_display_name] = CategoryNode(str_display_name)

                obj_top_node.dict_children[str_display_name].int_count += 1

        print(f"🌲 [CategoryManager] 트리 구축 완료! (총 {self.obj_root_node.int_count}개 에셋 분류됨)")
        
        # 구축된 트리의 최상위(Root) 노드를 신호에 실어서 보냅니다.
        self.sig_categories_updated.emit(self.obj_root_node)

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