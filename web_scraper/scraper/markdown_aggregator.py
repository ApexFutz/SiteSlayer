"""
Markdown Aggregator - Combines all scraped markdown files into a single content.md file
for AI chatbot consumption and generates HTML
"""

import os
from pathlib import Path
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)

def aggregate_markdown_content(domain, websites_dir='websites', sites_dir='sites'):
    """
    Aggregate all markdown files from a scraped website into a single content.md file
    
    Args:
        domain (str): The domain name (sanitized) of the website
        websites_dir (str): Directory containing individual markdown files
        sites_dir (str): Directory where content.md will be saved
        
    Returns:
        str: Path to the created content.md file, or None if failed
    """
    logger.info(f"Aggregating markdown content for: {domain}")
    
    # Define paths
    source_dir = Path(websites_dir) / domain
    target_dir = Path(sites_dir) / domain
    
    # Validate source directory exists
    if not source_dir.exists():
        logger.error(f"Source directory not found: {source_dir}")
        return None
    
    # Get all markdown files
    md_files = list(source_dir.glob('*.md'))
    
    if not md_files:
        logger.warning(f"No markdown files found in: {source_dir}")
        return None
    
    logger.info(f"Found {len(md_files)} markdown files to aggregate")
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare aggregated content
    aggregated_content = []
    
    # Add header
    aggregated_content.append(f"# Website Content: {domain}")
    aggregated_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    aggregated_content.append(f"Total Pages: {len(md_files)}")
    aggregated_content.append("\n---\n")
    
    # Process each markdown file
    successful_files = 0
    for md_file in sorted(md_files):
        try:
            logger.debug(f"Processing: {md_file.name}")
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata from the file
            metadata = extract_metadata(content)
            
            # Add page section
            aggregated_content.append(f"\n## PAGE: {metadata['title']}")
            aggregated_content.append(f"**Source URL:** {metadata['url']}")
            
            if metadata['link_text']:
                aggregated_content.append(f"**Link Text:** {metadata['link_text']}")
            
            aggregated_content.append(f"**File:** {md_file.name}")
            aggregated_content.append("")  # Empty line
            
            # Add the actual content (skip the metadata section)
            page_content = extract_page_content(content)
            aggregated_content.append(page_content)
            
            aggregated_content.append("\n---\n")
            
            successful_files += 1
            
        except Exception as e:
            logger.error(f"Error processing {md_file.name}: {str(e)}", exc_info=True)
            continue
    
    if successful_files == 0:
        logger.error("Failed to process any markdown files")
        return None
    
    # Write aggregated content to file
    output_file = target_dir / 'content.md'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(aggregated_content))
        
        logger.info(f"Successfully created content.md at: {output_file}")
        logger.info(f"Aggregated {successful_files} pages")
        
        # Automatically generate HTML file
        html_file = generate_html_from_content(output_file, domain, len(md_files))
        if html_file:
            logger.info(f"Successfully created index.html at: {html_file}")
        
        return str(output_file)
        
    except Exception as e:
        logger.error(f"Error writing content.md: {str(e)}", exc_info=True)
        return None


def extract_metadata(content):
    """
    Extract metadata from markdown file
    
    Args:
        content (str): The markdown file content
        
    Returns:
        dict: Dictionary containing title, url, and link_text
    """
    metadata = {
        'title': 'Untitled',
        'url': '',
        'link_text': ''
    }
    
    lines = content.split('\n')
    
    for line in lines[:10]:  # Check first 10 lines for metadata
        line = line.strip()
        
        # Extract title (first heading)
        if line.startswith('# ') and metadata['title'] == 'Untitled':
            metadata['title'] = line[2:].strip()
        
        # Extract source URL
        elif line.startswith('Source:'):
            metadata['url'] = line.replace('Source:', '').strip()
        
        # Extract link text
        elif line.startswith('Link Text:'):
            metadata['link_text'] = line.replace('Link Text:', '').strip()
    
    return metadata


def extract_page_content(content):
    """
    Extract the main page content, skipping the metadata header section
    
    Args:
        content (str): The full markdown file content
        
    Returns:
        str: The page content without metadata
    """
    lines = content.split('\n')
    
    # Find the separator (---) that marks end of metadata
    separator_index = -1
    for i, line in enumerate(lines):
        if line.strip() == '---':
            separator_index = i
            break
    
    # If separator found, return content after it
    if separator_index >= 0 and separator_index < len(lines) - 1:
        return '\n'.join(lines[separator_index + 1:]).strip()
    
    # Otherwise return content after the first few metadata lines
    # Skip first heading, source, link text, and empty line
    content_start = 0
    for i, line in enumerate(lines[:10]):
        if line.strip() == '' and content_start == 0:
            content_start = i + 1
            break
    
    return '\n'.join(lines[content_start:]).strip()


def generate_html_from_content(content_md_path, domain, total_pages):
    """
    Generate an HTML file from the aggregated content.md
    
    Args:
        content_md_path (str): Path to the content.md file
        domain (str): Domain name for the title
        total_pages (int): Total number of pages aggregated
        
    Returns:
        str: Path to the created index.html file, or None if failed
    """
    try:
        from pathlib import Path
        
        content_path = Path(content_md_path)
        html_path = content_path.parent / 'index.html'
        
        # Read the content.md file
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the content to extract pages
        pages = parse_aggregated_content(content)
        
        # Generate HTML
        html = generate_html_template(domain, total_pages, pages)
        
        # Write HTML file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(html_path)
        
    except Exception as e:
        logger.error(f"Error generating HTML: {str(e)}", exc_info=True)
        return None


def parse_aggregated_content(content):
    """
    Parse the aggregated content.md to extract individual pages
    
    Args:
        content (str): The full aggregated content
        
    Returns:
        list: List of page dictionaries with title, url, and content
    """
    pages = []
    sections = content.split('\n## PAGE: ')
    
    for section in sections[1:]:  # Skip the header section
        lines = section.split('\n')
        page = {
            'title': lines[0].strip(),
            'url': '',
            'content': ''
        }
        
        # Extract URL
        for i, line in enumerate(lines[1:10], 1):
            if line.startswith('**Source URL:**'):
                page['url'] = line.replace('**Source URL:**', '').strip()
                # Find where content starts (after the metadata)
                content_start = i + 1
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip() == '':
                        content_start = j + 1
                        break
                
                # Get content until the separator
                content_lines = []
                for line in lines[content_start:]:
                    if line.strip() == '---':
                        break
                    content_lines.append(line)
                
                page['content'] = '\n'.join(content_lines).strip()
                break
        
        pages.append(page)
    
    return pages


def generate_html_template(domain, total_pages, pages):
    """
    Generate complete HTML from template
    
    Args:
        domain (str): Domain name
        total_pages (int): Total number of pages
        pages (list): List of page dictionaries
        
    Returns:
        str: Complete HTML content
    """
    # Generate table of contents
    toc_html = ""
    for i, page in enumerate(pages, 1):
        icon = get_page_icon(page['title'])
        toc_html += f'                <li><a href="#page-{i}">{icon} {page["title"]}</a></li>\n'
    
    # Generate page sections
    sections_html = ""
    for i, page in enumerate(pages, 1):
        icon = get_page_icon(page['title'])
        sections_html += f'''
        <div class="page-section" id="page-{i}">
            <div class="page-header">
                <h2>{icon} {page["title"]}</h2>
            </div>
            <div class="page-metadata">
                <strong>Source:</strong> <a href="{page["url"]}" target="_blank">{page["url"]}</a>
            </div>
            <div class="page-content">
                {format_markdown_to_simple_html(page["content"])}
            </div>
        </div>
'''
    
    # Get timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{domain} - Aggregated Content</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 20px;
            opacity: 0.9;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .metadata {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        .metadata p {{
            margin: 5px 0;
            font-size: 14px;
            color: #666;
        }}
        .page-section {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .page-header {{
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        .page-header h2 {{
            color: #667eea;
            font-size: 32px;
        }}
        .page-metadata {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .page-metadata a {{
            color: #667eea;
            text-decoration: none;
        }}
        .page-metadata a:hover {{
            text-decoration: underline;
        }}
        .page-content {{
            line-height: 1.8;
        }}
        .page-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .page-content h1, .page-content h2, .page-content h3 {{
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
        }}
        .page-content p {{
            margin-bottom: 16px;
        }}
        .page-content a {{
            color: #667eea;
            text-decoration: none;
        }}
        .page-content a:hover {{
            text-decoration: underline;
        }}
        .toc {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .toc h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        .toc ul {{
            list-style: none;
            padding: 0;
        }}
        .toc li {{
            margin: 10px 0;
        }}
        .toc a {{
            display: block;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 4px;
            color: #333;
            transition: background 0.2s;
            text-decoration: none;
        }}
        .toc a:hover {{
            background: #e9ecef;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin-top: 60px;
        }}
        .footer p {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 {domain}</h1>
        <p>Aggregated Website Content</p>
    </div>

    <div class="container">
        <div class="metadata">
            <p><strong>Website:</strong> {domain}</p>
            <p><strong>Generated:</strong> {timestamp}</p>
            <p><strong>Total Pages:</strong> {total_pages}</p>
        </div>

        <div class="toc">
            <h2>📋 Table of Contents</h2>
            <ul>
{toc_html}            </ul>
        </div>

{sections_html}
    </div>

    <div class="footer">
        <p>Generated by SiteSlayer Web Scraper</p>
        <p>Content aggregated from {total_pages} pages</p>
    </div>
</body>
</html>'''
    
    return html


def get_page_icon(title):
    """Get appropriate emoji icon based on page title"""
    title_lower = title.lower()
    
    if 'bounce' in title_lower or 'bouncer' in title_lower:
        return '🏰'
    elif 'water' in title_lower or 'slide' in title_lower:
        return '💦'
    elif 'game' in title_lower or 'interactive' in title_lower:
        return '🎮'
    elif 'mechanical' in title_lower or 'ride' in title_lower or 'carnival' in title_lower:
        return '🎡'
    elif 'obstacle' in title_lower or 'course' in title_lower:
        return '🏃'
    elif 'home' in title_lower or 'main' in title_lower:
        return '🏠'
    elif 'tent' in title_lower or 'table' in title_lower or 'chair' in title_lower:
        return '⛺'
    elif 'food' in title_lower or 'concession' in title_lower:
        return '🍿'
    elif 'train' in title_lower:
        return '🚂'
    elif 'entertainment' in title_lower:
        return '🎭'
    else:
        return '📄'


def format_markdown_to_simple_html(content):
    """
    Convert basic markdown to HTML (simple version)
    Handles: headers, paragraphs, images, links, bold, italic
    """
    import re
    
    lines = content.split('\n')
    html_lines = []
    in_paragraph = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            continue
        
        # Headers
        if line.startswith('# '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
        # Images
        elif line.startswith('!['):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt_text, url = match.groups()
                html_lines.append(f'<img src="{url}" alt="{alt_text}">')
        # Regular paragraphs
        else:
            # Process inline formatting
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
            
            if not in_paragraph:
                html_lines.append('<p>')
                in_paragraph = True
            html_lines.append(line + ' ')
    
    if in_paragraph:
        html_lines.append('</p>')
    
    return '\n'.join(html_lines)
