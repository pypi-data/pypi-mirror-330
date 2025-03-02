import os
import time
from typing import List, Dict, Optional
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the ApifyClient with API token
apify_client = ApifyClient(os.environ["APIFY_TOKEN"])


def crawl_webpage_and_linked_pages_into_md(url: str) -> List[Dict[str, str]]:
    """
    Calls the Apify API to crawl a given link and return the processed webpages in markdown string format.
    """
    md_pages: List[Dict[str, str]] = []

    # Prepare the Actor input for the web crawler
    run_input: Dict[str, any] = {
        "startUrls": [{"url": url}],
        "crawlerType": "playwright:adaptive",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "initialCookies": [],
        "proxyConfiguration": {"useApifyProxy": True},
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
            [role=\"alert\"],
            [role=\"banner\"],
            [role=\"dialog\"],
            [role=\"alertdialog\"],
            [role=\"region\"][aria-label*=\"skip\" i],
            [aria-modal=\"true\"]""",
        "clickElementsCssSelector": '[aria-expanded="false"]',
    }

    # Run the Actor and wait for it to finish
    run = apify_client.actor("apify/website-content-crawler").call(run_input=run_input)

    # Log the dataset ID for debugging
    print(
        f"💾 Check your data here: https://console.apify.com/storage/datasets/{run['defaultDatasetId']}"
    )

    # Iterate through dataset items and collect markdown content
    for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
        md_pages.append({"text": item["markdown"], "file_url": item["url"]})

    return md_pages


def get_google_reviews_apify(
    place_id: str, reviews_start_date: Optional[str] = None, retries: int = 3
) -> List[Dict[str, any]]:
    """
    Fetches Google reviews using Apify's Google Places crawler.
    """
    run_input: Dict[str, any] = {
        "deeperCityScrape": False,
        "includeWebResults": False,
        "language": "en",
        "maxImages": 0,
        "maxReviews": 2000,
        "oneReviewPerRow": True,
        "onlyDataFromSearchPage": False,
        "scrapeResponseFromOwnerText": True,
        "scrapeReviewId": True,
        "scrapeReviewUrl": True,
        "scrapeReviewerId": True,
        "scrapeReviewerName": True,
        "scrapeReviewerUrl": True,
        "searchStringsArray": [f"place_id:{place_id}"],
    }

    if reviews_start_date:
        run_input["reviewsStartDate"] = reviews_start_date

    google_reviews: List[Dict[str, any]] = []

    try:
        run = apify_client.actor("compass/crawler-google-places").call(
            run_input=run_input
        )
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            google_reviews.append(item)
    except Exception as e:
        time.sleep(600)  # Wait before retrying
        retries -= 1
        if retries > 0:
            return get_google_reviews_apify(place_id, reviews_start_date, retries)
        else:
            print("ERRORs on Apify:", e)
            return []

    return google_reviews
