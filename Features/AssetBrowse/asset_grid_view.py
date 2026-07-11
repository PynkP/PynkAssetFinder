# Features/AssetBrowse/asset_grid_view.py

from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout
from PySide6.QtCore import Qt, Signal, QRect  # ✅ QRect 추가 (뷰포트 가시 영역 계산용)

from Features.AssetBrowse.thumbnail_widget import ThumbnailWidget  # 💡 새 경로

class AssetGridView(QScrollArea):
    """
    에셋들을 반응형 바둑판(그리드) 형태로 정렬하여 보여주는 전용 뷰(전시관)입니다.
    창 크기가 변하면 알아서 썸네일들의 줄 바꿈을 계산해 줍니다.
    """
    
    # ==========================================
    # 📐 [레이아웃 수치(상수) 정의 구역] 
    # 나중에 썸네일 크기나 간격을 바꾸고 싶다면 여기 숫자만 고치면 됩니다!
    # ==========================================
    ITEM_WIDTH = 256      # ✅ 1.6배 확대 (160→256)
    ITEM_SPACING = 15     # 썸네일 사이의 세로 간격 (고정)
    MARGIN = 10           # 그리드 전체의 바깥쪽 여백 (좌/우/상/하)
    # 썸네일 중 하나가 클릭되었을 때 발생시킬 신호 (외부 컨트롤러가 받음)
    sig_asset_clicked = Signal(str, str)
    sig_asset_right_clicked = Signal(str, str, object) # 우클릭 시 컨트롤러에게 전달
    # 💡 [추가] 스크롤이 바닥에 닿았을 때 로더에게 다음 청크를 요구하는 시그널
    sig_scroll_bottom_reached = Signal()
    
    def __init__(self):
        super().__init__()
        
        # [상태 저장소]
        self.list_thumb_widgets = [] # 생성된 썸네일들을 보관하는 리스트 (창고)
        self.int_current_cols = 0    # 현재 화면이 몇 칸(열)으로 줄 세워져 있는지 기억하는 변수
        
        self.initScrollConfig()
        self.initGridUI()

    def initScrollConfig(self):
        """마우스 휠로 내려볼 수 있도록 스크롤 영역의 껍데기를 세팅합니다."""
        self.setWidgetResizable(True)
        self.setStyleSheet("border: none; background-color: transparent;")
        # ✅ [Lazy Loading & 무한 스크롤] 스크롤 시마다 이벤트 감지
        self.verticalScrollBar().valueChanged.connect(self._onScroll)

    def _onScroll(self, value):
        """스크롤이 움직일 때마다 호출되어 가시 위젯 체크 및 무한 스크롤을 처리합니다."""
        self._checkVisibleWidgets()
        
        # 스크롤바가 끝에 도달했는지 확인 (여유분 50픽셀 정도)
        scrollbar = self.verticalScrollBar()
        # 💡 [방어코드] 그리드를 비울 때(clearGrid) scrollbar.maximum()이 0이 되면서 
        # 잘못된 추가 로딩이 발생하는 것을 막기 위해 조건 추가
        if scrollbar.maximum() > 0 and value >= scrollbar.maximum() - 50:
            self.sig_scroll_bottom_reached.emit()

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
        self.lay_grid.setAlignment(Qt.AlignTop)  # ✅ AlignLeft 제거 (콜럼 stretch와 충돌 방지)
        
        # 3. 도화지에 바둑판을 깔고, 그 도화지를 스크롤 영역에 집어넣습니다.
        self.wgt_container.setLayout(self.lay_grid)
        self.setWidget(self.wgt_container)

    def clearGrid(self):
        """
        다른 폴더를 스캔했을 때, 화면의 썸네일들을 깨끗이 지우고
        컴퓨터 메모리(RAM)에서도 완전히 삭제(해제)하는 청소부 역할을 합니다.
        """
        # ✅ [최적화 B] takeAt + deleteLater를 루프 1번으로 통합
        while self.lay_grid.count():
            item = self.lay_grid.takeAt(0)
            wgt = item.widget()
            if wgt is not None:
                wgt.deleteLater()

        self.list_thumb_widgets.clear()
        self.int_current_cols = 0

    def addThumbnailChunk(self, _list_chunk_data):
        for data_img in _list_chunk_data:
            str_display_name = f"{data_img.str_asset_name}_{data_img.str_id}"
            wgt_thumbnail = ThumbnailWidget(data_img.str_path_preview, str_display_name, data_img.str_id)
            wgt_thumbnail.sig_clicked.connect(self.sig_asset_clicked.emit)
            wgt_thumbnail.sig_right_clicked.connect(self.sig_asset_right_clicked.emit)
            self.list_thumb_widgets.append(wgt_thumbnail)

        self.rearrangeGrid()
        # ✅ [Lazy Loading] 청크 배치 후 현재 보이는 위젯 즉시 로드 (첫 화면 표시용)
        self._checkVisibleWidgets()
    
    # ==========================================
    # 🧮 [반응형 그리드 수학 계산 구역] 
    # ==========================================
    def rearrangeGrid(self):
        """현재 창 너비를 계산하여 썸네일들을 바둥판의 알맞은 위치에 꼽아 넣습니다."""
        if not self.list_thumb_widgets:
            return

        # ✅ 항상 4열 고정
        self.int_current_cols = 4

        # 1. 완벽한 비율의 위젯 크기 계산
        int_area_width = self.viewport().width()
        # 전체 너비 - 양쪽 마진(MARGIN*2) - 위젯사이 간격(ITEM_SPACING*3)
        int_available = int_area_width - (self.MARGIN * 2) - (self.ITEM_SPACING * 3)
        
        int_w = max(200, int_available // 4)
        int_h = int_w + 64  # 정사각형 이미지 공간 + 이름 영역(64px)

        # 간격 고정
        self.lay_grid.setSpacing(self.ITEM_SPACING)

        # 2. 모든 위젯을 현재 뷰포트에 꽉 차도록 사이즈 동기화
        for wgt in self.list_thumb_widgets:
            wgt.updateSize(int_w, int_h)

        # 3. 새로운 위젯만 추가 배치 (이미 배치된 건 건드리지 않음)
        int_current_count = self.lay_grid.count()
        for int_idx in range(int_current_count, len(self.list_thumb_widgets)):
            wgt = self.list_thumb_widgets[int_idx]
            int_row = int_idx // self.int_current_cols
            int_col = int_idx % self.int_current_cols
            self.lay_grid.addWidget(wgt, int_row, int_col)

    # ==========================================
    # ✅ [Lazy Loading 핵심] 뷰포트 가시 위젯 체크
    # ==========================================
    def _checkVisibleWidgets(self):
        """현재 뷰포트에 보이는 썸네일 위젯들에만 이미지 로드를 요청합니다."""
        viewport_rect = self.viewport().rect()

        for wgt in self.list_thumb_widgets:
            if wgt.bool_image_loaded:
                continue
            # 위젯의 절대 위치를 뷰포트 기준 좌표로 변환
            wgt_pos = self.wgt_container.mapTo(self.viewport(), wgt.pos())
            wgt_rect = QRect(wgt_pos, wgt.size())

            if viewport_rect.intersects(wgt_rect):
                wgt.loadImage()

    def resizeEvent(self, _event):
        """유저가 마우스로 프로그램 창 크기를 쭈욱 늘리거나 줄일 때마다 자동으로 실행됩니다."""
        super().resizeEvent(_event)
        self.int_current_cols = 0
        self.rearrangeGrid()
        # ✅ [Lazy Loading] 창 크기 변경 시 새로 보이는 위젯 체크
        self._checkVisibleWidgets()
