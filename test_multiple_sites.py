"""
Test script to evaluate SiteSlayer performance across multiple websites
"""
import subprocess
import time
from datetime import datetime

# Test sites - diverse set of website types
TEST_SITES = [
    "https://www.example.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.reddit.com",
    "https://www.stackoverflow.com",
    "https://www.npmjs.com",
    "https://www.mozilla.org",
    "https://www.w3.org",
    "https://www.eff.org",
    "https://www.apache.org"
]

def run_scraper(url):
    """Run the scraper on a single URL and track performance"""
    print(f"\n{'='*80}")
    print(f"Testing: {url}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ['python', 'web_scraper/main.py', url],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per site
        )
        
        elapsed_time = time.time() - start_time
        
        # Parse output for results
        output = result.stdout
        success = "SCRAPING COMPLETE" in output
        
        # Extract page count
        pages_scraped = 0
        for line in output.split('\n'):
            if "Total pages scraped:" in line:
                try:
                    pages_scraped = int(line.split(":")[-1].strip())
                except:
                    pass
        
        return {
            'url': url,
            'success': success,
            'pages_scraped': pages_scraped,
            'time_elapsed': elapsed_time,
            'error': None
        }
        
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        return {
            'url': url,
            'success': False,
            'pages_scraped': 0,
            'time_elapsed': elapsed_time,
            'error': 'Timeout (>5 minutes)'
        }
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            'url': url,
            'success': False,
            'pages_scraped': 0,
            'time_elapsed': elapsed_time,
            'error': str(e)
        }

def main():
    """Run tests on all sites and generate report"""
    print("\n" + "="*80)
    print("SiteSlayer Multi-Site Performance Test")
    print(f"Testing {len(TEST_SITES)} websites")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    results = []
    
    for i, url in enumerate(TEST_SITES, 1):
        print(f"\n[{i}/{len(TEST_SITES)}] Starting test for: {url}")
        result = run_scraper(url)
        results.append(result)
        
        # Print quick summary
        if result['success']:
            print(f"[SUCCESS] {result['pages_scraped']} pages in {result['time_elapsed']:.1f}s")
        else:
            print(f"[FAILED] {result.get('error', 'Unknown error')}")
    
    # Generate final report
    print("\n\n" + "="*80)
    print("FINAL REPORT")
    print("="*80)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    total_pages = sum(r['pages_scraped'] for r in results)
    total_time = sum(r['time_elapsed'] for r in results)
    
    print(f"\nOverall Statistics:")
    print(f"  Total Sites Tested: {len(results)}")
    print(f"  Successful: {successful} ({successful/len(results)*100:.1f}%)")
    print(f"  Failed: {failed} ({failed/len(results)*100:.1f}%)")
    print(f"  Total Pages Scraped: {total_pages}")
    print(f"  Total Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"  Average Time per Site: {total_time/len(results):.1f}s")
    
    print(f"\nDetailed Results:")
    print(f"{'#':<4} {'URL':<35} {'Status':<10} {'Pages':<8} {'Time (s)':<10}")
    print("-" * 80)
    
    for i, r in enumerate(results, 1):
        status = "SUCCESS" if r['success'] else "FAILED"
        url_short = r['url'][:35]
        print(f"{i:<4} {url_short:<35} {status:<10} {r['pages_scraped']:<8} {r['time_elapsed']:<10.1f}")
        if r['error']:
            print(f"     Error: {r['error']}")
    
    print("\n" + "="*80)
    print(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
