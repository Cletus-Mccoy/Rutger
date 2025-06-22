import aiohttp
import asyncio

URL = "http://perplexica-backend:3000/api/search"

async def search(question):
    headers = {"Content-Type": "application/json"}
    payload = {
        "chatModel": {
            "provider": "openai",
            "name": "gpt-4o-mini"
        },
        "embeddingModel": {
            "provider": "openai",
            "name": "text-embedding-3-large"
        },
        "optimizationMode": "speed",
        "focusMode": "webSearch",
        "query": question,
        "history": [],
        "stream": False
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload, headers=headers) as response:
            print('Status:', response.status)
            try:
                data = await response.json()
                print('JSON response:', data)
                return data
            except Exception as e:
                text = await response.text()
                print('Non-JSON response:', text)
                print('Error:', e)
                return {"message": "Failed to parse JSON response", "error": str(e)} 

