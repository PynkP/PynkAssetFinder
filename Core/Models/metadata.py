# Core/Models/metadata.py

from dataclasses import dataclass, field

@dataclass
class MetaData:
    """
    PynkAssetFinder의 모든 에셋(이미지, 메가스캔)의 표준 데이터 규약(Struct)입니다.
    이 형태가 아니면 우리 창고(AssetManager)에 들어올 수 없습니다!
    """
    str_id: str                 # 파일명 또는 메가스캔 ID (예: tiiieh1fa, image_01)
    str_path_preview: str       # 썸네일로 띄울 프리뷰 이미지의 절대 경로
    str_asset_type: str         # 에셋 타입 ("Image" 또는 json의 "asset_type" 값)
    str_asset_name: str = "Unknown" # 💡 새로 추가된 자산 이름
    list_categories: list = field(default_factory=list) # 카테고리 (기본값은 빈 리스트)

    def __post_init__(self):
        # ✅ [최적화 A] 필터링용 소문자 카테고리를 로드 시점에 미리 캐싱
        # → 카테고리 클릭 때마다 소문자 변환을 반복하지 않아도 됩니다.
        self.list_categories_lower = [cat.lower() for cat in self.list_categories]
    
    # 💡 [꿀팁] 나중에 CacheController에서 JSON으로 얼릴(Save) 때 쓰기 위한 변환 함수
    def to_dict(self) -> dict:
        return {
            "str_id": self.str_id,
            "str_path_preview": self.str_path_preview,
            "str_asset_type": self.str_asset_type,
            "str_asset_name": self.str_asset_name,
            "list_categories": self.list_categories
        }
