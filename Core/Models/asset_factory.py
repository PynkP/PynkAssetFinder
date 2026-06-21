# Core/Models/asset_factory.py
import os
import json
from Core.Models.metadata import MetaData

class AssetFactory:
    """파일 경로를 받아 즉시 완벽한 MetaData 객체로 만들어주는 공장"""
    
    @staticmethod
    def create_from_image(_str_file_path):
        """일반 이미지(png, jpg 등) 경로를 받아 MetaData를 생성합니다."""
        str_filename = os.path.basename(_str_file_path)
        str_pure_name = os.path.splitext(str_filename)[0]
        
        return MetaData(
            str_id=str_pure_name,            
            str_path_preview=_str_file_path,  
            str_asset_type="Image",          
            str_asset_name=str_pure_name,
            list_categories=["2d"]           
        )

    @staticmethod
    def create_from_json(_str_json_path):
        """Megascans JSON 경로를 받아 분석 후 MetaData를 생성합니다."""
        str_filename = os.path.basename(_str_json_path)
        str_json_name = os.path.splitext(str_filename)[0]
        str_folder_path = os.path.dirname(_str_json_path)
        
        try:
            with open(_str_json_path, 'r', encoding='utf-8') as f:
                dict_data = json.load(f)
                
            # 💡 assetCategories(중첩 딕셔너리)를 평탄화하여 리스트로 변환
            dict_asset_categories = dict_data.get("assetCategories", {})
            list_categories = AssetFactory._flattenAssetCategories(dict_asset_categories)
            
            # 💡 프리뷰 이미지: JSON파일이름_Preview.png
            str_preview_filename = f"{str_json_name}_Preview.png"
            str_thumb_path = os.path.join(str_folder_path, str_preview_filename)
            
            # 썸네일 이미지가 없으면 None 반환 (오류 처리)
            if not os.path.exists(str_thumb_path):
                print(f"⚠️ [AssetFactory] 썸네일 파일이 존재하지 않습니다: {str_thumb_path}")
                return None
                
            # 💡 semanticTags에서 name과 asset_type 추출
            dict_semantic_tags = dict_data.get("semanticTags", {})
            str_asset_name = dict_semantic_tags.get("name", "Untitled")
            str_asset_type = dict_semantic_tags.get("asset_type")
            
            # 💡 [핵심 수정] semanticTags에 명시된 asset_type이 우선! 
            # 만약 아주 옛날 포맷이라 없다면 카테고리 첫 번째 폴더명을 빌려옵니다.
            if not str_asset_type:
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
