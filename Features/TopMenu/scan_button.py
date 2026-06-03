from PySide6.QtWidgets import QPushButton, QFileDialog
from PySide6.QtCore import Signal
from Core.folder_scanner import FolderScanner

class ScanButton(QPushButton):
    """스스로 폴더를 띄우고, 스캐너를 관리하며, 상태를 제어하는 똑똑한 버튼입니다."""
    
    # 💡 [핵심] 스캔이 완전히 끝났을 때 외부(main.py)로 쏠 전용 신호기!
    sig_scan_completed = Signal()

    def __init__(self, _str_title="Folder Scan"):
        super().__init__(_str_title)
        
        # 버튼 디자인 세팅 (필요에 따라 수정)
        self.setFixedSize(120, 35)
        self.setStyleSheet("background-color: rgb(70, 70, 70); color: white; border-radius: 5px;")
        
        # 자기가 눌리면 스스로의 onClicked 함수를 실행합니다.
        self.clicked.connect(self.onClicked)

    def onClicked(self):
        """버튼이 눌렸을 때 실행되는 로직"""
        # 1. 윈도우 폴더 선택 창 띄우기
        str_target_dir = QFileDialog.getExistingDirectory(self, "에셋 폴더 선택")
        if not str_target_dir:
            return # 취소 누르면 그냥 종료
            
        # 2. 💡 [UI 제어] 스캔하는 동안 유저가 또 누르지 못하게 스스로를 잠금!
        self.setEnabled(False)
        self.setText("Scanning...")
        
        # 3. 스캐너(하청업체) 고용 및 실행
        self.obj_scanner = FolderScanner(str_target_dir)
        self.obj_scanner.sig_finished.connect(self.onScannerFinished)
        self.obj_scanner.start()

    def onScannerFinished(self, _b_success):
        """스캐너가 일을 마쳤을 때 실행되는 로직"""
        # 1. 💡 [UI 복구] 스스로 잠금을 풀고 원래 이름으로 복구
        self.setEnabled(True)
        self.setText("Folder Scan")
        
        # 2. 대망의 최종 보고! "메인(main.py)님! 스캔 끝났습니다!" 하고 신호 쏘기
        if _b_success:
            self.sig_scan_completed.emit()