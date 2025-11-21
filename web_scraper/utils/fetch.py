"""
HTTP fetching utilities
"""

import requests
import time
from web_scraper.utils.logger import setup_logger

logger = setup_logger(__name__)

def fetch_page(url, config):
    """
    Fetch a web page and return its HTML content
    
    Args:
        url (str): URL to fetch
        config (Config): Configuration object
        
    Returns:
        str: HTML content or None if failed
    """
    # Use JavaScript rendering if enabled
    if getattr(config, 'use_js_rendering', False):
        return fetch_page_with_js(url, config)
    
    # Otherwise use regular HTTP fetch
    headers = {
        'User-Agent': config.user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=config.timeout,
            allow_redirects=True
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type.lower():
            logger.warning(f"Non-HTML content type for {url}: {content_type}")
            return None
        
        return response.text
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {e.response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {str(e)}", exc_info=True)
        return None

def fetch_page_with_js(url, config):
    """
    Fetch a web page using Selenium to execute JavaScript
    
    Args:
        url (str): URL to fetch
        config (Config): Configuration object
        
    Returns:
        str: Rendered HTML content or None if failed
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        logger.info(f"Fetching with JavaScript rendering: {url}")
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'user-agent={config.user_agent}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Set page load timeout
            driver.set_page_load_timeout(config.timeout)
            
            # Navigate to the URL
            driver.get(url)
            
            # Wait for the page to be ready and give JavaScript time to execute
            js_wait_time = getattr(config, 'js_wait_time', 3)
            time.sleep(js_wait_time)
            
            # Get the fully rendered HTML
            html_content = driver.page_source
            
            logger.info(f"Successfully fetched with JS rendering: {url}")
            return html_content
            
        finally:
            driver.quit()
            
    except ImportError:
        logger.error("Selenium not installed. Install with: pip install selenium")
        logger.info("Falling back to regular HTTP fetch")
        # Fall back to regular fetch
        config.use_js_rendering = False
        return fetch_page(url, config)
    except Exception as e:
        logger.error(f"Error fetching with JavaScript {url}: {str(e)}", exc_info=True)
        return None
