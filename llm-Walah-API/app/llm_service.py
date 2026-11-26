from app.providers import call_openai, call_gemini

PROVIDERS = [
    ("openai", call_openai),
    ("gemini", call_gemini),
]

async def get_answer(prompt: str) -> dict:   # correct    
    errors = {}

    for name, func in PROVIDERS:
        try:
            
            answer = await func(prompt)
            return {"provider": name, "answer": answer, "errors": errors}
        except Exception as e:
            errors[name] = str(e)
            # conrinue
    return {"provider": None, "answer": None, "errors": errors}