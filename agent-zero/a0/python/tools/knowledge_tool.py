import os
import asyncio
from python.helpers import dotenv, memory, duckduckgo_search
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from python.helpers.errors import handle_error
from python.helpers.searxng import search as searxng
from python.helpers.perplexica import search as perplexica

SEARCH_ENGINE_RESULTS = 10
class Knowledge(Tool):
    async def execute(self, question="", **kwargs):
        # Create tasks for all three search methods
        tasks = [
            self.searxng_search(question),
            self.perplexica_search(question),
            self.mem_search(question),
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        searxng_result, perplexica_result, memory_result = results

        # Handle exceptions and format results
        perplexica_result = self.format_result_perplexica(perplexica_result, "Perplexica")
        searxng_result = self.format_result_searxng(searxng_result, "Search Engine")
        memory_result = self.format_result(memory_result, "Memory")

        msg = self.agent.read_prompt(
            "tool.knowledge.response.md",
            online_sources=(
            ("\n## SearXNG results:\n\n" + (searxng_result) + "\n\n" if searxng_result else "## No results from SearXNG \n\n") +
            ("\n## Perplexica result:\n\n" + (perplexica_result) + "\n\n" if perplexica_result else "## No results from Perplexica \n\n")
            ),
            memory=memory_result,
        )

        await self.agent.handle_intervention(
            msg
        )  # wait for intervention and handle it, if paused

        return Response(message=msg, break_loop=False)

    async def perplexica_search(self, question):
        return await perplexica(question)

    async def searxng_search(self, question):
        return await searxng(question)

    async def mem_search(self, question: str):
        db = await memory.Memory.get(self.agent)
        docs = await db.search_similarity_threshold(
            query=question, limit=5, threshold=0.5
        )
        text = memory.Memory.format_docs_plain(docs)
        return "\n\n".join(text)

    def format_result(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"
        return str(result) if result else ""

    def format_result_searxng(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"
        
        outputs = []
        for item in result["results"]:
            outputs.append(f"{item['title']}\n{item['url']}\n{item['content']}")

        return "\n\n".join(outputs[:SEARCH_ENGINE_RESULTS]).strip()

    def format_result_perplexica(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"

        # Ensure result is a dictionary
        if isinstance(result, dict):
            # Extract and format the main message
            message = result.get("message", "No detailed message provided.")

            # Extract and format the sources
            sources = result.get("sources", [])
            if sources:
                formatted_sources = "\n\n".join(
                    f"- **{source.get('metadata', {}).get('title', 'No Title')}**\n  "
                    f"URL: {source.get('metadata', {}).get('url', 'No URL')}\n  "
                    f"Excerpt: {source.get('pageContent', 'No Content')[:200]}..."  # Truncate for readability
                    for source in sources
                )
                return f"**{source} Result**\n\n{message}\n\n**References:**\n{formatted_sources}"
            
            # Return just the message if no sources are available
            return f"**{source} Result**\n\n{message}"
        
        # Handle unexpected formats
        return str(result).strip() if result else f"{source} returned an empty response."