import re
import pandas as pd
from bs4 import BeautifulSoup


def split_by_tag_name(xml_text, tag_name):
    pattern = rf'(<{tag_name}.*?>.*?</{tag_name}>)'
    return re.findall(pattern, xml_text, re.DOTALL)

def count_keyword_occurrences(text, keyword):
    count = text.count(keyword)
    return count if count > 0 else None

def check_keyword_exists(text, keyword):
    return keyword in text

def extract_tag_contents(xml_text, tag_name):
    pattern = rf'<{tag_name}[^>]*>(.*?)</{tag_name}>'
    return re.findall(pattern, xml_text, re.DOTALL)

def extract_tag_with_keyword(xml_text, keyword):
    pattern = rf'<(\w+)[^>]*>[^<]*{keyword}[^<]*</\1>'
    return re.findall(pattern, xml_text, re.DOTALL)

def extract_full_tag_with_keyword(xml_text, keyword):
    pattern = rf'<\w+[^>]*>[^<]*{keyword}[^<]*</\w+>'
    return re.findall(pattern, xml_text, re.DOTALL)

def extract_exact_tag_with_keyword(xml_text, keyword):
    pattern = rf'<(\w+)[^>]*>\s*{keyword}\s*</\1>'
    return re.findall(pattern, xml_text, re.DOTALL)

def extract_exact_full_tag_with_keyword(xml_text, keyword):
    pattern = rf'<\w+[^>]*>\s*{keyword}\s*</\w+>'
    return re.findall(pattern, xml_text, re.DOTALL)


def extract_table_tag_text_containing_target_td_tag_text(xml_text, target_td):
    # 1. 특정 TD 태그가 등장하는 위치 찾기
    td_match = re.search(re.escape(target_td), xml_text)
    if not td_match:
        return None  # 해당 TD가 없으면 None 반환

    td_index = td_match.start()

    # 2. 해당 TD 이전에서 가장 가까운 <TABLE> 찾기
    table_start_matches = list(re.finditer(r'<TABLE[^>]*>', xml_text[:td_index]))
    if not table_start_matches:
        return None  # 해당하는 TABLE이 없으면 None 반환

    table_start_index = table_start_matches[-1].start()  # 가장 마지막으로 등장한 TABLE 시작 위치

    # 3. 해당 TD 이후에서 가장 가까운 </TABLE> 찾기
    table_end_match = re.search(r'</TABLE>', xml_text[td_index:])
    if not table_end_match:
        return None  # 닫는 TABLE 태그가 없으면 None 반환

    table_end_index = td_index + table_end_match.end()  # 전체 텍스트에서 닫는 TABLE 태그 위치

    # 4. 해당 TABLE 전체 추출
    return xml_text[table_start_index:table_end_index]

def map_table_tag_text_to_df(table_tag_text):
    # BeautifulSoup을 사용하여 HTML/XML 파싱
    soup = BeautifulSoup(table_tag_text, "html.parser")
    
    # 테이블 헤더 추출
    headers = [th.text.strip() for th in soup.find_all("th")]

    # 테이블 데이터 추출
    data = []
    for row in soup.find_all("tr")[1:]:  # 첫 번째 행은 헤더이므로 제외
        cells = [td.text.strip() for td in row.find_all("td")]
        if cells:  # 빈 행 방지
            data.append(cells)

    # DataFrame 생성
    if headers and data:
        try:
            df = pd.DataFrame(data, columns=headers)
        except:
            df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(data)

    return df


def map_table_tag_text_to_df_version2(table_tag_text):
    # BeautifulSoup을 사용하여 HTML/XML 파싱
    soup = BeautifulSoup(table_tag_text, "html.parser")
    
    # 테이블의 모든 행 가져오기
    rows = soup.find_all("tr")
    
    # 첫 번째 행에서 헤더 추출 (TH가 없으면 TD 사용)
    first_row_cells = rows[0].find_all(["th", "td"])
    headers = [cell.text.strip() for cell in first_row_cells]

    # 테이블 데이터 추출
    data = []
    for row in rows[1:]:  # 첫 번째 행은 이미 헤더로 사용했으므로 제외
        cells = [td.text.strip() for td in row.find_all("td")]
        if cells:  # 빈 행 방지
            data.append(cells)

    # DataFrame 생성
    try:
        df = pd.DataFrame(data, columns=headers)
    except ValueError:  # 컬럼 개수가 안 맞을 경우 처리
        df = pd.DataFrame(data)

    return df


def map_table_tag_text_to_df_version3(table_tag_text):
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(table_tag_text, "html.parser")

    # 모든 행(tr) 가져오기
    rows = soup.find_all("tr")

    # 첫 번째 행에서 헤더 추출 (th가 없으면 td 사용)
    first_row_cells = rows[0].find_all(["th", "td"])
    headers = []
    for cell in first_row_cells:
        colspan = int(cell.get("colspan", 1))  # colspan이 있으면 해당 개수만큼 확장
        headers.extend([cell.text.strip()] * colspan)  # 같은 헤더를 colspan 개수만큼 반복

    # 테이블 데이터 추출
    data = []
    for row in rows[1:]:  # 첫 번째 행(헤더)은 제외
        row_data = []
        for cell in row.find_all("td"):
            colspan = int(cell.get("colspan", 1))  # colspan 반영
            row_data.extend([cell.text.strip()] * colspan)  # colspan 개수만큼 같은 값 추가
        if row_data:
            data.append(row_data)

    # DataFrame 생성 (헤더 개수와 행 개수가 맞지 않는 경우 대비)
    try:
        df = pd.DataFrame(data, columns=headers)
    except ValueError:
        df = pd.DataFrame(data)  # 컬럼 개수가 안 맞으면 헤더 없이 반환

    return df
