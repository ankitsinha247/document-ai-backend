import os

from django import forms
from django.core.exceptions import ValidationError

from .models import AssessmentFramework
from .widgets import MultipleFileField, MultipleFileInput


class DocumentUploadForm(forms.Form):

    framework = forms.ModelChoiceField(
        queryset=AssessmentFramework.objects.filter(is_active=True),
        empty_label="Select Framework"
    )

    title = forms.CharField(
        max_length=255,
        required=False
    )

    files = MultipleFileField(
        widget=MultipleFileInput(
            attrs={
                "accept": ".pdf,.zip,.xlsx,.png,.jpg,.jpeg,.bmp,.tif,.tiff"
            }
        )
    )

    def clean_files(self):
        files = self.cleaned_data.get("files", [])
        allowed_extensions = [
            ".pdf",
            ".zip",
            ".xlsx",
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tif",
            ".tiff",
        ]

        for uploaded_file in files:
            extension = os.path.splitext(uploaded_file.name)[1].lower()
            if extension not in allowed_extensions:
                raise ValidationError(
                    "Only PDF, ZIP, XLSX, and image files are allowed."
                )

        return files


class QuestionForm(forms.Form):

    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4
            }
        )
    )