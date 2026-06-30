import sys
sys.path.append(".")
from agents.ocr_tool import extract_text_from_image

# Use any image with text on your laptop - update this path
image_path = "tests/sample_prescription.jpg"

try:
    text = extract_text_from_image(image_path)
    print("Extracted text:")
    print(text)
except FileNotFoundError:
    print("No sample image found at", image_path)
    print("Take a photo of any printed text and save it as tests/sample_prescription.jpg to test")