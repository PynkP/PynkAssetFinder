from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget
from PySide6.QtCore import Signal # 💡 시그널 임포트 추가

# 💡 [핵심] 결합도를 낮추기 위해 CategoryManager 임포트를 삭제했습니다!

class CategoryPanel(QWidget):
    """왼쪽에 스캔된 폴더들의 이름과 파일 갯수를 보여주는 뷰입니다."""
    
    # 💡 [미래를 위한 대비] 카테고리가 클릭되면 컨트롤러에게 알릴 시그널
    sig_category_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(40, 40, 40); color: white;")
        self.initUI()
        self.initConnections() # 시그널 연결 함수 호출

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

    def initConnections(self):
        """리스트 위젯 자체의 클릭 이벤트를 커스텀 프라이빗 함수로 연결합니다."""
        self.wgt_list.itemClicked.connect(self._onItemClicked)

    def updateCategoryList(self, _list_categories):
        """
        💡 [변경됨] 직접 매니저를 찾아가지 않고, 컨트롤러가 던져주는 데이터를 받아 그립니다.
        """
        self.wgt_list.clear() # 기존 목록 비우기
        
        for dict_cat in _list_categories:
            str_display = f"* {dict_cat['name']} {dict_cat['count']}"
            self.wgt_list.addItem(str_display)

    def _onItemClicked(self, _item):
        """
        프라이빗 함수: 아이템이 클릭되면 해당 텍스트를 시그널에 담아 밖으로 쏩니다.
        (추후 컨트롤러가 이 시그널을 받아서 에셋을 필터링하게 될 것입니다!)
        """
        self.sig_category_clicked.emit(_item.text())