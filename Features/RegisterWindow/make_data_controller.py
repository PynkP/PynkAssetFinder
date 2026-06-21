# Features/RegisterWindow/make_data_controller.py

from PySide6.QtCore import QObject

class MakeDataController(QObject):
    """
    Make Data 폼의 복잡한 동적 상호작용(콤보박스 변경, 태그 생성 등)을 
    전담하여 관리하는 컨트롤러입니다. (단일 책임 원칙 적용)
    """
    def __init__(self, _wgt_form, _obj_asset_manager, _obj_category_manager):
        super().__init__()
        self.wgt_form = _wgt_form
        self.obj_asset_manager = _obj_asset_manager
        self.obj_category_manager = _obj_category_manager
        
        # 상태 관리: 현재 사용자가 파고들어간 카테고리 경로 (예: ["3D asset", "nature"])
        self.list_current_category_path = []
        
        # 창이 켜질 때가 아니라 Make ID를 누를 때 갱신되도록 initUIState() 호출 제거
        self.initConnections()
        
    def refreshUIState(self):
        """최신 데이터를 불러와 콤보박스와 상태를 갱신합니다."""
        # 1. Asset Type 목록 채우기
        list_types = self.obj_asset_manager.getUniqueAssetTypes()
        self.wgt_form.setAssetTypeOptions(list_types)
        
        # 2. Category 상태 초기화 및 1뎁스 목록 채우기
        self.list_current_category_path = []
        self.wgt_form.clearCategoryTags()
        self._updateCategoryComboBox()

    def initConnections(self):
        self.wgt_form.sig_asset_type_changed.connect(self._onAssetTypeChanged)
        self.wgt_form.sig_category_combo_changed.connect(self._onCategoryComboChanged)
        self.wgt_form.sig_add_category_clicked.connect(self._onAddCategoryClicked)
        self.wgt_form.sig_remove_category_clicked.connect(self._onRemoveCategoryClicked)
        
    def _onAssetTypeChanged(self, _str_text):
        """Asset Type 콤보박스 선택이 바뀔 때"""
        if _str_text == "직접 입력":
            self.wgt_form.toggleAssetTypeInput(True)
        else:
            self.wgt_form.toggleAssetTypeInput(False)
            
    def _onCategoryComboChanged(self, _str_text):
        """Category 콤보박스 선택이 바뀔 때"""
        if _str_text == "직접 입력":
            self.wgt_form.toggleCategoryInput(True)
        else:
            # 기존 목록을 선택했다면? 바로 태그로 추가하고 다음 뎁스로 이동!
            self.wgt_form.toggleCategoryInput(False)
            self._addCategoryTagAndGoDeeper(_str_text)
            
    def _onAddCategoryClicked(self, _str_text):
        """직접 입력 후 Add 버튼을 눌렀을 때"""
        self._addCategoryTagAndGoDeeper(_str_text)
        
    def _addCategoryTagAndGoDeeper(self, _str_tag):
        """태그를 추가하고, 콤보박스를 다음 뎁스 목록으로 갱신합니다."""
        # 1. 상태 및 UI에 태그 추가
        self.list_current_category_path.append(_str_tag)
        self.wgt_form.addCategoryTag(_str_tag)
        
        # 2. 다음 뎁스 목록 불러오기
        self._updateCategoryComboBox()
        
    def _onRemoveCategoryClicked(self, _str_target_tag):
        """
        태그의 'X' 버튼을 눌렀을 때.
        선택한 태그와 그 이후 뎁스 태그들이 일괄 삭제되어야 합니다.
        """
        if _str_target_tag in self.list_current_category_path:
            # 삭제할 태그의 인덱스를 찾아 그 이후를 모두 잘라냄 (롤백)
            int_idx = self.list_current_category_path.index(_str_target_tag)
            self.list_current_category_path = self.list_current_category_path[:int_idx]
            
            # UI 태그들 다시 그리기
            self.wgt_form.clearCategoryTags()
            for tag in self.list_current_category_path:
                self.wgt_form.addCategoryTag(tag)
                
            # 콤보박스 목록 다시 갱신
            self._updateCategoryComboBox()

    def _updateCategoryComboBox(self):
        """현재 경로에 기반하여 자식 카테고리들을 찾아 콤보박스를 갱신합니다."""
        list_children = self.obj_category_manager.getChildrenOfPath(self.list_current_category_path)
        self.wgt_form.setCategoryOptions(list_children)

    def getFormData(self):
        """현재 폼에 입력된 데이터를 수집하여 반환합니다."""
        str_asset_type = self.wgt_form.cmb_asset_type.currentText()
        if str_asset_type == "직접 입력":
            str_asset_type = self.wgt_form.let_asset_type.text().strip()
            
        list_categories = self.list_current_category_path.copy()
        
        return {
            "asset_type": str_asset_type,
            "categories": list_categories
        }
