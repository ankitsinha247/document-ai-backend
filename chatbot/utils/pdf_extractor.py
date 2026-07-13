import fitz
import pytesseract
from PIL import Image

def extract_pdf_text(pdf_path):

    text = ""

    pdf = fitz.open(pdf_path)

    for page in pdf:
        text += page.get_text()

    return text


def extract_using_ocr(pdf_path):

    pdf = fitz.open(pdf_path)

    text = ""

    for page in pdf:

        pix = page.get_pixmap()

        image_path = "temp.png"

        pix.save(image_path)

        image = Image.open(image_path)

        text += pytesseract.image_to_string(image)

    return text