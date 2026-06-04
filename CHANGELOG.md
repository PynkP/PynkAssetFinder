# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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