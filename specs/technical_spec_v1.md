# Technical Specification - Version 1.1
# Bali Restaurant Food Safety Checker

**Document Version:** 1.1
**Date:** October 5, 2025
**Status:** Draft
**Last Updated:** October 5, 2025 (Updated for Apify API integration)

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Data Structures](#data-structures)
4. [Component Specifications](#component-specifications)
5. [Google Maps URL Parsing](#google-maps-url-parsing)
6. [Detection Engine](#detection-engine)
7. [Dashboard Implementation Options](#dashboard-implementation-options)
8. [File Structure](#file-structure)
9. [API Integration Details](#api-integration-details)
10. [Error Handling](#error-handling)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────┐
│   User Input    │
│  (Google Maps   │
│      URL)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  URL Validator  │
│  (Basic check)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Apify Client   │
│  Fetch Reviews  │
│ (Last 6 months, │
│   max 1000)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Detection     │
│    Engine       │
│ (Regex Match)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Data          │
│   Processor     │
│ (Calculate KPIs │
│  & Timeline)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
│   Renderer      │
│  (Display UI)   │
└─────────────────┘
```

### Component Flow

**Step 1: Input → URL Validator**
- User provides Google Maps URL
- Validator performs basic format check
- Confirms it's a Google Maps restaurant URL

**Step 2: Validator → Apify Client**
- Full Google Maps URL sent directly to Apify API
- No need to extract place ID (Apify handles this)
- Configure API to fetch:
  - Maximum 1000 reviews
  - From last 6 months only
  - Sorted by newest first
- API returns restaurant details + filtered reviews

**Step 3: Apify Client → Detection Engine**
- Reviews passed to detection engine
- Each review scanned for keywords
- Flagged reviews collected

**Step 4: Detection Engine → Data Processor**
- Calculate total mentions (from 6-month dataset)
- Calculate this month's mentions
- Group mentions by month for 6-month timeline

**Step 5: Data Processor → Dashboard**
- Pass processed data to dashboard
- Render KPIs, chart, and review list

---

## Technology Stack

### Core Technologies

**Language:** Python 3.9+

**Required Libraries:**
```
apify-client==1.6.0       # Apify API client
python-dotenv==1.0.0      # Environment variable management
```

**Additional Libraries (depending on dashboard choice):**

**Option A: Streamlit** (Recommended for V1)
```
streamlit==1.29.0         # Dashboard framework
plotly==5.18.0           # Interactive charts
```

**Option B: Flask + Chart.js**
```
flask==3.0.0             # Web framework
```

**Option C: CLI (Minimal)**
```
rich==13.7.0             # Terminal formatting
```

### Why These Choices?

**Python:**
- Already using for API integration
- Great for data processing
- Rich ecosystem for dashboards

**Streamlit (Recommended):**
- ✅ Fastest development time
- ✅ Built for data dashboards
- ✅ Built-in charting
- ✅ No HTML/CSS/JS knowledge needed
- ✅ Auto-refreshing UI
- ❌ Less customizable than Flask

**Flask (Alternative):**
- ✅ More flexible/customizable
- ✅ Better for production apps
- ❌ Requires HTML/CSS/JS knowledge
- ❌ Slower development

**CLI (Simplest):**
- ✅ No web server needed
- ✅ Fastest to build
- ❌ Limited visualization options
- ❌ Less user-friendly

---

## Data Structures

### Restaurant Data Model

```python
{
    "place_id": "ChIJXxe2rXNH0i0Rnt_qeoqnQcc",
    "name": "Uma Garden Seminyak",
    "address": "Jl. Umalas 1 No.8, Kerobokan Kelod...",
    "rating": 4.7,
    "total_reviews": 1352,
    "reviews": [
        # List of Review objects (see below)
    ]
}
```

### Review Data Model

```python
{
    "author": "Sarah Verrall",
    "rating": 5,
    "text": "Wow! What a stunning restaurant...",
    "time": "in the last week",
    "publish_time": "2025-09-28T10:30:00Z",  # ISO format
    "relative_time": "in the last week"
}
```

### Flagged Review Data Model

```python
{
    "author": "John Doe",
    "rating": 2,
    "text": "Got terrible food poisoning after eating here...",
    "time": "2 months ago",
    "publish_time": "2025-08-05T14:20:00Z",
    "matched_keywords": ["food poisoning", "terrible"],
    "month": "Aug 2025"  # For timeline grouping
}
```

### Analysis Results Model

```python
{
    "restaurant": {
        # Restaurant data (see above)
    },
    "analyzed_reviews_count": 847,  # Total reviews analyzed from 6-month period
    "flagged_reviews": [
        # List of flagged reviews from last 6 months
    ],
    "total_mentions": 12,          # Count of flagged reviews (last 6 months)
    "mentions_this_month": 3,      # Count from current month only
    "monthly_timeline": {
        "Apr 2025": 0,
        "May 2025": 2,
        "Jun 2025": 1,
        "Jul 2025": 0,
        "Aug 2025": 3,
        "Sep 2025": 1,
        # Only last 6 months shown
    }
}
```

---

## Component Specifications

### 1. URL Validator Module

**File:** `utils/url_validator.py`

**Purpose:** Validate Google Maps restaurant URLs

**Functions:**

```python
def validate_google_maps_url(url: str) -> bool:
    """
    Validate if URL is a Google Maps URL

    Note: Apify accepts full Google Maps URLs directly,
    so we only need basic validation, not place_id extraction

    Args:
        url: URL string to validate

    Returns:
        bool: True if valid Google Maps URL

    Raises:
        ValueError: If URL is not a valid Google Maps URL
    """
    pass
```

**Implementation Details:**

Since Apify accepts full Google Maps URLs directly, we only need simple validation:

**Accepted URL Formats:**
```
https://www.google.com/maps/place/...
https://maps.google.com/...
https://goo.gl/maps/...
https://maps.app.goo.gl/...
```

**Simple Validation Strategy:**

```python
def validate_google_maps_url(url: str) -> bool:
    """Simple validation - check if URL contains Google Maps domains"""

    valid_patterns = [
        'google.com/maps',
        'maps.google.com',
        'goo.gl/maps',
        'maps.app.goo.gl'
    ]

    # Check if URL contains any valid Google Maps pattern
    is_valid = any(pattern in url.lower() for pattern in valid_patterns)

    if not is_valid:
        raise ValueError("Invalid Google Maps URL. Please provide a valid restaurant link from Google Maps.")

    return True

# Example usage:
url = "https://www.google.com/maps/place/Restaurant+Name/..."
validate_google_maps_url(url)  # Returns True or raises ValueError
```

---

### 2. Apify API Client Module

**File:** `api/apify_client.py`

**Purpose:** Fetch restaurant reviews from Google Maps using Apify API

**Functions:**

```python
def fetch_restaurant_reviews(url: str, api_key: str) -> dict:
    """
    Fetch restaurant details and reviews from Google Maps via Apify

    Args:
        url: Full Google Maps restaurant URL
        api_key: Apify API key

    Returns:
        dict: Restaurant data with reviews from last 6 months (max 1000)
    """
    pass
```

**Implementation:**

```python
from apify_client import ApifyClient
from datetime import datetime, timedelta

def fetch_restaurant_reviews(url: str, api_key: str) -> dict:
    """
    Use Apify Google Maps Reviews Scraper to fetch reviews
    """
    # Initialize Apify client
    client = ApifyClient(api_key)

    # Calculate date 6 months ago
    six_months_ago = datetime.now() - timedelta(days=180)
    start_date = six_months_ago.strftime('%Y-%m-%d')

    # Configure scraper run
    run_input = {
        "startUrls": [url],
        "maxReviews": 1000,           # Cap at 1000 reviews
        "reviewsSort": "newest",       # Get most recent first
        "reviewsStartDate": start_date # Only last 6 months
    }

    # Run the Apify actor (Google Maps Reviews Scraper)
    # Actor ID: compass/google-maps-reviews-scraper
    run = client.actor("compass/google-maps-reviews-scraper").call(run_input=run_input)

    # Fetch results
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    return results[0] if results else None

# Example usage:
api_key = "your_apify_api_key"
url = "https://www.google.com/maps/place/..."
data = fetch_restaurant_reviews(url, api_key)
```

**Benefits of Apify:**
- ✅ Gets ALL reviews (not limited to 5)
- ✅ Accepts full Google Maps URLs (no place_id extraction needed)
- ✅ Supports date filtering (last 6 months)
- ✅ Supports review limits (max 1000)
- ✅ Returns structured data with all fields we need

---

### 3. Detection Engine Module

**File:** `engine/detector.py`

**Purpose:** Scan reviews for food poisoning keywords

**Functions:**

```python
def detect_food_poisoning(review_text: str, keywords: list) -> tuple:
    """
    Check if review contains food poisoning keywords

    Args:
        review_text: Full text of the review
        keywords: List of keyword patterns to match

    Returns:
        tuple: (is_flagged: bool, matched_keywords: list)
    """
    pass

def analyze_reviews(reviews: list, keywords: list) -> list:
    """
    Analyze all reviews and return flagged ones

    Args:
        reviews: List of review objects
        keywords: List of keyword patterns

    Returns:
        list: Flagged reviews with matched keywords
    """
    pass
```

**Implementation:**

```python
import re

def detect_food_poisoning(review_text: str, keywords: list) -> tuple:
    """
    Use regex to detect food poisoning keywords
    """
    matched_keywords = []

    # Convert to lowercase for case-insensitive matching
    text_lower = review_text.lower()

    for keyword in keywords:
        # Create case-insensitive regex pattern
        pattern = re.compile(keyword, re.IGNORECASE)

        if pattern.search(review_text):
            matched_keywords.append(keyword)

    is_flagged = len(matched_keywords) > 0

    return is_flagged, matched_keywords

def analyze_reviews(reviews: list, keywords: list) -> list:
    """
    Scan all reviews and collect flagged ones
    """
    flagged_reviews = []

    for review in reviews:
        review_text = review.get('text', '')
        is_flagged, matched = detect_food_poisoning(review_text, keywords)

        if is_flagged:
            flagged_review = review.copy()
            flagged_review['matched_keywords'] = matched
            flagged_reviews.append(flagged_review)

    return flagged_reviews
```

**Keywords List:** See `food_poisoning_keywords.md` for complete list

---

### 4. Data Processor Module

**File:** `engine/processor.py`

**Purpose:** Calculate KPIs and timeline data from flagged reviews

**Functions:**

```python
def calculate_kpis(flagged_reviews: list) -> dict:
    """
    Calculate total mentions and mentions in last 6 months
    """
    pass

def generate_timeline(flagged_reviews: list) -> dict:
    """
    Generate monthly timeline of mentions
    """
    pass
```

**Implementation:**

```python
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_kpis(flagged_reviews: list) -> dict:
    """
    Calculate KPI metrics
    """
    total_mentions = len(flagged_reviews)

    # Calculate mentions in last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    recent_mentions = 0

    for review in flagged_reviews:
        # Parse review date (need to convert relative time to date)
        review_date = parse_review_date(review.get('time'))

        if review_date >= six_months_ago:
            recent_mentions += 1

    return {
        'total_mentions': total_mentions,
        'mentions_last_6_months': recent_mentions
    }

def generate_timeline(flagged_reviews: list) -> dict:
    """
    Group mentions by month for timeline chart
    """
    timeline = {}

    for review in flagged_reviews:
        review_date = parse_review_date(review.get('time'))
        month_key = review_date.strftime('%b %Y')  # e.g., "Jan 2025"

        if month_key in timeline:
            timeline[month_key] += 1
        else:
            timeline[month_key] = 1

    return timeline

def parse_review_date(relative_time: str) -> datetime:
    """
    Convert relative time to datetime

    Examples:
      "in the last week" → 7 days ago
      "2 months ago" → 60 days ago
      "a year ago" → 365 days ago
    """
    # Implementation details for parsing relative dates
    # This is approximate - exact dates not available from API
    pass
```

---

## Google Maps URL Parsing

### URL Format Examples

**Example 1: Standard Place URL**
```
https://www.google.com/maps/place/Uma+Garden+Seminyak/@-8.6536049,115.1572823,17z/data=!3m1!4b1!4m6!3m5!1s0x2dd247b1b7e76c5f:0xc7419aa68ea8fade!8m2!3d-8.6536049!4d115.1598572!16s%2Fg%2F11c5z8qw7n
```

**Parsing Logic:**
- Look for `1s` parameter in the URL
- Extract the value after `1s`
- Format: `1s[PLACE_ID]`
- Place ID: `0x2dd247b1b7e76c5f:0xc7419aa68ea8fade`

**Example 2: Direct Place ID**
```
https://www.google.com/maps/place/?q=place_id:ChIJXxe2rXNH0i0Rnt_qeoqnQcc
```

**Parsing Logic:**
- Look for `place_id:` in URL
- Extract everything after the colon
- Place ID: `ChIJXxe2rXNH0i0Rnt_qeoqnQcc`

**Example 3: Shortened URL**
```
https://goo.gl/maps/abc123
```

**Parsing Logic:**
- Follow HTTP redirect
- Extract place ID from final destination URL
- Requires making HTTP request

### Implementation Code

```python
import re
import requests
from urllib.parse import urlparse, parse_qs

def extract_place_id(url: str) -> str:
    """
    Extract place ID from various Google Maps URL formats
    """
    # Validate it's a Google Maps URL
    if not ('google.com/maps' in url or 'goo.gl' in url or 'maps.app.goo.gl' in url):
        raise ValueError("Not a valid Google Maps URL")

    # Handle shortened URLs by following redirect
    if 'goo.gl' in url or 'maps.app.goo.gl' in url:
        response = requests.get(url, allow_redirects=True)
        url = response.url

    # Method 1: Look for place_id parameter
    if 'place_id:' in url:
        match = re.search(r'place_id:([A-Za-z0-9_-]+)', url)
        if match:
            return match.group(1)

    # Method 2: Extract from data parameter (1s format)
    match = re.search(r'!1s([A-Za-z0-9_:-]+)', url)
    if match:
        return match.group(1)

    # Method 3: Look in query parameters
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if 'place_id' in params:
        return params['place_id'][0]

    raise ValueError("Could not extract place ID from URL")

# Example usage:
url = "https://www.google.com/maps/place/Uma+Garden/@-8.6536049,115.1572823,17z/data=!3m1!4b1!4m6!3m5!1s0x2dd247b1b7e76c5f:0xc7419aa68ea8fade"
place_id = extract_place_id(url)
print(place_id)  # Output: 0x2dd247b1b7e76c5f:0xc7419aa68ea8fade
```

---

## Detection Engine

### Keyword Matching Strategy

**Approach:** Case-insensitive regex matching

**Why Regex:**
- ✅ Simple to implement
- ✅ Fast performance
- ✅ Sufficient for V1
- ✅ Easy to test and debug

**Limitations:**
- ❌ May have false positives (e.g., "miss" contains "iss")
- ❌ No context understanding
- ❌ Won't catch synonyms not in list

### Regex Patterns

**Basic Patterns (exact match):**
```python
keywords = [
    r'\bfood poisoning\b',
    r'\bgot sick\b',
    r'\bgot ill\b',
    r'\bstomach ache\b',
    r'\bstomach pain\b',
]
```

**Note:** `\b` = word boundary (prevents matching "miss" when looking for "iss")

**Pattern with Variations:**
```python
keywords = [
    r'\bfood poisoning\b',
    r'\b(got|became|gotten|feeling|felt) (sick|ill)\b',
    r'\bstomach (ache|pain|cramp|issue)\b',
    r'\b(vomit|vomiting|threw up|throw up)\b',
    r'\b(diarrhea|diarrhoea|diarrhœa)\b',
]
```

### Complete Keyword List

See `food_poisoning_keywords.md` for the full list of patterns to implement.

---

## Dashboard Implementation Options

### Option A: Streamlit (Recommended)

**Pros:**
- Fastest development
- No frontend knowledge needed
- Built-in components for charts
- Auto-reloading during development

**Cons:**
- Less customizable
- May be overkill for simple V1

**Example Code:**

```python
import streamlit as st
import plotly.express as px

# Page config
st.set_page_config(page_title="Food Safety Checker", layout="wide")

# Title
st.title("🍴 Bali Restaurant Food Safety Checker")

# Input
url = st.text_input("Paste Google Maps Restaurant URL:")

if st.button("Analyze"):
    # Process URL
    place_id = extract_place_id(url)

    # Fetch reviews
    data = get_place_details(place_id, api_key)

    # Detect issues
    flagged = analyze_reviews(data['reviews'], keywords)

    # Calculate KPIs
    kpis = calculate_kpis(flagged)

    # Display restaurant info
    st.header(data['name'])
    st.write(f"Rating: {data['rating']} ⭐ | {data['total_reviews']} reviews")

    # KPI cards
    col1, col2 = st.columns(2)
    col1.metric("Total Mentions", kpis['total_mentions'])
    col2.metric("Last 6 Months", kpis['mentions_last_6_months'])

    # Timeline chart
    timeline = generate_timeline(flagged)
    fig = px.bar(x=list(timeline.keys()), y=list(timeline.values()))
    st.plotly_chart(fig)

    # Reviews
    st.subheader("Flagged Reviews")
    for review in flagged[:5]:
        st.write(f"**{review['author']}** - {review['rating']}⭐")
        st.write(review['text'])
        st.write(f"Keywords: {', '.join(review['matched_keywords'])}")
        st.divider()
```

**To Run:**
```bash
streamlit run app.py
```

---

### Option B: Flask + Chart.js

**Pros:**
- More control over UI
- Better for production deployment
- Can use any frontend framework

**Cons:**
- Requires HTML/CSS/JS knowledge
- Slower development

**File Structure:**
```
app.py                 # Flask backend
templates/
  └── index.html      # Frontend template
static/
  ├── style.css       # Styles
  └── script.js       # Chart.js code
```

**Example Flask Route:**

```python
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')

    # Process
    place_id = extract_place_id(url)
    data = get_place_details(place_id, api_key)
    flagged = analyze_reviews(data['reviews'], keywords)
    kpis = calculate_kpis(flagged)
    timeline = generate_timeline(flagged)

    return jsonify({
        'restaurant': data,
        'kpis': kpis,
        'timeline': timeline,
        'flagged_reviews': flagged
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Option C: Command-Line Interface

**Pros:**
- Simplest to build
- No web server needed

**Cons:**
- Limited visualization
- Less user-friendly

**Example:**

```python
from rich.console import Console
from rich.table import Table

console = Console()

# Get input
url = input("Enter Google Maps URL: ")

# Process
place_id = extract_place_id(url)
data = get_place_details(place_id, api_key)
flagged = analyze_reviews(data['reviews'], keywords)
kpis = calculate_kpis(flagged)

# Display KPIs
console.print(f"\n[bold]Restaurant:[/bold] {data['name']}")
console.print(f"[bold]Total Mentions:[/bold] {kpis['total_mentions']}")
console.print(f"[bold]Last 6 Months:[/bold] {kpis['mentions_last_6_months']}\n")

# Display reviews in table
table = Table(title="Flagged Reviews")
table.add_column("Author", style="cyan")
table.add_column("Rating")
table.add_column("Review", style="white")

for review in flagged:
    table.add_row(
        review['author'],
        str(review['rating']),
        review['text'][:100] + "..."
    )

console.print(table)
```

---

## File Structure

### Recommended Project Structure

```
BaliRestaurants/
├── .env                          # API keys (not in git)
├── .env.example                  # Template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # Project readme
│
├── specs/                        # Documentation
│   ├── PRD_v1.md
│   ├── technical_spec_v1.md
│   └── food_poisoning_keywords.md
│
├── app.py                        # Main application (Streamlit/Flask)
│
├── utils/                        # Utility modules
│   ├── __init__.py
│   └── url_parser.py            # Google Maps URL parsing
│
├── api/                          # API clients
│   ├── __init__.py
│   └── google_maps_client.py    # Google Maps API integration
│
├── engine/                       # Core logic
│   ├── __init__.py
│   ├── detector.py              # Food poisoning detection
│   ├── processor.py             # Data processing/KPI calculation
│   └── keywords.py              # Keyword list/patterns
│
├── tests/                        # Test files
│   ├── test_url_parser.py
│   ├── test_detector.py
│   └── test_integration.py
│
└── scripts/                      # Existing test scripts
    ├── test_api.py
    └── search_restaurant.py
```

---

## API Integration Details

### Google Maps Places API (New)

**Endpoint:** `GET https://places.googleapis.com/v1/places/{place_id}`

**Headers:**
```
Content-Type: application/json
X-Goog-Api-Key: YOUR_API_KEY
X-Goog-FieldMask: id,displayName,formattedAddress,rating,userRatingCount,reviews
```

**Field Mask Explanation:**
- Specifies which fields to return
- Reduces data transfer
- Only pay for fields you request

**Response Structure:**
```json
{
  "id": "places/ChIJ...",
  "displayName": {
    "text": "Restaurant Name"
  },
  "formattedAddress": "123 Street, Bali, Indonesia",
  "rating": 4.5,
  "userRatingCount": 1234,
  "reviews": [
    {
      "authorAttribution": {
        "displayName": "John Doe"
      },
      "rating": 5,
      "originalText": {
        "text": "Great food!"
      },
      "relativePublishTimeDescription": "2 months ago"
    }
  ]
}
```

**Rate Limits:**
- Standard: 1000 requests per day (free tier)
- Returns maximum 5 reviews per request

**Error Handling:**
- `400`: Invalid request
- `403`: API key issue or API not enabled
- `404`: Place not found
- `429`: Rate limit exceeded

---

## Error Handling

### Error Types & Responses

**1. Invalid URL**
```python
try:
    place_id = extract_place_id(url)
except ValueError as e:
    # Display user-friendly message
    error_message = "Invalid Google Maps URL. Please check the URL and try again."
```

**2. API Errors**
```python
try:
    data = get_place_details(place_id, api_key)
except requests.HTTPError as e:
    if e.response.status_code == 404:
        error_message = "Restaurant not found. Please check the URL."
    elif e.response.status_code == 403:
        error_message = "API key error. Please check your configuration."
    else:
        error_message = f"API error: {e.response.status_code}"
```

**3. No Reviews**
```python
if not reviews or len(reviews) == 0:
    # Display message
    message = "This restaurant has no reviews yet."
```

**4. No Flagged Reviews**
```python
if len(flagged_reviews) == 0:
    # Display positive message
    message = "✅ No food poisoning mentions found in available reviews!"
```

### Error Logging

For debugging and monitoring:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Analyzing restaurant: {place_id}")
logger.error(f"API error: {error_message}")
logger.warning(f"No reviews found for {place_id}")
```

---

## Performance Considerations

### V1 Performance Targets

- **URL Parsing:** < 100ms
- **API Request:** < 2 seconds (depends on Google)
- **Detection Engine:** < 500ms (for 5 reviews)
- **Dashboard Render:** < 1 second
- **Total Time (Input → Results):** < 5 seconds

### Optimization Opportunities (Future)

- Cache API responses (avoid repeated calls for same restaurant)
- Batch processing for multiple restaurants
- Background processing for slow operations

---

## Security Considerations

### API Key Protection

**✅ Do:**
- Store API key in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in code
- Restrict API key in Google Cloud Console

**❌ Don't:**
- Commit API key to git
- Expose key in client-side code
- Share key publicly

### Input Validation

**✅ Validate:**
- URL format before processing
- Place ID format
- API responses before using data

**❌ Don't Trust:**
- User input without validation
- External API responses without checks

---

## Testing Strategy

### Unit Tests

**Test URL Parser:**
```python
def test_extract_place_id_standard_url():
    url = "https://www.google.com/maps/place/..."
    place_id = extract_place_id(url)
    assert place_id is not None
    assert len(place_id) > 0

def test_invalid_url_raises_error():
    with pytest.raises(ValueError):
        extract_place_id("https://www.example.com")
```

**Test Detection Engine:**
```python
def test_detect_food_poisoning_positive():
    text = "We got food poisoning after eating here"
    is_flagged, keywords = detect_food_poisoning(text, KEYWORDS)
    assert is_flagged == True
    assert "food poisoning" in keywords

def test_detect_no_keywords():
    text = "Great food, loved it!"
    is_flagged, keywords = detect_food_poisoning(text, KEYWORDS)
    assert is_flagged == False
```

### Integration Tests

**Test Full Flow:**
```python
def test_full_analysis_flow():
    url = "https://www.google.com/maps/place/test-restaurant"
    place_id = extract_place_id(url)
    data = get_place_details(place_id, API_KEY)
    flagged = analyze_reviews(data['reviews'], KEYWORDS)
    kpis = calculate_kpis(flagged)

    assert 'total_mentions' in kpis
    assert 'mentions_last_6_months' in kpis
```

---

## Deployment (Future)

**For V1:** Run locally only

**For Future Versions:**
- **Streamlit:** Deploy to Streamlit Cloud (free tier available)
- **Flask:** Deploy to Heroku, Railway, or similar
- **Docker:** Containerize for easier deployment

---

**Document End**
