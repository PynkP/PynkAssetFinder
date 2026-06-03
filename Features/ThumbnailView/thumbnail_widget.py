
"""썸네일 위젯 클래스 
사진과 이름표만 신경 쓰고, 클릭되면 관리자에게 보고"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFontMetrics
from PySide6.QtCore import Qt

from Core.asset_manager import AssetManager

class ThumbnailWidget(QFrame):
    """
    개별 에셋의 이미지와 파일명을 화면에 보여주고, 
    클릭 등의 상호작용을 처리하는 가장 기초적인 UI 부품(위젯)입니다.
    """
    
    # ==========================================
    # 🎨 [스타일(CSS) 정의 구역] 
    # 마우스 이벤트마다 긴 문자열을 쓰지 않도록 상단에 미리 정의해 둡니다.
    # ==========================================
    STYLE_DEFAULT = """
        ThumbnailWidget {
            background-color: black; 
            border: 2px solid transparent; /* 평소에는 테두리 투명하게 유지 */
            border-radius: 5px;
        }
    """
    
    STYLE_HOVER = """
        ThumbnailWidget {
            background-color: rgb(50, 50, 50); 
            border: 2px solid rgb(100, 200, 255); /* 마우스가 올라가면 밝은 파란색 테두리 */
            border-radius: 5px;
        }
    """
    
    # 최기화 영역 wgt_thumbnail = ThumbnailWidget(dict_img['path'], dict_img['name']) 이런식으로 불로올 예정
    def __init__(self, _str_path, _str_name):
        # QFrame을 상속받아야 배경색이나 테두리(border) 같은 CSS 스타일이 정상적으로 먹힙니다.
        super().__init__()
        
        # 💡 [데이터 보관] 이 위젯이 대표하는 실제 파일의 경로와 이름을 기억해 둡니다.
        self.str_file_path = _str_path
        self.str_file_name = _str_name
        
        # 함수들을 역할별로 쪼개어 실행합니다. (유지보수가 훨씬 쉬워집니다)
        self.initWidgetConfig()
        self.initUI()
        self.initLayout()

    def initWidgetConfig(self):
        """위젯 자체의 기본 속성(크기, 커서, 초기 스타일)을 세팅합니다."""
        self.setFixedSize(160, 190) 
        
        # 유저가 '이거 누를 수 있구나'라고 직관적으로 알도록 마우스 커서를 손가락 모양으로 변경
        self.setCursor(Qt.PointingHandCursor)
        
        # 미리 정의해둔 기본 스타일 적용
        self.setStyleSheet(self.STYLE_DEFAULT)

    def initUI(self):
        """위젯 안에 들어갈 내용물(이미지, 텍스트)을 만듭니다."""
        
        # --- 1. 이미지 라벨 세팅 ---
        self.wgt_lbl_img = QLabel()
        self.wgt_lbl_img.setAlignment(Qt.AlignCenter)
        
        # 하드디스크에 있는 이미지를 메모리(QPixmap)로 퍼옵니다.
        obj_pixmap = QPixmap(self.str_file_path) 
        
        if not obj_pixmap.isNull():
            # 아무리 4K 텍스처라도 150x150 사이즈로 리사이징합니다.
            # Qt.KeepAspectRatio: 원본 비율 찌그러짐 방지
            # Qt.SmoothTransformation: 계단 현상(안티앨리어싱) 방지하여 부드럽게 축소
            obj_pixmap = obj_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.wgt_lbl_img.setPixmap(obj_pixmap)

        # --- 2. 파일명 라벨 세팅 ---
        self.wgt_lbl_name = QLabel()
        self.wgt_lbl_name.setAlignment(Qt.AlignCenter)
        self.wgt_lbl_name.setStyleSheet("color: gray; border: none;")
        self.wgt_lbl_name.setFixedHeight(40) # 이름이 길어서 2줄이 되더라도 레이아웃이 안 밀리게 높이 고정

        # [글자 말줄임표 처리 로직]
        # 1) 현재 라벨의 폰트 정보를 기반으로 글자 크기를 재는 '줄자'를 만듭니다.
        obj_font_metrics = QFontMetrics(self.wgt_lbl_name.font()) 
        
        # 2) 파일명을 150픽셀 길이에 맞춰봅니다. 넘치면 오른쪽(ElideRight)을 잘라내고 '...'을 붙입니다.
        str_elided_name = obj_font_metrics.elidedText(self.str_file_name, Qt.ElideRight, 150)
        
        # 3) 예쁘게 잘린 문자열을 라벨에 적용합니다.
        self.wgt_lbl_name.setText(str_elided_name)

    def initLayout(self):
        """만들어진 내용물들을 위에서 아래로(세로로) 조립합니다."""
        lay_main = QVBoxLayout()
        lay_main.setContentsMargins(0, 0, 0, 0) # 위젯 내부의 불필요한 여백 제거
        lay_main.setSpacing(0)                  # 이미지와 텍스트 사이의 간격 제거

        # 박스 안에 이미지 넣고, 그 아래에 이름표를 넣습니다.
        lay_main.addWidget(self.wgt_lbl_img)
        lay_main.addWidget(self.wgt_lbl_name)
        
        # 조립된 레이아웃을 위젯에 최종 적용합니다.
        self.setLayout(lay_main)

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
        # 좌클릭일 때만 작동하도록 방어 로직 (나중에 우클릭 메뉴를 달기 위해 분리)
        if _event.button() == Qt.LeftButton:
            
            # [MVC 패턴 핵심] UI가 직접 운영체제를 건드리지 않고, 중앙 관리자에게 '경로'만 전달합니다.
            obj_manager = AssetManager()
            obj_manager.openAssetFolder(self.str_file_path)
            
        super().mousePressEvent(_event)