# Features/RegisterWindow/register_controller.py
import os
import json
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox
from Features.RegisterWindow.register_window import RegisterWindow
from Core.Models.asset_factory import AssetFactory
from Core.id_manager import IDManager
from Features.RegisterWindow.make_data_controller import MakeDataController # 💡 수입

class RegisterController(QObject):
    # 등록 성공 시 UI 갱신을 위해 사장님(MainController)에게 보낼 신호
    sig_asset_registered = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager, _obj_category_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        self.obj_category_manager = _obj_category_manager
        
        self.dialog_register = None
        self.ctrl_make_data = None # 💡 하위 컨트롤러
        self.initConnections()

    def initConnections(self):
        # 1. 메인 화면의 TopBar Register 버튼 연결
        obj_top_bar = self.wgt_main.wgt_top_bar
        obj_top_bar.btn_register.clicked.connect(self.handleOpenRegisterWindow)

    def handleOpenRegisterWindow(self):
        if self.dialog_register is None:
            self.dialog_register = RegisterWindow(self.wgt_main)
            # 2. RegisterWindow 내부의 Load Data 버튼 연결
            self.dialog_register.btn_load_data.clicked.connect(self.handleLoadData)
            
            # 💡 [추가] Make ID 버튼에 기능 연결!
            self.dialog_register.btn_make_id.clicked.connect(self.handleMakeId)
            
            # 💡 [신규 연결] Asset Name을 칠 때마다 즉각 폴더명을 갱신합니다!
            self.dialog_register.let_asset_name.textChanged.connect(self.handleAssetNameChanged)
            
            # 💡 [추가] Make Data 하위 컨트롤러 생성 및 연결!
            self.ctrl_make_data = MakeDataController(
                self.dialog_register.wgt_make_data_form, 
                self.obj_asset_manager, 
                self.obj_category_manager
            )
            
            # 💡 [추가] 최종 Make Data (저장) 버튼 연결
            self.dialog_register.btn_make_data.clicked.connect(self.handleMakeDataProcess)
            
        self.dialog_register.exec()

    def handleMakeId(self):
        # 1. 창고에서 기존 ID 목록 모두 가져오기
        list_all_assets = self.obj_asset_manager.getAllAssets()
        list_existing_ids = [asset.str_id for asset in list_all_assets]
        
        # 2. IDManager에게 절대 안 겹치는 ID 1개 발급 요청
        str_new_id = IDManager.generate_unique_ids(list_existing_ids)
        
        # 3. 텍스트 창에 예쁘게 표시!
        self.dialog_register.let_id.setText(str_new_id)
        
        # 4. 💡 Make ID 버튼을 눌렀을 때 비로소 폼의 콤보박스 데이터들을 최신으로 갱신합니다!
        if self.ctrl_make_data:
            self.ctrl_make_data.refreshUIState()
            str_asset_name = self.dialog_register.let_asset_name.text().strip()
            self.ctrl_make_data.wgt_form.setPreviewNames(str_new_id, str_asset_name)

    def handleAssetNameChanged(self, str_text):
        if not self.ctrl_make_data: return
        str_id = self.dialog_register.let_id.text().strip()
        if str_id:
            self.ctrl_make_data.wgt_form.setPreviewNames(str_id, str_text.strip())

    def handleMakeDataProcess(self):
        """Make Data 버튼 클릭 시 JSON 파일로 저장합니다."""
        if not self.ctrl_make_data: return
        
        # 💡 ID는 RegisterWindow 소속이므로 직접 가져옵니다.
        str_id = self.dialog_register.let_id.text().strip()
        
        if not str_id:
            QMessageBox.warning(self.dialog_register, "경고", "먼저 Make ID 버튼을 눌러 고유 ID를 발급받으세요.")
            return

        # 💡 새로 추가된 Asset Name 가져오기
        str_asset_name = self.dialog_register.let_asset_name.text().strip()
        if not str_asset_name:
            QMessageBox.warning(self.dialog_register, "경고", "Asset Name을 입력하세요.")
            return
            
        # 나머지 폼 데이터 가져오기
        dict_data = self.ctrl_make_data.getFormData()
        
        # 1. 저장할 폴더 선택 (Windows 탐색기)
        str_folder_path = QFileDialog.getExistingDirectory(self.dialog_register, "JSON 파일을 저장할 에셋 폴더를 선택하세요")
        if not str_folder_path:
            return
            
        # 2. AssetFactory 규격에 맞게 JSON 중첩 딕셔너리 조립
        str_raw_type = dict_data.get("asset_type", "")
        str_asset_type = str_raw_type.capitalize() if str_raw_type else ""
        
        list_raw_categories = dict_data.get("categories", [])
        list_categories = [cat.capitalize() if cat else cat for cat in list_raw_categories]
        
        # 💡 [핵심 수정] Asset Type을 카테고리에 억지로 끼워넣지 않고, 순수하게 추가한 태그들만 사용합니다!
        list_full_path = list_categories
        
        # 역순으로 순회하며 중첩 딕셔너리로 만듦 (예: {"nature": {"tree": {}}})
        dict_asset_categories = {}
        for str_cat in reversed(list_full_path):
            dict_asset_categories = {str_cat: dict_asset_categories}
            
        dict_save_data = {
            "semanticTags": {
                "name": str_asset_name,
                "asset_type": str_asset_type
            },
            "assetCategories": dict_asset_categories
        }
        
        # 3. JSON 파일 저장
        str_file_path = os.path.join(str_folder_path, f"{str_id}.json")
        try:
            with open(str_file_path, 'w', encoding='utf-8') as f:
                json.dump(dict_save_data, f, indent=4)
                
            QMessageBox.information(self.dialog_register, "저장 완료", f"에셋 데이터가 성공적으로 생성되었습니다!\n\n경로: {str_file_path}")
            
        except Exception as e:
            QMessageBox.critical(self.dialog_register, "저장 오류", f"파일을 저장하는 중 오류가 발생했습니다.\n\n{e}")

    def handleLoadData(self):
        # 1. 파일 선택기 열기 (이미지 및 JSON)
        str_file_path, _ = QFileDialog.getOpenFileName(
            self.dialog_register, 
            "Load Asset Data", 
            "", 
            "Asset Files (*.png *.jpg *.jpeg *.json);;Images (*.png *.jpg *.jpeg);;JSON (*.json)"
        )
        if not str_file_path: return

        str_filename = os.path.basename(str_file_path)
        str_pure_name, str_ext = os.path.splitext(str_filename)
        str_ext = str_ext.lower()

        # 2. 중복 검사 (경우의 수 1~4번 방어: 겹치는 ID가 있으면 튕겨냄)
        list_all_assets = self.obj_asset_manager.getAllAssets()
        for asset in list_all_assets:
            if asset.str_id == str_pure_name:
                QMessageBox.warning(self.dialog_register, "중복 오류", f"'{str_pure_name}' 에셋은 이미 창고에 존재합니다!")
                return

        # 3. 공장을 통해 파일 분석 후 MetaData 생성 (경우의 수 5번)
        obj_new_metadata = None
        if str_ext == '.json':
            obj_new_metadata = AssetFactory.create_from_json(str_file_path)
            if obj_new_metadata is None:
                QMessageBox.critical(self.dialog_register, "파싱 오류", "올바르지 않은 JSON이거나 프리뷰 썸네일 파일이 없습니다.")
                return
        else:
            obj_new_metadata = AssetFactory.create_from_image(str_file_path)

        # 4. 창고에 성공적으로 적재
        self.obj_asset_manager.addAssets([obj_new_metadata])
        
        # 5. 사장님(MainController)에게 UI 갱신 요청
        self.sig_asset_registered.emit()
        
        QMessageBox.information(self.dialog_register, "등록 완료", "에셋이 성공적으로 등록되었습니다!")
