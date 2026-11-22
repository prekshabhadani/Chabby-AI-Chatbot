from langchain_openai import ChatOpenAI

# OpenRouter model IDs selected for this project.
MODEL_CONFIG = {
    "text": "nvidia/nemotron-3.5-lightning:free",
    "vision": "nvidia/nemotron-3.5-super-vl:free",
    "reasoning": "nvidia/nemotron-3-ultra-550b-a55b:free",
}

CHABBY_SYSTEM_PROMPT = """
You are Chabby, a friendly and intelligent AI assistant.

Your name is Chabby. You are an independent AI chatbot project.
Never introduce yourself as NVIDIA Nemotron, Google Gemini, or another
underlying model or provider.

If someone asks who you are, say:
"I'm Chabby, your little AI companion!"

Be friendly, helpful, clear, and conversational.
Use simple explanations when appropriate.
The underlying model is an implementation detail.
Do not claim to have capabilities or access that you do not have.
"""


def get_chat_model(api_key, task="text", temperature=0.4):
    if task not in MODEL_CONFIG:
        raise ValueError(f"Unknown model task: {task}")

    return ChatOpenAI(
        model=MODEL_CONFIG[task],
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=temperature,
        timeout=90,
        max_retries=1,
    )


def get_response_with_fallback(api_key, messages, tasks=None, temperature=0.4):
    """
    Try the requested models in order.
    Vision is kept separate because a text-only fallback cannot inspect images.
    """
    if tasks is None:
        tasks = ["text", "reasoning"]

    errors = []
    for task in tasks:
        try:
            model = get_chat_model(
                api_key,
                task=task,
                temperature=temperature,
            )
            return model.invoke(messages)
        except Exception as error:
            errors.append(f"{task}: {error}")

    details = "\n".join(errors)
    raise RuntimeError(
        "All selected Chabby models were unavailable. "
        "The free OpenRouter providers may be busy or rate-limited.\n"
        + details
    )
