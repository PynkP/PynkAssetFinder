# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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