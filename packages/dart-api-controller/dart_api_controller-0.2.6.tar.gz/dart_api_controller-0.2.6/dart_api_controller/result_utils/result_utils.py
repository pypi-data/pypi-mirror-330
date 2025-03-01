from shining_pebbles import scan_files_including_regex
from .result_path_director import FILE_FOLDER_CONTENT_RESULT

def get_existing_rcept_numbers_in_content_result_folder(keyword_content):
    file_folder = FILE_FOLDER_CONTENT_RESULT(keyword_content=keyword_content)
    regex = f'dataset-dart_content_result-rcept_no'
    file_names = scan_files_including_regex(file_folder=file_folder, regex=regex)
    rcept_numbers = [file_name.split('-rcept_no')[-1].split('-')[0] for file_name in file_names]
    return rcept_numbers

EXISTING_RCEPT_NUMBERS = get_existing_rcept_numbers_in_content_result_folder
