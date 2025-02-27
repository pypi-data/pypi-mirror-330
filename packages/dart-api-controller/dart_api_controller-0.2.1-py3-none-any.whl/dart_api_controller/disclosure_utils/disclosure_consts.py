from shining_pebbles import check_folder_and_create_folder, get_today
import os

BASE_DIR_RESULT = 'dataset-result'

def format_file_folder_result(keyword_title, keyword_content):
    keyword_title = keyword_title.replace('(', '_').replace(')', '_')
    keyword_content = keyword_content.replace('(', '_').replace(')', '_')
    file_folder = f'dataset-dart_search_result-title{keyword_title}-content{keyword_content}'
    file_folder = os.path.join(BASE_DIR_RESULT, file_folder)
    check_folder_and_create_folder(folder_name=file_folder)
    return file_folder

FILE_FOLDER_RESULT =format_file_folder_result

def format_file_name_result(keyword_title, keyword_content, date_ref):
    keyword_title = keyword_title.replace('(', '_').replace(')', '_')
    keyword_content = keyword_content.replace('(', '_').replace(')', '_')
    file_name = f'dataset-dart_search_result-title{keyword_title}-content{keyword_content}-at{date_ref.replace("-","")}-save{get_today().replace("-","")}.csv'
    return file_name

FILE_NAME_RESULT = format_file_name_result