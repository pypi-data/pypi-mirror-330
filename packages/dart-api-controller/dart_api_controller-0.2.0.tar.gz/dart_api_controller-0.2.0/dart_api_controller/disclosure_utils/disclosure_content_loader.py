import zipfile
import io
import os
from .disclosure_path_director import FILE_FOLDER
from dart_api_controller.xml_contoller import load_xml_file_as_text

def load_disclosure_xml_text(rcept_no, file_folder=FILE_FOLDER['disclosure']):
    file_name = f'xml-disclosure_content-rcept_no{rcept_no}.xml'
    file_path = os.path.join(file_folder, file_name)
    text = load_xml_file_as_text(file_path=file_path)
    return text

def load_xml_text_from_response(response):
   """
   Extract XML content directly as text from ZIP response
   Args:
       response: API response object
   Returns:
       str: XML string content
       None: If error occurs
   """
   try:
       # Process response as memory stream
       with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
           # Find XML filename
           xml_filename = zf.namelist()[0]
           
           # Convert XML content directly to string
           with zf.open(xml_filename) as xml_file:
               return xml_file.read().decode('utf-8')
               
   except Exception as e:
       print(f"Error extracting XML text: {e}")
       return None
