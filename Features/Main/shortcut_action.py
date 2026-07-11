# Features/Main/shortcut_action.py
from PySide6.QtCore import QObject
from PySide6.QtGui import QKeySequence, QShortcut, QCursor
from PySide6.QtWidgets import QApplication

from Features.AssetBrowse.thumbnail_widget import ThumbnailWidget

class ShortcutAction(QObject):
    """
    프로그램 전체의 단축키를 관리하는 전담 클래스입니다.
    (SRP: 단일 책임 원칙 적용)
    """
    def __init__(self, _wgt_main, _obj_controller):
        # 단축키 객체들이 메모리에서 사라지지 않도록 parent로 _wgt_main을 줍니다.
        super().__init__(_wgt_main) 
        self.wgt_main = _wgt_main
        self.obj_controller = _obj_controller
        
        self._initShortcuts()

    def _initShortcuts(self):
        # 💡 1. Save Cache 단축키 (Ctrl + S)
        self.obj_shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self.wgt_main)
        self.obj_shortcut_save.activated.connect(self.wgt_main.wgt_top_bar.btn_save.click)

        # 💡 2. 호버된 썸네일 삭제 단축키 (Ctrl + X)
        self.obj_shortcut_delete = QShortcut(QKeySequence("Ctrl+X"), self.wgt_main)
        self.obj_shortcut_delete.activated.connect(self._handleHoverDelete)

    def _handleHoverDelete(self):
        """마우스 커서 위치에 있는 위젯이 썸네일이라면 삭제 로직을 호출합니다."""
        wgt_under_mouse = QApplication.widgetAt(QCursor.pos())
        
        # 마우스가 썸네일의 글자나 이미지 위에 있을 수 있으므로 부모 위젯을 타고 올라가며 확인
        while wgt_under_mouse:
            if isinstance(wgt_under_mouse, ThumbnailWidget):
                str_id = wgt_under_mouse.str_id
                print(f"✂️ [ShortcutAction] 단축키(Ctrl+X)로 썸네일 삭제 요청: {str_id}")
                
                # 뷰 컨트롤러의 삭제 함수 호출
                self.obj_controller.ctrl_view.handleDeleteList(str_id)
                break
                
            wgt_under_mouse = wgt_under_mouse.parentWidget()
