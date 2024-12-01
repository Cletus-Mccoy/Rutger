import requests

def search(query:str, base_url="http://perplexica-backend:3001/api/search"):    

    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "chatModel": {
            "provider": "ollama",
            "model": "llama3.1:latest"  # Updated to include the :latest tag
        },
        "embeddingModel": {
            "provider": "ollama",
            "model": "nomic-embed-text:latest"  # Updated to include the :latest tag
        },
        "optimizationMode": "speed", # speed, balanced
        "focusMode": "webSearch", # webSearch, academicSearch, writingAssistant, wolframAlphaSearch, youtubeSearch, redditSearch.
        "query": query,
        "history": []
    }
    
    response = requests.post(base_url, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        print("Response content:", response.content)
        raise
    results = response.json()["message"]
    return results

# Example Response: 
#
# {
#	"message": "Perplexica is an innovative, open-source AI-powered search engine designed to enhance the way users search for information online. Here are some key features and characteristics of Perplexica:\n\n- **AI-Powered Technology**: It utilizes advanced machine learning algorithms to not only retrieve information but also to understand the context and intent behind user queries, providing more relevant results [1][5].\n\n- **Open-Source**: Being open-source, Perplexica offers flexibility and transparency, allowing users to explore its functionalities without the constraints of proprietary software [3][10].",
#	"sources": [
#		{
#			"pageContent": "Perplexica is an innovative, open-source AI-powered search engine designed to enhance the way users search for information online.",
#			"metadata": {
#				"title": "What is Perplexica, and how does it function as an AI-powered search ...",
#				"url": "https://askai.glarity.app/search/What-is-Perplexica--and-how-does-it-function-as-an-AI-powered-search-engine"
#			}
#		},
#		{
#			"pageContent": "Perplexica is an open-source AI-powered search tool that dives deep into the internet to find precise answers.",
#			"metadata": {
#				"title": "Sahar Mor's Post",
#				"url": "https://www.linkedin.com/posts/sahar-mor_a-new-open-source-project-called-perplexica-activity-7204489745668694016-ncja"
#			}
#		}
#       ....
#	]
# }