import os
import aiohttp

GEMINI_URL = os.getenv("GEMINI_API_URL", "https://api.gemini.com/v1/query")
GROK_URL = os.getenv("GROK_API_URL", "https://api.grok.com/v1/query")

async def ai_query(prompt: str, model: str = "gemini"):
    if model == "gemini":
        url = GEMINI_URL
        headers = {"Authorization": f"Bearer {os.getenv('GEMINI_API_KEY', '')}"}
    else:
        url = GROK_URL
        headers = {"Authorization": f"Bearer {os.getenv('GROK_API_KEY', '')}"}
    payload = {"prompt": prompt}
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()
