# Douzone-crawl

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-4.0+-green.svg)

🔍 빠르고 쉬운 웹 크롤링을 위한 파이썬 라이브러리입니다. Google 검색 결과와 웹 페이지 콘텐츠를 손쉽게 추출하세요.

## 주요 기능

- Google 검색 결과 수집
- 검색 결과 페이지 내용 추출
- 검색 결과의 제목, URL, 날짜, 설명 정보 제공
- 결과 파일 저장 기능

## 설치 방법

```bash
pip install douzone_crawl
```

## 사용 방법

### 기본 사용 예시

```python
import douzone_crawl

# 크롤러 생성
crawler = douzone_crawl.DouzoneCrawler(max_results=2)

# # 검색 실행
results = crawler.crawl("더존비즈온")

# # 결과 저장
crawler.save_to_json(results)
```

## 요구사항

- pip install requirements.txt


## 기여하기

- 버그 신고나 기능 제안은 이슈 트래커를 이용해 주세요. 풀 리퀘스트도 환영합니다!
