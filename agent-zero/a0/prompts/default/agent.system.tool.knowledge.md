### knowledge_tool:
Provide "question" & "context" argument and get both online and memory response.
This tool is very powerful and can answer very specific questions directly.
First always try to ask for result rather that guidance.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
Specify a search type (perplexica, searchxng, duckduckgo, newsapi, memory, all) to save time.
Always pass a type when using the knowledge tool!

    * Perplexica - context search engine
    * searxng - metasearch engine
    * DuckDuckGo - privacy-focused search engine
    * Memory - internal knowledge base
    * All - Give all results (slower, takes up context)


**Example usage**:
~~~json
{
    "thoughts": [
        "I need to gather information about...",
        "First I will search...",
        "Then I will...",
    ],
    "tool_name": "knowledge_tool",
    "tool_args": {
        "question": "How to perform...",
        "type": "Type from list: (perplexica, searchxng, duckduckgo, memory, all)", 
        "context": [
        "While I'm trying to achieve...",
        "While I'm using...",
        "And I'm encountering error/issue...",
        ]
    }
}
~~~