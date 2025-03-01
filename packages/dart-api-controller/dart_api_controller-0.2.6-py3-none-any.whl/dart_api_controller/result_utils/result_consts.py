from shining_pebbles import get_today

def format_file_name_content_result(rcept_no, keyword_content, i):
    keyword_content = keyword_content.replace('(', '_').replace(')', '_')
    if i == 0 or i is None:
        file_name = f'dataset-dart_content_result-rcept_no{rcept_no}-content{keyword_content}-save{get_today().replace("-","")}.csv'
    else:
        file_name = f'dataset-dart_content_result-rcept_no{rcept_no}-content{keyword_content}-remark{i}-save{get_today().replace("-","")}.csv'
    return file_name

FILE_NAME_CONTENT_RESULT = format_file_name_content_result

def format_file_name_concatenated_content_result(keyword_content, i=0):
    if i == 0 or i is None:
        file_name = f'dataset-dart_concatenated_content_result-content{keyword_content}-save{get_today().replace("-","")}.csv'
    else:
        file_name = f'dataset-dart_concatenated_content_result-content{keyword_content}-remark{i}-save{get_today().replace("-","")}.csv'
    return file_name

FILE_NAME_CONCATENATED_CONTENT_RESULT = format_file_name_concatenated_content_result