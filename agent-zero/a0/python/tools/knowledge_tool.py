import os
import shutil
import asyncio
import requests
from python.helpers import memory, perplexica_search, duckduckgo_search, searxng_search
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from python.helpers.errors import handle_error

class Knowledge(Tool):
    async def execute(self, question="", context="", type=None, **kwargs):
        query = self.compose_query(question, context)
        
        self.clear_pycache()
        
        # Map search types to their methods
        search_methods = {
            "perplexica": self.perplexica_search,
            "searxng": self.searxng_search,
            "duckduckgo": self.duckduckgo_search,
            "memory": self.mem_search
        }

        # Collect relevant methods based on type
        if type is None or type == "all":
            selected_methods = search_methods.values()
        else:
            selected_methods = [search_methods[type]] if type in search_methods else []

        # Execute the selected methods concurrently
        tasks = [method(query) for method in selected_methods]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Map results to their respective sources
        result_map = {method_name: None for method_name in search_methods.keys()}
        for (method_name, result) in zip(search_methods.keys(), results):
            if type is None or type == "all" or type == method_name:
                result_map[method_name] = self.format_result(result, method_name.capitalize())

        # Combine results for display
        combined_results = "\n\n".join(filter(None, result_map.values()))

        msg = self.agent.read_prompt(
            "tool.knowledge.response.md",
            online_sources=combined_results,
            memory=result_map["memory"]
        )

        await self.agent.handle_intervention(msg)

        return Response(message=msg, break_loop=False)

    def clear_pycache(self):
        pycache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')
        if os.path.exists(pycache_dir):
            shutil.rmtree(pycache_dir)
            PrintStyle.hint(f"Deleted {pycache_dir}")
            self.agent.context.log.log(type="hint", content=f"Deleted {pycache_dir}")

    def compose_query(self, question, context):
        return f"{question} using context: {context}"

    async def perplexica_search(self, query):
        try:
            response = requests.get("http://perplexica-backend:3001/api")
            if response.status_code == 200:
                result = await asyncio.to_thread(perplexica_search.search, query)
                if not result:
                    raise Exception("Perplexica search returned no results")
                return result
            else:
                raise Exception(f"Perplexica health check failed with status code: {response.status_code}")
        except Exception as e:
            handle_error(e)
            self.agent.context.log.log(type="hint", content=f"Perplexica search failed: {str(e)}")
            return None

    async def searxng_search(self, query):
        try:
            response = requests.get("http://searxng:8080")
            if response.status_code == 200:
                result = await asyncio.to_thread(searxng_search.search, query)
                if not result:
                    raise Exception("SearXNG search returned no results")
                return result
            else:
                raise Exception(f"SearXNG health check failed with status code: {response.status_code}")
        except Exception as e:
            handle_error(e)
            self.agent.context.log.log(type="hint", content=f"SearXNG search failed: {str(e)}")
            return None

    async def duckduckgo_search(self, query):
        try:
            result = await asyncio.to_thread(duckduckgo_search.search, query)
            return result
        except Exception as e:
            handle_error(e)
            self.agent.context.log.log(type="hint", content=f"DuckDuckGo search failed: {str(e)}")
            return None

    async def mem_search(self, query):
        try:
            db = await memory.Memory.get(self.agent)
            docs = await db.search_similarity_threshold(query=query, limit=5, threshold=0.5)
            text = memory.Memory.format_docs_plain(docs)
            return "\n\n".join(text)
        except Exception as e:
            handle_error(e)
            self.agent.context.log.log(type="hint", content=f"Memory search failed: {str(e)}")
            return None

    def format_result(self, result, source):
        if isinstance(result, Exception):
            return f"{source} search failed: {str(result)}"
        return f"{source} results:\n{result}" if result else f"{source} returned no results."
