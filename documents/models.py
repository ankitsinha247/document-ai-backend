from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField



# ==========================================
# Assessment Framework
# ==========================================

class AssessmentFramework(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    version = models.CharField(
        max_length=20,
        default="1.0"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["code"]

    def __str__(self):

        return f"{self.code} - {self.name}"

class FrameworkRuleGroup(models.Model):

    CONDITION_TYPES = [

        ("AND", "AND"),

        ("OR", "OR")

    ]

    framework = models.ForeignKey(

        "AssessmentFramework",

        on_delete=models.CASCADE,

        related_name="rule_groups"

    )

    group_name = models.CharField(

        max_length=255

    )

    description = models.TextField(

        blank=True

    )

    category = models.CharField(

        max_length=100

    )

    eligible = models.BooleanField(

        default=True

    )

    remarks = models.TextField(

        blank=True

    )

    condition_type = models.CharField(

        max_length=10,

        choices=CONDITION_TYPES,

        default="AND"

    )

    priority = models.PositiveIntegerField(

        default=1

    )

    is_active = models.BooleanField(

        default=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = [

            "priority"

        ]

    def __str__(self):

        return self.group_name
    
class FrameworkPrompt(models.Model):

    framework = models.ForeignKey(
        AssessmentFramework,
        on_delete=models.CASCADE,
        related_name="prompts"
    )

    name = models.CharField(
        max_length=255,
        default="Default Prompt"
    )

    prompt = models.TextField()

    version = models.CharField(
        max_length=20,
        default="1.0"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["framework", "-version"]

    def __str__(self):

        return f"{self.framework.code} - {self.name}"
 
class FrameworkField(models.Model):

    FIELD_TYPES = [

        ("text", "Text"),

        ("integer", "Integer"),

        ("float", "Float"),

        ("date", "Date"),

        ("boolean", "Boolean"),

        ("choice", "Choice")

    ]

    framework = models.ForeignKey(

        AssessmentFramework,

        on_delete=models.CASCADE,

        related_name="fields"

    )

    field_name = models.CharField(

        max_length=100

    )

    field_label = models.CharField(

        max_length=255

    )

    field_type = models.CharField(

        max_length=20,

        choices=FIELD_TYPES,

        default="text"

    )

    required = models.BooleanField(

        default=True

    )

    display_order = models.PositiveIntegerField(

        default=1

    )

    ai_description = models.TextField(

        blank=True

    )

    default_value = models.CharField(

        max_length=255,

        blank=True

    )

    is_active = models.BooleanField(

        default=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = [

            "framework",

            "display_order"

        ]

    def __str__(self):

        return f"{self.framework.code} - {self.field_name}"  
    
class FrameworkRule(models.Model):

    OPERATORS = [

        ("contains", "Contains"),
        ("equals", "Equals"),
        ("startswith", "Starts With"),
        ("endswith", "Ends With"),
        ("regex", "Regex")

    ]

    framework = models.ForeignKey(
        AssessmentFramework,
        on_delete=models.CASCADE,
        related_name="rules"
    )

    rule_group = models.ForeignKey(
        "FrameworkRuleGroup",
        on_delete=models.SET_NULL,
        related_name="framework_rules",
        null=True,
        blank=True
    )
    
    

    rule_name = models.CharField(max_length=255)

    rule_description = models.TextField(blank=True)

    field_name = models.CharField(max_length=100)

    operator = models.CharField(
        max_length=20,
        choices=OPERATORS,
        default="contains"
    )

    match_value = models.TextField()

    # Keep these fields for now
    category = models.CharField(
        max_length=50,
        blank=True
    )

    eligible = models.BooleanField(
        default=True
    )

    remarks = models.TextField(
        blank=True
    )

    priority = models.PositiveIntegerField(
        default=1
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return f"{self.framework.code} - {self.rule_name}"
    
    
class ScoringRule(models.Model):

    framework = models.ForeignKey(
        AssessmentFramework,
        on_delete=models.CASCADE,
        related_name="scoring_rules"
    )

    category = models.CharField(
        max_length=50
    )

    min_days = models.PositiveIntegerField(
        default=1
    )

    max_days = models.PositiveIntegerField(
        default=365
    )

    weightage_per_day = models.FloatField()

    max_score = models.FloatField(
        default=9999
    )

    remarks = models.TextField(
        blank=True
    )

    priority = models.PositiveIntegerField(
        default=1
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "framework",
            "priority"
        ]

    def __str__(self):

        return (
            f"{self.framework.code} - "
            f"{self.category}"
        )
        
class OutputColumn(models.Model):

    framework = models.ForeignKey(
        AssessmentFramework,
        on_delete=models.CASCADE,
        related_name="output_columns"
    )

    field_name = models.CharField(
        max_length=100
    )

    column_title = models.CharField(
        max_length=255
    )

    column_order = models.PositiveIntegerField(
        default=1
    )

    source = models.CharField(
        max_length=30,
        choices=[
            ("document", "Document"),
            ("extracted", "Extracted Data"),
            ("evaluation", "Evaluation"),
            ("rule", "Rule Engine"),
            ("scoring", "Scoring Engine"),
        ],
        default="extracted",
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = [
            "column_order"
        ]

    def __str__(self):

        return (
            f"{self.framework.code} - "
            f"{self.column_title}"
        )  
# ==========================================
# Document
# ==========================================

class Document(models.Model):

    DOCUMENT_TYPES = [
        ("pdf", "PDF"),
        ("docx", "DOCX"),
        ("xlsx", "XLSX"),
        ("image", "IMAGE"),
    ]

    framework = models.ForeignKey(
        "AssessmentFramework",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=500
    )

   
    document_type = models.CharField(
        max_length=50,
        blank=True
    )

    file = models.FileField(
        upload_to="documents/"
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=50,
        default="Uploaded"
    )

    extracted_text = models.TextField(
        blank=True,
        null=True
    )

    summary = models.TextField(
        blank=True,
        null=True
    )

    extracted_json = models.JSONField(
        blank=True,
        null=True
    )

    level = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    score = models.IntegerField(
        default=0
    )

    excel_report = models.FileField(
        upload_to="reports/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


# ==========================================
# Document Chunks
# ==========================================

class DocumentChunk(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    chunk_text = models.TextField()

    embedding = VectorField(
        dimensions=1536
    )

    page_number = models.IntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.document.title} - Chunk {self.id}"


# ==========================================
# Chat History
# ==========================================

class ChatHistory(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question[:50]
