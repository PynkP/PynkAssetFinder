"""백엔드 부분 CHUNK_SIZE씩 썸네일을 불러옴 그냥 썸네일 리스트 인덱스 관리자임"""
from PySide6.QtCore import QObject, QTimer, Signal

class ThumbnailLoader(QObject):
    CHUNK_SIZE = 50

    # 💡 [변경] 콜백 대신 Qt의 안전한 시그널/슬롯 시스템으로 변경
    sig_clear_requested = Signal()
    sig_chunk_ready = Signal(list)
    sig_load_completed = Signal()

    def __init__(self):
        super().__init__()
        self.list_pending_data = []
        self.int_current_idx = 0
        
        self.obj_timer = QTimer(self)
        self.obj_timer.timeout.connect(self._onTimeout)

    def reloadAssets(self, _list_new_assets):
        """
        💡 [변경] 더 이상 AssetManager를 몰래 뒤지지 않고, 
        컨트롤러가 던져주는 데이터(_list_new_assets)를 넙죽 받아서 쓰기만 합니다.
        """
        self.obj_timer.stop()
        self.sig_clear_requested.emit() # 화면 지워달라고 시그널 방출
            
        self.list_pending_data = _list_new_assets
        self.int_current_idx = 0 
        
        if not self.list_pending_data:
            self.sig_load_completed.emit()
            return
            
        self.obj_timer.start(10) 

    def stopLoading(self):
        self.obj_timer.stop()

    def _onTimeout(self):
        int_end = self.int_current_idx + self.CHUNK_SIZE
        list_chunk = self.list_pending_data[self.int_current_idx:int_end]
        
        # 💡 [변경] 콜백 함수 실행 대신, 데이터 덩어리를 시그널에 담아서 방출
        self.sig_chunk_ready.emit(list_chunk)
            
        self.int_current_idx = int_end

        if self.int_current_idx >= len(self.list_pending_data):
            self.obj_timer.stop()
            self.sig_load_completed.emit() # 렌더링 끝났다고 시그널 방출