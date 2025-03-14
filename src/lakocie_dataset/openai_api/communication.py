from openai import OpenAI
from enum import Enum
from .output_models import AnalyticalComponents, DietaryComponents


class AIModelChoice(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"


def gpt_structured_output_reuqest(
    data: str,
    data_context: str,
    output_model_choice: type[AnalyticalComponents] | type[DietaryComponents],
    ai_model_choice: AIModelChoice = AIModelChoice.GPT_4O_MINI,
):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model=ai_model_choice.value,
        messages=[
            {
                "role": "system",
                "content": f"Jesteś specjalistą od mokrej karmy dla kotów. Wyodrębnij informacje o {data_context}",
            },
            {"role": "user", "content": data},
        ],
        response_format=output_model_choice,
    )
    return completion.choices[0].message.parsed
