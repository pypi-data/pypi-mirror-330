# __init__.py

from .crawler import (
    setup_chrome_options,
    create_title_link_list,
    find_search_items,
    find_element_with_selectors,
    extract_date_info,
    extract_description,
    extract_page_content,
    extract_text_with_selectors,
    create_search_results,
    save_results
)

__version__ = '0.1.0'
__author__ = 'choheejin'
__email__ = 'hjcho1027@douzone.com'
__description__ = 'Google 검색 결과를 크롤링하여 웹 페이지 내용을 추출하는 라이브러리'

# 주요 기능 노출
__all__ = [
    'setup_chrome_options',
    'create_title_link_list',
    'extract_page_content',
    'create_search_results',
    'save_results',
    # 사용자가 직접 사용할 가능성이 있는 보조 함수들
    'find_search_items',
    'find_element_with_selectors',
    'extract_date_info',
    'extract_description',
    'extract_text_with_selectors'
]

# 기본 매개변수 설정
MAX_RESULTS = 5

# 편의 함수 - 모듈 이름으로 바로 호출할 수 있는 기능
def search(query, max_results=MAX_RESULTS):
    """
    Google 검색을 수행하고 결과를 반환하는 편의 함수
    
    Args:
        query (str): 검색어
        max_results (int, optional): 검색 결과 수. 기본값은 5.
        
    Returns:
        list: (제목, 링크, 날짜, 설명) 튜플의 리스트
    """
    return create_title_link_list(query, max_results)

def get_content(url):
    """
    주어진 URL에서 웹 페이지 내용을 추출하는 편의 함수
    
    Args:
        url (str): 웹 페이지 URL
        
    Returns:
        str: 추출된 웹 페이지 내용
    """
    return extract_page_content(url)

def search_and_extract(query, max_results=MAX_RESULTS, save_to_file=None):
    """
    검색을 수행하고 각 결과의 내용을 추출하는 편의 함수
    
    Args:
        query (str): 검색어
        max_results (int, optional): 검색 결과 수. 기본값은 5.
        save_to_file (str, optional): 결과를 저장할 파일 경로. 기본값은 None.
        
    Returns:
        str: 검색 결과 보고서
    """
    results = create_search_results(query)
    if save_to_file:
        save_results(results, save_to_file)
    return results