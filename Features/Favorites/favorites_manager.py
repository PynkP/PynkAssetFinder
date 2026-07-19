# Features/Favorites/favorites_manager.py

from Features.Category.category_manager import CategoryManager

class FavoritesManager(CategoryManager):
    """
    즐겨찾기 전용 트리 매니저입니다. (SRP 적용)
    CategoryManager의 완벽한 뼈대(로직)를 그대로 물려받아 사용하며(OCP 적용), 
    로그 출력만 다르게 유지하여 유지보수를 극대화합니다.
    """
    def buildCategoryTree(self, _list_metadata_assets):
        # 부모의 튼튼한 로직을 그대로 사용해 트리를 짓습니다.
        super().buildCategoryTree(_list_metadata_assets)
        print(f"💖 [FavoritesManager] 즐겨찾기 전용 트리 구축 완료!")
