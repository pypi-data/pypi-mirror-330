# Utils
import os
from typing import List, Callable, Union, Dict

# Webscraping
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from firecrawl import FirecrawlApp
from googleapiclient.discovery import build

from sarthakai.models import WebSearchResponse


def get_webpage_content(url: str) -> Union[tuple[bool, str], tuple[bool, Exception]]:
    """
    Fetches webpage content and returns the title and text content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title: str = soup.title.string if soup.title else ""
        text_content: str = " ".join(soup.stripped_strings)
        return True, f"{title}\n{text_content}"
    except requests.exceptions.RequestException as e:
        return False, e


def scrape_website_firecrawl(
    url: str, retries: int = 5, timeout: int = 30
) -> Dict[str, Union[bool, str]]:
    """
    Scrapes a website using Firecrawl, with retry logic.
    """
    api_key: Union[str, None] = os.environ.get("FIRECRAWL_API_KEY")
    app = FirecrawlApp(api_key=api_key)
    try:
        scrape_result = app.scrape_url(
            url=url,
            params={"formats": ["markdown"], "timeout": timeout},
        )
        return scrape_result
    except Exception as e:
        print(e)
        if retries > 0:
            return scrape_website_firecrawl(
                url=url, retries=retries - 1, timeout=timeout
            )
        else:
            return {"error": True}


def web_search_ddg(search_term: str, max_results: int = 5) -> List[WebSearchResponse]:
    """
    Searches the web using DuckDuckGo and returns a list of WebSearchResponse objects.
    """
    raw_search_results: List[Dict[str, str]] = DDGS().text(
        search_term, max_results=max_results
    )
    web_search_results: List[WebSearchResponse] = [
        WebSearchResponse(
            url=search_result.get("href", ""),
            title=search_result.get("title", ""),
            snippet=search_result.get("body", ""),
        )
        for search_result in raw_search_results
    ]
    return web_search_results


def web_search_google(
    search_term: str, max_results: int = 5, **kwargs
) -> List[WebSearchResponse]:
    """
    Searches Google using the Custom Search API and returns a list of WebSearchResponse objects.
    """
    google_api_key: str = os.environ["GOOGLE_API_KEY"]
    google_cse_id: str = os.environ["GOOGLE_CSE_ID"]
    service = build("customsearch", "v1", developerKey=google_api_key)
    raw_search_results: Dict[str, List[Dict[str, str]]] = (
        service.cse().list(q=search_term, cx=google_cse_id, **kwargs).execute()
    )
    if "items" not in raw_search_results:
        return []
    raw_search_results = raw_search_results["items"][:max_results]
    web_search_results: List[WebSearchResponse] = [
        WebSearchResponse(
            url=search_result.get("link", ""),
            title=search_result.get("title", ""),
            snippet=search_result.get("snippet", ""),
        )
        for search_result in raw_search_results
    ]
    return web_search_results


def search_web_within_limited_domains(
    web_search_function: Callable[[str, int], List[WebSearchResponse]],
    search_term: str,
    allowed_domains: Union[List[str], None] = None,
    max_results: int = 5,
) -> List[WebSearchResponse]:
    """
    Performs a web search within specified domains.
    """
    if allowed_domains:
        domain_filters: str = " OR ".join(
            f"site:{domain}" for domain in allowed_domains
        )
        search_term_with_domains: str = f"{search_term} {domain_filters}"
    else:
        search_term_with_domains = search_term
    search_results: List[WebSearchResponse] = web_search_function(
        search_term=search_term_with_domains, max_results=max_results
    )
    return search_results
