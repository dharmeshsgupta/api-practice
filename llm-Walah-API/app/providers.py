import httpx 
from app import config

class ProviderError(Exception):
    pass

async def call_openai(prompt: str) -> str: 
    async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
        resp = await client.post(
            "https://api.openai.com/v1/completions",
            headers={
                "Authorization": f"Bearer {config.OPPENAI_API_KEY}",
            },
            json={
                    "model": config.OPENAI_MODEL,
                    "messages": [[{"role": "user", "content": prompt}]]
            },
        )
    if resp.status_code != 200:
        raise ProviderError(f"OpenAI {resp.status_code}: {resp.text[:300]}")
    return resp.json()["choices"][0]["message"]["content"]

async def call_gemini(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.GEMINI_MODEL}:generateContent"
    async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
        resp = await client.post(
            url,
            headers={"x-goog-api-key": config.GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
    if resp.status_code != 200:
        raise ProviderError(f"Gemini {resp.status_code}: {resp.text[:300]}")
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]