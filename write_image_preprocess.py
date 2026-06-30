content = '''from PIL import Image, ImageEnhance, ImageFilter
import io


def preprocess_prescription_image(image_file):
    image_file.seek(0)
    img = Image.open(image_file)

    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size
    max_dimension = max(width, height)
    if max_dimension < 1600:
        scale = 1600 / max_dimension
        new_size = (int(width * scale), int(height * scale))
        img = img.resize(new_size, Image.LANCZOS)

    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(1.4)

    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(2.0)

    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(1.1)

    output_buffer = io.BytesIO()
    img.save(output_buffer, format="JPEG", quality=95)
    output_buffer.seek(0)
    return output_buffer
'''

with open("agents/image_preprocess.py", "w", encoding="utf-8") as f:
    f.write(content)

print("image_preprocess.py written successfully!")