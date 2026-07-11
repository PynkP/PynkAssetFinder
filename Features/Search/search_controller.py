# Features/Search/search_controller.py

from PySide6.QtCore import QObject, Signal

class SearchController(QObject):
    """검색창 UI와 데이터를 연결하는 검색 전담 팀장입니다."""
    
    # 검색 완료 시 결과 리스트를 담아 앱 컨트롤러에 알리는 신호
    sig_search_completed = Signal(list)
    
    def __init__(self, _wgt_search_bar, _obj_asset_manager):
        super().__init__()
        self.wgt_search_bar = _wgt_search_bar
        self.obj_asset_manager = _obj_asset_manager
        
        self.initConnections()
        
    def initConnections(self):
        # 검색 버튼 클릭 또는 엔터키 입력 시 검색 실행
        self.wgt_search_bar.btn_search.clicked.connect(self.handleSearch)
        self.wgt_search_bar.input_search.returnPressed.connect(self.handleSearch)
        
    def handleSearch(self):
        str_keyword = self.wgt_search_bar.input_search.text().strip()
        print(f"🔍 [SearchController] 검색 요청 접수: '{str_keyword}'")
        
        # 창고장(AssetManager)에게 검색 지시
        list_result = self.obj_asset_manager.searchAssets(str_keyword)
        
        # 검색 완료 신호 발생 (이 신호를 AppController가 받아서 화면 갱신을 지시함)
        self.sig_search_completed.emit(list_result)
