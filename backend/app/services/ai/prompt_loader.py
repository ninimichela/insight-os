from pathlib import Path


PROMPT_ROOT = Path(__file__).resolve().parents[4] / "packages" / "prompts"


def load_prompt(version: str = "v1", module: str = "analysis", name: str = "summarize") -> str:
    """Load a versioned prompt from packages/prompts.

    Example:
        load_prompt(version="v1", module="analysis", name="summarize")
    """
    prompt_path = PROMPT_ROOT / version / module / f"{name}.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")
