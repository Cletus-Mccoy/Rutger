import requests
import json

def search(query: str, amount=5, categories=None, engines=None, language="en", page=1, time_range=None, format="json") -> list[str]:
    try:
        params = {
            "q": query,
            "categories": categories,
            "engines": engines,
            "language": language,
            "pageno": page,
            "time_range": time_range,
            "format": format
        }
        response = requests.get("http://searxng:8080/search", params=params)
        response.raise_for_status()
        search_results = response.json()
        results = [result['title'] + " - " + result['url'] for result in search_results['results'][:int(amount)]]
        return results
    except Exception as e:
        print(f"Error: {e}")
        if 'response' in locals():
            print("Response content:", response.content)
        raise

def format_results_as_json(results: list[str]) -> str:
    return json.dumps({"results": results}, indent=4)
