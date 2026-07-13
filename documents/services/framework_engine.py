def evaluate_framework(framework, extracted_data):
    """
    Evaluate extracted AI data according to
    the selected assessment framework.
    """

    result = {}

    result["framework"] = framework.code

    result["framework_name"] = framework.name

    result["category"] = extracted_data.get(
        "category",
        ""
    )

    result["level"] = extracted_data.get(
        "level",
        ""
    )

    result["duration"] = extracted_data.get(
        "duration",
        ""
    )

    result["title"] = extracted_data.get(
        "title",
        ""
    )

    result["participant_name"] = extracted_data.get(
        "participant_name",
        ""
    )

    result["organization"] = extracted_data.get(
        "organization",
        ""
    )

    result["remarks"] = extracted_data.get(
        "remarks",
        ""
    )

    result["eligible"] = True

    return result
def framework_14(data):

    category = data["category"]

    days = int(data["duration_days"])

    return category, days