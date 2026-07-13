""" from documents.services.ai_extractor import extract_information

from documents.services.framework_engine import evaluate_framework

from documents.services.scoring_engine import calculate_score

from documents.services.excel_generator import generate_excel

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
import os
from documents.services.rule_engine import evaluate_rules
from .forms import DocumentUploadForm

from documents.models import (
    Document,
    DocumentChunk,
    ChatHistory
)

from documents.services.ocr_service import extract_pdf_text

from documents.utils.chunker import chunk_text
from documents.utils.embedding import create_embedding
from documents.utils.search import search_chunks
from documents.utils.chat import ask_gpt
from documents.models import Document
from documents.models import ChatHistory
from django.shortcuts import redirect
from documents.services.ocr_service import extract_text """

import os

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import DocumentUploadForm

from documents.models import (
    Document,
    DocumentChunk,
    ChatHistory,
)

from documents.services.ai_extractor import extract_information
from documents.services.rule_engine import evaluate_rules
from documents.services.scoring_engine import calculate_score
from documents.services.excel_generator import generate_excel
from documents.services.ocr_service import extract_text

from documents.utils.chunker import chunk_text
from documents.utils.embedding import create_embedding
from documents.utils.search import search_chunks
from documents.utils.chat import ask_gpt

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_documents(request):

    if request.method == "POST":

        ids = request.POST.getlist(
            "documents"
        )

        Document.objects.filter(
            id__in=ids
        ).delete()

    return redirect(
        "document_library"
    )
@login_required
def document_library(request):

    documents = Document.objects.all().order_by(
        "-uploaded_at"
    )

    return render(
        request,
        "documents/library.html",
        {
            "documents": documents
        }
    )

@login_required
def chat_history(request):

    chats = ChatHistory.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "documents/history.html",
        {
            "chats": chats
        }
    )

# =========================
# DOCUMENT UPLOAD
# =========================

@login_required
def upload_document(request):

    documents = Document.objects.order_by("-uploaded_at")
    if request.method == "POST":

        form = DocumentUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save(commit=False)

            document.uploaded_by = request.user
            document.framework = form.cleaned_data["framework"]

            extension = os.path.splitext(
                document.file.name
            )[1].lower()

            if extension == ".pdf":
                document.document_type = "pdf"

            elif extension in [
                ".png",
                ".jpg",
                ".jpeg",
                ".bmp",
                ".tif",
                ".tiff"
            ]:
                document.document_type = "image"

            elif extension == ".docx":
                document.document_type = "docx"

            elif extension == ".xlsx":
                document.document_type = "xlsx"

            elif extension == ".pptx":
                document.document_type = "pptx"

            elif extension == ".csv":
                document.document_type = "csv"

            elif extension == ".txt":
                document.document_type = "txt"

            else:
                document.document_type = "unknown"

            document.save()

            print("\n")
            print("=" * 70)
            print("ASSESSMENT STARTED")
            print("=" * 70)
            print("Framework    :", document.framework.code)
            print("Document     :", document.title)
            print("Document Type:", document.document_type)
            print("File Path    :", document.file.path)
            print("=" * 70)

            # --------------------------------------------------
            # OCR
            # --------------------------------------------------

            text = extract_text(
                document.file.path,
                document.document_type
            )

            document.extracted_text = text

            if text:

                print("\n")
                print("=" * 70)
                print("OCR COMPLETED")
                print("=" * 70)
                print("Characters Extracted :", len(text))
                print("=" * 70)

                # --------------------------------------------------
                # AI Extraction
                # --------------------------------------------------

                extracted_data = extract_information(
                    text,
                    document.framework
                )

                print("\n")
                print("=" * 70)
                print("AI EXTRACTION")
                print("=" * 70)
                print(extracted_data)
                print("=" * 70)

                # --------------------------------------------------
                # Rule Engine
                # --------------------------------------------------

                evaluation = evaluate_rules(
                    document.framework,
                    extracted_data
                )

                print("\n")
                print("=" * 70)
                print("RULE ENGINE RESULT")
                print("=" * 70)
                print(evaluation)
                print("=" * 70)

                # --------------------------------------------------
                # Scoring Engine
                # --------------------------------------------------

                category = evaluation.get(
                    "category",
                    ""
                )

                days = int(
                    extracted_data.get(
                        "duration_days",
                        0
                    )
                )

                print("\n")
                print("=" * 70)
                print("SCORING INPUT")
                print("=" * 70)
                print("Category :", category)
                print("Days     :", days)
                print("=" * 70)

                scoring = calculate_score(
                    document.framework,
                    category,
                    days
                )

                print("\n")
                print("=" * 70)
                print("SCORING RESULT")
                print("=" * 70)
                print(scoring)
                print("=" * 70)

                # --------------------------------------------------
                # Excel Generation
                # --------------------------------------------------

                excel_path = generate_excel(
                    document=document,
                    framework=document.framework,
                    extracted_data=extracted_data,
                    evaluation=evaluation,
                    scoring=scoring
                )

                print("\n")
                print("=" * 70)
                print("EXCEL GENERATED")
                print("=" * 70)
                print("Excel Path :", excel_path)
                print("=" * 70)

                # --------------------------------------------------
                # Embedding Generation
                # --------------------------------------------------

                document.status = "Processed"

                chunks = chunk_text(text)

                for chunk in chunks:

                    try:

                        vector = create_embedding(chunk)

                        DocumentChunk.objects.create(
                            document=document,
                            chunk_text=chunk,
                            embedding=vector,
                            page_number=1
                        )

                    except Exception as e:

                        print("Embedding Error:", e)

                print("\n")
                print("=" * 70)
                print("EMBEDDING COMPLETED")
                print("=" * 70)
                print("Total Chunks :", len(chunks))
                print("=" * 70)

                print("\n")
                print("=" * 70)
                print("ASSESSMENT COMPLETED")
                print("=" * 70)
                print("Framework :", document.framework.code)
                print("Document  :", document.title)
                print("Excel     :", excel_path)
                print("=" * 70)

                document.save(
                    update_fields=[
                        "status",
                        "extracted_text"
                    ]
                )

            else:

                document.status = "OCR Required"

                print("\n")
                print("=" * 70)
                print("OCR FAILED")
                print("=" * 70)
                print("No text could be extracted from the document.")
                print("=" * 70)

                document.save(
                    update_fields=[
                        "status",
                        "extracted_text"
                    ]
                )

        else:

            print(form.errors)

            return render(
                request,
                "documents/upload.html",
                {
                    "form": form,
                    "documents": documents
                }
            )

    else:

        form = DocumentUploadForm()

    return render(
        request,
        "documents/upload.html",
        {
            "form": form,
            "documents": documents
        }
    )

    return render(
        request,
        "documents/upload.html",
        {
            "form": form,
            "documents": documents
        }
    )
# =========================
# CHAT WITH DOCUMENT
# =========================
@login_required
def ask_document(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get(
            "question"
        )

        document_id = request.POST.get(
            "document_id"
        )

        query_embedding = create_embedding(
            question
        )

        results = search_chunks(
            query_embedding,
            document_id=document_id,
            limit=10
        )

        context = ""

        for chunk in results:

            context += f"""

Document:
{chunk.document.title}

Content:
{chunk.chunk_text}

"""

        answer = ask_gpt(
            question,
            context
        )

        ChatHistory.objects.create(
            question=question,
            answer=answer
        )

    return render(
        request,
        "documents/chat.html",
        {
            "answer": answer,
            "documents": Document.objects.all(),
            "history": ChatHistory.objects.order_by(
                "-created_at"
            )[:20]
        }
    )