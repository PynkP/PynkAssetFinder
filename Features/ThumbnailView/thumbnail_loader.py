"""백엔드 부분 CHUNK_SIZE씩 썸네일을 불러옴 그냥 썸네일 리스트 인덱스 관리자임"""
from PySide6.QtCore import QObject, Signal

class ThumbnailLoader(QObject):
    CHUNK_SIZE = 50  # 💡 한 번에 불러올 개수 (무한 스크롤이므로 처음에는 적당히 50개)

    # 💡 [변경] 콜백 대신 Qt의 안전한 시그널/슬롯 시스템으로 변경
    sig_clear_requested = Signal()
    sig_chunk_ready = Signal(list)
    sig_load_completed = Signal()

    def __init__(self):
        super().__init__()
        self.list_pending_data = []
        self.int_current_idx = 0
        self.bool_is_loading = False # 💡 여러번 스크롤 이벤트가 동시에 들어오는 것을 방지

    def reloadAssets(self, _list_new_assets):
        """
        새로운 데이터를 세팅하고 처음 1묶음(Chunk)만 불러옵니다.
        나머지는 스크롤할 때마다 불러옵니다.
        """
        self.sig_clear_requested.emit() # 화면 지워달라고 시그널 방출
            
        self.list_pending_data = _list_new_assets
        self.int_current_idx = 0 
        self.bool_is_loading = False
        
        if not self.list_pending_data:
            self.sig_load_completed.emit()
            return
            
        # 첫 번째 청크 로드
        self.loadNextChunk()

    def loadNextChunk(self):
        """
        스크롤이 바닥에 닿았을 때 호출되어 다음 묶음을 방출합니다.
        """
        # 이미 로딩이 다 끝났거나 처리 중이면 무시
        if self.bool_is_loading or self.int_current_idx >= len(self.list_pending_data):
            return
            
        self.bool_is_loading = True
        
        int_end = self.int_current_idx + self.CHUNK_SIZE
        list_chunk = self.list_pending_data[self.int_current_idx:int_end]
        
        # 💡 데이터 덩어리를 시그널에 담아서 방출
        self.sig_chunk_ready.emit(list_chunk)
            
        self.int_current_idx = int_end

        if self.int_current_idx >= len(self.list_pending_data):
            self.sig_load_completed.emit() # 렌더링 끝났다고 시그널 방출
            
        self.bool_is_loading = False