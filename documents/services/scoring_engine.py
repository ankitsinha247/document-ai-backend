from documents.models import ScoringRule
from django.db.models import Q


def calculate_score(framework, category, days):
    """
    Calculate score using database-driven Scoring Rules.
    """

    # ----------------------------------------
    # Normalize Category
    # ----------------------------------------

    category = str(category).strip()
    category = category.replace("-", " ")
    category = " ".join(category.split())

    # Preserve original and normalized forms
    category_normalized = category.title()

    # ----------------------------------------
    # Convert Days
    # ----------------------------------------

    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 0

    if days < 0:
        days = 0

    # ----------------------------------------
    # Debug Input
    # ----------------------------------------

    print("=" * 70)
    print("SCORING LOOKUP")
    print("=" * 70)
    print("Framework :", framework.code)
    print("Category  :", repr(category))
    print("Normalized:", repr(category_normalized))
    print("Days      :", days)
    print("=" * 70)

    # ----------------------------------------
    # Load Scoring Rule
    # ----------------------------------------

    scoring_rule = (
        ScoringRule.objects.filter(
            framework=framework,
            min_days__lte=days,
            max_days__gte=days,
            is_active=True
        )
        .filter(
            Q(category__iexact=category) |
            Q(category__iexact=category_normalized) |
            Q(category__iexact=f"Category {category}") |
            Q(category__iexact=f"Category {category_normalized}")
        )
        .order_by("priority")
        .first()
    )

    # ----------------------------------------
    # Fallback 1
    # If no exact range found,
    # use highest available slab
    # ----------------------------------------

    if scoring_rule is None:
        print("No exact day range found. Trying highest available slab...")

        scoring_rule = (
            ScoringRule.objects.filter(
                framework=framework,
                is_active=True
            )
            .filter(
                Q(category__iexact=category) |
                Q(category__iexact=category_normalized) |
                Q(category__iexact=f"Category {category}") |
                Q(category__iexact=f"Category {category_normalized}")
            )
            .order_by("-max_days", "priority")
            .first()
        )

    # ----------------------------------------
    # Fallback 2
    # If category also doesn't match,
    # use highest framework rule
    # ----------------------------------------

    if scoring_rule is None:
        print("No category match. Using framework default rule...")

        scoring_rule = (
            ScoringRule.objects.filter(
                framework=framework,
                is_active=True
            )
            .order_by("-max_days", "priority")
            .first()
        )

    if scoring_rule is None:
        print("No scoring rule found for framework:", framework.code)
        return {
            "category": category,
            "days": days,
            "weightage_per_day": 0.0,
            "total_score": 0.0,
            "eligible": False,
            "remarks": "No active scoring rule found."
        }

    # ----------------------------------------
    # Score Calculation
    # ----------------------------------------

    total_score = float(scoring_rule.weightage_per_day) * days

    if total_score > float(scoring_rule.max_score):
        total_score = float(scoring_rule.max_score)

    print("=" * 70)
    print("DATABASE SCORING ENGINE")
    print("=" * 70)
    print("Matched Rule ID     :", scoring_rule.id)
    print("Framework           :", framework.code)
    print("Category            :", scoring_rule.category)
    print("Days                :", days)
    print("Weightage Per Day   :", scoring_rule.weightage_per_day)
    print("Maximum Score       :", scoring_rule.max_score)
    print("Total Score         :", total_score)
    print("=" * 70)

    

    # ----------------------------------------
# Dynamic Remarks
# ----------------------------------------

   # ----------------------------------------
# Effective Days Used for Scoring
    effective_days = min(days, scoring_rule.max_days)

    remarks = (
        f"The certificate falls under {scoring_rule.category}. "
        f"The submitted certificate is for {days} days. "
        f"As per the framework, a maximum of {scoring_rule.max_days} days is considered for scoring. "
        f"The score is calculated as "
        f"{scoring_rule.weightage_per_day} × {effective_days} = {total_score}."
    )

    if scoring_rule.remarks:
        remarks += f" {scoring_rule.remarks}"

    # ----------------------------------------
    # Return
    # ----------------------------------------

    return {
        "category": scoring_rule.category,
        "days": days,
        "weightage_per_day": scoring_rule.weightage_per_day,
        "total_score": total_score,
        "eligible": True,
        "remarks": remarks
    }