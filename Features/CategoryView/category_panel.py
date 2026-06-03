from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget
from Core.category_manager import CategoryManager

class CategoryPanel(QWidget):
    """왼쪽에 스캔된 폴더들의 이름과 파일 갯수를 보여주는 뷰입니다."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(40, 40, 40); color: white;")
        self.initUI()

    def initUI(self):
        lay_main = QVBoxLayout()
        lay_main.setContentsMargins(10, 10, 10, 10)

        self.wgt_list = QListWidget()
        self.wgt_list.setStyleSheet("""
            QListWidget { background-color: transparent; border: none; font-size: 14px; outline: none; }
            QListWidget::item { padding: 10px; }
            QListWidget::item:selected { background-color: rgb(80, 120, 200); border-radius: 5px; }
        """)
        
        lay_main.addWidget(self.wgt_list)
        self.setLayout(lay_main)

    def updateCategoryList(self):
        """💡 CategoryManager를 찾아가서 리스트를 싹 다 가져와서 화면에 다시 그립니다."""
        self.wgt_list.clear() # 기존 목록 비우기
        
        obj_category_manager = CategoryManager()
        list_categories = obj_category_manager.getAllCategories()
        
        for dict_cat in list_categories:
            str_display = f"* {dict_cat['name']} {dict_cat['count']}"
            self.wgt_list.addItem(str_display)