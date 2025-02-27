import datetime
import json
from dotenv import load_dotenv
from urllib.parse import quote
import os

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables (if any)
load_dotenv()

class DouzoneCrawler:
    """웹 크롤링 및 검색 결과 처리를 위한 라이브러리 클래스"""
    
    def __init__(self, max_results=5, headless=True):
        """
        Douzone_crawl 초기화
        
        Args:
            max_results (int): 검색 결과 최대 개수 (기본값: 5)
            headless (bool): 헤드리스 모드 사용 여부 (기본값: True)
        """
        self.max_results = max_results
        self.headless = headless
    
    def setup_chrome_options(self):
        """Chrome 브라우저 옵션을 설정하는 함수"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')  # 크롬 창이 보이지 않게
        
        chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화로 성능 향상
        chrome_options.add_argument('--disable-dev-shm-usage')  # 메모리 사용 최적화
        chrome_options.add_argument('--disable-gpu')  # GPU 가속 비활성화
        chrome_options.add_argument('--window-size=1920x1080')  # 가상 브라우저 창 크기 설정
        chrome_options.add_argument("--disable-notifications")  # 알림 비활성화
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 제어 기능 비활성화
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 관련 스위치 비활성화
        chrome_options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 비활성화
        # 봇 감지 방지를 위한 User-Agent 설정
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        return chrome_options
    
    def find_search_items(self, driver):
        """여러 CSS 선택자를 시도하여 검색 결과 항목을 찾는 함수"""
        selectors = ["div.g", "div[data-hveid]", "div.MjjYud"]
        
        for selector in selectors:
            items = driver.find_elements(By.CSS_SELECTOR, selector)
            if items:
                return items
        
        return []
    
    def find_element_with_selectors(self, parent, selectors):
        """여러 CSS 선택자를 시도하여 요소를 찾는 함수"""
        for selector in selectors:
            elements = parent.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                return elements[0]
        return None
    
    def extract_date_info(self, item):
        """검색 결과에서 날짜 정보를 추출하는 함수"""
        # 기본값은 현재 날짜
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try:
            date_selectors = ["span.MUxGbd.wuQ4Ob.WZ8Tjf", "span.r0bn4c", "div.fG8Fp.uo4vr"]
            date_element = self.find_element_with_selectors(item, date_selectors)
            
            if date_element:
                date_text = date_element.text.strip()
                if date_text:
                    date = date_text
        except:
            pass  # 날짜 정보를 찾지 못하면 기본값 사용
        
        return date
    
    def extract_description(self, item):
        """검색 결과에서 설명 정보를 추출하는 함수"""
        description = "설명 없음"
        
        try:
            desc_selectors = ["div.VwiC3b", "span.aCOpRe", "div[data-content]"]
            desc_element = self.find_element_with_selectors(item, desc_selectors)
            
            if desc_element:
                desc_text = desc_element.text.strip()
                if desc_text:
                    description = desc_text
        except:
            pass
        
        return description
    
    def extract_text_with_selectors(self, driver, selectors):
        """여러 선택자를 시도하여 텍스트를 추출하는 함수"""
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            content = ""
            
            for element in elements:
                text = element.text.strip()
                if text:
                    content += text + "\n\n"
            
            if content:
                return content
        
        return ""
    
    def get_search_results(self, search_query):
        """
        Google 검색을 통해 전체 검색 결과의 제목과 링크를 수집하는 함수
        
        Args:
            search_query (str): 검색어
            
        Returns:
            list: (제목, 링크, 날짜, 설명) 튜플의 리스트
        """
        chrome_options = self.setup_chrome_options()
        
        # 검색 URL 설정
        encoded_query = quote(search_query)
        url = f"https://www.google.com/search?q={encoded_query}&num={self.max_results}"
        
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        
        try:
            driver.get(url)
            driver.implicitly_wait(10)
            
            # 검색 결과 컨테이너 대기
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
            )
            
            # 여러 가능한 CSS 선택자로 검색 결과 찾기
            search_items = self.find_search_items(driver)
            
            title_link_list = []
            
            for item in search_items:
                try:
                    # 제목 추출
                    title_element = self.find_element_with_selectors(item, ["h3", "h3.LC20lb", "div.vvjwJb"])
                    if not title_element:
                        continue
                    
                    title = title_element.text.strip()
                    if not title:
                        continue
                    
                    # 링크 추출
                    link_element = self.find_element_with_selectors(item, ["a", "a[href]", "div.yuRUbf a"])
                    if not link_element or not link_element.get_attribute("href"):
                        continue
                        
                    link = link_element.get_attribute("href")
                    
                    # Google 내부 링크 제외
                    if "google.com/search" in link:
                        continue
                    
                    # 중복 링크 제외
                    if any(link == existing[1] for existing in title_link_list):
                        continue
                    
                    # 날짜/시간 정보 추출
                    date = self.extract_date_info(item)
                    
                    # 설명 정보 추출
                    description = self.extract_description(item)
                    
                    # 결과 추가
                    title_link_list.append((title, link, date, description))
                    
                except Exception as e:
                    # print(f"항목 추출 오류: {str(e)}")
                    continue
            
            print(f"총 {len(title_link_list)}개의 검색 결과를 찾았습니다.")
            return title_link_list[:self.max_results]
            
        except Exception as e:
            print(f"검색 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
            
        finally:
            driver.quit()
    
    def extract_page_content(self, url):
        """
        주어진 URL에서 웹 페이지의 주요 콘텐츠를 추출하는 함수
        
        Args:
            url (str): 웹 페이지 URL
            
        Returns:
            str: 추출된 페이지 내용
        """
        chrome_options = self.setup_chrome_options()
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        
        try:
            driver.get(url)
            driver.implicitly_wait(3)  # 페이지 로드 대기

            # 페이지 제목 가져오기
            title = driver.title.strip()
            page_text = [f"{title}"]

            # 주요 콘텐츠를 추출
            content_selectors = [
                "article", "main", "div.content", "div.main-content", "div.entry-content",
                "div.post-content", "div.article-content", "div.page-content",
                "div#articletxt", "div.article-body", "div.story-news", 
                "div.article-view-content-div", "div.art_body", "div.article_txt",
                "div.article_content", "div.article_body", "div.articleView",
                "div.news-contents", "div.content", "div.detail_editor", 
                "div.article_con", "div.articleBody", "div.article-text",
                "div.entry", "section.content", "div#content", "div.container"
            ]

            extracted_text = self.extract_text_with_selectors(driver, content_selectors)

            # 주요 콘텐츠를 찾지 못한 경우 body 태그에서 전체 텍스트 가져오기
            if not extracted_text:
                body = driver.find_element(By.TAG_NAME, "body").text.strip()
                extracted_text = body

            page_text.append(extracted_text)

        except Exception as e:
            print(f"페이지 내용을 가져오는 중 오류 발생: {str(e)}")
            page_text.append("페이지 내용을 가져오는 중 오류가 발생했습니다.")
        
        finally:
            driver.quit()

        return "\n".join(page_text)
    
    def crawl(self, search_query, verbose=True):
        """
        검색어를 기반으로 검색 결과를 수집하고 JSON 형식으로 반환하는 함수
        
        Args:
            search_query (str): 검색어
            verbose (bool): 진행 상황 출력 여부
            
        Returns:
            list: [{"url": url, "content": content}, ...] 형식의 결과 리스트
        """
        if verbose:
            print(f"[{search_query}] 검색을 진행합니다.")
            
        # 검색 결과 가져오기
        results = self.get_search_results(search_query)
        
        if not results:
            if verbose:
                print(f"'{search_query}' 관련 결과를 찾을 수 없습니다.")
            return []
        
        # JSON 형식 결과 생성
        json_results = []

        # 각 결과에 대해 처리
        for i, (title, link, date, description) in enumerate(results, 1):
            if verbose:
                print(f"[{i}/{len(results)}] '{title}' 페이지 내용을 가져오는 중...")
            content = self.extract_page_content(link)
            
            # JSON 객체 생성
            result_obj = {
                "url": link,
                "date": date,
                "description": description,
                "content": content
            }
            
            json_results.append(result_obj)
        
        return json_results
    
    def save_to_json(self, results, filename=None, search_query=None):
        """
        검색 결과를 JSON 파일로 저장하는 함수
        
        Args:
            results (list): 저장할 결과 리스트
            filename (str, optional): 저장할 파일 이름
            search_query (str, optional): 검색 쿼리 (파일명 생성에 사용)
            
        Returns:
            str: 저장된 파일 경로
        """
        if filename is None:
            if search_query is None:
                search_query = "search"
            filename = f"crawl_{search_query}_{datetime.datetime.now().strftime('%Y-%m-%d')}.json"
        
        # 결과 저장
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        print(f"검색 결과가 '{filename}' 파일로 저장되었습니다.")
        
        return os.path.abspath(filename)


# 라이브러리를 직접 실행할 경우의 예제 코드
# def main():
#     import sys
    
#     # 명령행 인수가 제공되면 사용하고, 그렇지 않으면 기본값 사용
#     search_term = sys.argv[1] if len(sys.argv) > 1 else '더존비즈온'
    
#     # 크롤러 인스턴스 생성
#     crawler = Douzone_crawl(max_results=2)
    
#     # 검색 및 크롤링 실행
#     results = crawler.crawl(search_term)
    
#     # 결과 저장
#     crawler.save_to_json(results, search_query=search_term)
    
#     print("=" * 100)

# if __name__ == "__main__":
#     main()