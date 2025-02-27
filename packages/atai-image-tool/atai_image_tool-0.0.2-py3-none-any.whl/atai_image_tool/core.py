import easyocr
import re
import json

def extract_image_content(image_path, languages=['en']):
    """Extract text from an image file using OCR.
    
    Args:
        image_path (str): Path to the image file
        languages (list): List of language codes to use for OCR
        
    Returns:
        str: Extracted text from the image
    """
    reader = easyocr.Reader(languages)
    results = reader.readtext(image_path)
    combined_text = ""
    for result in results:
        combined_text += result[1] + " "
    return combined_text

def clean_control_characters(s):
    """Clean control characters from a string.
    
    Args:
        s (str): String to clean
        
    Returns:
        str: Cleaned string
    """
    cleaned = ""
    for char in s:
        if ord(char) < 32:
            if char in '\n\r\t':
                cleaned += char.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
        else:
            cleaned += char
    return cleaned

def clean_text(text):
    """Clean text for JSON output.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    cleaned_text = cleaned_text.replace('\n', '')
    cleaned_text = cleaned_text.replace('"', "'")
    cleaned_string = clean_control_characters(cleaned_text)
    cleaned_string = cleaned_string.replace("\\", "\\\\")
    cleaned_string = cleaned_string.replace("\"", "\\\"")
    return cleaned_string

def save_as_json(text, output_file):
    """Save text to a JSON file.
    
    Args:
        text (str): Text to save
        output_file (str): Path to output file
        
    Returns:
        bool: True if successful
    """
    cleaned_text = clean_text(text)
    data = {"text": cleaned_text}
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    return True