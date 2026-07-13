from django import forms
from .models import (
    Document,
    AssessmentFramework
)


class DocumentUploadForm(forms.ModelForm):

    framework = forms.ModelChoiceField(

        queryset=AssessmentFramework.objects.filter(
            is_active=True
        ),

        empty_label="Select Framework"
    )

    class Meta:

        model = Document

        fields = [

            "framework",

            "title",

            "file"

        ]

class QuestionForm(forms.Form):

    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4
            }
        )
    )