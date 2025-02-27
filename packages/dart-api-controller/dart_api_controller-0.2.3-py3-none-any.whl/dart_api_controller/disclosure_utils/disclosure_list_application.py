from .disclosure_list_fetcher import get_data_all_disclosures_by_date
from .disclosure_content_fetcher import fetch_disclosure_content
from .disclosure_content_loader import load_xml_text_from_response
from .disclosure_consts import FILE_FOLDER_RESULT, FILE_NAME_RESULT
from dart_api_controller.xml_contoller.xml_parser import check_keyword_exists
from canonical_transformer import get_mapping_of_column_pairs, map_df_to_csv
import pandas as pd

def get_df_disclosures_including_keyword_by_date(keyword, date_ref=None):
    data = get_data_all_disclosures_by_date(date_ref=date_ref)
    df = pd.DataFrame(data)
    df = df[df['report_nm'].str.contains(keyword)]
    return df    

def get_mapping_corpcode_to_rcept_no(keyword, date_ref=None):
    df = get_df_disclosures_including_keyword_by_date(keyword=keyword, date_ref=date_ref)
    mapping_corpcode_to_rcept_no = get_mapping_of_column_pairs(df=df, key_col='corp_code', value_col='rcept_no')
    return mapping_corpcode_to_rcept_no


def search_disclosures_including_keyword_by_date(keyword_title, keyword_content, date_ref, option_save=True):
    df = get_df_disclosures_including_keyword_by_date(date_ref=date_ref, keyword=keyword_title)
    mapping = get_mapping_of_column_pairs(df=df, key_col='corp_code', value_col='rcept_no')

    is_including = []
    is_not_including = []
    for corpcode, rcept_no in mapping.items():
        print(f'check {rcept_no}')
        response =fetch_disclosure_content(rcept_no=rcept_no)
        text = load_xml_text_from_response(response)
        is_in_text = check_keyword_exists(text=text, keyword=keyword_content) if text else None
        if is_in_text:
            is_including.append(rcept_no)
        else: 
            is_not_including.append(rcept_no)

    df_including = df[df['rcept_no'].isin(is_including)]
    if option_save:
        file_folder = FILE_FOLDER_RESULT(keyword_title=keyword_title, keyword_content=keyword_content)
        map_df_to_csv(df=df_including, file_folder=file_folder, file_name=FILE_NAME_RESULT(keyword_title=keyword_title, keyword_content=keyword_content, date_ref=date_ref))
    return df_including
