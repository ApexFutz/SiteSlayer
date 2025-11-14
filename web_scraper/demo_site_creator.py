#!/usr/bin/env python3
"""
Demo Site Creator - Creates a local HTML copy with absolute URLs
Perfect for showcasing AI chatbot integrations on customer websites
"""

import os
import re
import sys
import argparse
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DemoSiteCreator:
    def __init__(self, url, output_dir='web_scraper/demo_sites', chatbot_file=None):
        self.url = url
        self.domain = urlparse(url).netloc
        self.output_dir = Path(output_dir) / self.domain.replace('.', '_')
        self.chatbot_file = chatbot_file
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_homepage(self):
        """Fetch the homepage HTML"""
        try:
            logger.info(f"Fetching: {self.url}")
            response = requests.get(self.url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch homepage: {str(e)}")
            return None
    
    def make_url_absolute(self, url, base_url=None):
        """Convert relative URL to absolute URL"""
        if not url or url.startswith(('data:', '#', 'javascript:', 'mailto:', 'tel:')):
            return url
        
        # Already absolute
        if url.startswith(('http://', 'https://')):
            return url
        
        # Protocol-relative URL
        if url.startswith('//'):
            return 'https:' + url
        
        # Make relative URL absolute
        base = base_url or self.url
        return urljoin(base, url)
    
    def process_html(self, html):
        """Process HTML and convert all URLs to absolute"""
        soup = BeautifulSoup(html, 'html.parser')
        
        logger.info("Converting URLs to absolute...")
        
        # Process script tags
        logger.info("  Processing <script> tags...")
        for script in soup.find_all('script', src=True):
            script['src'] = self.make_url_absolute(script['src'])
        
        # Process link tags (CSS, icons, etc.)
        logger.info("  Processing <link> tags...")
        for link in soup.find_all('link', href=True):
            link['href'] = self.make_url_absolute(link['href'])
        
        # Process img tags
        logger.info("  Processing <img> tags...")
        for img in soup.find_all('img'):
            if img.get('src'):
                img['src'] = self.make_url_absolute(img['src'])
            if img.get('srcset'):
                img['srcset'] = self.process_srcset(img['srcset'])
            if img.get('data-src'):
                img['data-src'] = self.make_url_absolute(img['data-src'])
            if img.get('data-srcset'):
                img['data-srcset'] = self.process_srcset(img['data-srcset'])
        
        # Process picture/source tags
        logger.info("  Processing <source> tags...")
        for source in soup.find_all('source'):
            if source.get('src'):
                source['src'] = self.make_url_absolute(source['src'])
            if source.get('srcset'):
                source['srcset'] = self.process_srcset(source['srcset'])
        
        # Process video tags
        logger.info("  Processing <video> tags...")
        for video in soup.find_all('video'):
            if video.get('src'):
                video['src'] = self.make_url_absolute(video['src'])
            if video.get('poster'):
                video['poster'] = self.make_url_absolute(video['poster'])
        
        # Process audio tags
        logger.info("  Processing <audio> tags...")
        for audio in soup.find_all('audio'):
            if audio.get('src'):
                audio['src'] = self.make_url_absolute(audio['src'])
        
        # Process iframe tags
        logger.info("  Processing <iframe> tags...")
        for iframe in soup.find_all('iframe'):
            if iframe.get('src'):
                iframe['src'] = self.make_url_absolute(iframe['src'])
        
        # Process form actions
        logger.info("  Processing <form> tags...")
        for form in soup.find_all('form'):
            if form.get('action'):
                form['action'] = self.make_url_absolute(form['action'])
        
        # Process anchor tags
        logger.info("  Processing <a> tags...")
        for a in soup.find_all('a', href=True):
            a['href'] = self.make_url_absolute(a['href'])
        
        # Process inline styles with URLs
        logger.info("  Processing inline styles...")
        for tag in soup.find_all(style=True):
            tag['style'] = self.process_inline_style(tag['style'])
        
        # Process style tags
        logger.info("  Processing <style> tags...")
        for style in soup.find_all('style'):
            if style.string:
                style.string = self.process_css_urls(style.string)
        
        # Add base tag to help with any missed URLs
        if soup.head:
            base_tag = soup.new_tag('base', href=self.url)
            soup.head.insert(0, base_tag)
        
        return soup
    
    def process_srcset(self, srcset):
        """Process srcset attribute"""
        if not srcset:
            return srcset
        
        parts = []
        for item in srcset.split(','):
            item = item.strip()
            if not item:
                continue
            
            # Split URL from descriptor (e.g., "image.jpg 2x")
            tokens = item.split()
            if tokens:
                url = self.make_url_absolute(tokens[0])
                tokens[0] = url
                parts.append(' '.join(tokens))
        
        return ', '.join(parts)
    
    def process_inline_style(self, style):
        """Process inline style attribute"""
        def replace_url(match):
            url = match.group(1).strip('\'"')
            absolute_url = self.make_url_absolute(url)
            return f'url("{absolute_url}")'
        
        return re.sub(r'url\([\'"]?([^\)]+?)[\'"]?\)', replace_url, style)
    
    def process_css_urls(self, css):
        """Process URLs in CSS content"""
        def replace_url(match):
            url = match.group(1).strip('\'"')
            absolute_url = self.make_url_absolute(url)
            return f'url("{absolute_url}")'
        
        return re.sub(r'url\([\'"]?([^\)]+?)[\'"]?\)', replace_url, css)
    
    def inject_chatbot(self, soup):
        """Inject chatbot code into the HTML"""
        if not self.chatbot_file:
            # Add placeholder comment
            body = soup.find('body')
            if body:
                comment = soup.new_string('\n\n<!-- AI CHATBOT INJECTION POINT -->\n<!-- Insert your chatbot code here -->\n')
                body.append(comment)
            return soup
        
        # Load chatbot code from file
        try:
            with open(self.chatbot_file, 'r', encoding='utf-8') as f:
                chatbot_code = f.read()
            
            body = soup.find('body')
            if body:
                # Add comment before injection
                comment = soup.new_string('\n\n<!-- AI CHATBOT INJECTED BY SITESLAYER -->\n')
                body.append(comment)
                
                # Inject the chatbot code
                script_tag = soup.new_tag('script')
                script_tag.string = chatbot_code
                body.append(script_tag)
                
                logger.info(f"Chatbot code injected from: {self.chatbot_file}")
        except Exception as e:
            logger.warning(f"Failed to inject chatbot: {str(e)}")
        
        return soup
    
    def create_demo_site(self):
        """Main function to create the demo site"""
        logger.info("=" * 60)
        logger.info("SiteSlayer - Demo Site Creator")
        logger.info(f"Target: {self.url}")
        logger.info("=" * 60)
        print()
        
        # Fetch homepage
        html = self.fetch_homepage()
        if not html:
            logger.error("Failed to fetch homepage")
            return False
        
        print()
        
        # Process HTML
        soup = self.process_html(html)
        
        print()
        
        # Inject chatbot
        logger.info("Adding chatbot integration...")
        soup = self.inject_chatbot(soup)
        
        print()
        
        # Save the demo site
        output_file = self.output_dir / 'index.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        logger.info("=" * 60)
        logger.info("SUCCESS: Demo Site Created Successfully!")
        logger.info("=" * 60)
        print()
        logger.info(f"Location: {output_file.absolute()}")
        logger.info(f"Original: {self.url}")
        logger.info(f"Demo File: {output_file.name}")
        logger.info(f"Chatbot: {'Injected' if self.chatbot_file else 'Placeholder added'}")
        print()
        logger.info("Note: All assets (CSS, JS, images) load from original site")
        logger.info("Open the file in a browser to preview with your chatbot!")
        print()
        
        return True


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Create a demo site with absolute URLs for chatbot showcasing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python web_scraper/demo_site_creator.py https://example.com
  python web_scraper/demo_site_creator.py https://example.com --chatbot chatbot.js
  python web_scraper/demo_site_creator.py https://example.com --output custom_output
        """
    )
    
    parser.add_argument('url', help='Target website URL')
    parser.add_argument('--chatbot', '-c', help='Path to chatbot JavaScript file to inject')
    parser.add_argument('--output', '-o', default='web_scraper/demo_sites', 
                       help='Output directory (default: web_scraper/demo_sites)')
    
    args = parser.parse_args()
    
    # Ensure URL has proper scheme
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    # Create demo site
    creator = DemoSiteCreator(url, args.output, args.chatbot)
    success = creator.create_demo_site()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
