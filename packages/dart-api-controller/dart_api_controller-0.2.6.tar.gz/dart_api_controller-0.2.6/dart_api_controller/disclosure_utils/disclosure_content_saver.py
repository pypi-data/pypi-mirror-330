from .disclosure_content_fetcher import fetch_disclosure_content
from shining_pebbles import check_folder_and_create_folder
import zipfile
import io
import os

def save_xml_from_response(response, file_path):
   """
   Extract and save XML file from ZIP response
   Args:
       response: API response object
       file_path: Path to save XML file
   Returns:
       bool: Success status
   """
   try:
       # Process response as memory stream
       with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
           # Find XML filename
           xml_filename = zf.namelist()[0]
           
           # Extract and save XML content
           with zf.open(xml_filename) as xml_file:
               with open(file_path, 'wb') as f:
                   f.write(xml_file.read())
       return True
   except Exception as e:
       print(f"Error saving XML: {e}")
       return False


def save_xml_by_rcept_no(rcept_no):
    response = fetch_disclosure_content(rcept_no=rcept_no)
    file_folder = os.path.join('data-dart', 'xml-disclosure')
    check_folder_and_create_folder(folder_name=file_folder)
    file_name = f'xml-disclosure_content-rcept_no{rcept_no}.xml'
    file_path = os.path.join(file_folder, file_name)
    save_xml_from_response(response, file_path=file_path)
    print(f'|- xml saved: {file_path}')
    return None

def save_all_xmls(rcept_numbers):
    print(f'|- start saving xmls: {len(rcept_numbers)}')
    for rcept_no in rcept_numbers:
        try:
            save_xml_by_rcept_no(rcept_no=rcept_no)
        except Exception as e:
            print(f'|- failed to save xml: {rcept_no}, {e}')
    print(f'|- finished saving xmls: {len(rcept_numbers)}')
    return None