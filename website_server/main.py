"""
FastAPI web server for serving scraped sites from the sites/ directory.
"""
<<<<<<< Updated upstream
=======
import html
import os
import re
>>>>>>> Stashed changes
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SiteSlayer Web Server")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory (project root)
BASE_DIR = Path(__file__).parent.parent
SITES_DIR = BASE_DIR / "sites"


@app.get("/site/{site_path:path}")
async def serve_site(site_path: str):
    """
    Serve a site from the sites/ directory.
    
    Args:
        site_path: The site identifier (e.g., 'www.bigthunderevents.com')
                   Can include subdirectories if needed (e.g., 'www.example.com/subdir')
    
    Returns:
        The index.html file from the corresponding site directory.
    """
    # Normalize the path to prevent directory traversal attacks
    # Remove any leading/trailing slashes and normalize
    site_path = site_path.strip("/")
    
    # Prevent directory traversal
    if ".." in site_path or site_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid site path")
    
    # Construct the path to the site directory
    site_dir = SITES_DIR / site_path
    
    # Check if the directory exists
    if not site_dir.exists() or not site_dir.is_dir():
        raise HTTPException(
            status_code=404,
            detail=f"Site '{site_path}' not found in sites directory"
        )
    
    # Look for index.html in the site directory
    index_file = site_dir / "index.html"
    
    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"index.html not found for site '{site_path}'"
        )
    
    # Serve the HTML file
    return FileResponse(
        index_file,
        media_type="text/html",
        headers={"Cache-Control": "no-cache"}
    )


<<<<<<< Updated upstream
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "SiteSlayer Web Server",
        "endpoints": {
            "serve_site": "/site/{site_path}",
            "example": "/site/www.bigthunderevents.com"
        }
    }
=======
def extract_title_and_description(site_name: str) -> tuple[str, str]:
    """Extract title and description from content.md file."""
    content_file = SITES_DIR / site_name / "content.md"
    
    title = site_name.replace("_", " ").replace("www ", "").title()
    description = "Scraped website content"
    
    if content_file.exists():
        try:
            with open(content_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Find first heading (title)
            for line in lines:
                if line.startswith("# ") and not line.startswith("## "):
                    title = line.replace("# ", "").strip()
                    break
            
            # Find first paragraph (description)
            in_metadata = True
            for i, line in enumerate(lines):
                line = line.strip()
                # Skip metadata section
                if in_metadata and (line.startswith("#") or line.startswith("**") or line.startswith("---") or line == ""):
                    if line.startswith("---") and i > 5:  # Second --- marks end of metadata
                        in_metadata = False
                    continue
                
                # Get first non-empty, non-special line as description
                if not in_metadata and line and not line.startswith("#") and not line.startswith("**") and not line.startswith("["):
                    description = line[:100] + ("..." if len(line) > 100 else "")
                    break
        except Exception as e:
            pass
    
    return title, description


@app.get("/api/sites")
async def get_sites_api():
    """API endpoint returning sites data as JSON."""
    websites = []
    if SITES_DIR.exists() and SITES_DIR.is_dir():
        for item in sorted(SITES_DIR.iterdir()):
            if item.is_dir():
                index_file = item / "index.html"
                if index_file.exists():
                    site_name = item.name
                    title, description = extract_title_and_description(site_name)
                    websites.append({
                        "name": site_name,
                        "title": title,
                        "description": description,
                        "url": f"/site/{site_name}"
                    })
    
    return {"sites": websites}


@app.get("/")
async def root():
    """Root endpoint with improved homepage."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SiteSlayer - Website Repository</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 60px;
            padding: 40px 20px;
        }
        
        header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: -1px;
        }
        
        header .subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 300;
            margin-bottom: 30px;
        }
        
        .search-container {
            display: flex;
            justify-content: center;
            margin-bottom: 40px;
        }
        
        .search-box {
            width: 100%;
            max-width: 500px;
            padding: 15px 25px;
            font-size: 1rem;
            border: none;
            border-radius: 50px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .search-box:focus {
            outline: none;
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }
        
        .search-box::placeholder {
            color: #999;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            text-decoration: none;
            color: inherit;
        }
        
        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
        }
        
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 24px;
            color: white;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 8px;
            word-break: break-word;
        }
        
        .card-body {
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .card-description {
            font-size: 0.95rem;
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
            flex-grow: 1;
        }
        
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
        }
        
        .card-link {
            display: inline-flex;
            align-items: center;
            color: #667eea;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            font-size: 0.95rem;
        }
        
        .card-link:hover {
            color: #764ba2;
            gap: 8px;
        }
        
        .card-link::after {
            content: "→";
            margin-left: 8px;
            transition: margin 0.2s ease;
        }
        
        .card-link:hover::after {
            margin-left: 12px;
        }
        
        .site-name {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.8);
            font-family: 'Courier New', monospace;
            margin-top: 10px;
        }
        
        .no-results {
            grid-column: 1 / -1;
            text-align: center;
            padding: 40px;
            color: white;
        }
        
        .no-results h2 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        
        footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            margin-top: 40px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .stat {
            text-align: center;
            color: white;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 2.5rem;
            }
            
            header .subtitle {
                font-size: 1rem;
            }
            
            .grid {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            
            .stats {
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ SiteSlayer</h1>
            <p class="subtitle">Explore scraped websites from across the web</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number" id="siteCount">0</span>
                    <span class="stat-label">Websites</span>
                </div>
            </div>
        </header>
        
        <div class="search-container">
            <input 
                type="text" 
                class="search-box" 
                id="searchInput" 
                placeholder="🔍 Search sites by name or description..."
            >
        </div>
        
        <div class="grid" id="sitesGrid"></div>
        
        <footer>
            <p>&copy; 2025 SiteSlayer. Powered by web scraping technology.</p>
        </footer>
    </div>
    
    <script>
        let allSites = [];
        
        async function loadSites() {
            try {
                const response = await fetch('/api/sites');
                const data = await response.json();
                allSites = data.sites;
                
                document.getElementById('siteCount').textContent = allSites.length;
                renderSites(allSites);
            } catch (error) {
                console.error('Error loading sites:', error);
                const grid = document.getElementById('sitesGrid');
                grid.innerHTML = '<div class="no-results"><h2>Error loading sites</h2></div>';
            }
        }
        
        function renderSites(sites) {
            const grid = document.getElementById('sitesGrid');
            
            if (sites.length === 0) {
                grid.innerHTML = '<div class="no-results"><h2>No sites found</h2><p>Try adjusting your search.</p></div>';
                return;
            }
            
            grid.innerHTML = sites.map(site => `
                <a href="${site.url}" class="card">
                    <div class="card-header">
                        <h2 class="card-title">${escapeHtml(site.title)}</h2>
                        <div class="site-name">${escapeHtml(site.name)}</div>
                    </div>
                    <div class="card-body">
                        <p class="card-description">${escapeHtml(site.description)}</p>
                        <div class="card-footer">
                            <a href="${site.url}" class="card-link">Visit Site</a>
                        </div>
                    </div>
                </a>
            `).join('');
        }
        
        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        }
        
        function filterSites() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            if (!searchTerm) {
                renderSites(allSites);
                return;
            }
            
            const filtered = allSites.filter(site => 
                site.title.toLowerCase().includes(searchTerm) ||
                site.description.toLowerCase().includes(searchTerm) ||
                site.name.toLowerCase().includes(searchTerm)
            );
            
            renderSites(filtered);
        }
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterSites);
        
        // Load sites on page load
        loadSites();
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html_content)
>>>>>>> Stashed changes


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

