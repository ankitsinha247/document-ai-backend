import fitz
import pytesseract
from PIL import Image

def extract_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    full_text = ""

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)

        text = page.get_text()

        if text.strip():

            full_text += text

        else:

            pix = page.get_pixmap(matrix=fitz.Matrix(2,2))

            image_path = f"/tmp/page_{page_num}.png"

            pix.save(image_path)

            image = Image.open(image_path)

            ocr_text = pytesseract.image_to_string(image)

            full_text += ocr_text

    return full_text.strip()