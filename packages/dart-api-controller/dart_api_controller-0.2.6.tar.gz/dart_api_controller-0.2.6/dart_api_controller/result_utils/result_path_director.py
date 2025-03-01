import os

ROOT_DIR_RESULT = 'dataset-result'
 
def format_content_result_folder_name(keyword_content, remark=None):
    keyword_content = keyword_content.replace('(', '_').replace(')', '_')
    folder_name = f'dataset-dart_content_result-content{keyword_content}'
    if remark:
        folder_name = f'{folder_name}-{remark}'
    return os.path.join(ROOT_DIR_RESULT, folder_name)

FILE_FOLDER_CONTENT_RESULT = format_content_result_folder_name

def format_search_result_folder_name(keyword_title, keyword_content, remark=None):
    keyword_title = keyword_title.replace('(', '_').replace(')', '_')
    keyword_content = keyword_content.replace('(', '_').replace(')', '_')
    folder_name = f'dataset-dart_search_result-title{keyword_title}-content{keyword_content}'
    if remark:
        folder_name = f'{folder_name}-{remark}'
    return os.path.join(ROOT_DIR_RESULT, folder_name)

FILE_FOLDER_SEARCH_RESULT = format_search_result_folder_name