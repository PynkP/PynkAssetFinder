# Features/Modify/modify_controller.py

import os
import json
import shutil
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from Features.Modify.modify_window import ModifyWindow
from Features.Register.make_data_controller import MakeDataController

class ModifyController(QObject):
    """
    Modify Asset 기능 전담 컨트롤러입니다.
    우클릭 메뉴 → ModifyWindow 오픈 → 데이터 수정 → JSON 덮어쓰기 + AssetManager 갱신을 담당합니다.
    카테고리 콤보박스 동적 로직은 MakeDataController를 재사용합니다. (결합도 최소화)
    """
    sig_asset_modified = Signal()  # 수정 완료 시 AppController에게 UI 갱신 요청

    def __init__(self, _wgt_main, _obj_asset_manager, _obj_category_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        self.obj_category_manager = _obj_category_manager

        self.dialog_modify = None
        self.ctrl_make_data = None
        # 현재 수정 중인 에셋의 ID와 원본 MetaData를 기억합니다
        self.str_current_id = ""
        self.obj_current_asset = None

    def handleOpenModifyWindow(self, _str_id):
        """우클릭 메뉴에서 Modify Asset을 눌렀을 때 호출됩니다."""

        # 1. 창고에서 해당 에셋의 MetaData 조회
        self.obj_current_asset = None
        for asset in self.obj_asset_manager.getAllAssets():
            if asset.str_id == _str_id:
                self.obj_current_asset = asset
                break

        if self.obj_current_asset is None:
            QMessageBox.warning(self.wgt_main, "오류", f"ID '{_str_id}' 에 해당하는 에셋을 찾을 수 없습니다.")
            return

        self.str_current_id = _str_id

        # 2. 매번 새 창으로 열기 (항상 최신 데이터 반영)
        self.dialog_modify = ModifyWindow(self.wgt_main)

        # 3. MakeDataController를 폼에 연결 (카테고리 콤보박스 로직 재사용)
        self.ctrl_make_data = MakeDataController(
            self.dialog_modify.wgt_make_data_form,
            self.obj_asset_manager,
            self.obj_category_manager
        )

        # 4. 기존 데이터를 폼에 채워넣기
        self._loadAssetDataIntoForm()

        # 5. Modify Data 버튼 연결
        self.dialog_modify.btn_modify_data.clicked.connect(self.handleModifyDataProcess)

        # 6. 💡 에셋 이름 변경 시 실시간으로 추천 폴더명 갱신
        self.dialog_modify.wgt_make_data_form.let_asset_name.textChanged.connect(self._onAssetNameChanged)

        self.dialog_modify.exec()

    def _loadAssetDataIntoForm(self):
        """
        현재 수정 대상 에셋의 기존 데이터를 ModifyWindow의 폼에 채웁니다.
        Asset Type 콤보박스 선택 동기화, 카테고리 태그 복원을 포함합니다.
        """
        asset = self.obj_current_asset
        form = self.dialog_modify.wgt_make_data_form

        # 1. 콤보박스(타입/카테고리)에 최신 목록 채우기
        self.ctrl_make_data.refreshUIState()

        # 2. 이름, 타입, 썸네일 폼에 로드
        form.loadExistingData(
            _str_asset_name=asset.str_asset_name,
            _str_asset_type=asset.str_asset_type,
            _str_thumbnail_path=asset.str_path_preview,
            _list_categories=asset.list_categories
        )

        # 3. 기존 카테고리 태그들을 폼에 복원하고 MakeDataController 내부 상태도 동기화
        self.ctrl_make_data.list_current_category_path = asset.list_categories.copy()
        for str_cat in asset.list_categories:
            form.addCategoryTag(str_cat)

        # 4. Asset Type 콤보박스 선택 동기화
        #    기존 타입이 목록에 있으면 선택, 없으면 직접 입력 모드로 전환
        int_idx = form.cmb_asset_type.findText(asset.str_asset_type)
        if int_idx >= 0:
            form.cmb_asset_type.blockSignals(True)
            form.cmb_asset_type.setCurrentIndex(int_idx)
            form.cmb_asset_type.blockSignals(False)
            form.let_asset_type.setEnabled(False)
        else:
            # 직접 입력 모드로 전환
            form.cmb_asset_type.blockSignals(True)
            form.cmb_asset_type.setCurrentIndex(0)  # "직접 입력"
            form.cmb_asset_type.blockSignals(False)
            form.let_asset_type.setEnabled(True)
            form.let_asset_type.setText(asset.str_asset_type)

        # 5. 💡 ID는 이미 발급된 상태이므로 프리뷰 파일명과 추천 폴더명을 즉시 채웁니다
        form.setPreviewNames(self.str_current_id, asset.str_asset_name)

    def _onAssetNameChanged(self, _str_text):
        """에셋 이름이 바뀔 때마다 추천 폴더명을 실시간으로 갱신합니다."""
        form = self.dialog_modify.wgt_make_data_form
        form.setPreviewNames(self.str_current_id, _str_text.strip())

    def handleModifyDataProcess(self):
        """
        Modify Data 버튼 클릭 시 실행됩니다.
        1. 폼 데이터 수집
        2. JSON 파일 덮어쓰기
        3. 썸네일이 교체됐으면 파일 복사
        4. AssetManager 인메모리 갱신
        5. sig_asset_modified 신호 발생 → AppController가 UI 전체 갱신
        """
        if not self.ctrl_make_data or not self.obj_current_asset:
            return

        form = self.dialog_modify.wgt_make_data_form

        # ── 입력값 수집 ──
        str_new_name = form.let_asset_name.text().strip()
        if not str_new_name:
            QMessageBox.warning(self.dialog_modify, "경고", "Asset Name을 입력하세요.")
            return

        dict_form_data = self.ctrl_make_data.getFormData()
        str_raw_type = dict_form_data.get("asset_type", "")
        str_new_type = str_raw_type.capitalize() if str_raw_type else ""

        list_raw_categories = dict_form_data.get("categories", [])
        list_new_categories = [cat.capitalize() if cat else cat for cat in list_raw_categories]

        str_new_thumbnail_path = dict_form_data.get("thumbnail_path", "")

        # ── JSON 파일 경로 찾기 ──
        str_original_preview = self.obj_current_asset.str_path_preview
        str_asset_folder = os.path.dirname(str_original_preview)
        str_json_path = os.path.join(str_asset_folder, f"{self.str_current_id}.json")

        if not os.path.exists(str_json_path):
            QMessageBox.critical(self.dialog_modify, "오류", f"JSON 파일을 찾을 수 없습니다.\n경로: {str_json_path}")
            return

        # ── assetCategories 중첩 딕셔너리 재조립 ──
        dict_asset_categories = {}
        for str_cat in reversed(list_new_categories):
            dict_asset_categories = {str_cat: dict_asset_categories}

        dict_save_data = {
            "id": self.str_current_id,
            "semanticTags": {
                "name": str_new_name,
                "asset_type": str_new_type
            },
            "assetCategories": dict_asset_categories
        }

        try:
            # ── JSON 덮어쓰기 ──
            with open(str_json_path, 'w', encoding='utf-8') as f:
                json.dump(dict_save_data, f, indent=4)

            # ── 썸네일이 새 이미지로 교체됐으면 파일 복사 ──
            str_updated_preview_path = str_original_preview  # 기본값은 기존 경로 유지
            if str_new_thumbnail_path and str_new_thumbnail_path != str_original_preview:
                _, str_ext = os.path.splitext(str_new_thumbnail_path)
                str_target_thumb = os.path.join(str_asset_folder, f"{self.str_current_id}_Preview{str_ext}")
                shutil.copy2(str_new_thumbnail_path, str_target_thumb)
                str_updated_preview_path = str_target_thumb

            # ── AssetManager 인메모리 갱신 ──
            self.obj_asset_manager.updateAsset(
                self.str_current_id,
                _str_new_name=str_new_name,
                _str_new_type=str_new_type,
                _list_new_categories=list_new_categories,
                _str_new_preview_path=str_updated_preview_path
            )

            QMessageBox.information(self.dialog_modify, "수정 완료", "에셋 데이터가 성공적으로 수정되었습니다!")

            # ── AppController에게 UI 갱신 요청 ──
            self.sig_asset_modified.emit()
            self.dialog_modify.accept()

        except Exception as e:
            QMessageBox.critical(self.dialog_modify, "오류", f"수정 중 오류가 발생했습니다.\n\n{e}")
