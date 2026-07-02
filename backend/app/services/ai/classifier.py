from .prompt_loader import load_prompt


def get_classifier_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="analysis", name="classify")

