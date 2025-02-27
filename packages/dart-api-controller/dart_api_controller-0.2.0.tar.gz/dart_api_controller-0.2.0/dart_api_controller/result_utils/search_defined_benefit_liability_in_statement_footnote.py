from financial_dataset_preprocessor import format_commaed_number
from canonical_transformer import map_df_to_csv
from dart_api_controller.disclosure_utils.disclosure_content_loader import load_disclosure_xml_text
from dart_api_controller.disclosure_utils.disclosure_xml_parser import get_hierachically_filtered_tag_contents
from dart_api_controller.xml_contoller.xml_parser import extract_exact_full_tag_with_keyword, extract_table_tag_text_containing_target_td_tag_text, map_table_tag_text_to_df, extract_full_tag_with_keyword
from shining_pebbles import check_folder_and_create_folder
from .result_path_director import FILE_FOLDER_CONTENT_RESULT
from .result_consts import FILE_NAME_CONTENT_RESULT

ROOT_DIR = 'dataset-result'
OPTION_EXACT = True

class DisclosureContents:
    def __init__(self, rcept_no, keywords=['. 연결재무제표 주석', '순확정급여부채'], option_exact=OPTION_EXACT):
        self.rcept_no = rcept_no
        self.keywords = self.set_keywords(keywords=keywords)
        self.contents = self.load_contents()
        self.contents_filtered = self.get_filtered_contents()
        self.target = self.get_target()
        self.table = self.get_table(option_exact=option_exact)
        self.df = self.get_df()

    def set_keywords(self, keywords):
        self.keywords = keywords
        self.keyword_section = keywords[0]
        self.keyword_target = keywords[1]
        return self.keywords

    def load_contents(self):
        self.contents = load_disclosure_xml_text(rcept_no=self.rcept_no)
        return self.contents

    def get_filtered_contents(self):
        self.contents_filtered = get_hierachically_filtered_tag_contents(xml_text=self.contents, keywords=self.keywords)[0]
        return self.contents_filtered

    def get_target(self):
        self.target_entries = extract_exact_full_tag_with_keyword(xml_text=self.contents_filtered, keyword=self.keyword_target)
        self.target = self.target_entries[0]
        return self.target

    def get_table(self, option_exact=OPTION_EXACT):
        self.table = extract_table_tag_text_containing_target_td_tag_text(xml_text=self.contents_filtered, target_td=self.target) if option_exact else extract_full_tag_with_keyword(xml_text=self.contents_filtered, keyword=self.keyword_target)[0]
        return self.table

    def get_df(self, option_save=False):
        self.df_raw = map_table_tag_text_to_df(table_tag_text=self.table)
        self.df = self.parse_table_having_negative_backet_commaed_numbers(df=self.df_raw)
        if option_save:
            self.save()
        return self.df

    def save(self, remark=None):
        file_folder = FILE_FOLDER_CONTENT_RESULT(keyword_content=self.keyword_target)
        if remark:
            file_folder = f'{file_folder}-remark{remark}'
        file_folder = check_folder_and_create_folder(folder_name=file_folder)
        file_name = FILE_NAME_CONTENT_RESULT(rcept_no=self.rcept_no, keyword_content=self.keyword_target)
        map_df_to_csv(df=self.df, file_folder=file_folder, file_name=file_name)
        return None

    @staticmethod
    def parse_table_having_negative_backet_commaed_numbers(df):
        # 두산로보틱스 반기보고서 방식
        for col in df.columns[1:]:
            df[col] = df[col].apply(lambda x: -format_commaed_number(x.strip("()")) if x.startswith("(") and x.endswith(")") else format_commaed_number(x))
        return df

