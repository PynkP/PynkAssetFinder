# Features/SharedUI/scan_button.py

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal

class ScanButton(QPushButton):
    # 외부(컨트롤러)에서 들을 수 있도록 깔끔한 시그널 딱 하나만 선언
    sig_scan_requested = Signal()

    def __init__(self, _str_title):
        super().__init__(_str_title)
        self.str_original_title = _str_title
        # 자신의 클릭 시그널을 내부 프라이빗 핸들러에 연결
        self.clicked.connect(self._onButtonClicked)

    def _onButtonClicked(self):
        """프라이빗 함수: 버튼이 클릭되면 복잡한 일 안 하고 상위에 신호만 전달합니다."""
        self.sig_scan_requested.emit()

    def setScanningState(self, _bool_is_scanning: bool):
        if _bool_is_scanning:
            self.setEnabled(False)
            self.setText("Scanning...")
        else:
            self.setEnabled(True)
            self.setText(self.str_original_title)
