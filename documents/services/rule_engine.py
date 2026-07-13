from documents.models import (
    FrameworkRule,
    FrameworkRuleGroup,
)


def match_rule(values, operator, match_values):
    """
    Generic Rule Matcher

    Supports:
    - Single Field
    - Multiple Fields
    - Single Match Value
    - Multiple Match Values
    """

    # ---------------------------------------
    # Normalize Field Values
    # ---------------------------------------

    if not isinstance(values, list):
        values = [values]

    values = [
        str(v).strip().lower()
        for v in values
        if v is not None
    ]

    # ---------------------------------------
    # Normalize Match Values
    # Supports comma/newline separated values
    # ---------------------------------------

    match_list = []

    raw_values = (
        str(match_values)
        .replace("\n", ",")
        .split(",")
    )

    for item in raw_values:

        item = item.strip().lower()

        if item:
            match_list.append(item)

    # ---------------------------------------
    # Wildcard Rule
    # ---------------------------------------

    if "*" in match_list:
        return True

    # ---------------------------------------
    # Contains
    # ---------------------------------------

    if operator == "contains":

        return any(
            keyword in value
            for value in values
            for keyword in match_list
        )

    # ---------------------------------------
    # Equals
    # ---------------------------------------

    elif operator == "equals":

        return any(
            value == keyword
            for value in values
            for keyword in match_list
        )

    # ---------------------------------------
    # Startswith
    # ---------------------------------------

    elif operator == "startswith":

        return any(
            value.startswith(keyword)
            for value in values
            for keyword in match_list
        )

    # ---------------------------------------
    # Endswith
    # ---------------------------------------

    elif operator == "endswith":

        return any(
            value.endswith(keyword)
            for value in values
            for keyword in match_list
        )

    # ---------------------------------------
    # Regex
    # ---------------------------------------

    elif operator == "regex":

        import re

        return any(
            re.search(keyword, value)
            for value in values
            for keyword in match_list
        )

    return False

def evaluate_rule_group(group, extracted_data):
    """
    Evaluate one Framework Rule Group.
    """

    rules = group.framework_rules.filter(
        is_active=True
    ).order_by("priority")

    results = []

    print("\n")
    print("=" * 70)
    print(f"RULE GROUP : {group.group_name}")
    print("=" * 70)

    for rule in rules:

        field_names = [
            field.strip()
            for field in rule.field_name.split(",")
            if field.strip()
        ]

        field_values = []

        for field in field_names:

            value = extracted_data.get(field, "")

            field_values.append(value)

        matched = match_rule(
            field_values,
            rule.operator,
            rule.match_value
        )

        results.append(matched)

        print(
            f"{rule.rule_name} -> {matched}"
        )
        
    if group.condition_type == "AND":

        return all(results)    
    
    print("=" * 60)
    print("Rule Group :", group.group_name)
    print("Field Names:", field_names)
    print("Field Values:", field_values)
    print("Match Value:", rule.match_value)
    print("=" * 60)

    return any(results)
def evaluate_rules(framework, extracted_data):
    """
    Evaluate all Framework Rules.

    Supports:

    ✓ Multiple Fields
    ✓ Multiple Match Values
    ✓ Priority
    """

    rules = FrameworkRule.objects.filter(
        framework=framework,
        is_active=True
    ).order_by("priority")

    print("\n")
    print("=" * 70)
    print("DATABASE RULE ENGINE")
    print("=" * 70)

    for rule in rules:

        # ---------------------------------------
        # Multiple Fields
        # ---------------------------------------

        field_names = [

            field.strip()

            for field in rule.field_name.split(",")

            if field.strip()

        ]

        field_values = []

        for field in field_names:

            value = extracted_data.get(field, "")

            if value is None:
                value = ""

            field_values.append(value)

        print(f"Rule Name     : {rule.rule_name}")
        print(f"Fields        : {field_names}")
        print(f"Values        : {field_values}")
        print(f"Operator      : {rule.operator}")
        print(f"Match Values  : {rule.match_value}")

        matched = match_rule(
            field_values,
            rule.operator,
            rule.match_value
        )

        print(f"Matched       : {matched}")
        print("-" * 70)

        if matched:

            print("RULE MATCHED")
            print("=" * 70)

            return {

                "category": rule.category,

                "eligible": rule.eligible,

                "rule_name": rule.rule_name,

                "remarks": rule.remarks

            }

    print("NO RULE MATCHED")

    return {

        "category": "",

        "eligible": False,

        "rule_name": "No Rule Matched",

        "remarks": "No matching rule found."

    }