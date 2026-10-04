from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()


def create_ai_plan(task):
    prompt = f"""
You are an AI task planner.

Convert the user's task into a simple sequence of executable actions.

User task:
{task}

Return ONLY valid JSON in this format:

{{
  "goal": "short description of the goal",
  "steps": [
    {{
      "step": 1,
      "action": "action_name",
      "description": "what the worker should do"
    }}
  ]
}}

Keep the plan practical and concise.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    text = response.output_text

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "goal": task,
            "steps": [],
            "raw_response": text
        }


if __name__ == "__main__":
    task = (
        "Find the latest invoice from Acme Corp, "
        "save the payment in the internal system, "
        "and verify that it was saved."
    )

    result = create_ai_plan(task)

    print("AI GENERATED PLAN")
    print("=" * 50)
    print(json.dumps(result, indent=2))