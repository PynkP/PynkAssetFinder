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
    sig_toggleFavorite = Signal(str) # 💡 컨트롤러에게 알릴 신호
    sig_modifyAsset = Signal(str)    # 💡 [신규] Modify Asset 클릭 시 ID 전달

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

    def __init__(self, _str_id, _str_file_path, _bool_favorite=False, parent=None):
        super().__init__(parent)
        self.str_id = _str_id
        self.str_file_path = _str_file_path
        self.bool_favorite = _bool_favorite
        
        self.setStyleSheet(self.STYLE_MENU)
        self.initActions()

    def initActions(self):
        """메뉴에 들어갈 액션(버튼)들을 세팅합니다."""
        str_fav_text = "Remove from Favorites" if self.bool_favorite else "Add to Favorites"
        act_toggle_favorite = self.addAction(str_fav_text)

        act_modify_asset = self.addAction("Modify Asset")  # 💡 [신규]
        act_go_to_files  = self.addAction("Go to Files")
        act_delete_list  = self.addAction("Delete List")

        # 버튼이 눌렸을 때 내부 함수로 연결
        act_toggle_favorite.triggered.connect(self._emitToggleFavorite)
        act_modify_asset.triggered.connect(self._emitModifyAsset)   # 💡 [신규]
        act_go_to_files.triggered.connect(self._emitGoToFiles)
        act_delete_list.triggered.connect(self._emitDeleteList)

    def _emitToggleFavorite(self):
        self.sig_toggleFavorite.emit(self.str_id)

    def _emitModifyAsset(self):  # 💡 [신규]
        self.sig_modifyAsset.emit(self.str_id)

    def _emitGoToFiles(self):
        self.sig_goToFiles.emit(self.str_file_path, self.str_id)

    def _emitDeleteList(self):
        self.sig_deleteList.emit(self.str_id)
