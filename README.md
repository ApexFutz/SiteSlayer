# SiteSlayer

SiteSlayer is a web scraping and site replication tool that automatically scrapes websites, generates email content, and serves mock versions of scraped pages with an embedded AI chatbot.

## Setup

Before you can use SiteSlayer, you'll need to install a few tools and set up some credentials:

### 1. Install Fly.io

Fly.io is used to deploy the web server. Install it by following the instructions at: https://fly.io/docs/getting-started/installing-flyctl/

### 2. Install Git

Git is used for version control. If you don't have it installed:
- **macOS**: `brew install git` or download from https://git-scm.com/download/mac
- **Linux**: `sudo apt-get install git` (Ubuntu/Debian) or use your distribution's package manager
- **Windows**: Download from https://git-scm.com/download/win

### 3. Install uv

uv is the Python package manager used by this project. Install it by following the instructions at: https://github.com/astral-sh/uv

### 4. Get OpenAI API Key

You'll need an OpenAI API key for the AI-powered features (link ranking and chatbot):

1. Sign up or log in at https://platform.openai.com/
2. Navigate to API Keys section
3. Create a new API key
4. Add it as a GitHub Secret:
   - Go to your GitHub repository settings
   - Navigate to Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
   - Click "Add secret"

Once these are set up, everything else should work automatically!

## How It Works

### Basic Workflow

1. Edit `sites_to_scrape.txt` to add, remove, or modify the list of websites you want to scrape
2. Run the deploy script: `./scripts/deploy_server.sh`
3. The system will:
   - Automatically scrape the websites listed in `sites_to_scrape.txt`
   - Generate email content for each site
   - Deploy the updated web server to Fly.io

### Main Components

**URL Scraper** (`web_scraper/`)
- Crawls websites and extracts HTML content
- Converts pages to markdown format
- Uses AI to rank and prioritize important links
- Stores scraped content in the `sites/` directory

**Web Server** (`website_server/`)
- Serves mock versions of the scraped webpages
- Displays the home page showing all sites from `sites_to_scrape.txt`
- Shows generated emails for each site
- Embeds a chatbot widget on each page

**Chat Bot** (`website_server/chat_bot/`)
- AI-powered chatbot that uses the scraped content
- Provides interactive chat experience on scraped pages
- Answers questions based on the content from each site

**Email Generator** (`web_scraper/email_writer.py`)
- Generates email content based on scraped website data
- Creates personalized email templates for each site

## File Structure

- `sites_to_scrape.txt` - List of URLs to scrape (one per line, comments with `#`)
- `sites/` - Directory containing scraped content for each site
- `web_scraper/` - Scraping and content extraction logic
- `website_server/` - FastAPI server for serving scraped pages
- `scripts/deploy_server.sh` - Deployment script

## Customization

All components are editable and modifiable. The system is designed to be as simple as possible while remaining flexible:

- Modify scraping behavior in `web_scraper/`
- Customize the web server in `website_server/main.py`
- Adjust chatbot behavior in `website_server/agent.py`
- Update email generation in `web_scraper/email_writer.py`

## Notes

- The scraper automatically runs via GitHub Actions when `sites_to_scrape.txt` is modified
- The web server deploys automatically when other files are pushed to the main branch
- Scraped content is stored locally in the `sites/` directory, organized by domain name

