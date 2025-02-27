import argparse
import sys
from .crawl import DouzoneCrawler

def main():
    parser = argparse.ArgumentParser(description="더존 크롤러: 웹 검색 및 크롤링 도구")
    parser.add_argument("search_term", nargs="?", default="더존비즈온", help="검색어")
    parser.add_argument("--max-results", type=int, default=5, help="최대 검색 결과 수 (기본값: 5)")
    parser.add_argument("--headless", action="store_true", default=True, help="헤드리스 모드 사용 (기본값: True)")
    parser.add_argument("--output", help="결과를 저장할 JSON 파일 이름")
    
    args = parser.parse_args()
    
    # 크롤러 인스턴스 생성
    crawler = DouzoneCrawler(max_results=args.max_results, headless=args.headless)
    
    # 검색 및 크롤링 실행
    results = crawler.crawl(args.search_term)
    
    # 결과 저장
    crawler.save_to_json(results, filename=args.output, search_query=args.search_term)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())