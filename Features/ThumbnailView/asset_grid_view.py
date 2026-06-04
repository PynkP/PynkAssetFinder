from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout
from PySide6.QtCore import Qt, Signal # 💡 Signal 추가

from Features.ThumbnailView.thumbnail_widget import ThumbnailWidget

class AssetGridView(QScrollArea):
    """
    에셋들을 반응형 바둑판(그리드) 형태로 정렬하여 보여주는 전용 뷰(전시관)입니다.
    창 크기가 변하면 알아서 썸네일들의 줄 바꿈을 계산해 줍니다.
    """
    
    # ==========================================
    # 📐 [레이아웃 수치(상수) 정의 구역] 
    # 나중에 썸네일 크기나 간격을 바꾸고 싶다면 여기 숫자만 고치면 됩니다!
    # ==========================================
    ITEM_WIDTH = 160      # 썸네일 위젯 하나의 가로 길이
    ITEM_SPACING = 15     # 썸네일 사이의 간격
    MARGIN = 10           # 그리드 전체의 바깥쪽 여백 (좌/우/상/하)
    # 💡 [추가] 썸네일 중 하나가 클릭되면 밖으로 알려줄 릴레이 시그널
    sig_asset_clicked = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        # [상태 저장소]
        self.list_thumb_widgets = [] # 생성된 썸네일들을 보관하는 리스트 (창고)
        self.int_current_cols = 0    # 현재 화면이 몇 칸(열)으로 줄 세워져 있는지 기억하는 변수
        
        self.initScrollConfig()
        self.initGridUI()

    def initScrollConfig(self):
        """마우스 휠로 내려볼 수 있도록 스크롤 영역의 껍데기를 세팅합니다."""
        self.setWidgetResizable(True) # 내부 위젯 크기가 스크롤 영역에 맞춰 자동으로 늘어나게 설정
        
        # 투명한 배경과 테두리 없는 디자인(border: none)을 적용하여 깔끔하게 만듭니다.
        self.setStyleSheet("border: none; background-color: transparent;")

    def initGridUI(self):
        """실제로 썸네일들이 바둑판처럼 배치될 내부 도화지를 만듭니다."""
        # 1. 그리드 레이아웃이 올라갈 내부 컨테이너 위젯 (도화지)
        self.wgt_container = QWidget()
        self.wgt_container.setStyleSheet("background-color: transparent;")
        
        # 2. 바둑판 레이아웃(QGridLayout) 생성
        self.lay_grid = QGridLayout()
        # 좌, 상, 우, 하 여백 설정 (미리 정의한 MARGIN 사용)
        self.lay_grid.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        # 아이템들 사이의 간격 설정
        self.lay_grid.setSpacing(self.ITEM_SPACING)
        # 아이템들을 좌측 상단부터 차곡차곡 쌓이도록 정렬
        self.lay_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # 3. 도화지에 바둑판을 깔고, 그 도화지를 스크롤 영역에 집어넣습니다.
        self.wgt_container.setLayout(self.lay_grid)
        self.setWidget(self.wgt_container)

    def clearGrid(self):
        """
        다른 폴더를 스캔했을 때, 화면의 썸네일들을 깨끗이 지우고 
        컴퓨터 메모리(RAM)에서도 완전히 삭제(해제)하는 청소부 역할을 합니다.
        """
        # 1. 레이아웃에 배치된 틀을 모두 빼냅니다.
        while self.lay_grid.count():
            self.lay_grid.takeAt(0)
            
        # 2. 실제로 메모리 상에 존재하는 위젯 객체들을 파괴합니다.
        for wgt in self.list_thumb_widgets:
            wgt.deleteLater()
            
        # 3. 창고와 칸수 기억을 초기화합니다.
        self.list_thumb_widgets.clear()
        self.int_current_cols = 0

    def addThumbnailChunk(self, _list_chunk_data):
        for dict_img in _list_chunk_data:
            wgt_thumbnail = ThumbnailWidget(dict_img['path'], dict_img['name'])
            
            # 💡 [핵심 추가] 개별 썸네일이 눌리면 -> 그리드 뷰의 시그널로 토스(연결)해 줍니다.
            wgt_thumbnail.sig_clicked.connect(self.sig_asset_clicked.emit)
            
            self.list_thumb_widgets.append(wgt_thumbnail)
            
        self.rearrangeGrid()
    
    # ==========================================
    # 🧮 [반응형 그리드 수학 계산 구역] 
    # ==========================================
    def rearrangeGrid(self):
        """현재 창 너비를 계산하여 썸네일들을 바둑판의 알맞은 위치에 꽂아 넣습니다."""
        if not self.list_thumb_widgets:
            return

        # 1. 수학 계산 준비
        int_area_width = self.viewport().width() # 현재 스크롤 영역의 실제 가로 길이
        int_total_margin = self.MARGIN * 4       # 양쪽 여백 + 스크롤바 여유 공간 확보
        int_item_total_width = self.ITEM_WIDTH + self.ITEM_SPACING # 위젯 1개가 차지하는 실제 덩치

        # 2. "이 창 크기면 한 줄에 몇 개 들어갈까?" 몫(//)을 구해서 칸수(Column)를 계산합니다.
        # (최소 1칸은 보장하기 위해 max(1, ...) 사용)
        int_new_cols = max(1, (int_area_width - int_total_margin) // int_item_total_width)

        # 3. 창 크기가 변해서 칸수가 달라졌다면? -> 줄을 처음부터 완전히 다시 세워야 합니다.
        if self.int_current_cols != int_new_cols:
            self.int_current_cols = int_new_cols
            # 레이아웃에서 위젯들을 싹 다 뺍니다. (삭제하는 게 아니라 위치만 초기화)
            while self.lay_grid.count():
                self.lay_grid.takeAt(0)

        # 4. 바둑판에 위젯 배치하기 (핵심 최적화 구간)
        # 이미 배치된 녀석들은 냅두고, '아직 배치 안 된 새로운 녀석들'만 추가합니다.
        # (만약 위 3번에서 초기화됐다면 int_current_count가 0이 되어 전부 다시 배치됩니다)
        int_current_count = self.lay_grid.count()
        for int_idx in range(int_current_count, len(self.list_thumb_widgets)):
            wgt = self.list_thumb_widgets[int_idx]
            
            # 수학의 몫과 나머지를 이용한 그리드 좌표(x, y) 계산!
            # 예: 1줄에 3개씩일 때, 4번째(idx 3) 위젯은? 3//3 = 1(두번째 줄), 3%3 = 0(첫번째 칸)
            int_row = int_idx // self.int_current_cols
            int_col = int_idx % self.int_current_cols
            
            self.lay_grid.addWidget(wgt, int_row, int_col)

    def resizeEvent(self, _event):
        """유저가 마우스로 프로그램 창 크기를 쭈욱 늘리거나 줄일 때마다 자동으로 실행됩니다."""
        super().resizeEvent(_event)
        
        # 강제로 칸수를 0으로 만들어서, rearrangeGrid()가 무조건 줄을 다시 세우도록 유도합니다.
        self.int_current_cols = 0 
        self.rearrangeGrid()