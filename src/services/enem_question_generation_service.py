import json

from openai import OpenAI

from src.helpers.enem_question_common import validate_generated_question_payload

client = OpenAI()


def generate_enem_question(
    topic: str,
    build_context_fn,
    build_prompt_fn,
    *,
    max_attempts: int = 4,
) -> dict:
    last_error = None
    selected_context = build_context_fn(topic)

    for _ in range(max_attempts):
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=build_prompt_fn(**selected_context),
        )
        response_text = response.output[0].content[0].text

        try:
            payload = json.loads(response_text)
        except json.JSONDecodeError:
            last_error = ValueError("AI response is not a valid JSON object.")
            continue

        validation_error = validate_generated_question_payload(payload)
        if validation_error is not None:
            last_error = ValueError(validation_error)
            continue

        payload.update(selected_context)
        return payload

    raise last_error or ValueError("Unable to generate a valid ENEM question.")
