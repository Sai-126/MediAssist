import pytesseract
from PIL import Image
import shutil
import os
import platform

def _configure_tesseract():
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return True

    if platform.system() == "Windows":
        windows_path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        if os.path.exists(windows_path):
            pytesseract.pytesseract.tesseract_cmd = windows_path
            return True

    return False

_TESSERACT_AVAILABLE = _configure_tesseract()


def extract_text_from_image(image_file) -> str:
    if not _TESSERACT_AVAILABLE:
        return ""
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception:
        return ""
