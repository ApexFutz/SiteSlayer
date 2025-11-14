#!/usr/bin/env python3
"""
Script to create a local version of the scraped website
with fixed links and navigation
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Configuration
OUTPUT_DIR = Path(__file__).parent / "output"
LOCAL_SITE_DIR = Path(__file__).parent / "local_site"


def create_url_mapping():
    """Create mapping from original URLs to local HTML filenames"""
    mapping = {
        '/': 'www_bigthunderevents_com_homepage.html',
        'https://www.bigthunderevents.com/': 'www_bigthunderevents_com_homepage.html',
        '/category/mechanical_rides__and__bulls/': 'www.bigthunderevents.com_category_mechanical_rides__and__bulls.html',
        '/category/water_slide_rentals/': 'www.bigthunderevents.com_category_water_slide_rentals.html',
        '/category/obstacle_courses/': 'www.bigthunderevents.com_category_obstacle_courses.html',
        '/category/interactive_games/': 'www.bigthunderevents.com_category_interactive_games.html',
        '/category/bounce_house_rentals/': 'www.bigthunderevents.com_category_bounce_house_rentals.html',
        '/category/combo_bouncers/': 'www.bigthunderevents.com_category_combo_bouncers.html',
        '/category/tents_tables_and_chairs/': 'www.bigthunderevents.com_category_tents_tables_and_chairs.html',
        '/category/package_super_savings/': 'www.bigthunderevents.com_category_package_super_savings.html',
        '/category/trackless_trains/': 'www.bigthunderevents.com_category_trackless_trains.html',
        '/category/entertainment/': 'www.bigthunderevents.com_category_entertainment.html',
        '/category/fun_foods_and_more/': 'www.bigthunderevents.com_category_fun_foods_and_more.html',
        '/category/dry_slides/': 'www.bigthunderevents.com_category_dry_slides.html',
    }
    return mapping


def get_all_pages():
    """Get list of all pages with titles"""
    pages = [
        ('www_bigthunderevents_com_homepage.html', 'Home'),
        ('www.bigthunderevents.com_category_bounce_house_rentals.html', 'Bounce House Rentals'),
        ('www.bigthunderevents.com_category_combo_bouncers.html', 'Combo Bouncers'),
        ('www.bigthunderevents.com_category_dry_slides.html', 'Dry Slides'),
        ('www.bigthunderevents.com_category_entertainment.html', 'Entertainment'),
        ('www.bigthunderevents.com_category_fun_foods_and_more.html', 'Fun Foods and More'),
        ('www.bigthunderevents.com_category_interactive_games.html', 'Interactive Games'),
        ('www.bigthunderevents.com_category_mechanical_rides__and__bulls.html', 'Mechanical Rides & Bulls'),
        ('www.bigthunderevents.com_category_obstacle_courses.html', 'Obstacle Courses'),
        ('www.bigthunderevents.com_category_package_super_savings.html', 'Package Super Savings'),
        ('www.bigthunderevents.com_category_tents_tables_and_chairs.html', 'Tents Tables and Chairs'),
        ('www.bigthunderevents.com_category_trackless_trains.html', 'Trackless Trains'),
        ('www.bigthunderevents.com_category_water_slide_rentals.html', 'Water Slide Rentals'),
    ]
    return pages


def create_navigation_html(current_page):
    """Create navigation bar HTML"""
    pages = get_all_pages()
    
    nav_html = """
    <nav class="main-navigation">
        <div class="nav-container">
            <div class="nav-logo">Big Thunder Events</div>
            <ul class="nav-menu">
"""
    
    for filename, title in pages:
        if filename == current_page:
            nav_html += f'                <li class="nav-item active"><a href="{filename}">{title}</a></li>\n'
        else:
            nav_html += f'                <li class="nav-item"><a href="{filename}">{title}</a></li>\n'
    
    nav_html += """            </ul>
        </div>
    </nav>
"""
    return nav_html


def get_navigation_css():
    """Return CSS for navigation"""
    return """
        .main-navigation {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
            margin: -40px -40px 30px -40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .nav-logo {
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .nav-item {
            margin: 0;
            padding: 0;
            background: none;
        }
        .nav-item a {
            display: block;
            color: white;
            padding: 15px 20px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.3s, transform 0.2s;
            border-radius: 0;
        }
        .nav-item a:hover {
            background: rgba(255,255,255,0.2);
            text-decoration: none;
            transform: translateY(-2px);
        }
        .nav-item.active a {
            background: rgba(255,255,255,0.3);
            border-bottom: 3px solid white;
        }
"""


def fix_image_urls(html_content):
    """Fix protocol-relative URLs in images"""
    # Fix //files.sysers.com URLs
    html_content = re.sub(r'src="//files\.sysers\.com', r'src="https://files.sysers.com', html_content)
    return html_content


def rewrite_internal_links(html_content, url_mapping):
    """Rewrite internal links to point to local files"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # Check if it's in our mapping
        if href in url_mapping:
            a_tag['href'] = url_mapping[href]
        # Remove links to items pages that we don't have
        elif href.startswith('/items/'):
            a_tag['href'] = '#'
            a_tag['title'] = 'Item details not available in local version'
    
    return str(soup)


def process_html_file(input_path, output_path, url_mapping):
    """Process a single HTML file"""
    print(f"Processing: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Add navigation CSS to existing style tag
    style_tag = soup.find('style')
    if style_tag:
        style_tag.string += get_navigation_css()
    
    # Add navigation after opening body tag and before container
    container = soup.find('div', class_='container')
    if container:
        nav_html = create_navigation_html(input_path.name)
        nav_soup = BeautifulSoup(nav_html, 'html.parser')
        container.insert(0, nav_soup)
    
    # Convert back to string for regex processing
    html_content = str(soup)
    
    # Fix image URLs
    html_content = fix_image_urls(html_content)
    
    # Rewrite internal links (do this after BeautifulSoup to catch all links)
    html_content = rewrite_internal_links(html_content, url_mapping)
    
    # Write processed file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  ✓ Saved to: {output_path.name}")


def create_index_page():
    """Create an improved index page"""
    pages = get_all_pages()
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Big Thunder Events - Local Site</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 60px 40px;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        .logo {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 18px;
        }
        .page-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .page-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .page-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .page-card a {
            color: white;
            text-decoration: none;
            font-size: 18px;
            font-weight: 600;
            display: block;
        }
        .page-card a:hover {
            text-decoration: none;
        }
        .info-box {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
            border-left: 4px solid #667eea;
        }
        .info-box h2 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .info-box ul {
            list-style: none;
            padding-left: 0;
        }
        .info-box li {
            padding: 8px 0;
            color: #555;
        }
        .info-box li:before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }
        .footer {
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Big Thunder Events</div>
            <p class="subtitle">Local Website Version - Nashville Party Rentals</p>
        </div>
        
        <div class="info-box">
            <h2>Welcome to Your Local Site</h2>
            <p>This is a fully functional local version of the Big Thunder Events website. All pages have been scraped and optimized for offline viewing.</p>
            <ul>
                <li>Navigate between pages using the menu at the top of each page</li>
                <li>All images are loaded from the original CDN</li>
                <li>Internal navigation works seamlessly</li>
                <li>No internet connection required (except for images)</li>
            </ul>
        </div>
        
        <h2 style="margin-bottom: 20px; color: #2c3e50;">Browse All Pages:</h2>
        <div class="page-grid">
"""
    
    for filename, title in pages:
        html_content += f"""            <div class="page-card">
                <a href="{filename}">{title}</a>
            </div>
"""
    
    html_content += """        </div>
        
        <div class="footer">
            <p><strong>Generated by SiteSlayer Web Scraper</strong></p>
            <p>Total Pages: """ + str(len(pages)) + """</p>
            <p style="margin-top: 15px; font-size: 14px;">This local site was created from scraped content and is for personal use only.</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content


def main():
    """Main function to process all files"""
    print("=" * 60)
    print("Creating Local Version of Scraped Website")
    print("=" * 60)
    print()
    
    # Create local_site directory
    LOCAL_SITE_DIR.mkdir(exist_ok=True)
    print(f"📁 Created directory: {LOCAL_SITE_DIR}")
    print()
    
    # Get URL mapping
    url_mapping = create_url_mapping()
    
    # Get all HTML files to process
    html_files = [f for f in OUTPUT_DIR.glob("*.html") if f.name.startswith("www")]
    
    print(f"Found {len(html_files)} HTML files to process")
    print()
    
    # Process each HTML file
    for html_file in sorted(html_files):
        output_path = LOCAL_SITE_DIR / html_file.name
        process_html_file(html_file, output_path, url_mapping)
    
    print()
    print("Creating index page...")
    
    # Create new index.html
    index_html = create_index_page()
    index_path = LOCAL_SITE_DIR / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"  ✓ Created: index.html")
    
    print()
    print("=" * 60)
    print("✅ Local site created successfully!")
    print("=" * 60)
    print()
    print(f"📂 Location: {LOCAL_SITE_DIR}")
    print(f"🌐 Open this file to start: {index_path}")
    print()
    print("You can now browse the website locally!")


if __name__ == "__main__":
    main()
