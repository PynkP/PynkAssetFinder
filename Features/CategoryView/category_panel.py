# CategoryView/category_panel.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal, Qt # 💡 Qt 임포트 추가 (데이터 숨기기 용도)

class CategoryPanel(QWidget):
    """왼쪽에 스캔된 폴더들의 계층(Tree)과 파일 갯수를 보여주는 뷰입니다."""
    
    # 클릭 시 컨트롤러에게 '순수한 폴더 이름'만 쏙 뽑아서 전달할 시그널
    sig_category_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        # 💡 [삭제] self.setStyleSheet("background-color: rgb(40, 40, 40); color: white;")
        
        # 💡 [추가] QSS에서 콕 집어내기 위해 고유 이름표 달기
        self.setObjectName("CategoryPanel") 
        
        self.initUI()
        self.initConnections()

    def initUI(self):
        lay_main = QVBoxLayout()
        lay_main.setContentsMargins(5, 5, 5, 5)

        self.wgt_tree = QTreeWidget()
        self.wgt_tree.setHeaderHidden(True)
        
        # 💡 [추가] 이 트리 위젯에도 고유 이름표 달기
        self.wgt_tree.setObjectName("CategoryTree")
        
        # 💡 [삭제] 길었던 self.wgt_tree.setStyleSheet(""" ... """) 부분 전체 삭제!
        
        lay_main.addWidget(self.wgt_tree)
        self.setLayout(lay_main)

    def initConnections(self):
        """트리 아이템 클릭 시그널 연결"""
        self.wgt_tree.itemClicked.connect(self._onItemClicked)

    # ========================================================
    # 🌲 트리 그리기 로직 (Controller가 호출함)
    # ========================================================
    def updateCategoryTree(self, _obj_root_node):
        """
        CategoryManager가 쏴준 Root 노드를 받아서 트리를 그립니다!
        Root(All) 노드도 클릭 가능하게 최상단에 표시합니다.
        """
        self.wgt_tree.clear()

        # 💡 Root(All) 노드를 최상단 아이템으로 직접 추가!
        item_root = QTreeWidgetItem(self.wgt_tree)
        item_root.setText(0, f"📁 Root (All) ({_obj_root_node.int_count})")
        item_root.setData(0, Qt.UserRole, "Root")

        # Root의 자식들(2D, 3D, Uncategorized)을 Root 아래에 추가
        for str_name, obj_child_node in _obj_root_node.dict_children.items():
            item_top = QTreeWidgetItem(item_root)
            self._buildTreeItem(item_top, obj_child_node)

        self.wgt_tree.expandAll()

    def _buildTreeItem(self, _item_ui, _node_data):
        """
        [마법의 재귀 함수] 노드의 자식들을 파고들며 UI 꼬리를 뭅니다.
        """
        # 1. 화면에 보일 텍스트 설정 (예: "📁 3D (총 50개)")
        _item_ui.setText(0, f"📁 {_node_data.str_name} ({_node_data.int_count})")
        
        # 💡 2. [비밀 꿀팁] 나중에 필터링할 때 편하게 쓰기 위해, 
        # "📁 "나 "(총 50개)"가 없는 순수한 이름("3D")을 UI 뒤편(UserRole)에 몰래 숨겨둡니다!
        _item_ui.setData(0, Qt.UserRole, _node_data.str_name)

        # 3. 자식 방이 또 있다면? 자기 자신(함수)을 다시 호출! (재귀)
        for str_child_name, obj_child_node in _node_data.dict_children.items():
            # 부모 UI를 _item_ui로 지정해서 생성하면 자동으로 하위 뎁스(열)로 들어갑니다!
            item_child_ui = QTreeWidgetItem(_item_ui) 
            self._buildTreeItem(item_child_ui, obj_child_node)

    # ========================================================
    # 🖱️ 클릭 이벤트 처리
    # ========================================================
    def _onItemClicked(self, _item, _column):
        """
        아이템이 클릭되면, 아까 몰래 숨겨뒀던 '순수 폴더 이름'만 뽑아서 밖으로 쏩니다.
        """
        str_pure_name = _item.data(0, Qt.UserRole)
        print(f"🖱️ [CategoryPanel] 카테고리 클릭됨: {str_pure_name}")
        self.sig_category_clicked.emit(str_pure_name)