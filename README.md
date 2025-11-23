# SiteSlayer

A web scraper that extracts content from websites and converts it to Markdown. Also includes a web server to serve scraped sites.

## Installation

Requires Python 3.11.9+ and [UV](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/ApexFutz/SiteSlayer.git
cd SiteSlayer
uv sync
```

Optional: Set `OPENAI_API_KEY` in `.env` for AI-powered link ranking.

## Web Scraper

Scrapes websites and converts HTML content to Markdown files.

```bash
python web_scraper/main.py https://example.com
```

The scraper:
1. Downloads the homepage
2. Extracts and ranks internal links (uses AI if `OPENAI_API_KEY` is set)
3. Crawls up to 50 pages (configurable via `MAX_PAGES` env var)
4. Saves content as Markdown files in `web_scraper/output/`

To convert scraped Markdown to HTML:

```bash
python web_scraper/replicate_site.py
```

## Website Server

FastAPI server that serves scraped sites from the `sites/` directory. Each site can be accessed at `/site/{site_name}` and includes a chatbot widget.

Start locally:

```bash
./scripts/start_server.sh
```

Deploy to Fly.io:

```bash
./scripts/deploy_server.sh
```
