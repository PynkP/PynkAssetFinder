# Features/RegisterWindow/register_controller.py
import os
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox
from Features.RegisterWindow.register_window import RegisterWindow
from Core.Models.asset_factory import AssetFactory

class RegisterController(QObject):
    # 등록 성공 시 UI 갱신을 위해 사장님(MainController)에게 보낼 신호
    sig_asset_registered = Signal()

    def __init__(self, _wgt_main, _obj_asset_manager):
        super().__init__()
        self.wgt_main = _wgt_main
        self.obj_asset_manager = _obj_asset_manager
        
        self.dialog_register = None
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
            
        self.dialog_register.exec()

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
