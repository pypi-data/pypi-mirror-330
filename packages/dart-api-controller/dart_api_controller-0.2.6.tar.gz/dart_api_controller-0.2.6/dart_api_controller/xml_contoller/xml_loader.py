
def load_xml_file_as_text(file_path):
   """
   Load XML file as text
   
   Args:
       file_path (str): Path to the XML file
       
   Returns:
       str: Content of the XML file as text
       
   Raises:
       FileNotFoundError: When file is not found
       IOError: When error occurs while reading file
   """
   try:
       with open(file_path, 'r', encoding='utf-8') as file:
           return file.read()
   except UnicodeDecodeError:
       # Try with different encodings if UTF-8 fails
       try:
           with open(file_path, 'r', encoding='euc-kr') as file:
               return file.read()
       except UnicodeDecodeError:
           # Fallback to binary mode and try best effort decoding
           with open(file_path, 'rb') as file:
               content = file.read()
               try:
                   return content.decode('utf-8', errors='replace')
               except:
                   return content.decode('cp949', errors='replace')
   except FileNotFoundError:
       raise FileNotFoundError(f"File not found: {file_path}")
   except Exception as e:
       raise IOError(f"Error loading file: {str(e)}")