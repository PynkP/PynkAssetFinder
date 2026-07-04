
"""썸네일 위젯 클래스 
사진과 이름표만 신경 쓰고, 클릭되면 관리자에게 보고"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFontMetrics, QImageReader
from PySide6.QtCore import Qt, Signal, QSize

class ThumbnailWidget(QFrame):
    """
    개별 에셋의 이미지와 파일명을 화면에 보여주고, 
    클릭 등의 상호작용을 처리하는 가장 기초적인 UI 부품(위젯)입니다.
    """
    
    # ==========================================
    # 🎨 [스타일(CSS) 정의 구역] 
    # ==========================================
    STYLE_DEFAULT = """
        ThumbnailWidget {
            background-color: black; 
            border: 2px solid transparent;
            border-radius: 5px;
        }
    """
    STYLE_HOVER = """
        ThumbnailWidget {
            background-color: rgb(50, 50, 50); 
            border: 2px solid rgb(100, 200, 255);
            border-radius: 5px;
        }
    """
    sig_clicked = Signal(str)

    def __init__(self, _str_path, _str_name):
        super().__init__()
        self.str_file_path = _str_path
        self.str_file_name = _str_name
        # ✅ [Lazy Loading] 이미지 로드 여부 상태 플래그
        self.bool_image_loaded = False

        self.initWidgetConfig()
        self.initUI()
        self.initLayout()

    def initWidgetConfig(self):
        """위젯 자체의 기본 속성(크기, 커서, 초기 스타일)을 세팅합니다."""
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self.STYLE_DEFAULT)

    def initUI(self):
        """위젯 안에 들어갈 내용물(이미지, 텍스트)을 만듭니다."""
        # --- 1. 이미지 라벨 세팅 ---
        self.wgt_lbl_img = QLabel()
        self.wgt_lbl_img.setAlignment(Qt.AlignCenter)

        # --- 2. 파일명 라벨 세팅 ---
        self.wgt_lbl_name = QLabel()
        self.wgt_lbl_name.setAlignment(Qt.AlignCenter)
        self.wgt_lbl_name.setStyleSheet("color: gray; border: none;")
        self.wgt_lbl_name.setFixedHeight(64)

    def initLayout(self):
        """만들어진 내용물들을 위에서 아래로(세로로) 조립합니다."""
        lay_main = QVBoxLayout()
        lay_main.setContentsMargins(0, 0, 0, 0)
        lay_main.setSpacing(0)
        lay_main.addWidget(self.wgt_lbl_img)
        lay_main.addWidget(self.wgt_lbl_name)
        self.setLayout(lay_main)

    # ==========================================
    # ✅ [동적 크기 조정] 외부 뷰에서 픽셀 크기를 완벽하게 주입
    # ==========================================
    def updateSize(self, int_w, int_h):
        self.setFixedSize(int_w, int_h)
        self.wgt_lbl_img.setFixedSize(int_w, int_h - 64)
        
        # 이름 텍스트 말줄임 재계산
        obj_font_metrics = QFontMetrics(self.wgt_lbl_name.font())
        str_elided_name = obj_font_metrics.elidedText(self.str_file_name, Qt.ElideRight, int_w - 20)
        self.wgt_lbl_name.setText(str_elided_name)
        
        # 이미 로드된 이미지가 있다면 새 크기에 맞춰 픽스맵 리스케일링
        if self.bool_image_loaded and hasattr(self, 'original_pixmap'):
            self.wgt_lbl_img.setPixmap(self.original_pixmap.scaled(
                int_w, int_h - 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

    # ==========================================
    # ✅ [Lazy Loading 핵심] 이미지 로드 함수
    # ==========================================
    def loadImage(self):
        """뷰포트에 보일 때만 외부에서 호출됩니다."""
        if self.bool_image_loaded:
            return

        obj_reader = QImageReader(self.str_file_path)
        obj_size_original = obj_reader.size()

        if obj_size_original.isValid():
            # ✅ 확대 시 깨짐 방지를 위해 원본을 충분히 큰 해상도로 읽어옵니다
            obj_size_scaled = obj_size_original.scaled(QSize(512, 512), Qt.KeepAspectRatio)
            obj_reader.setScaledSize(obj_size_scaled)

        img_scaled = obj_reader.read()

        if not img_scaled.isNull():
            self.original_pixmap = QPixmap.fromImage(img_scaled)
            int_w = self.wgt_lbl_img.width()
            int_h = self.wgt_lbl_img.height()
            self.wgt_lbl_img.setPixmap(self.original_pixmap.scaled(
                int_w, int_h, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

        self.bool_image_loaded = True

    # ==========================================
    # 🖱️ [마우스 이벤트 처리 구역] 
    # ==========================================
    def enterEvent(self, _event):
        """마우스 커서가 썸네일 영역 안으로 들어왔을 때 (Hover 효과 켜기)"""
        self.setStyleSheet(self.STYLE_HOVER)
        super().enterEvent(_event)

    def leaveEvent(self, _event):
        """마우스 커서가 썸네일 영역 밖으로 나갔을 때 (Hover 효과 끄기)"""
        self.setStyleSheet(self.STYLE_DEFAULT)
        super().leaveEvent(_event)

    def mousePressEvent(self, _event):
        """마우스로 썸네일을 클릭했을 때"""
        if _event.button() == Qt.LeftButton:
            self.sig_clicked.emit(self.str_file_path)
        super().mousePressEvent(_event)