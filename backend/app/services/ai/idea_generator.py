from .prompt_loader import load_prompt


def get_idea_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="idea", name="generate")

