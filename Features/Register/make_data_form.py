# Features/Register/make_data_form.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QComboBox, QLineEdit, QPushButton, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication
from Features.Register.category_tag import CategoryTag
# 💡 [분리] ThumbnailDropLabel을 SharedUI에서 가져옵니다
from Features.SharedUI.thumbnail_drop_label import ThumbnailDropLabel

class MakeDataForm(QWidget):
    """
    RegisterWindow / ModifyWindow 중앙에 배치될 동적 입력 폼입니다.
    Asset Name, ID, Asset Type, Categories 콤보박스 및 카테고리 태그들을 관리합니다.
    Register / Modify 두 창에서 모두 재사용됩니다.
    """
    # 이벤트 신호 정의
    sig_make_id_clicked = Signal()          # 💡 Make ID 버튼 클릭 시 외부로 신호 전달
    sig_asset_type_changed = Signal(str)
    sig_category_combo_changed = Signal(str)
    sig_add_category_clicked = Signal(str)
    sig_remove_category_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lay_main = QVBoxLayout()
        lay_main.setAlignment(Qt.AlignTop)
        lay_main.setContentsMargins(0, 0, 0, 0)

        # ==========================================
        # 1. Asset Name 행 (💡 RegisterWindow에서 이동됨)
        # ==========================================
        lay_name_row = QHBoxLayout()

        lbl_name = QLabel("Asset Name")
        lbl_name.setMinimumWidth(80)

        self.let_asset_name = QLineEdit()
        self.let_asset_name.setPlaceholderText("에셋 이름을 입력하세요")
        self.let_asset_name.setMinimumHeight(30)

        lay_name_row.addWidget(lbl_name)
        lay_name_row.addWidget(self.let_asset_name)

        # ==========================================
        # 2. ID 발급 행 (💡 Modify 모드에서는 setModifyMode()로 숨김)
        #    행 전체를 QWidget으로 묶어 hide() 한 번으로 제어합니다
        # ==========================================
        self.wgt_id_row = QWidget()
        lay_id_row = QHBoxLayout(self.wgt_id_row)
        lay_id_row.setContentsMargins(0, 0, 0, 0)

        self.btn_make_id = QPushButton("Make ID")
        self.btn_make_id.setMinimumHeight(30)
        self.btn_make_id.setMinimumWidth(80)
        self.btn_make_id.clicked.connect(self.sig_make_id_clicked.emit)  # 클릭 시 외부(Controller)로 신호 발송

        self.let_id = QLineEdit()
        self.let_id.setReadOnly(True)
        self.let_id.setPlaceholderText("버튼을 눌러 고유 ID를 발급받으세요")
        self.let_id.setMinimumHeight(30)

        lay_id_row.addWidget(self.btn_make_id)
        lay_id_row.addWidget(self.let_id)

        # ==========================================
        # 3. Asset Type 행
        # ==========================================
        lay_type = QHBoxLayout()
        lbl_type = QLabel("Asset Type")
        lbl_type.setMinimumWidth(80)

        self.cmb_asset_type = QComboBox()
        self.cmb_asset_type.setMinimumHeight(30)

        self.let_asset_type = QLineEdit()
        self.let_asset_type.setPlaceholderText("에셋 타입을 입력하세요")
        self.let_asset_type.setMinimumHeight(30)
        self.let_asset_type.setEnabled(False)

        lay_type.addWidget(lbl_type)
        lay_type.addWidget(self.cmb_asset_type, stretch=1)
        lay_type.addWidget(self.let_asset_type, stretch=1)

        # ==========================================
        # 4. Categories 행
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
        # 5. 카테고리 태그 블록을 담을 영역
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
        # 5.5 썸네일 드래그 앤 드롭 영역 (💡 SharedUI에서 import하여 재사용)
        # ==========================================
        self.lbl_thumbnail = ThumbnailDropLabel()

        # ==========================================
        # 6. 프리뷰 파일명 표시 및 복사 영역
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
        # 7. 폴더명 표시 및 복사 영역
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
        lay_main.addLayout(lay_name_row)
        lay_main.addWidget(self.wgt_id_row)   # 💡 QWidget으로 묶어서 숨기기 용이하게
        lay_main.addLayout(lay_type)
        lay_main.addLayout(lay_cat)
        lay_main.addWidget(self.scroll_tags)
        lay_main.addWidget(self.lbl_thumbnail)  # 💡 썸네일 영역 추가
        lay_main.addLayout(lay_preview)
        lay_main.addLayout(lay_folder)

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
        self.sig_asset_type_changed.emit("직접 입력")

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

    # ==========================================
    # 💡 [신규] Modify 모드 전환 함수
    # ==========================================
    def setModifyMode(self):
        """
        Modify 창에서 사용할 때 호출합니다.
        Register 전용 요소(Make ID 행)를 숨겨 폼을 재사용합니다.
        """
        self.wgt_id_row.hide()

    # ==========================================
    # 💡 [신규] 기존 에셋 데이터를 폼에 채우는 함수
    # ==========================================
    def loadExistingData(self, _str_asset_name, _str_asset_type, _str_thumbnail_path, _list_categories):
        """
        Modify 창 오픈 시, 기존에 저장된 에셋 데이터를 각 입력 필드에 채워넣습니다.
        카테고리 태그 복원은 ModifyController가 직접 처리하며, 여기서는 이름·타입·썸네일만 담당합니다.
        """
        # 1. 에셋 이름 세팅
        self.let_asset_name.setText(_str_asset_name)

        # 2. Asset Type 직접 입력 필드 세팅 (콤보박스 선택은 ModifyController가 후처리)
        self.let_asset_type.setText(_str_asset_type)

        # 3. 썸네일 이미지 로드 (loadImage는 ThumbnailDropLabel의 신규 메서드)
        self.lbl_thumbnail.loadImage(_str_thumbnail_path)
