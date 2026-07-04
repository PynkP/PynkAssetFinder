# Core/Models/asset_factory.py
import os
import json
from Core.Models.metadata import MetaData

class AssetFactory:
    """파일 경로를 받아 즉시 완벽한 MetaData 객체로 만들어주는 공장"""
    
    @staticmethod
    def create_from_json(_str_json_path):
        """Megascans JSON 경로를 받아 분석 후 MetaData를 생성합니다."""
        str_filename = os.path.basename(_str_json_path)
        str_json_name = os.path.splitext(str_filename)[0]
        str_folder_path = os.path.dirname(_str_json_path)
        
        try:
            # ✅ 파일을 한 번만 열어 캐시 확인 + JSON 파싱 동시 처리
            with open(_str_json_path, 'r', encoding='utf-8') as f:
                str_raw = f.read()

            # 캐시 파일이면 즉시 None 반환
            if "_pynk_cache_signature" in str_raw[:256]:
                return None

            dict_data = json.loads(str_raw)  # 이미 읽은 문자열을 파싱 (추가 I/O 없음)

            # ✅ 썸네일 경로만 조립 (Lazy Loading에서 실제 존재 여부 판단)
            str_preview_filename = f"{str_json_name}_Preview.png"
            str_thumb_path = os.path.join(str_folder_path, str_preview_filename)
                
            # 💡 assetCategories(중첩 딕셔너리)를 평탄화하여 리스트로 변환
            dict_asset_categories = dict_data.get("assetCategories", {})
            list_raw_categories = AssetFactory._flattenAssetCategories(dict_asset_categories)
            
            # 💡 capitalize()를 사용해 대소문자 통일 및 정리
            list_categories = [cat.capitalize() if cat else cat for cat in list_raw_categories]
            
            # 💡 semanticTags에서 name과 asset_type 추출
            dict_semantic_tags = dict_data.get("semanticTags", {})
            str_asset_name = dict_semantic_tags.get("name", "Untitled")
            str_raw_type = dict_semantic_tags.get("asset_type")
            
            # 💡 semanticTags에 명시된 asset_type이 우선! 
            if str_raw_type:
                str_asset_type = str_raw_type.capitalize()
            else:
                str_asset_type = list_categories[0] if list_categories else "Unknown"
            
            return MetaData(
                str_id=str_json_name,
                str_path_preview=str_thumb_path,
                str_asset_type=str_asset_type,
                str_asset_name=str_asset_name,
                list_categories=list_categories
            )
            
        except Exception as e:
            print(f"❌ [AssetFactory] JSON 분석 에러: {e}")
            return None

    @staticmethod
    def _flattenAssetCategories(_dict_categories):
        """중첩된 assetCategories 딕셔너리를 평탄한 리스트로 변환합니다.
        예: {"3D asset": {"nature": {"tree": {}}}} -> ["3D asset", "nature", "tree"]
        """
        list_result = []
        dict_current = _dict_categories
        while dict_current:
            str_key = next(iter(dict_current))
            list_result.append(str_key)
            dict_current = dict_current[str_key]
        return list_result
