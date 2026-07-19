# Features/SharedUI/thumbnail_drop_label.py

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class ThumbnailDropLabel(QLabel):
    """
    썸네일 이미지를 드래그 앤 드롭으로 교체할 수 있는 라벨 위젯입니다.
    Register와 Modify 창 모두에서 재사용됩니다.
    """
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag & Drop\nThumbnail Image")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 10px;
                background-color: #2b2b2b;
                color: #888888;
                font-size: 14px;
            }
            QLabel:hover {
                border-color: #aaaaaa;
                background-color: #3b3b3b;
            }
        """)
        # 세로 높이 고정
        self.setFixedHeight(400)
        self.str_thumbnail_path = ""
        self._original_pixmap = None  # 원본 이미지를 보관할 변수

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile() and url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg')):
                event.acceptProposedAction()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        str_file_path = url.toLocalFile()
        self.str_thumbnail_path = str_file_path

        # 원본 이미지를 로드하여 보관하고 화면 갱신
        self._original_pixmap = QPixmap(str_file_path)
        self._update_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_pixmap()

    def _update_pixmap(self):
        if self._original_pixmap and not self._original_pixmap.isNull():
            # 가로 폭은 현재 라벨 크기에 맞춤
            scaled = self._original_pixmap.scaledToWidth(self.width(), Qt.SmoothTransformation)

            # 세로가 길면 위에서부터 크롭
            if scaled.height() > self.height():
                scaled = scaled.copy(0, 0, scaled.width(), self.height())

            self.setPixmap(scaled)

    def loadImage(self, _str_path):
        """
        외부에서 이미지 경로를 받아 썸네일을 세팅합니다.
        Modify 창에서 기존 이미지를 불러올 때 사용합니다.
        """
        if not _str_path:
            return
        self.str_thumbnail_path = _str_path
        self._original_pixmap = QPixmap(_str_path)
        self._update_pixmap()
