# Demo Site Creator - User Guide

## Overview

The **Demo Site Creator** is a powerful tool that creates a local HTML copy of any website's homepage with all URLs converted to absolute references. This is perfect for showcasing AI chatbot integrations to customers without modifying their live site.

## Use Case

You want to show a customer what their website would look like with your AI chatbot installed, without needing:
- Access to their server
- Modifications to their live site
- Complex setup or hosting

## How It Works

1. **Fetches** the target website's homepage HTML
2. **Converts** all relative URLs to absolute URLs (pointing back to the original site)
3. **Injects** your chatbot code (optional)
4. **Saves** a single HTML file that you can open locally

### What Gets Converted

- ✅ `<script src="/js/app.js">` → `<script src="https://example.com/js/app.js">`
- ✅ `<link href="style.css">` → `<link href="https://example.com/style.css">`
- ✅ `<img src="./image.png">` → `<img src="https://example.com/image.png">`
- ✅ Background images in CSS and inline styles
- ✅ Video/audio sources, iframes, forms, and anchors
- ✅ Srcset attributes for responsive images

## Installation

No additional dependencies needed beyond the existing SiteSlayer requirements!

## Usage

### Basic Usage (No Chatbot)

Creates a demo site with a placeholder for chatbot code:

```bash
python web_scraper/demo_site_creator.py https://customersite.com
```

**Output:**
- File: `web_scraper/demo_sites/customersite_com/index.html`
- Contains: HTML with all absolute URLs + chatbot placeholder comment

### With Chatbot Injection

Automatically inject your chatbot code:

```bash
python web_scraper/demo_site_creator.py https://customersite.com --chatbot web_scraper/chatbot_example.js
```

Or use your own chatbot file:

```bash
python web_scraper/demo_site_creator.py https://customersite.com --chatbot path/to/your-chatbot.js
```

### Custom Output Directory

Specify a custom output location:

```bash
python web_scraper/demo_site_creator.py https://customersite.com --output custom_demos
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `url` | - | Target website URL (required) | - |
| `--chatbot` | `-c` | Path to chatbot JS file to inject | None |
| `--output` | `-o` | Output directory | `web_scraper/demo_sites` |

## Example Workflow

### 1. Create Demo Site

```bash
python web_scraper/demo_site_creator.py https://example.com --chatbot web_scraper/chatbot_example.js
```

### 2. View in Browser

Open the generated file:
```
web_scraper/demo_sites/example_com/index.html
```

### 3. Share with Customer

The customer will see:
- Their exact website design
- All styling and functionality preserved
- Your AI chatbot widget in the corner
- Everything works just like the live site

## Chatbot Integration

### Using the Example Chatbot

A sample chatbot widget is included at `web_scraper/chatbot_example.js`. It features:
- 💬 Toggle button in bottom-right corner
- Modern, professional UI
- Fully self-contained (no external dependencies)
- Easy to customize

### Using Your Own Chatbot

Replace the example with your actual chatbot code. Your file should:

1. Be valid JavaScript
2. Initialize automatically when loaded
3. Create its own UI elements
4. Handle positioning (suggest bottom-right corner)

**Example structure:**

```javascript
(function() {
    'use strict';
    
    // Your chatbot initialization code
    // Create UI elements
    // Add event listeners
    // Connect to your backend
    
    console.log('Chatbot loaded!');
})();
```

### Manual Injection

If you don't use the `--chatbot` flag, the script adds a placeholder comment:

```html
<!-- AI CHATBOT INJECTION POINT -->
<!-- Insert your chatbot code here -->
</body>
```

You can then manually edit the HTML file and paste your chatbot code.

## Output Structure

After running the tool:

```
web_scraper/
└── demo_sites/
    └── example_com/
        └── index.html (demo site with chatbot)
```

## Important Notes

### ✅ Advantages

- **Fast**: No downloads, just one HTML fetch
- **Accurate**: Looks exactly like the original site
- **Portable**: Single file, easy to share
- **No backend**: Works offline after creation
- **Safe**: No modifications to live site

### ⚠️ Limitations

- **Assets load from original site**: Requires internet connection when viewing
- **Homepage only**: Only captures the homepage (not subpages)
- **Dynamic content**: JavaScript-generated content may not work perfectly
- **CORS**: Some sites may block cross-origin requests for assets
- **Links functional**: All links point to the real site (customer might navigate away)

### 🔒 Privacy & Security

- Original site assets remain on their servers
- No data is stored or transmitted
- Customer's site is not modified
- Perfect for demos and presentations

## Troubleshooting

### Issue: Assets Not Loading

**Problem**: Images, CSS, or JS fail to load

**Solutions:**
1. Check if the original site blocks cross-origin requests (CORS)
2. Try opening the HTML file via a local web server instead of `file://`
3. Use the original `homepage_duplicate.py` to download assets locally

**Local server example:**
```bash
cd web_scraper/demo_sites/example_com
python -m http.server 8000
# Open: http://localhost:8000
```

### Issue: Chatbot Not Appearing

**Problem**: Chatbot code doesn't execute

**Solutions:**
1. Check browser console for JavaScript errors (F12)
2. Verify your chatbot file path is correct
3. Ensure chatbot code is valid JavaScript
4. Check if original site's Content Security Policy blocks inline scripts

### Issue: Site Looks Broken

**Problem**: Layout or styling issues

**Solutions:**
1. Original site may use relative URLs in JavaScript-generated CSS
2. Some sites require specific headers or cookies
3. Try the example.com first to verify tool is working
4. Check if site requires authentication

### Issue: "Failed to fetch homepage"

**Problem**: Can't download the site

**Solutions:**
1. Check your internet connection
2. Verify the URL is correct and accessible
3. Some sites block automated requests - try adding the URL to your browser first
4. Site may be behind a firewall or require authentication

## Advanced Usage

### Batch Processing

Create demos for multiple sites:

```bash
# Create a script
for url in https://site1.com https://site2.com https://site3.com
do
    python web_scraper/demo_site_creator.py "$url" --chatbot web_scraper/chatbot_example.js
done
```

### Custom Modifications

After generating the demo site, you can manually edit the HTML to:
- Remove certain elements (e.g., existing chatbots)
- Add custom CSS for your branding
- Inject additional analytics or tracking
- Modify the chatbot appearance

### Integration with Other Tools

Combine with other SiteSlayer features:

```bash
# 1. Create demo with chatbot
python web_scraper/demo_site_creator.py https://example.com --chatbot chatbot.js

# 2. Also create full offline backup
python web_scraper/homepage_duplicate.py https://example.com

# 3. Scrape entire site to markdown
python web_scraper/main.py https://example.com
```

## Best Practices

### For Sales Demos

1. **Test first**: Create demo with example.com to ensure it works
2. **Use customer's live site**: Shows real data and design
3. **Customize chatbot**: Match customer's brand colors
4. **Prepare backup**: Have screenshots ready if live assets fail
5. **Have story ready**: Explain how the integration works

### For Development

1. **Version control**: Keep different versions of your chatbot
2. **Test locally**: Use local server to test properly
3. **Respect robots.txt**: Don't scrape sites that prohibit it
4. **Get permission**: Inform customers you're creating a demo

### For Sharing

1. **Zip the file**: Easy to email or share
2. **Include instructions**: Tell customer how to open it
3. **Host online**: Upload to simple hosting for live links
4. **Record video**: Show customer a recording if they can't run HTML

## Comparison: Demo Site vs. Full Duplicate

| Feature | Demo Site Creator | Homepage Duplicator |
|---------|------------------|---------------------|
| Speed | ⚡ Very Fast | 🐢 Slower (downloads assets) |
| File Size | 📄 Small (KB) | 📦 Large (MB) |
| Internet Required | ✅ Yes | ❌ No |
| Perfect for | Quick demos | Offline backups |
| Asset Quality | Original quality | Preserved locally |

## Support

If you encounter issues:

1. Check this guide first
2. Verify your Python and dependencies are up to date
3. Test with a simple site (example.com)
4. Check the console logs for detailed error messages

## Examples

### Example 1: Quick Demo

```bash
python web_scraper/demo_site_creator.py https://apple.com
```

### Example 2: Full Featured Demo

```bash
python web_scraper/demo_site_creator.py https://shopify.com --chatbot my_ai_bot.js --output client_demos
```

### Example 3: Multiple Demos

```bash
python web_scraper/demo_site_creator.py https://client1.com --chatbot chatbot.js
python web_scraper/demo_site_creator.py https://client2.com --chatbot chatbot.js
python web_scraper/demo_site_creator.py https://client3.com --chatbot chatbot.js
```

---

## Quick Start Checklist

- [ ] Install SiteSlayer dependencies: `pip install -r requirements.txt`
- [ ] Test with example: `python web_scraper/demo_site_creator.py https://example.com`
- [ ] Create your chatbot JS file (or use the example)
- [ ] Run with customer's URL: `python web_scraper/demo_site_creator.py https://customersite.com --chatbot chatbot.js`
- [ ] Open generated HTML file in browser
- [ ] Show customer the demo!

---

**Happy demoing! 🚀**

For more information about SiteSlayer, see the main [README.md](README.md).
