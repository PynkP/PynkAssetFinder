"""백엔드 부분 CHUNK_SIZE씩 썸네일을 불러옴 그냥 썸네일 리스트 인덱스 관리자임 main.py에서 reloadAssets 실행해 줌"""

from PySide6.QtCore import QObject, QTimer
from Core.asset_manager import AssetManager

class ThumbnailLoader(QObject):
    """
    [컨트롤러] 화면이 멈추지 않도록(Freezing 방지) 
    대량의 데이터를 잘게 쪼개서(Chunk) UI에 순차적으로 넘겨주는 '배식원' 역할입니다.
    """

    # ==========================================
    # ⚙️ [설정 값(상수) 정의 구역] 
    # 나중에 컴퓨터 성능에 맞춰 한 번에 로딩할 개수를 조절하고 싶다면 이 숫자만 바꾸면 됩니다!
    # ==========================================
    CHUNK_SIZE = 50

    def __init__(self):
        super().__init__()
        
        # 📦 [상태 저장소]
        self.list_pending_data = [] # 대기 중인 전체 데이터 목록 (예: 10만 개)
        self.int_current_idx = 0    # 현재 어디까지 배식(렌더링)했는지 기억하는 책갈피
        
        # ⏱️ [타이머 설정] 메인 스레드를 멈추지 않게 하는 핵심 부품
        self.obj_timer = QTimer(self)
        self.obj_timer.timeout.connect(self._onTimeout) # timer.start(함수) 할 때 실행될 함수
        
        # 🔌 [스위치(콜백) 보관소] 외부(main.py)에서 연결해 줄 동작 선들
        self.func_on_clear = None           # 화면 지우기 스위치
        self.func_on_chunk_ready = None     # 일정 개수(Chunk)만큼 그리기 스위치
        self.func_on_load_completed = None  # 모든 렌더링 완료 알림 스위치

    def setCallbacks(self, _func_clear, _func_chunk, _func_completed):
        """View를 제어할 함수 2개와 TopBar를 제어할 함수 1개를 세팅(선 연결)합니다."""
        self.func_on_clear = _func_clear
        self.func_on_chunk_ready = _func_chunk
        self.func_on_load_completed = _func_completed

    def reloadAssets(self):
        """
        💡 [핵심] 외부의 지시 없이, 스스로 중앙 창고(AssetManager)를 찾아가 데이터를 가져오고 로딩을 시작합니다.
        스캔이 끝났을 때(TopBar) 호출됩니다.
        """
        self.obj_timer.stop() # 혹시 기존에 돌고 있던 타이머가 있다면 안전하게 정지
        
        # 1. 화면 싹 지우기 명령 발송 (AssetGridView의 clearGrid 실행)
        if self.func_on_clear is not None:
            self.func_on_clear()
            
        # 2. 중앙 창고(AssetManager)에서 최신 데이터(리스트) 직접 꺼내오기
        obj_manager = AssetManager()
        self.list_pending_data = obj_manager.getAllAssets()
        self.int_current_idx = 0 # 책갈피 초기화
        
        # 3. 방어 로직: 만약 스캔한 폴더에 파일이 하나도 없다면? 바로 종료 알림 발송
        if not self.list_pending_data:
            if self.func_on_load_completed is not None:
                self.func_on_load_completed()
            return
            
        # 4. 타이머 가동: 이제 0.01초(10ms)마다 _onTimeout 함수가 반복 실행됩니다.
        self.obj_timer.start(10) 

    def stopLoading(self):
        """프로그램이 종료되거나 중간에 스캔을 멈출 때 타이머를 강제 정지합니다."""
        self.obj_timer.stop()

    def _onTimeout(self):
        """
        타이머에 의해 0.01초마다 반복 실행되는 함수.
        전체 데이터 중 CHUNK_SIZE(50개)만큼만 잘라서 UI 쪽에 던져줍니다.
        """
        # 시작점(현재 책갈피)에서 50개를 더해 이번 턴의 끝점을 계산합니다.
        int_end = self.int_current_idx + self.CHUNK_SIZE
        
        # 전체 리스트에서 이번 턴에 그릴 50개만 가위로 잘라냅니다. (리스트 슬라이싱)
        list_chunk = self.list_pending_data[self.int_current_idx:int_end]
        
        # 50개의 데이터 뭉치를 View(AssetGridView) 쪽에 던져줍니다. -> 화면에 그려짐!
        if self.func_on_chunk_ready is not None:
            self.func_on_chunk_ready(list_chunk)
            
        # 책갈피를 끝점으로 이동시킵니다. (다음 턴에는 여기서부터 다시 시작)
        self.int_current_idx = int_end

        # 💡 종료 조건: 책갈피가 전체 데이터 길이보다 크거나 같아지면? (다 그렸다면)
        if self.int_current_idx >= len(self.list_pending_data):
            self.obj_timer.stop() # 타이머 정지
            
            # TopBar 쪽으로 "렌더링 진짜 끝났어! 버튼 원상복구 해!" 라고 알림을 보냅니다.
            if self.func_on_load_completed is not None:
                self.func_on_load_completed()