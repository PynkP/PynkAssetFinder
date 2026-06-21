# Features/RegisterWindow/make_data_form.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QScrollArea
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication # 💡 추가 (클립보드 복사용)
from Features.RegisterWindow.category_tag import CategoryTag

class MakeDataForm(QWidget):
    """
    RegisterWindow 중앙에 배치될 동적 입력 폼입니다.
    Asset Type, Categories 콤보박스 및 카테고리 태그들을 관리합니다.
    """
    # 이벤트 신호 정의
    sig_asset_type_changed = Signal(str) # 콤보박스 선택 변경 시
    sig_category_combo_changed = Signal(str)
    sig_add_category_clicked = Signal(str) # 텍스트(직접입력) 추가 시
    sig_remove_category_clicked = Signal(str) # 태그 'X' 버튼 클릭 시
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        lay_main = QVBoxLayout()
        lay_main.setAlignment(Qt.AlignTop)
        
        # 💡 [핵심] 내부 박스의 기본 여백을 없애서, 바깥쪽 요소들과 시작선을 완벽히 일치시킵니다.
        lay_main.setContentsMargins(0, 0, 0, 0)
        
        # ==========================================
        # 1. Asset Type 행
        # ==========================================
        lay_type = QHBoxLayout()
        lbl_type = QLabel("Asset Type")
        lbl_type.setMinimumWidth(80)
        
        self.cmb_asset_type = QComboBox()
        self.cmb_asset_type.setMinimumHeight(30)
        
        self.let_asset_type = QLineEdit()
        self.let_asset_type.setPlaceholderText("에셋 타입을 입력하세요")
        self.let_asset_type.setMinimumHeight(30)
        self.let_asset_type.setEnabled(False) # 처음엔 비활성화
        
        lay_type.addWidget(lbl_type)
        lay_type.addWidget(self.cmb_asset_type, stretch=1)
        lay_type.addWidget(self.let_asset_type, stretch=1)
        
        # ==========================================
        # 2. Categories 행
        # ==========================================
        lay_cat = QHBoxLayout()
        lbl_cat = QLabel("Categories")
        lbl_cat.setMinimumWidth(80)
        
        self.cmb_category = QComboBox()
        self.cmb_category.setMinimumHeight(30)
        
        self.let_category = QLineEdit()
        self.let_category.setPlaceholderText("카테고리를 입력하세요")
        self.let_category.setMinimumHeight(30)
        self.let_category.setEnabled(False)
        
        self.btn_add_category = QPushButton("Add")
        self.btn_add_category.setMinimumHeight(30)
        self.btn_add_category.setMinimumWidth(60)
        
        lay_cat.addWidget(lbl_cat)
        lay_cat.addWidget(self.cmb_category, stretch=1)
        lay_cat.addWidget(self.let_category, stretch=1)
        lay_cat.addWidget(self.btn_add_category)
        
        # ==========================================
        # 3. 카테고리 태그 블록을 담을 영역 (스크롤 가능)
        # ==========================================
        self.scroll_tags = QScrollArea()
        self.scroll_tags.setWidgetResizable(True)
        self.scroll_tags.setFixedHeight(50)
        self.scroll_tags.setStyleSheet("QScrollArea { border: 1px solid #555555; background-color: #2b2b2b; border-radius: 5px; }")
        
        self.wgt_tags_container = QWidget()
        self.wgt_tags_container.setStyleSheet("background-color: transparent;")
        
        self.lay_tags = QHBoxLayout()
        self.lay_tags.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lay_tags.setContentsMargins(5, 0, 5, 0)
        self.wgt_tags_container.setLayout(self.lay_tags)
        
        self.scroll_tags.setWidget(self.wgt_tags_container)
        
        # ==========================================
        # 4. 프리뷰 파일명 표시 및 복사 영역 (신규)
        # ==========================================
        lay_preview = QHBoxLayout()
        
        self.let_preview_name = QLineEdit()
        self.let_preview_name.setReadOnly(True)
        self.let_preview_name.setPlaceholderText("ID 발급 시 프리뷰 파일명이 여기에 표시됩니다")
        self.let_preview_name.setMinimumHeight(30)
        self.let_preview_name.setStyleSheet("background-color: #2b2b2b; color: #aaaaaa;")
        
        self.btn_copy_preview = QPushButton("Copy")
        self.btn_copy_preview.setMinimumHeight(30)
        self.btn_copy_preview.setMinimumWidth(60)
        self.btn_copy_preview.clicked.connect(self._onCopyPreviewClicked)
        
        lay_preview.addWidget(self.let_preview_name)
        lay_preview.addWidget(self.btn_copy_preview)
        
        # ==========================================
        # 5. 폴더명 표시 및 복사 영역 (신규)
        # ==========================================
        lay_folder = QHBoxLayout()
        
        self.let_folder_name = QLineEdit()
        self.let_folder_name.setReadOnly(True)
        self.let_folder_name.setPlaceholderText("ID 발급 시 추천 폴더명이 여기에 표시됩니다")
        self.let_folder_name.setMinimumHeight(30)
        self.let_folder_name.setStyleSheet("background-color: #2b2b2b; color: #aaaaaa;")
        
        self.btn_copy_folder = QPushButton("Copy")
        self.btn_copy_folder.setMinimumHeight(30)
        self.btn_copy_folder.setMinimumWidth(60)
        self.btn_copy_folder.clicked.connect(self._onCopyFolderClicked)
        
        lay_folder.addWidget(self.let_folder_name)
        lay_folder.addWidget(self.btn_copy_folder)
        
        # 레이아웃 결합
        lay_main.addLayout(lay_type)
        lay_main.addLayout(lay_cat)
        lay_main.addWidget(self.scroll_tags)
        lay_main.addLayout(lay_preview) # 💡 추가
        lay_main.addLayout(lay_folder) # 💡 추가
        
        self.setLayout(lay_main)
        
        # 내부 UI 이벤트 연결
        self.cmb_asset_type.currentTextChanged.connect(self.sig_asset_type_changed.emit)
        self.cmb_category.currentTextChanged.connect(self.sig_category_combo_changed.emit)
        self.btn_add_category.clicked.connect(self._onAddCategoryClicked)
        
    def _onAddCategoryClicked(self):
        str_text = self.let_category.text().strip()
        if str_text:
            self.sig_add_category_clicked.emit(str_text)
            self.let_category.clear()

    def _onCopyPreviewClicked(self):
        """클립보드에 프리뷰 파일명을 복사합니다."""
        str_text = self.let_preview_name.text()
        if str_text:
            QGuiApplication.clipboard().setText(str_text)

    def _onCopyFolderClicked(self):
        """클립보드에 폴더명을 복사합니다."""
        str_text = self.let_folder_name.text()
        if str_text:
            QGuiApplication.clipboard().setText(str_text)

    # --- 외부에서 UI를 조작하기 위한 유틸 함수들 ---
    def setAssetTypeOptions(self, _list_options):
        self.cmb_asset_type.blockSignals(True)
        self.cmb_asset_type.clear()
        self.cmb_asset_type.addItem("직접 입력")
        self.cmb_asset_type.addItems(_list_options)
        self.cmb_asset_type.blockSignals(False)
        self.sig_asset_type_changed.emit("직접 입력") # 초기 상태 세팅
        
    def setCategoryOptions(self, _list_options):
        self.cmb_category.blockSignals(True)
        self.cmb_category.clear()
        self.cmb_category.addItem("직접 입력")
        self.cmb_category.addItems(_list_options)
        self.cmb_category.blockSignals(False)
        self.sig_category_combo_changed.emit("직접 입력")

    def toggleAssetTypeInput(self, _bool_enable):
        self.let_asset_type.setEnabled(_bool_enable)
        if _bool_enable:
            self.let_asset_type.setFocus()
        else:
            self.let_asset_type.clear()

    def toggleCategoryInput(self, _bool_enable):
        self.let_category.setEnabled(_bool_enable)

    def setPreviewNames(self, _str_id, _str_asset_name):
        """발급된 ID와 Asset Name 기반으로 텍스트들을 세팅합니다."""
        self.let_preview_name.setText(f"{_str_id}_Preview")
        str_safe_name = _str_asset_name if _str_asset_name else "Untitled"
        self.let_folder_name.setText(f"{str_safe_name}_{_str_id}")

    def addCategoryTag(self, _str_text):
        """태그 UI 위젯을 꼬리물기 방식으로 추가합니다."""
        tag = CategoryTag(_str_text)
        tag.sig_remove_requested.connect(self.sig_remove_category_clicked.emit)
        self.lay_tags.addWidget(tag)
        
    def clearCategoryTags(self):
        """모든 태그 위젯을 초기화합니다."""
        while self.lay_tags.count():
            item = self.lay_tags.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
