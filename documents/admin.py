from django.contrib import admin

from .models import (
    Document,
    DocumentChunk,
    ChatHistory,
    AssessmentFramework,
)
from .models import FrameworkPrompt
from .models import FrameworkField
from .models import FrameworkRule
from .models import ScoringRule
from .models import OutputColumn
from .models import FrameworkRuleGroup


@admin.register(FrameworkRuleGroup)

class FrameworkRuleGroupAdmin(admin.ModelAdmin):

    list_display = (

        "group_name",

        "framework",

        "category",

        "condition_type",

        "priority",

        "is_active"

    )

    list_filter = (

        "framework",

        "condition_type",

        "is_active"

    )

    search_fields = (

        "group_name",

        "category"

    )

    ordering = (

        "priority",

    )
    
@admin.register(OutputColumn)
class OutputColumnAdmin(admin.ModelAdmin):

    list_display = (

        "framework",

        "column_title",

        "field_name",

        "source",

        "column_order",

        "is_active"

    )

    list_filter = (

        "framework",

        "source",

        "is_active"

    )

    ordering = (

        "framework",

        "column_order"

    )

@admin.register(ScoringRule)
class ScoringRuleAdmin(admin.ModelAdmin):

    list_display = (

        "framework",

        "category",

        "min_days",

        "max_days",

        "weightage_per_day",

        "max_score",

        "priority",

        "is_active"

    )

    list_filter = (

        "framework",

        "category",

        "is_active"

    )

    search_fields = (

        "category",

    )

    ordering = (

        "framework",

        "priority"

    )
    
@admin.register(FrameworkRule)
class FrameworkRuleAdmin(admin.ModelAdmin):

    list_display = (
        "framework",
        "rule_name",
        "field_name",
        "operator",
        "match_value",
        "category",
        "eligible",
        "priority",
        "is_active",
    )

    search_fields = (
        "rule_name",
        "match_value",
        "field_name",
    )

    list_filter = (
        "framework",
        "category",
        "eligible",
        "is_active",
    )

    ordering = (
        "framework",
        "priority",
    )
    
@admin.register(FrameworkField)
class FrameworkFieldAdmin(admin.ModelAdmin):

    list_display = (

        "framework",

        "field_name",

        "field_label",

        "field_type",

        "required",

        "display_order",

        "is_active"

    )

    list_filter = (

        "framework",

        "field_type",

        "is_active"

    )

    search_fields = (

        "field_name",

        "field_label"

    )

    ordering = (

        "framework",

        "display_order"

    )
@admin.register(FrameworkPrompt)
class FrameworkPromptAdmin(admin.ModelAdmin):

    list_display = (

        "framework",

        "name",

        "version",

        "is_active"

    )

    list_filter = (

        "framework",

        "is_active"

    )

    search_fields = (

        "framework__code",

        "framework__name"

    )
    
@admin.register(AssessmentFramework)
class AssessmentFrameworkAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "version",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = (
        "code",
    )


admin.site.register(Document)
admin.site.register(DocumentChunk)
admin.site.register(ChatHistory)