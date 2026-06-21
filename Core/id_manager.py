# Core/id_manager.py

import secrets
import string

class IDManager:
    """메가스캔 스타일의 고유 ID를 안전하게 생성하는 전문가입니다."""

    @staticmethod
    def generate_unique_ids(_list_existing_ids, _int_count=1, _int_length=9):
        """
        기존 창고의 ID 목록을 참고하여, 절대 겹치지 않는 새 ID를 발급합니다.
        _int_count가 1이면 문자열 1개를, 2 이상이면 리스트를 반환합니다.
        """
        str_characters = string.ascii_lowercase + string.digits
        
        # 💡 중복 검사를 빛의 속도로 하기 위해 기존 ID들을 Set으로 변환
        set_existing = set(_list_existing_ids) 
        list_generated = []
        
        while len(list_generated) < _int_count:
            # 1. 무작위 9자리 ID 생성 (예: 'tiiieh1fa')
            str_new_id = ''.join(secrets.choice(str_characters) for _ in range(_int_length))
            
            # 2. 기존 창고에도 없고, 방금 만든 것들과도 안 겹친다면 합격!
            if str_new_id not in set_existing:
                set_existing.add(str_new_id) # 다음 바퀴에서 또 겹치지 않게 Set에 임시 추가
                list_generated.append(str_new_id)
                
        # 1개만 요청했으면 문자열 자체를, 여러 개면 리스트를 반환
        return list_generated[0] if _int_count == 1 else list_generated
