# Features/AssetBrowse/asset_context_menu.py

from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal

class AssetContextMenu(QMenu):
    """
    에셋 전용 우클릭 메뉴입니다.
    어느 뷰에서든 이 클래스만 호출하면 동일한 메뉴를 띄울 수 있습니다.
    """
    sig_goToFiles = Signal(str, str)
    sig_deleteList = Signal(str)

    # [우클릭 메뉴 스타일]
    STYLE_MENU = """
        QMenu {
            background-color: rgb(45, 45, 45);
            color: rgb(220, 220, 220);
            border: 1px solid rgb(80, 80, 80);
        }
        QMenu::item {
            padding: 6px 24px 6px 24px;
        }
        QMenu::item:selected {
            background-color: rgb(70, 70, 70);
        }
    """

    def __init__(self, _str_id, _str_file_path, parent=None):
        super().__init__(parent)
        self.str_id = _str_id
        self.str_file_path = _str_file_path
        
        self.setStyleSheet(self.STYLE_MENU)
        self.initActions()

    def initActions(self):
        """메뉴에 들어갈 액션(버튼)들을 세팅합니다."""
        act_go_to_files = self.addAction("Go to Files")
        act_delete_list = self.addAction("Delete List")

        # 버튼이 눌렸을 때 내부 함수로 연결
        act_go_to_files.triggered.connect(self._emitGoToFiles)
        act_delete_list.triggered.connect(self._emitDeleteList)

    def _emitGoToFiles(self):
        self.sig_goToFiles.emit(self.str_file_path, self.str_id)

    def _emitDeleteList(self):
        self.sig_deleteList.emit(self.str_id)
