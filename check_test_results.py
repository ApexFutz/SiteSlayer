"""
Quick script to check scraping results from the websites directory
"""
from pathlib import Path
import os

def check_results():
    """Check all scraped websites and count pages"""
    websites_dir = Path('websites')
    
    if not websites_dir.exists():
        print("No websites directory found!")
        return
    
    print("\n" + "="*80)
    print("SCRAPED WEBSITES SUMMARY")
    print("="*80 + "\n")
    
    sites = []
    
    for site_dir in sorted(websites_dir.iterdir()):
        if site_dir.is_dir():
            # Count markdown files
            md_files = list(site_dir.glob('*.md'))
            file_count = len(md_files)
            
            # Get total size
            total_size = sum(f.stat().st_size for f in md_files)
            size_kb = total_size / 1024
            
            sites.append({
                'name': site_dir.name,
                'pages': file_count,
                'size_kb': size_kb
            })
    
    if not sites:
        print("No scraped sites found yet.")
        return
    
    # Print table
    print(f"{'#':<4} {'Site':<40} {'Pages':<8} {'Size (KB)':<12}")
    print("-" * 80)
    
    for i, site in enumerate(sites, 1):
        print(f"{i:<4} {site['name']:<40} {site['pages']:<8} {site['size_kb']:<12.1f}")
    
    # Summary
    total_sites = len(sites)
    total_pages = sum(s['pages'] for s in sites)
    total_size = sum(s['size_kb'] for s in sites)
    
    print("\n" + "-" * 80)
    print(f"Total Sites: {total_sites}")
    print(f"Total Pages: {total_pages}")
    print(f"Total Size: {total_size:.1f} KB ({total_size/1024:.1f} MB)")
    print(f"Average Pages per Site: {total_pages/total_sites if total_sites > 0 else 0:.1f}")
    print("="*80 + "\n")

if __name__ == "__main__":
    check_results()
