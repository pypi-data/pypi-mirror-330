import datetime
import json
import time
from dotenv import load_dotenv
from urllib.parse import quote
import concurrent.futures
import os

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 환경 변수 로드
load_dotenv()

class DouzoneCrawler:
    """웹 크롤링 및 검색 결과 처리를 위한 라이브러리 클래스"""
    
    def __init__(self, max_results=5, timeout=10, use_threading=True, thread_workers=3):
        """
        Douzone_crawl 초기화
        
        Args:
            max_results (int): 검색 결과 최대 개수 (기본값: 5)
            timeout (int): 요소 대기 시간(초) (기본값: 10)
            use_threading (bool): 멀티스레딩 사용 여부 (기본값: True)
            thread_workers (int): 동시 실행할 스레드 수 (기본값: 3)
        """
        self.max_results = max_results
        self.timeout = timeout
        self.use_threading = use_threading
        self.thread_workers = thread_workers
        self._driver_cache = None # 드라이버 캐시 - 생성 시간 및 비용 절약
    
    def setup_chrome_options(self):
        """Chrome 브라우저 옵션을 설정하는 함수"""
        chrome_options = Options()
        
        chrome_options.add_argument('--headless=new')  # 크롬 창이 보이지 않게
        chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화로 성능 향상
        chrome_options.add_argument('--disable-dev-shm-usage')  # 메모리 사용 최적화
        chrome_options.add_argument('--disable-gpu')  # GPU 가속 비활성화
        chrome_options.add_argument('--window-size=1920x1080')  # 가상 브라우저 창 크기 설정
        chrome_options.add_argument("--disable-notifications")  # 알림 비활성화
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 제어 기능 비활성화
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 관련 스위치 비활성화
        chrome_options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 비활성화
        chrome_options.add_argument('--blink-settings=imagesEnabled=false') # 이미지 로딩 비활성화
        chrome_options.add_argument('--disable-extensions') # 페이지 로딩 최적화
        chrome_options.add_argument('--disable-default-apps') # 페이지 로딩 최적화
        chrome_options.add_argument('--js-flags=--expose-gc') # 메모리 사용 최적화
        chrome_options.add_argument('--enable-precise-memory-info') # 메모리 사용 최적화
        chrome_options.add_argument('--disable-popup-blocking') # 메모리 사용 최적화
        chrome_options.add_argument('--disable-hang-monitor') # 메모리 사용 최적화
        chrome_options.add_argument('--disable-application-cache') # 캐시 비활성화로 메모리 사용 감소
        chrome_options.add_argument('--disable-cache') # 캐시 비활성화로 메모리 사용 감소
        chrome_options.add_argument('--disable-offline-load-stale-cache') # 캐시 비활성화로 메모리 사용 감소
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36") # 봇 감지 방지를 위한 User-Agent 설정
        
        return chrome_options
    
    def get_driver(self):
        """Selenium 웹드라이버를 생성하거나 캐시된 드라이버를 반환하는 함수"""
        if self._driver_cache is None:
            chrome_options = self.setup_chrome_options()
            self._driver_cache = webdriver.Chrome(service=Service(), options=chrome_options)
        return self._driver_cache
    
    def close_driver(self):
        """캐시된 드라이버를 닫는 함수"""
        if self._driver_cache:
            try:
                self._driver_cache.quit()
            except:
                pass
            self._driver_cache = None
    
    def find_search_items(self, driver):
        """여러 CSS 선택자를 시도하여 검색 결과 항목을 찾는 함수"""
        selectors = ["div.g", "div[data-hveid]", "div.MjjYud"]
        
        for selector in selectors:
            try:
                items = driver.find_elements(By.CSS_SELECTOR, selector)
                if items:
                    return items
            except:
                continue
        
        return []
    
    def find_element_with_selectors(self, parent, selectors):
        """여러 CSS 선택자를 시도하여 요소를 찾는 함수"""
        for selector in selectors:
            try:
                elements = parent.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return elements[0]
            except:
                continue
        return None
    
    def extract_date_info(self, item):
        """검색 결과에서 날짜 정보를 추출하는 함수"""
        date = datetime.datetime.now().strftime('%Y-%m-%d') # 기본값은 현재 날짜
        
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
            driver.implicitly_wait(1)
            
            # 페이지 로드 대기 시간 최적화
            try:
                # 명시적 대기로 변경하여 성능 향상
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g, div[data-hveid], div.MjjYud")))
            except:
                # 시간 초과 시 계속 진행
                pass
            
            # 여러 가능한 CSS 선택자로 검색 결과 찾기
            search_items = self.find_search_items(driver)
            
            title_link_list = []
            unique_links = set()  # 중복 링크 체크를 위한 세트
            
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
                    if not link:
                        continue
                    
                    # Google 내부 링크 제외
                    if "google.com/search" in link:
                        continue
                    
                    # 중복 링크 제외 - O(1) 확인으로 성능 향상
                    if link in unique_links:
                        continue

                    unique_links.add(link)
                    
                    # 날짜/시간 정보 추출
                    date = self.extract_date_info(item)
                    
                    # 설명 정보 추출
                    description = self.extract_description(item)
                    
                    # 결과 추가
                    title_link_list.append((title, link, date, description))

                    # 충분한 결과를 얻으면 중단
                    if len(title_link_list) >= self.max_results:
                        break
                    
                except Exception:
                    continue
            
            print(f"총 {len(title_link_list)}개의 검색 결과를 찾았습니다.")
            return title_link_list[:self.max_results]
            
        except Exception as e:
            print(f"검색 중 오류 발생: {str(e)}")
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
        # 병렬 처리를 위한 새 드라이버 생성
        chrome_options = self.setup_chrome_options()
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        page_text = ["페이지 로드 시간 초과로 페이지 내용을 가져오는 데 실패했습니다."] # 기본값
        
        try:
            # 페이지 로드 제한 시간 설정
            driver.set_page_load_timeout(60)
            driver.get(url)
            # driver.implicitly_wait(2)  # 페이지 로드 대기

            # 페이지 제목 가져오기
            title = driver.title.strip()
            page_text = [f"{title}"]

            # 빠른 내용 추출을 위한 성능 최적화된 선택자 목록
            high_priority_selectors = [
                "article", "main", "div.content", "div.main-content", 
                "div.entry-content", "div.article-content", "div#content"
            ]
            # 우선순위가 높은 선택자로 먼저 시도
            content = self.extract_text_with_selectors(driver, high_priority_selectors)
            
            # 찾지 못한 경우 확장된 선택자 목록 사용
            if not content:
                extended_selectors = [
                    "div.post-content", "div.page-content",
                    "div#articletxt", "div.article-body", "div.story-news", 
                    "div.article-view-content-div", "div.art_body", "div.article_txt",
                    "div.article_content", "div.article_body", "div.articleView",
                    "div.news-contents", "div.detail_editor", 
                    "div.article_con", "div.articleBody", "div.article-text",
                    "div.entry", "section.content", "div.container"
                ]
                content = self.extract_text_with_selectors(driver, extended_selectors)

            # 여전히 찾지 못한 경우 body 태그의 일부만 가져오기
            if not content:
                try:
                    body = driver.find_element(By.TAG_NAME, "body")
                    content = body.text[:50000]  # 최대 50k 문자로 제한
                except:
                    content = "페이지 내용을 가져오는 데 실패했습니다."

            page_text.append(content)

        # 멀티스레딩 환경이기 때문에 하위 함수의 오류가 상위로 전파되지 않도록 처리
        except Exception as e: 
            print(f"페이지 내용을 가져오는 중 오류 발생: {str(e)}")
            if len(page_text) == 1 and page_text[0].startswith("페이지 내용을 가져오는 데 실패"):
                # 이미 기본 오류 메시지가 있는 경우
                pass
            else:
                # 오류 메시지 추가
                page_text.append("페이지 내용을 가져오는 중 오류가 발생했습니다.")
            
        finally:
            driver.quit()

        return "\n".join(page_text)
    
    def process_single_result(self, item, search_query, i, total, verbose=True):
        """
        단일 검색 결과를 처리하는 함수 (스레드에서 호출됨)
        
        Args:
            item (tuple): (제목, 링크, 날짜, 설명) 튜플
            search_query (str): 검색어
            i (int): 현재 인덱스
            total (int): 총 결과 수
            verbose (bool): 진행 상황 출력 여부
            
        Returns:
            dict: 처리된 결과 객체
        """
        title, link, date, description = item
        
        if verbose:
            print(f"[{i}/{total}] '{title}' 페이지 내용을 가져오는 중...")
        
        content = self.extract_page_content(link)
        
        # JSON 객체 생성
        return {
            "query": search_query,
            "title": title,
            "url": link,
            "date": date,
            "description": description,
            "content": content
        }
    
    def crawl(self, search_query, verbose=True):
        """
        검색어를 기반으로 검색 결과를 수집하고 JSON 형식으로 반환하는 함수
        
        Args:
            search_query (str): 검색어
            verbose (bool): 진행 상황 출력 여부
            
        Returns:
            list: [{"url": url, "content": content}, ...] 형식의 결과 리스트
        """
        start_time = time.time()

        if verbose:
            print(f"[{search_query}] 검색을 진행합니다.")
            
        # 검색 결과 가져오기
        results = self.get_search_results(search_query)
        
        if not results:
            if verbose:
                print(f"'{search_query}' 관련 결과를 찾을 수 없습니다.")
            return []
        
        # 멀티스레딩 처리
        if self.use_threading and len(results) > 1:
            json_results = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(self.thread_workers, len(results))) as executor:
                # 각 결과에 대한 처리 작업 생성
                future_to_item = {
                    executor.submit(
                        self.process_single_result, 
                        item, search_query, i+1, len(results), verbose
                    ): i for i, item in enumerate(results)
                }
                
                # 완료된 작업 처리
                for future in concurrent.futures.as_completed(future_to_item):
                    try:
                        result = future.result()
                        json_results.append(result)
                    except Exception as e:
                        if verbose:
                            print(f"결과 처리 중 오류 발생: {str(e)}")
            
            # 원래 순서대로 정렬
            json_results.sort(key=lambda x: [i for i, item in enumerate(results) if item[1] == x["url"]][0])
            
        else:
            # 단일 스레드 처리
            json_results = []
            
            for i, item in enumerate(results, 1):
                try:
                    result = self.process_single_result(item, search_query, i, len(results), verbose)
                    json_results.append(result)
                except Exception as e:
                    if verbose:
                        print(f"결과 처리 중 오류 발생: {str(e)}")
        
        end_time = time.time()
        if verbose:
            print(f"크롤링 완료: {len(json_results)}개 결과, 소요 시간: {end_time - start_time:.2f}초")
        
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
        # 검색어가 None이면 결과의 첫 번째 항목에서 검색어 추출
        if search_query is None and results and 'query' in results[0]:
            search_query = results[0]['query']
        
        # 그래도 검색어가 없으면 기본값 사용
        if search_query is None:
            search_query = "search"

        if filename is None:
            safe_query = search_query.replace('/', '_').replace('\\', '_') # 파일명에 사용할 수 없는 문자 제거
            safe_query = ''.join(c for c in safe_query if c.isalnum() or c in '._- ')
            filename = f"{safe_query}_{datetime.datetime.now().strftime('%Y-%m-%d')}.json"
        
        # 결과 저장
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        print(f"검색 결과가 '{filename}' 파일로 저장되었습니다.")
        
        return os.path.abspath(filename)
    
    def __del__(self):
        """객체 소멸 시 드라이버 정리"""
        self.close_driver()