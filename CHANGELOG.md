# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-07-19

### Added
- **즐겨찾기(Favorites) 기능 추가:** 자주 사용하는 에셋을 따로 관리하고 빠르게 접근할 수 있는 즐겨찾기 시스템 도입
- **에셋 데이터 수정(Edit) 기능 추가:** 기존에 등록된 에셋의 정보를 수정할 수 있는 기능 지원
- **즐겨찾기 메타 데이터 추가:** 즐겨찾기 상태를 저장 및 관리하기 위한 표준 메타 데이터 규약 항목 추가

### Changed
- **Register Data 사용자 편의성(UX) 개선:** 에셋 등록 시 썸네일 이미지를 드래그 앤 드롭(Drag & Drop)으로 간편하게 등록할 수 있도록 개선
- **즐겨찾기 기능 도입에 따른 UI/UX 개편:**
  - 좌측 사이드바(Left UI) 패널에 즐겨찾기 탭 및 필터링 레이아웃 적용
  - 썸네일 아이템에 즐겨찾기 여부를 표시하고 설정할 수 있는 UI 요소 추가

## [0.9.0] - 2026-07-11

### Added
- **단축키(Shortcuts) 기능 추가:** 작업 효율성을 높이기 위한 주요 기능 단축키 지원
- **썸네일 경로 탐색 예외 처리:** 썸네일 이미지 경로를 찾지 못할 경우, JSON 데이터를 참조하여 경로를 재탐색하는 폴백(Fallback) 예외 처리 로직 추가

### Changed
- **폴더 트리 구조 리팩토링:** 단일 책임 원칙(SRP, Single Responsibility Principle)에 기반하여 각 기능(Feature)별로 디렉토리 구조를 분류 및 재정리
- **썸네일 지원 포맷 및 UI 개선:**
  - 기존 PNG 형식만 허용되던 썸네일 로드 기능을 JPG 등 일반적인 이미지 포맷 전반을 지원하도록 유연성 개선
  - 썸네일 이미지 표시 위치 및 레이아웃 조정
- **Register Make Data 규격 수정:** 에셋 데이터 생성 시 고유 ID 항목도 함께 포함되어 처리되도록 로직 수정

📦 PynkAssetFinder
 ┣ 📜 main.py
 ┣ 📂 Core                         ← 전역 공용 인프라
 ┃ ┣ 📜 app_controller.py          ← (구: main_controller.py)
 ┃ ┣ 📂 Models
 ┃ ┃ ┣ 📜 metadata.py              ← 위치 유지 (공유 데이터 규약)
 ┃ ┃ ┗ 📜 asset_factory.py         ← 위치 유지 (공유 데이터 규약)
 ┃ ┣ 📂 Repositories
 ┃ ┃ ┗ 📜 asset_manager.py         ← (구: Core/asset_manager.py)
 ┃ ┣ 📂 FileSystem
 ┃ ┃ ┗ 📜 folder_scanner.py        ← (구: Core/folder_scanner.py)
 ┃ ┗ 📂 Utils
 ┃   ┗ 📜 id_manager.py            ← (구: Core/id_manager.py)
 ┣ 📂 Features
 ┃ ┣ 📂 AssetBrowse                ← (구: ThumbnailView + Core/Controllers/view_controller)
 ┃ ┃ ┣ 📜 view_controller.py
 ┃ ┃ ┣ 📜 asset_grid_view.py
 ┃ ┃ ┣ 📜 asset_context_menu.py
 ┃ ┃ ┣ 📜 thumbnail_loader.py
 ┃ ┃ ┣ 📜 thumbnail_widget.py
 ┃ ┃ ┗ 📜 main_panel.py
 ┃ ┣ 📂 Scan                       ← (구: Core/Controllers/scan_controller)
 ┃ ┃ ┗ 📜 scan_controller.py
 ┃ ┣ 📂 Cache                      ← (구: Core/Controllers/cache_controller)
 ┃ ┃ ┗ 📜 cache_controller.py
 ┃ ┣ 📂 Category                   ← (구: CategoryView + Core/category_manager)
 ┃ ┃ ┣ 📜 category_manager.py
 ┃ ┃ ┗ 📜 category_panel.py
 ┃ ┣ 📂 Search                     ← (구: SearchBar)
 ┃ ┃ ┣ 📜 search_bar.py
 ┃ ┃ ┗ 📜 search_controller.py
 ┃ ┣ 📂 Register                   ← (구: RegisterWindow)
 ┃ ┃ ┣ 📜 register_controller.py
 ┃ ┃ ┣ 📜 register_window.py
 ┃ ┃ ┣ 📜 make_data_controller.py
 ┃ ┃ ┣ 📜 make_data_form.py
 ┃ ┃ ┗ 📜 category_tag.py
 ┃ ┗ 📂 SharedUI                   ← (구: TopMenu + BottomBar + LogView)
 ┃   ┣ 📜 top_bar.py
 ┃   ┣ 📜 scan_button.py
 ┃   ┣ 📜 bottom_bar.py
 ┃   ┗ 📜 log_window.py
 ┗ 📂 Resources                    ← 변경 없음

## [0.8.0] - 2026-07-05

### Added
- **우클릭 컨텍스트 메뉴(Context Menu) 추가**
  - **파일 찾기:** 선택한 에셋의 실제 파일 경로를 탐색기로 열어주는 기능 구현
  - **리스트 삭제하기:** 목록에서 선택한 에셋을 제거하는 기능 구현

## [0.7.0] - 2026-07-05

### Added
- 기존 데이터에 이어서 스캔할 수 있는 '추가 스캔' 기능 제작 및 적용
- 하단바(Bottom Bar)에 작업 내역을 확인할 수 있는 '로그 페이지' 추가
- 하단바에 프로그램 사용 방법 및 설명을 확인할 수 있는 'URL 링크' 추가

### Changed
- 전반적인 UI 스타일 및 디자인 개선

## [0.6.0] - 2026-07-04

### Added
- 에셋 검색 기능 추가

### Changed
- 썸네일 이미지 로드 속도 최적화 및 개선
- 전반적인 UI 스타일 개선

## [0.5.0] - 2026-06-21

### Added
- **개인 커스텀 에셋 지원:** MegaScan 에셋뿐만 아니라 개인의 에셋 데이터도 JSON으로 저장할 수 있는 기능 및 전용 UI 추가
- 커스텀 에셋 등록 시 MegaScan과 호환되는 유사한 규격의 고유 ID 자동 생성 기능 구현
- 메타 데이터(MetaData) 규약에 '에셋 이름(Asset Name)' 항목 추가

### Changed
- **파싱 기준 변경:** 에셋 파싱 및 프리뷰 이미지 로드 기준을 Quixel Bridge 다운로드 폴더 구조에 맞게 전면 개편
- 썸네일 하단에 표시되는 텍스트 형식을 '에셋 이름 + ID'로 변경하고, 에셋 리스트가 기본적으로 오름차순 정렬되도록 로직 수정

### Fixed
- 카테고리 뎁스(Depth) 트리 처리 과정에서 이름 기준 오름차순 정렬이 정상적으로 적용되지 않던 버그 수정
## [0.4.0] - 2026-06-07

### Added
- 신규 에셋 등록을 위한 Register 창 및 테스트 UI 추가
- 개별 데이터를 불러올 수 있는 Load Data 기능 구현
- 에셋 생성 및 관리를 담당하는 `asset_factory.py` 및 Register 관련 모듈 추가

### Changed
- **AssetManager 로직 최적화:** 중복으로 관리되던 `list_assets` 변수를 제거하고, `getAllAssets()` 함수를 통해 데이터를 직접 전달하도록 구조 개선
- **카테고리 폴더 트리 구조 개편:** 최상단(Root) 노드를 추가하고, 2D, 3D, Brush의 하위 카테고리까지만 표시되도록 분류 트리(Depth) 간소화

## [0.3.0] - 2026-06-05

### Added
- 메타 데이터(MetaData) 구조 추가 및 표준 데이터 규약 통일
- 카테고리 패널 UI 추가 및 클릭 기반의 필터링 기능 구현
- JSON 파일의 "categories" 값을 기준으로 카테고리를 자동 생성하는 로직 추가
- 애플리케이션 아이콘(App Icon) 적용

### Changed
- JSON 데이터의 저장(Save) 및 불러오기(Load) 기준을 새로운 메타 데이터(MetaData) 규약으로 전면 통합 및 변경

## [0.2.0] - 2026-06-05

### Added
- **MegaScanAsset 기능 구현**
  - MegaScanAsset JSON 파일 스캔 및 데이터 파싱 기능 추가
  - 에셋 데이터의 저장(Save) 및 로드(Load) 시스템 구현

### Changed
- **컨트롤러 구조 리팩토링**
  - `MainController` 로직 간소화 및 구조 비대화 방지
  - 역할 분담을 위한 `SubController` 신규 생성 및 아키텍처 분리(Cache, Scan, View)
- **UI 스타일 관리 개선**
  - 코드 내 인라인 스타일을 전면 배제하고 `StyleSheet` 파일로 분리 독립