import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

def duckduckgo_search(query: str, max_results: int = 10):
    """
    Perform a DuckDuckGo search and return a list of results.

    Args:
        query (str): The search query string.
        max_results (int): Maximum number of results to return.

    Returns:
        list[dict]: A list of results, each containing 'title', 'url', and 'snippet'.
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.select(".result")[:max_results]:
        link_tag = result.select_one(".result__a")
        snippet_tag = result.select_one(".result__snippet")

        if not link_tag:
            continue

        title = link_tag.get_text(strip=True)
        href = link_tag.get("href")

        # Fix DuckDuckGo redirect links
        if href and "uddg=" in href:
            parsed = urlparse(href)
            qs = parse_qs(parsed.query)
            if "uddg" in qs:
                href = unquote(qs["uddg"][0])

        if href and href.startswith("//"):
            href = "https:" + href

        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

        results.append({
            "title": title,
            "url": href,
            "snippet": snippet
        })

    return results


# Example usage
if __name__ == "__main__":
    results = duckduckgo_search("derivs", max_results=5)
    for r in results:
        print(r["title"])
        print(r["url"])
        print(r["snippet"])
        print("-" * 80)
