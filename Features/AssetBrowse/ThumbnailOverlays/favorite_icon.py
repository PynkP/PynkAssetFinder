# Features/AssetBrowse/ThumbnailOverlays/favorite_icon.py

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal

class FavoriteIcon(QLabel):
    """
    썸네일 위에 띄워지는 '즐겨찾기 하트(❤)' 오버레이 아이콘입니다.
    스스로 클릭을 감지하고 상태를 시각적으로 업데이트하는 단일 책임을 가집니다.
    """
    # 💡 추후 클릭 시 즐겨찾기 토글을 위해 미리 준비해둔 신호
    sig_icon_clicked = Signal()

    def __init__(self, _bool_favorite=False, parent=None):
        super().__init__("❤", parent)
        self.bool_favorite = _bool_favorite
        self.bool_hovered = False # 💡 호버 상태 기억 변수 추가
        
        self.initUI()
        self.updateVisuals()

    def initUI(self):
        self.setCursor(Qt.PointingHandCursor)

    def updateVisuals(self):
        """현재 상태(즐겨찾기, 호버)에 따라 하트 아이콘의 모양과 색상을 변경합니다."""
        if self.bool_favorite:
            # 💖 즐겨찾기 상태: 꽉 찬 핑크 하트
            self.setText("❤")
            self.setStyleSheet("color: rgb(255, 105, 180); font-size: 20px; font-weight: bold; background: transparent;")
            self.setVisible(True)
        else:
            # 💡 비즐겨찾기 상태: 마우스가 썸네일 위에 있을 때만 빈 회색 하트(♡) 표시
            if self.bool_hovered:
                self.setText("❤")
                self.setStyleSheet("color: rgb(150, 150, 150); font-size: 20px; font-weight: bold; background: transparent;")
                self.setVisible(True)
            else:
                self.setVisible(False)

    def setFavorite(self, _bool_fav):
        """외부(Controller나 ThumbnailWidget)에서 상태를 주입할 때 사용합니다."""
        self.bool_favorite = _bool_fav
        self.updateVisuals()

    def setHovered(self, _bool_hovered):
        """썸네일 위젯에서 마우스가 들어오고 나갈 때 이 함수를 호출해줍니다."""
        self.bool_hovered = _bool_hovered
        self.updateVisuals()

    def mousePressEvent(self, _event):
        """하트 아이콘이 직접 클릭되었을 때의 처리 (향후 토글 기능 연동 준비)"""
        if _event.button() == Qt.LeftButton:
            print("💖 [FavoriteIcon] 하트가 직접 클릭되었습니다! (토글 연동 준비 완료)")
            self.sig_icon_clicked.emit()
            _event.accept() # 💡 이벤트 먹어치우기 (부모인 썸네일 클릭 이벤트로 넘어가는 것을 막음)
        else:
            super().mousePressEvent(_event)
