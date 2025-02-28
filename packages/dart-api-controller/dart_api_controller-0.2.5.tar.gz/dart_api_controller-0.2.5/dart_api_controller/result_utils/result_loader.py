from .result_path_director import FILE_FOLDER_SEARCH_RESULT, FILE_FOLDER_CONTENT_RESULT
from .result_consts import FILE_NAME_CONTENT_RESULT
from shining_pebbles import open_df_in_file_folder_by_regex
from financial_dataset_preprocessor import ensure_n_digits_code
import os 

def load_search_result(keyword_title, keyword_content, date_ref=None):
    file_folder_search_result = FILE_FOLDER_SEARCH_RESULT(keyword_title=keyword_title, keyword_content=keyword_content)
    regex = f'at{date_ref.replace("-","")}-.*\.csv' if date_ref else f'at.*\.csv'
    df = open_df_in_file_folder_by_regex(file_folder=file_folder_search_result, regex=regex)
    df['stock_code'] = df['stock_code'].apply(lambda code: ensure_n_digits_code(code=code, n=6))
    return df

def load_search_results(keyword_title, keyword_content):
    file_folder_search_result = FILE_FOLDER_SEARCH_RESULT(keyword_title=keyword_title, keyword_content=keyword_content)
    regex = f'dataset-dart_search_results-title{keyword_title}-content{keyword_content}-.*\.csv'
    df = open_df_in_file_folder_by_regex(file_folder=file_folder_search_result, regex=regex)
    return df

def load_content_result(rcept_no, keyword_content, i=0):
    file_folder_content_result = FILE_FOLDER_CONTENT_RESULT(keyword_content=keyword_content)
    regex = FILE_NAME_CONTENT_RESULT(rcept_no=rcept_no, keyword_content=keyword_content, i=i).split('-save')[0]
    print(file_folder_content_result)
    print(regex)
    df = open_df_in_file_folder_by_regex(file_folder=file_folder_content_result, regex=regex)
    return df