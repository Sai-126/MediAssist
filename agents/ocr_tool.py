import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_file) -> str:
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text.strip()
