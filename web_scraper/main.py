"""
SiteSlayer - Main Entry Point
Web scraper for extracting and converting website content to markdown
"""

import sys
import os
from pathlib import Path
from web_scraper.config import Config
from web_scraper.scraper.homepage import scrape_homepage
from web_scraper.scraper.crawler import crawl_site
from web_scraper.scraper.markdown_aggregator import aggregate_markdown_content
from web_scraper.utils.logger import setup_logger
from urllib.parse import urlparse

def main():
    """Main execution function"""
    logger = setup_logger(__name__)
    
    # Get target URL from command line or config
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("Enter the website URL to scrape: ").strip()
    
    if not target_url:
        logger.error("No URL provided")
        return
    
    # Ensure URL has proper scheme
    if not target_url.startswith(('http://', 'https://')):
        target_url = f"https://{target_url}"
    
    # Load configuration with target URL
    config = Config(target_url)
    
    logger.info(f"Starting to scrape: {target_url}")
    
    try:
        # Step 1: Scrape homepage
        logger.info("Step 1: Scraping homepage...")
        homepage_data = scrape_homepage(target_url, config)
        
        if not homepage_data:
            logger.error("Failed to scrape homepage")
            return
        
        logger.info(f"Homepage scraped successfully: {homepage_data['title']}")
        
        # Step 2: Crawl the site
        logger.info("Step 2: Crawling site for links...")
        crawl_results = crawl_site(target_url, homepage_data['links'], config)
        
        logger.info(f"Crawl complete. Total pages scraped: {len(crawl_results)}")
        
        # Step 3: Aggregate markdown content for chatbot
        logger.info("Step 3: Aggregating markdown content...")
        domain = config._sanitize_domain(target_url)
        content_file = aggregate_markdown_content(domain)
        
        # Display results summary
        print("\n" + "="*50)
        print("SCRAPING COMPLETE")
        print("="*50)
        print(f"Total pages scraped: {len(crawl_results)}")
        print(f"Output directory: {config.output_dir}")
        if content_file:
            print(f"Aggregated content: {content_file}")
        print("="*50 + "\n")
        
    except KeyboardInterrupt:
        logger.info("\nScraping interrupted by user")
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}", exc_info=True)

if __name__ == "__main__":
    # python -m web_scraper.main https://example.com
    main()
