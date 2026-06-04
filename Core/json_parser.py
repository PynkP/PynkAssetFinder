# Core/json_parser.py
import json
import os
from PySide6.QtCore import QThread, Signal

class JsonParser(QThread):
    """
    FolderScanner가 찾은 list_info를 전달받아,
    JSON 파일 안의 categories 규칙을 이용해 프리뷰 이미지 경로만 조립해내는 전문가입니다.
    """
    sig_parse_finished = Signal(list) 

    def __init__(self, _list_json_info):
        super().__init__()
        self.list_json_info = _list_json_info 

    def run(self):
        list_parsed_assets = []
        
        print(f"🛠️ [JsonParser] 총 {len(self.list_json_info)}개의 JSON 분석 시작 (공식 적용 중...)")
        
        for dict_info in self.list_json_info:
            str_json_path = dict_info["path"]
            
            # JSON 파일의 순수 이름 추출 (예: tiiieh1fa.json -> tiiieh1fa)
            str_json_name = os.path.splitext(dict_info["name"])[0] 
            str_folder_path = os.path.dirname(str_json_path)
            
            try:
                with open(str_json_path, 'r', encoding='utf-8') as f:
                    dict_data = json.load(f)
                    
                    list_categories = dict_data.get("categories", [])
                    str_preview_filename = ""
                    
                    # 💡 스마트 알고리즘 시작!
                    if len(list_categories) > 0:
                        # 1. 맨 앞(0번) 카테고리 추출 (예: "3d")
                        str_c0 = list_categories[0] 
                        
                        # 2. 1번 인덱스부터 끝까지([1:]) 모든 단어를 대문자로 바꾸고, '_'로 찰싹 붙여줍니다!
                        # (카테고리가 2개든 100개든 이 한 줄로 완벽하게 조립됩니다)
                        list_prefix = [str_cat.capitalize() for str_cat in list_categories[1:]]
                        str_prefix = "_".join(list_prefix)
                        
                        # 3. 최종 조립
                        if str_prefix:
                            # 카테고리가 2개 이상일 때 (정상 패턴)
                            str_preview_filename = f"{str_prefix}_{str_json_name}_{str_c0}_Preview.png"
                        else:
                            # 카테고리가 1개밖에 없을 때 (혹시 모를 예외 대비)
                            str_preview_filename = f"{str_json_name}_{str_c0}_Preview.png"
                            
                    else:
                        # 카테고리가 아예 없을 때 (최후의 보루)
                        str_preview_filename = f"{str_json_name}_Preview.png"
                    
                    # 4. 폴더 경로와 조립된 파일명을 합쳐서 완벽한 절대 경로 완성!
                    str_thumb_path = os.path.join(str_folder_path, str_preview_filename)
                    
                    # 5. 화면(GridView)에 띄우기 위해 딕셔너리로 예쁘게 포장
                    dict_parsed_asset = {
                        "name": str_json_name,   # 썸네일 아래에 보여줄 이름 (에셋 ID)
                        "path": str_thumb_path,  # 방금 조립한 프리뷰 이미지 절대 경로
                        "ext": ".png"
                    }
                    
                    # 장바구니에 담기
                    list_parsed_assets.append(dict_parsed_asset)
                    
            except Exception as e:
                print(f"❌ JSON 분석 에러 ({str_json_name}): {e}")
                    
        # 분석이 모두 끝나면 통제탑에게 결과물을 쏴줍니다!
        self.sig_parse_finished.emit(list_parsed_assets)