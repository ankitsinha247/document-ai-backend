import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from documents.models import (
    FrameworkPrompt,
    FrameworkField
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def build_json_schema(framework):
    """
    Builds JSON dynamically from Framework Fields.
    """

    fields = FrameworkField.objects.filter(
        framework=framework,
        is_active=True
    ).order_by("display_order")

    json_data = {}

    for field in fields:

        if field.field_type == "integer":

            json_data[field.field_name] = 0

        elif field.field_type == "float":

            json_data[field.field_name] = 0.0

        elif field.field_type == "boolean":

            json_data[field.field_name] = False

        else:

            json_data[field.field_name] = ""

    return json.dumps(
        json_data,
        indent=4
    )


def build_field_description(framework):
    """
    Builds AI instructions dynamically.
    """

    fields = FrameworkField.objects.filter(
        framework=framework,
        is_active=True
    ).order_by("display_order")

    text = ""

    for field in fields:

        required = "Required" if field.required else "Optional"

        text += (
            f"- {field.field_name}"
            f" ({field.field_label})"
            f" [{field.field_type}]"
            f" - {required}"
            f" - {field.ai_description}\n"
        )

    return text


def extract_information(document_text, framework):

    prompt_obj = FrameworkPrompt.objects.filter(
        framework=framework,
        is_active=True
    ).first()

    if not prompt_obj:

        raise Exception(
            f"No prompt found for {framework.code}"
        )

    json_schema = build_json_schema(
        framework
    )

    field_description = build_field_description(
        framework
    )

    prompt = prompt_obj.prompt

    prompt = prompt.replace(
        "{{FRAMEWORK_CODE}}",
        framework.code
    )

    prompt = prompt.replace(
        "{{FRAMEWORK_NAME}}",
        framework.name
    )

    prompt = prompt.replace(
        "{{FIELDS}}",
        field_description
    )

    prompt = prompt.replace(
        "{{JSON_SCHEMA}}",
        json_schema
    )

    prompt = prompt.replace(
        "{{DOCUMENT_TEXT}}",
        document_text
    )

    print("=" * 80)
    print(prompt)
    print("=" * 80)

    try:

        response = client.responses.create(
            model="gpt-5",
            input=prompt
        )

        result = response.output_text.strip()

        if result.startswith("```json"):

            result = result.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

        elif result.startswith("```"):

            result = result.replace(
                "```",
                ""
            ).strip()

        return json.loads(result)

    except Exception as e:

        print(e)

        return {
            "error": str(e)
        }