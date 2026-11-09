import json
import re
import time

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_FALLBACK_MODELS


class AIPlanner:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "Gemini API key is missing. Add your key to the .env file."
            )

        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.models = self._make_model_list()

    def _make_model_list(self):
        model_names = [GEMINI_MODEL]
        if GEMINI_FALLBACK_MODELS:
            model_names.extend(GEMINI_FALLBACK_MODELS.split(","))

        clean_names = []
        for name in model_names:
            name = name.strip()
            if name and name not in clean_names:
                clean_names.append(name)
        return clean_names

    def _is_temporary_error(self, error):
        message = str(error).upper()
        temporary_words = [
            "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED",
            "500", "INTERNAL", "504", "DEADLINE_EXCEEDED",
            "SERVICE UNAVAILABLE", "TOO MANY REQUESTS"
        ]
        return any(word in message for word in temporary_words)

    def _make_prompt(self, test_case, starting_url):
        return f"""
Turn this plain-English browser test into a small JSON plan.

Starting website: {starting_url}
User test case: {test_case}

Return one JSON object with this shape:
{{
  "steps": [
    {{
      "action": "assert_title",
      "by": "text",
      "role": "heading",
      "target": "Expected title text",
      "value": ""
    }}
  ]
}}

Allowed actions: navigate, click, fill, select, check, uncheck, press,
assert_text, assert_visible, assert_title, assert_url, wait.
Allowed locator types: label, placeholder, role, text, test_id, css.

Rules:
1. Use only actions needed for the user's request.
2. Do not invent passwords, account details, or page results.
3. For a button use by="role" and target its accessible name.
4. For a field use label or placeholder when possible.
5. For a text check use action="assert_text" and by="text".
6. For a page title check use action="assert_title" and target the expected title text.
7. For a URL check use action="assert_url" and target the expected URL text.
8. The starting URL is opened automatically. Use navigate only for another page.
9. Do not submit payments, delete data, change account security, send messages,
   or perform other irreversible actions.
10. Include at least one verification action.
11. If required information is missing, return {{"steps": []}}.
12. Return JSON only. No Markdown and no explanation.
13. For wait, value must be a number from 0 to 5000 milliseconds.

For role, use a common role such as button, link, textbox, checkbox, radio,
heading, or combobox. For press, put the key name in value.
"""

    def _request_plan(self, model, prompt):
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        answer = response.text
        if not answer:
            raise ValueError("AI returned an empty test plan.")

        answer = answer.strip()
        answer = re.sub(r"^```(?:json)?\s*", "", answer)
        answer = re.sub(r"\s*```$", "", answer)

        try:
            data = json.loads(answer)
        except json.JSONDecodeError as error:
            raise ValueError("AI did not return valid JSON.") from error

        if not isinstance(data, dict):
            raise ValueError("AI plan must be a JSON object.")

        steps = data.get("steps")
        if not isinstance(steps, list) or not steps:
            raise ValueError(
                "AI could not make a safe test plan. Make the test case clearer."
            )
        return steps

    def create_plan(self, test_case, starting_url):
        prompt = self._make_prompt(test_case, starting_url)
        last_error = None

        for model in self.models:
            for attempt in range(2):
                try:
                    print("Trying Gemini model:", model)
                    return self._request_plan(model, prompt)
                except Exception as error:
                    last_error = error
                    if not self._is_temporary_error(error):
                        raise RuntimeError(
                            "Gemini request failed for model '" + model + "': " + str(error)
                        ) from error

                    if attempt == 0:
                        wait_seconds = 2
                        print(
                            "Gemini is temporarily busy. Retrying "
                            + model + " in " + str(wait_seconds) + " seconds..."
                        )
                        time.sleep(wait_seconds)

            print("Model is still unavailable. Trying the next model...")

        raise RuntimeError(
            "All configured Gemini models are temporarily unavailable. "
            "Please wait and try again. Last error: " + str(last_error)
        ) from last_error
