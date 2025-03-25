import easyocr
import re

reader = easyocr.Reader(['ar', 'en'])

def extract_cin_id(ocr_result):
    ocr_text = ' '.join(ocr_result)
    cin_regex = r"([A-Z]{2}\d{6,8})"
    cin_id = re.search(cin_regex, ocr_text)
    return cin_id.group() if cin_id else None

def perform_ocr(image_path):
    """ Perform OCR using EasyOCR on an image """
    ocr_result = reader.readtext(image_path, detail=0)
    return ocr_result