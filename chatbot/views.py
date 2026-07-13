from django.shortcuts import render
from .models import Document

from .utils.pdf_extractor import extract_pdf_text
from .utils.openai_helper import summarize_document
from .utils.pdf_extractor import extract_using_ocr

def upload_document(request):

    if request.method == "POST":

        uploaded_file = request.FILES['file']

        doc = Document.objects.create(
            title=uploaded_file.name,
            file=uploaded_file
        )

        text = extract_pdf_text(doc.file.path)
        if not text.strip():
            text = extract_using_ocr(doc.file.path)

        doc.extracted_text = text

        doc.summary = summarize_document(text)

        doc.save()

        return render(
            request,
            "chatbot/result.html",
            {"doc": doc}
        )

    return render(
        request,
        "chatbot/upload.html"
    )