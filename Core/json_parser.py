# Core/json_parser.py

import json
import os
from PySide6.QtCore import QThread, Signal
from Core.Models.metadata import MetaData # 💡 우리가 만든 완벽한 규약 수입!

class JsonParser(QThread):
    """
    FolderScanner가 찾은 list_info를 전달받아,
    JSON 파일 안의 categories 규칙을 이용해 프리뷰 이미지 경로를 조립하고,
    완벽한 MetaData 구조체로 포장해내는 전문가입니다.
    """
    sig_parse_finished = Signal(list) 

    def __init__(self, _list_json_info):
        super().__init__()
        self.list_json_info = _list_json_info 

    def run(self):
        list_parsed_assets = []
        
        print(f"🛠️ [JsonParser] 총 {len(self.list_json_info)}개의 JSON 분석 시작 (Pynk 스마트 알고리즘 적용 중...)")
        
        for dict_info in self.list_json_info:
            str_json_path = dict_info["path"]
            
            # JSON 파일의 순수 이름 추출 (예: tiiieh1fa.json -> tiiieh1fa)
            str_json_name = os.path.splitext(dict_info["name"])[0] 
            str_folder_path = os.path.dirname(str_json_path)
            
            try:
                with open(str_json_path, 'r', encoding='utf-8') as f:
                    dict_data = json.load(f)
                    
                    # 💡 MetaData에 넣기 위해 필요한 정보들 추출
                    list_categories = dict_data.get("categories", [])
                    str_asset_type = dict_data.get("asset_type", "Unknown") # 추가!
                    str_preview_filename = ""
                    
                    # ========================================================
                    # 💡 PynkP님의 스마트 알고리즘 (100% 원본 유지)
                    # ========================================================
                    if len(list_categories) > 0:
                        # 1. 맨 앞(0번) 카테고리 추출
                        str_c0 = list_categories[0] 
                        
                        # 2. 1번 인덱스부터 끝까지 대문자로 바꾸고 '_'로 붙이기
                        list_prefix = [str_cat.capitalize() for str_cat in list_categories[1:]]
                        str_prefix = "_".join(list_prefix)
                        
                        # 3. 최종 조립
                        if str_prefix:
                            str_preview_filename = f"{str_prefix}_{str_json_name}_{str_c0}_Preview.png"
                        else:
                            str_preview_filename = f"{str_json_name}_{str_c0}_Preview.png"
                            
                    else:
                        # 카테고리가 아예 없을 때
                        str_preview_filename = f"{str_json_name}_Preview.png"
                    
                    # 4. 폴더 경로와 조립된 파일명을 합쳐서 완벽한 절대 경로 완성!
                    str_thumb_path = os.path.join(str_folder_path, str_preview_filename)
                    
                    # 💡 [핵심 변경점] 딕셔너리 대신 MetaData 객체로 완벽하게 포장!
                    # (혹시 경로가 틀릴 수도 있으니, 파일이 실제로 존재하는지 한 번 검사해주면 더 안전합니다)
                    if os.path.exists(str_thumb_path):
                        obj_metadata = MetaData(
                            str_id=str_json_name,            # 파일명 (ID)
                            str_path_preview=str_thumb_path, # 방금 조립한 절대 경로
                            str_asset_type=str_asset_type,   # json에서 뽑은 asset_type
                            list_categories=list_categories  # json에서 뽑은 categories
                        )
                        list_parsed_assets.append(obj_metadata)
                    else:
                        print(f"⚠️ [JsonParser] 썸네일 없음 패스: {str_thumb_path}")
                    
            except Exception as e:
                print(f"❌ JSON 분석 에러 ({str_json_name}): {e}")
                    
        # 분석이 모두 끝나면 통제탑에게 결과물을 쏴줍니다!
        print(f"✅ [JsonParser] 분석 완료! 정상 에셋 {len(list_parsed_assets)}개 확보.")
        self.sig_parse_finished.emit(list_parsed_assets)