import os
import sys
from typing import Any, Dict

from InquirerPy import prompt


def prompt_for_values(
    vars: Dict[str, Dict], set_defaults: bool = True
) -> Dict[str, Any]:
    if set_defaults:
        vars = set_defaults_to_environment(vars)

    questions = []

    assert vars is not None, "Must provide dict of environment variables to prompt"

    hidden_defaults = {}
    for k, v in vars.items():
        if v.get("hidden", False):
            hidden_defaults[k] = v.get("default")
            continue

        def validate(value):
            if bool(value):
                return True

            return "Missing required value"

        default = v.get("default", "")

        if default is None:
            default = ""

        question = {
            "name": k,
            "type": v.get("type", "input"),
            "message": v.get("prompt", k),
            "default": default,
            "validate": validate if v.get("required") else None,
        }
        if (
            v.get("type", "input") == "list"
            or v.get("type", "input") == "rawlist"
            or v.get("type", "input") == "checkbox"
        ):
            question.update(
                {
                    "choices": v.get("choices"),
                }
            )
        questions.append(question)
    values = prompt(questions)

    return {**values, **hidden_defaults}


def set_defaults_to_environment(prompts: Dict[str, Dict]) -> Dict[str, Any]:
    for key, value in prompts.items():
        prompts[key] = {**value, "default": os.environ.get(key, value.get("default"))}

    return prompts
