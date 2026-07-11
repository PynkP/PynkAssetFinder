# Core/Models/asset_factory.py

import os
import json
from Core.Models.metadata import MetaData

class AssetFactory:
    """파일 경로를 받아 즉시 완벽한 MetaData 객체로 만들어주는 공장"""

    # QPixmap이 지원하는 이미지 확장자 목록
    LIST_SUPPORTED_EXTS = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp"]

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

            # ✅ 썸네일 경로: 지원 확장자 중 실제 존재하는 파일을 탐색
            str_thumb_path = AssetFactory._findPreviewPath(str_folder_path, str_json_name)
                
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
            print(f"[AssetFactory] {str_folder_path} \\ {str_filename} JSON 분석 에러: {e}")
            return None

    @staticmethod
    def _findPreviewPath(_str_folder_path, _str_json_name):
        """
        폴더를 스캔하여 '{json이름}_Preview.{확장자}' 형태의 파일을 찾습니다.
        QPixmap이 지원하는 확장자 중 첫 번째로 발견된 파일 경로를 반환합니다.
        아무것도 없으면 기본값으로 .png 경로를 반환합니다. (Lazy Loading에서 빈 이미지 처리)
        """
        str_preview_stem = f"{_str_json_name}_Preview"  # 확장자 없는 기준 이름

        try:
            # 폴더 파일 목록을 한 번만 읽어옴
            list_files = os.listdir(_str_folder_path)
        except OSError:
            # 폴더 접근 실패 시 기본값 반환
            return os.path.join(_str_folder_path, f"{str_preview_stem}.png")

        for str_file in list_files:
            str_name, str_ext = os.path.splitext(str_file)
            # 이름이 일치하고, 지원하는 확장자인지 확인 (대소문자 무시)
            if str_name == str_preview_stem and str_ext.lower() in AssetFactory.LIST_SUPPORTED_EXTS:
                return os.path.join(_str_folder_path, str_file)

        # 찾지 못했을 경우 기본 .png 경로 반환
        return os.path.join(_str_folder_path, f"{str_preview_stem}.png")

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
