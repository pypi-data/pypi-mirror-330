from dart_api_controller.xml_contoller import split_by_tag_name, extract_tag_contents

def split_by_section1(xml_text):
    return split_by_tag_name(xml_text, 'SECTION-1')

def split_by_section2(xml_text):
    return split_by_tag_name(xml_text, 'SECTION-2')

def filter_sections_including_keyword(sections, keyword):
    return [section for section in sections if keyword in section]

def count_keyword_occurences_in_each_section(sections, keyword):
    lst_counts = {i: count_keyword_occurrences(text=section, keyword='연결재무제표 주석') for i, section in enumerate(sections)}
    return lst_counts

def extract_title(xml_text):
    return extract_tag_contents(xml_text, 'TITLE')

def get_data_section_title_and_contents(sections):
    return {extract_title(section)[0]: section for section in sections}

def get_data_section_title_and_contents_including_keywords(sections, keywords):
    for keyword in keywords:
        sections = filter_sections_including_keyword(sections=sections, keyword=keyword)
    data_sections = get_data_section_title_and_contents(sections=sections)
    return data_sections

def get_filtered_sections_including_keywords(sections, keywords):
    for keyword in keywords:
        sections = filter_sections_including_keyword(sections=sections, keyword=keyword)
    return sections

def get_hierachically_filtered_tag_contents(xml_text, keywords):
    lst_results = []
    section_0_text = xml_text
    sections_1 = split_by_section1(xml_text=section_0_text)
    sections_1 = get_filtered_sections_including_keywords(sections=sections_1, keywords=keywords)
    for section_1_text in sections_1:
        sections_2 = split_by_section2(xml_text=section_1_text)
        sections_2 = get_filtered_sections_including_keywords(sections=sections_2, keywords=keywords)
        lst_results = [*lst_results, *sections_2]
    return lst_results 

# def get_recursively_filtered_tag_contents(xml_text, tag_names, keywords):

