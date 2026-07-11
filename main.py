# main.py
import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from Core.Utils.resource_helper import resource_path
from Features.Main.main_window import MainWindow

if __name__ == "__main__":
    try:
        # 윈도우 작업표시줄 아이콘 분리 독립 선언!
        try:
            str_app_id = 'pynkp.assetfinder.version_1' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(str_app_id)
        except Exception:
            pass 

        app = QApplication(sys.argv)
        
        # 프로그램 전체 아이콘 적용
        app.setWindowIcon(QIcon(resource_path("Resources/icons/app_icon.ico")))

        # 기능별로 나뉜 여러 개의 스타일 시트를 차례대로 읽어 합칩니다.
        list_qss_files = [
            "Resources/Styles/main_style.qss",
            "Resources/Styles/topbar_style.qss",
            "Resources/Styles/category_style.qss",
            "Resources/Styles/thumbnail_style.qss",
            "Resources/Styles/register_style.qss",
            "Resources/Styles/bottombar_style.qss",
        ]

        str_combined_qss = ""
        for str_file in list_qss_files:
            str_qss_path = resource_path(str_file)
            if os.path.exists(str_qss_path):
                with open(str_qss_path, "r", encoding="utf-8") as f:
                    str_combined_qss += f.read() + "\n"
            else:
                print(f"⚠️ 경고: {str_file} 파일을 찾을 수 없습니다.")

        app.setStyleSheet(str_combined_qss)
        print("🎨 분할된 스타일 시트 로드 및 병합 완료!")

        # 2. 메인 윈도우 실행
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        traceback.print_exc()