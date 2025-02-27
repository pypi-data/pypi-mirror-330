
import os

def save_xml_content_as_xml_file(xml_content, file_path):
    """
    Save XML content to a file
    
    Args:
        xml_content (str or bytes): XML content to save
        file_path (str): Path to save the XML file
        
    Returns:
        bool: Success status
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Save XML content based on its type
        if isinstance(xml_content, bytes):
            with open(file_path, 'wb') as f:
                f.write(xml_content)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
        return True
    except Exception as e:
        print(f"Error saving XML: {e}")
        return False