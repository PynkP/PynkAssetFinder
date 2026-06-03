class CategoryManager:
    """왼쪽 카테고리 뷰에 표시될 폴더(분류)들의 정보를 전담해서 기억하는 관리소입니다."""
    
    # 싱글턴 객체를 저장할 클래스 변수
    _instance = None

    def __new__(cls):
        # 이미 생성된 객체가 없다면 새로 만들고, 있다면 기존 객체를 그대로 반환합니다.
        if cls._instance is None:
            cls._instance = super(CategoryManager, cls).__new__(cls)
            # 초기화 작업은 여기서 최초 1회만 실행됩니다.
            cls._instance.list_categories = []
        return cls._instance

    def addCategory(self, _str_name, _int_count):
        """새로 스캔된 폴더의 이름과 파일 갯수를 리스트에 추가합니다."""
        dict_category = {
            "name": _str_name,
            "count": _int_count
        }
        self.list_categories.append(dict_category)

    def getAllCategories(self):
        """저장된 모든 카테고리 목록을 반환합니다."""
        return self.list_categories

    def clearCategories(self):
        """저장된 카테고리 목록을 모두 지웁니다."""
        self.list_categories.clear()