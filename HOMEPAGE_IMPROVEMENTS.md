# Homepage Improvements - SiteSlayer

## Overview
The SiteSlayer homepage has been completely redesigned to be more modern, ergonomic, and user-friendly.

## Features Implemented

### 1. **Responsive Card Grid Layout**
- Converts the primitive link list into a modern responsive grid
- Cards automatically adjust from 3 columns on desktop → 1 column on mobile
- Minimum card width: 300px with intelligent spacing
- Smooth hover animations with elevation effects

### 2. **Metadata Extraction**
- **New API Endpoint**: `/api/sites` returns sites data as JSON
- Automatically extracts titles from `content.md` (first H1 heading)
- Extracts descriptions (first paragraph, truncated to 100 characters)
- Fallback to friendly site names if metadata extraction fails
- Sorts sites alphabetically for consistency

### 3. **Modern Visual Design**
- **Gradient Background**: Purple gradient (667eea → 764ba2) for visual depth
- **Card Styling**:
  - Smooth shadows that increase on hover (0 4px 15px → 0 12px 30px)
  - Gradient header matching the page theme
  - 12px border radius for modern appearance
  - Hover elevation: cards lift 8px with enhanced shadows
- **Typography**: System fonts with proper hierarchy and weights
- **Color Scheme**: Harmonious purple/lavender with white cards

### 4. **Client-Side Search Functionality**
- Real-time search bar at the top of the page
- Searches across:
  - Site titles
  - Descriptions
  - Directory names
- Case-insensitive filtering
- Instant visual feedback with no page reload
- Beautiful placeholder text with search icon

### 5. **SiteSlayer Branding**
- Bold header with lightning bolt emoji (⚡) 
- Large, prominent title: "⚡ SiteSlayer"
- Subtitle: "Explore scraped websites from across the web"
- Live counter showing total number of available sites
- Professional footer

### 6. **Responsive Design**
- **Desktop**: 
  - 3-column grid layout
  - Full header with large typography
  - Optimized spacing
- **Tablet/Mobile**: 
  - Single column card layout
  - Reduced header size
  - Touch-friendly card sizes
  - Adjusted spacing and gaps

## Technical Details

### New Endpoint
```
GET /api/sites
```
Returns:
```json
{
  "sites": [
    {
      "name": "example_com",
      "title": "Example Domain",
      "description": "This domain is for use in documentation examples...",
      "url": "/site/example_com"
    }
  ]
}
```

### Helper Function
`extract_title_and_description(site_name: str)` - Parses `content.md` files to extract human-readable titles and descriptions.

### JavaScript Features
- Async site loading with error handling
- Dynamic HTML injection with XSS protection (HTML escaping)
- Real-time search filtering
- Smooth transitions and animations

## Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive with touch-friendly elements
- CSS Grid and Flexbox for layout

## File Modified
- `website_server/main.py` - Added new endpoint and improved homepage HTML/CSS/JS

## How to Deploy
Simply redeploy the application. The changes are backward compatible and don't require any data migration.

```bash
# If running locally
uvicorn website_server.main:app --reload

# Then visit http://localhost:8000
```

## Performance Notes
- Zero external dependencies (all CSS and JS is inline)
- Fast client-side rendering with no page reloads during search
- Metadata extraction happens server-side but is cached efficiently
- Sites loaded asynchronously for better UX
