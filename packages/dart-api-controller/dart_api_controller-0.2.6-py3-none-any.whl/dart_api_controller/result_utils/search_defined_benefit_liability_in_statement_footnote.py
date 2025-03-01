from financial_dataset_preprocessor import format_commaed_number
from canonical_transformer import map_df_to_csv, get_mapping_of_column_pairs, map_df_to_csv_including_korean
from dart_api_controller.disclosure_utils.disclosure_content_loader import load_disclosure_xml_text
from dart_api_controller.disclosure_utils.disclosure_xml_parser import get_hierachically_filtered_tag_contents
from dart_api_controller.result_utils.result_loader import load_content_result
from dart_api_controller.xml_contoller.xml_parser import extract_exact_full_tag_with_keyword, extract_table_tag_text_containing_target_td_tag_text, map_table_tag_text_to_df_version3, extract_full_tag_with_keyword
from shining_pebbles import check_folder_and_create_folder
from tqdm import tqdm
import pandas as pd
from .result_path_director import FILE_FOLDER_CONTENT_RESULT
from .result_loader import load_search_results, load_concatenated_content_result
from .result_consts import FILE_NAME_CONTENT_RESULT, FILE_NAME_CONCATENATED_CONTENT_RESULT
from .result_utils import get_existing_rcept_numbers_in_content_result_folder

ROOT_DIR = 'dataset-result'
OPTION_EXACT = False
KEYWORDS_EXAMPLE = ['. 연결재무제표 주석', '순확정급여부채']

class DisclosureContents:
    def __init__(self, rcept_no, keywords=KEYWORDS_EXAMPLE, option_exact=OPTION_EXACT):
        self.rcept_no = rcept_no
        self.keywords = self.set_keywords(keywords=keywords)
        self.contents = self.load_contents()
        self.contents_filtered = self.get_filtered_contents()
        self.targets = self.get_targets(option_exact=option_exact)
        self.tables = self.get_tables()
        self.dfs = self.get_dfs()

    def set_keywords(self, keywords):
        self.keywords = keywords
        self.keyword_section = keywords[0]
        self.keyword_target = keywords[1]
        return self.keywords

    def load_contents(self):
        self.contents = load_disclosure_xml_text(rcept_no=self.rcept_no)
        return self.contents

    def get_filtered_contents(self):
        self.contents_filtered = get_hierachically_filtered_tag_contents(xml_text=self.contents, keywords=self.keywords)
        return self.contents_filtered

    def get_targets(self, option_exact=OPTION_EXACT):
        targets = []
        for content_filtered in self.contents_filtered:
            if option_exact:
                tags = extract_exact_full_tag_with_keyword(xml_text=content_filtered, keyword=self.keyword_target)
            else:
                tags = extract_full_tag_with_keyword(xml_text=content_filtered, keyword=self.keyword_target)
            targets = [*targets, *tags]
        targets_table = [target for target in targets if any(tag in target for tag in ['TD', 'TH'])]
        self.targets = targets_table
        return self.targets

    def get_tables(self):
        tables = []
        for target in self.targets:
            table = extract_table_tag_text_containing_target_td_tag_text(xml_text=self.contents, target_td=target)
            tables.append(table)
        self.tables = tables
        return self.tables

    def get_dfs(self, option_save=False):
        dfs_raw = []
        dfs = []
        for table in self.tables:
            df_raw = map_table_tag_text_to_df_version3(table_tag_text=table)
            dfs_raw.append(df_raw)
            df = self.parse_table_having_negative_backet_commaed_numbers(df=df_raw)
            dfs.append(df)
        self.dfs_raw = dfs_raw
        self.dfs = dfs
        if option_save:
            self.save()
        return self.dfs

    def save(self, remark=None):
        file_folder = FILE_FOLDER_CONTENT_RESULT(keyword_content=self.keyword_target)
        if remark:
            file_folder = f'{file_folder}-remark{remark}'
        file_folder = check_folder_and_create_folder(folder_name=file_folder)
        for i, df in enumerate(self.dfs):
            file_name = FILE_NAME_CONTENT_RESULT(rcept_no=self.rcept_no, keyword_content=self.keyword_target, i=i)
            map_df_to_csv(df=df, file_folder=file_folder, file_name=file_name)
        return self.dfs

    def load(self, i=0):
        df = load_content_result(rcept_no=self.rcept_no, keyword_content=self.keyword_target, i=i)
        return df

    @staticmethod
    def parse_table_having_negative_backet_commaed_numbers(df):
        # 두산로보틱스 반기보고서 방식
        for col in df.columns[1:]:
            df[col] = df[col].apply(lambda x: -format_commaed_number(x.strip("()")) if isinstance(x, str) and x.startswith("(") and x.endswith(")") else format_commaed_number(x) if isinstance(x, str) else x)
        return df

class Macro:
    def __init__(self, keyword_title='분기보고서', keyword_content='순확정급여부채'):
        self.keyword_title = keyword_title
        self.keyword_content = keyword_content
        self.search_results = self.get_search_results()
        self.rcept_numbers = self.get_rcept_numbers()
        self.passes = []
        self.fails = []

    def get_search_results(self):
        search_results = load_search_results(keyword_title=self.keyword_title, keyword_content=self.keyword_content)
        self.search_results = search_results
        return self.search_results

    def get_rcept_numbers(self):
        rcept_numbers = self.search_results.index.unique()
        self.rcept_numbers = rcept_numbers
        return self.rcept_numbers

    def run(self):
        passes, fails = run_macro(rcept_numbers=self.rcept_numbers, keywords=['. 연결재무제표 주석', self.keyword_content])
        self.passes = passes
        self.fails = fails
        return self.passes, self.fails

    def concatenate_content_results(self, option_save=True):
        df, passes, fails = concatenate_all_content_results(option_save=option_save)
        self.contenated_result = df
        self.passes_concatenated = passes
        self.fails_concatenated = fails
        return self.contenated_result

def transform_column_value_type_as_str(df, column):
    return df.assign(**{column: df[column].astype(str)})

def load_search_results_local():
    search_results = load_search_results(keyword_title='분기보고서', keyword_content='순확정급여부채')
    return (search_results
          .reset_index()
          .pipe(transform_column_value_type_as_str, column='receipt_number'))

def get_mapping_corpname():
    df = load_search_results_local()
    mapping_corpname = get_mapping_of_column_pairs(df=df, key_col='receipt_number', value_col='corp_name')
    return mapping_corpname

def get_mapping_corpcode():
    df = load_search_results_local()
    mapping_corpcode = get_mapping_of_column_pairs(df=df, key_col='receipt_number', value_col='corp_code')
    return mapping_corpcode

def get_all_disclosure_contents(rcept_numbers, keywords):
    passes = []
    fails = []
    for rcept_no in tqdm(rcept_numbers):
        try:
            dc = DisclosureContents(rcept_no=rcept_no, keywords=keywords)
            dc.save()
            passes.append(rcept_no)
        except Exception as e:
            print(e)
            fails.append(rcept_no)
    return passes, fails

run_macro = get_all_disclosure_contents

def get_existing_rcept_numbers():
    return get_existing_rcept_numbers_in_content_result_folder(keyword_content='순확정급여부채')

def preprocess_content_result_ith_table(rcept_no, i=0):
    df = load_content_result(rcept_no=rcept_no, keyword_content='순확정급여부채', i=i)
    for i, col in enumerate(df.columns):
        df[f'value: {i}'] = df[col]
    df['key'] = df.index
    df['rcept_no'] = rcept_no
    df['table_no'] = i
    df['corpname'] = get_mapping_corpname()[rcept_no]
    df['corpcode'] = get_mapping_corpcode()[rcept_no]
    df = df[df.index.str.contains('확정급여|사외적립')]
    df = df.reset_index()
    col_names_with_value = [col for col in df.columns if 'value' in col]
    for col in col_names_with_value:
        df[col] = df[col].apply(lambda x: -format_commaed_number(x.strip("()")) if isinstance(x, str) and x.startswith("(") and x.endswith(")") else format_commaed_number(x) if isinstance(x, str) else x)
    cols_ordered = ['corpname', 'key'] +col_names_with_value + ['corpcode', 'rcept_no', 'table_no']
    df = df[cols_ordered]
    return df

def concatenate_all_content_results(i=0, option_save=True):
    passes = []
    fails = []
    dfs = []
    existing_rcept_numbers = get_existing_rcept_numbers()
    for rcept_no in existing_rcept_numbers:
        try:
            df = preprocess_content_result_ith_table(rcept_no=rcept_no, i=i)
            dfs.append(df)
            passes.append(rcept_no)
        except Exception as e:
            print(e)
            fails.append(rcept_no)
    df = pd.concat(dfs)
    if option_save:
        file_folder = FILE_FOLDER_CONTENT_RESULT(keyword_content='순확정급여부채')
        file_name = FILE_NAME_CONCATENATED_CONTENT_RESULT(keyword_content='순확정급여부채', i=i)
        map_df_to_csv_including_korean(df=df, file_folder=file_folder, file_name=file_name)
    return df, passes, fails

def load_concatenated_result(i=0):
    df = load_concatenated_content_result(keyword_content='순확정급여부채', i=i)
    return df