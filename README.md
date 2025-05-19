# RSS IOC Reader

This project collects new articles from a list of RSS feeds and extracts Indicators of Compromise (IOCs) from each article using the IOCParser.com API.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a text file named `feeds.txt` containing RSS feed URLs, one per line. Example:
   ```
   https://example.com/feed.xml
   https://another.example.com/rss
   ```

3. Run the script (the script automatically loads `feeds.txt`; use `--feeds` to specify a different file):
   ```bash
   python rss_ioc_reader.py --hours 24 --api-key YOUR_API_KEY
   ```
   Replace `YOUR_API_KEY` with your IOCParser.com API key.

## Notes

- The IOCParser API endpoint and authentication method may vary. Adjust `rss_ioc_reader.py` as needed based on the official documentation.
- The `--hours` option controls how far back the script looks for new items.
