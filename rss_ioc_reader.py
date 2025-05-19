import argparse
from datetime import datetime, timedelta, timezone
import feedparser
import requests


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse RSS feeds and fetch IOCs from articles using IOCParser.com"
    )
    parser.add_argument(
        "--feeds",
        default="feeds.txt",
        help="Path to RSS feed list (default: feeds.txt)"
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Look back this many hours for new items (default: 24)"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="IOCParser.com API key"
    )
    return parser.parse_args()


def load_feed_urls(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def fetch_recent_items(feed_url, since):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries:
        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            published = datetime(*entry.updated_parsed[:6])
        if published and published > since:
            items.append({"title": entry.get("title"), "link": entry.get("link"), "published": published})
    return items


def extract_iocs_from_url(url, api_key):
    """Query IOCParser.com to extract IOCs from the given URL."""
    endpoint = "https://api.iocparser.com/url"  # Based on public example
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }
    payload = {"url": url}
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("iocs", [])


def main():
    args = parse_arguments()
    since = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    feed_urls = load_feed_urls(args.feeds)
    all_iocs = {}

    for feed_url in feed_urls:
        items = fetch_recent_items(feed_url, since)
        for item in items:
            url = item["link"]
            try:
                iocs = extract_iocs_from_url(url, args.api_key)
                if iocs:
                    all_iocs[url] = iocs
                    print(f"Found {len(iocs)} IOCs in {url}")
            except Exception as e:
                print(f"Failed to process {url}: {e}")

    if not all_iocs:
        print("No IOCs found.")
    else:
        print("\nSummary:")
        for url, iocs in all_iocs.items():
            print(f"{url}: {len(iocs)} IOCs")


if __name__ == "__main__":
    main()
