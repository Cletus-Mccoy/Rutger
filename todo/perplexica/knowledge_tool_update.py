import os
import asyncio
import httpx  # Ensure you have httpx installed for HTTP requests
from python.helpers import memory, duckduckgo_search
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from python.helpers.errors import handle_error

class Knowledge(Tool):
    async def execute(self, question="", **kwargs):
        # Create tasks for all three search methods
        tasks = [
            self.perplexica_search(question),
            self.duckduckgo_search(question),
            self.mem_search(question)
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Unpack results
        perplexica_result, duckduckgo_result, memory_result = results

        # Format results
        perplexica_result = self.format_result(perplexica_result, "Perplexica")
        duckduckgo_result = self.format_result(duckduckgo_result, "DuckDuckGo")
        memory_result = self.format_result(memory_result, "Memory")

        # Compose the final message
        msg = self.agent.read_prompt(
            "tool.knowledge.response.md", 
            online_sources=((perplexica_result + "\n\n") if perplexica_result else "") + str(duckduckgo_result),
            memory=memory_result
        )

        await self.agent.handle_intervention(msg)  # wait for intervention and handle it, if paused

        return Response(message=msg, break_loop=False)

    async def perplexica_search(self, question):
        # Set Perplexica's endpoint
        url = os.getenv("SEARXNG_API_URL", "http://localhost:3001/api/search")
        payload = {
            "chatModel": {"provider": "openai", "model": "gpt-4o-mini"},
            "embeddingModel": {"provider": "openai", "model": "text-embedding-3-large"},
            "optimizationMode": "speed",
            "focusMode": "webSearch",
            "query": question,
            "history": []
        }
        headers = {"Content-Type": "application/json"}

        # Make the async request to Perplexica's API
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("message", "No result")
            else:
                handle_error(response.text)
                return f"Perplexica search failed with status {response.status_code}: {response.text}"

    async def duckduckgo_search(self, question):
        return await asyncio.to_thread(duckduckgo_search.search, question)

    async def mem_search(self, question: str):
        db = await memory.Memory.get(self.agent)
        docs = await db.search_similarity_threshold(query=question, limit=5, threshold=0.5)
        text = memory.Memory.format_docs_plain(docs)
        return "\n\n".join(text)

    def format_result(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"
        return result if result else ""
