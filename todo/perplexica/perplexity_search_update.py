import os
import httpx  # Ensure you have httpx installed for making HTTP requests

async def perplexica_search(query: str):
    # Set Perplexica's API endpoint
    url = os.getenv("SEARXNG_API_URL", "http://localhost:3001/api/search")

    # Define the request payload according to Perplexica's structure
    payload = {
        "chatModel": {"provider": "openai", "model": "gpt-4o-mini"},
        "embeddingModel": {"provider": "openai", "model": "text-embedding-3-large"},
        "optimizationMode": "speed",
        "focusMode": "webSearch",
        "query": query,
        "history": []
    }
    headers = {"Content-Type": "application/json"}

    # Make the async request to Perplexica
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("message", "No result")
        else:
            raise Exception(f"Perplexica API request failed with status {response.status_code}: {response.text}")