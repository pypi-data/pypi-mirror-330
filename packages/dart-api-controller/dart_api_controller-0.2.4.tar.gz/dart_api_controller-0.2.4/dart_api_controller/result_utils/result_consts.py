from shining_pebbles import get_today

def format_file_name_content_result(rcept_no, keyword_content):
    keyword_content = keyword_content.replace('(', '_').replace(')', '_')
    return f'dataset-dart_content_result-rcept_no{rcept_no}-content{keyword_content}-save{get_today().replace("-","")}.csv'

FILE_NAME_CONTENT_RESULT = format_file_name_content_result