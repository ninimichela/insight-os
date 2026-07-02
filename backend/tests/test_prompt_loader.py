from app.services.ai.prompt_loader import load_prompt


def test_prompt_loader_loads_versioned_prompt():
    prompt = load_prompt(version="v1", module="analysis", name="summarize")

    assert "# Role" in prompt

