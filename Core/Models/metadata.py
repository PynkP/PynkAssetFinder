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
    list_categories: list = field(default_factory=list) # 카테고리 (기본값은 빈 리스트)
    
    # 💡 [꿀팁] 나중에 CacheController에서 JSON으로 얼릴(Save) 때 쓰기 위한 변환 함수
    def to_dict(self) -> dict:
        return {
            "str_id": self.str_id,
            "str_path_preview": self.str_path_preview,
            "str_asset_type": self.str_asset_type,
            "list_categories": self.list_categories
        }