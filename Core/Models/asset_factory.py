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
                
            list_categories = dict_data.get("categories", [])
            str_asset_type = dict_data.get("asset_type", "Unknown")
            
            # Pynk 스마트 알고리즘 (이름 규약 조립)
            if len(list_categories) > 0:
                str_c0 = list_categories[0] 
                list_prefix = [str_cat.capitalize() for str_cat in list_categories[1:]]
                str_prefix = "_".join(list_prefix)
                
                str_preview_filename = f"{str_prefix}_{str_json_name}_{str_c0}_Preview.png" if str_prefix else f"{str_json_name}_{str_c0}_Preview.png"
            else:
                str_preview_filename = f"{str_json_name}_Preview.png"
            
            str_thumb_path = os.path.join(str_folder_path, str_preview_filename)
            
            # 썸네일 이미지가 없으면 None 반환 (오류 처리)
            if not os.path.exists(str_thumb_path):
                print(f"⚠️ [AssetFactory] 썸네일 파일이 존재하지 않습니다: {str_thumb_path}")
                return None
                
            return MetaData(
                str_id=str_json_name,
                str_path_preview=str_thumb_path,
                str_asset_type=str_asset_type,
                list_categories=list_categories
            )
            
        except Exception as e:
            print(f"❌ [AssetFactory] JSON 분석 에러: {e}")
            return None
