# Core/Utils/resource_helper.py
import os
import sys

def resource_path(_str_relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller가 만든 임시 폴더 경로를 찾습니다.
        str_base_path = sys._MEIPASS
    except Exception:
        # 일반 파이썬 실행일 때는 현재 폴더를 기준으로 합니다.
        str_base_path = os.path.abspath(".")

    return os.path.join(str_base_path, _str_relative_path)
