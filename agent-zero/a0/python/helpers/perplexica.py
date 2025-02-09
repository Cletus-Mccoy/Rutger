import aiohttp
from python.helpers import runtime

URL = "http://perplexica-backend:3001/api/search"

async def search(query: str):
    return await runtime.call_development_function(_search, query=query)

async def _search(query: str):
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "chatModel": {
            "provider": "ollama",
            "model": "llama3.1:latest"
        },
        "embeddingModel": {
            "provider": "ollama",
            "model": "nomic-embed-text:latest"
        },
        "optimizationMode": "speed",
        "focusMode": "webSearch",
        "query": query,
        "history": []
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, headers=headers, json=payload) as response:
            return await response.json()