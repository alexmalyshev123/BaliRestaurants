# Product Requirements Document (PRD) - Version 1.0
# Bali Restaurant Food Safety Checker

**Document Version:** 1.0
**Date:** October 5, 2025
**Status:** Draft
**Owner:** Product Team

---

## Table of Contents
1. [Product Overview](#product-overview)
2. [Goals & Objectives](#goals--objectives)
3. [Success Metrics](#success-metrics)
4. [User Stories](#user-stories)
5. [User Flow](#user-flow)
6. [Feature Requirements](#feature-requirements)
7. [Dashboard Specifications](#dashboard-specifications)
8. [Out of Scope (V1)](#out-of-scope-v1)
9. [Testing Strategy](#testing-strategy)
10. [Timeline & Phases](#timeline--phases)

---

## Product Overview

### What is it?
A tool that helps users identify potential food safety issues at restaurants by analyzing Google Maps reviews for mentions of food poisoning, illness, or related symptoms.

### Who is it for?
- Travelers visiting Bali who want to make informed dining decisions
- Locals looking for safe restaurant options
- Anyone concerned about food safety when choosing where to eat

### Problem Statement
When choosing a restaurant, users can't easily identify if there have been food poisoning incidents. Reading through hundreds of reviews manually is time-consuming and inefficient. This tool automates the process of detecting food safety red flags in restaurant reviews.

### Solution
A simple dashboard application that:
1. Accepts a Google Maps restaurant URL
2. Scans reviews from the last 6 months for food poisoning-related keywords (up to 1000 reviews)
3. Displays a timeline of incidents and relevant statistics
4. Shows flagged reviews for user review

### Data Scope
- **Time Period**: Last 6 months of reviews only
- **Review Limit**: Up to 1000 reviews per restaurant
- **Rationale**: Focuses on recent, relevant data while controlling costs and processing time

---

## Goals & Objectives

### Primary Goal
Create a minimum viable product (MVP) that can successfully detect and visualize food poisoning mentions in restaurant reviews.

### V1 Objectives
1. ✅ **Functional Detection**: Accurately identify food poisoning-related reviews using keyword matching
2. ✅ **Simple Input**: Allow users to easily input Google Maps URLs
3. ✅ **Clear Visualization**: Present findings in an easy-to-understand dashboard
4. ✅ **Testable**: Build incrementally so each component can be tested independently

---

## Success Metrics

### Primary Metrics
- **Detection Accuracy**: Successfully identifies reviews containing food poisoning keywords
- **Usability**: Users can complete the full flow (input URL → view results) in under 1 minute
- **Reliability**: Tool works with 95%+ of valid Google Maps restaurant URLs

### Secondary Metrics
- Dashboard loads in under 5 seconds
- False positive rate for keyword detection < 20%

---

## User Stories

### Core User Story
```
As a traveler planning to dine at a restaurant in Bali,
I want to quickly check if there have been any food poisoning incidents,
So that I can make an informed decision about where to eat.
```

### Detailed User Stories

**Story 1: URL Input**
```
As a user,
I want to paste a Google Maps restaurant URL,
So that the app can analyze that specific restaurant.
```

**Story 2: View Summary Statistics**
```
As a user,
I want to see the total number of food poisoning mentions,
So that I can quickly assess the risk level.
```

**Story 3: View Recent Trends**
```
As a user,
I want to see if mentions are recent or old,
So that I can determine if issues are ongoing or resolved.
```

**Story 4: Read Flagged Reviews**
```
As a user,
I want to read the actual reviews that mentioned food poisoning,
So that I can judge the severity and context myself.
```

---

## User Flow

### Happy Path Flow

```
1. User opens the application
   ↓
2. User copies Google Maps URL for a restaurant
   (Example: https://maps.google.com/maps/place/Restaurant+Name/...)
   ↓
3. User pastes URL into input field
   ↓
4. User clicks "Analyze" button
   ↓
5. App validates URL and extracts place ID
   ↓
6. App fetches all available reviews from Google Maps API
   ↓
7. App scans each review for food poisoning keywords
   ↓
8. App displays dashboard with:
   - Total mentions (all time)
   - Mentions in last 6 months
   - Monthly trend chart
   - List of flagged reviews (first 5 shown)
   ↓
9. User clicks "Show More" to see additional flagged reviews
   ↓
10. User reads reviews and makes informed decision
```

### Error Flows

**Invalid URL:**
```
User pastes invalid URL
  ↓
App shows error: "Invalid Google Maps URL. Please use a valid restaurant link."
  ↓
User tries again with valid URL
```

**No Reviews Found:**
```
App successfully fetches restaurant but finds no reviews
  ↓
App shows message: "No reviews available for this restaurant."
```

**No Food Poisoning Mentions:**
```
App scans all reviews but finds no matches
  ↓
Dashboard shows: "✅ No food poisoning mentions found in available reviews"
  ↓
All KPIs show "0"
```

---

## Feature Requirements

### Feature 1: URL Input & Validation

**Description:** Accept and validate Google Maps restaurant URLs

**Requirements:**
- Accept URLs in common Google Maps formats:
  - `https://www.google.com/maps/place/...`
  - `https://maps.google.com/...`
  - `https://goo.gl/maps/...` (shortened URLs)
- Extract place ID from URL
- Validate that place ID exists
- Show clear error messages for invalid URLs

**Acceptance Criteria:**
- ✅ Valid URLs are successfully parsed
- ✅ Invalid URLs show user-friendly error message
- ✅ Place ID is correctly extracted

---

### Feature 2: Review Fetching

**Description:** Retrieve reviews from the last 6 months for the restaurant

**Requirements:**
- Use Apify Google Maps Reviews Scraper API to fetch reviews
- Filter reviews to last 6 months only
- Limit to maximum 1000 reviews per restaurant
- Sort by newest first to get most recent reviews
- Store review data including:
  - Author name
  - Rating
  - Review text
  - Published date
  - Review images (if any)

**Acceptance Criteria:**
- ✅ Successfully fetches reviews from Apify API
- ✅ Only retrieves reviews from last 6 months
- ✅ Respects 1000 review limit
- ✅ Handles cases where no reviews exist
- ✅ Stores reviews in a structured format for analysis

**API Configuration:**
- `maxReviews`: 1000
- `reviewsSort`: "newest"
- `reviewsStartDate`: [6 months ago from current date]

---

### Feature 3: Food Poisoning Detection Engine

**Description:** Scan reviews for food poisoning-related keywords using regex

**Requirements:**
- Implement case-insensitive keyword matching
- Detect variations of keywords (e.g., "sick", "sickness")
- Flag entire review if any keyword is found
- Store which keywords were matched for each review

**Keywords to Detect (see food_poisoning_keywords.md for full list):**
- food poisoning
- got sick / got ill
- stomach ache / stomach pain
- diarrhea / diarrhoea
- vomit / vomiting / threw up
- nausea / nauseous / nauseated
- food safety / food hygiene
- food borne illness

**Acceptance Criteria:**
- ✅ Correctly identifies reviews containing keywords
- ✅ Case-insensitive matching works
- ✅ Can detect partial word matches where appropriate
- ✅ No false negatives (doesn't miss obvious cases)

---

### Feature 4: Dashboard Visualization

**Description:** Display analysis results in an easy-to-read dashboard

**Components:** (See Dashboard Specifications section for details)
1. KPI Card: Total Mentions (Last 6 Months)
2. KPI Card: This Month
3. Timeline Chart: Monthly trend over last 6 months
4. Review List: Flagged reviews with "Show More" functionality
5. Analysis Transparency: Display number of reviews analyzed

**Acceptance Criteria:**
- ✅ Dashboard displays all components clearly
- ✅ Data is accurate and matches the analysis
- ✅ Interface is intuitive and easy to understand
- ✅ "Show More" functionality works correctly

---

## Dashboard Specifications

### Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│  BALI RESTAURANT FOOD SAFETY CHECKER                        │
│  Restaurant: [Restaurant Name]                              │
│  Rating: [4.5 stars] | Total Reviews: [1234]               │
│  Analyzed: [847] reviews from last 6 months                │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────┬──────────────────────────────────┐
│  🚨 Total Mentions       │  📅 This Month                   │
│                          │                                  │
│       [12]               │       [3]                        │
│                          │                                  │
│  Last 6 Months           │  Recent Activity                 │
└──────────────────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📈 MONTHLY TREND                                           │
│                                                             │
│   [Timeline Chart: Bar or Line Chart]                      │
│   X-Axis: Months                                           │
│   Y-Axis: Number of Mentions                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📝 FLAGGED REVIEWS                                         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ⭐⭐ - Author Name - 2 months ago                     │ │
│  │ Keywords found: food poisoning, stomach ache         │ │
│  │                                                       │ │
│  │ "We ate here last week and both got terrible food    │ │
│  │  poisoning. Had stomach aches for days..."           │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [5 reviews shown by default]                              │
│                                                             │
│  [ Show More Reviews ]  ← Button (if more than 5)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Analysis Transparency
- **Purpose:** Show user how much data was analyzed
- **Display:** Text line below restaurant info
- **Data:** Number of reviews analyzed and time period
- **Example:** "Analyzed: 847 reviews from last 6 months"

#### KPI Card 1: Total Mentions (Last 6 Months)
- **Purpose:** Show total number of food poisoning mentions in analyzed reviews
- **Display:** Large number with label
- **Data:** Count of all flagged reviews from the last 6 months
- **Calculation:** Count reviews with matched keywords from the 6-month dataset
- **Example:** "12" with label "Last 6 Months"

#### KPI Card 2: This Month
- **Purpose:** Show if issues are current/ongoing
- **Display:** Large number with label
- **Data:** Count of flagged reviews from current month only
- **Calculation:** Filter flagged reviews where date is within current month
- **Example:** "3" with label "This Month"
- **Note:** Helps identify if problems are recent vs historical

#### Timeline Chart: Monthly Trend
- **Purpose:** Visualize when incidents occurred over time
- **Chart Type:** Bar chart or line chart
- **X-Axis:** Last 6 months (e.g., "Apr 2025", "May 2025", ... "Oct 2025")
- **Y-Axis:** Number of mentions
- **Time Range:** Show last 6 months only
- **Data Points:** One bar/point per month
- **Example:** Apr: 0, May: 2, Jun: 1, Jul: 0, Aug: 3, Sep: 1, Oct: 3

#### Review List
- **Purpose:** Allow users to read actual flagged reviews
- **Display:** List of review cards
- **Default:** Show first 5 reviews
- **Show More:** Button appears if more than 5 flagged reviews exist
- **Clicking "Show More":** Expands to show next 5 reviews (or all remaining)

**Each Review Card Contains:**
- Star rating (1-5 stars)
- Author name
- Relative time (e.g., "2 months ago")
- Keywords matched (e.g., "food poisoning, vomiting")
- Full review text
- Visual highlight or badge indicating it's a flagged review

---

## Out of Scope (V1)

The following features are intentionally excluded from V1 to keep the MVP simple:

### Not Included in V1:
❌ **Machine Learning Detection** - V1 uses simple regex; ML can be added later
❌ **Sentiment Analysis** - Focus on keyword detection only
❌ **Multiple Restaurant Comparison** - V1 analyzes one restaurant at a time
❌ **User Accounts / Authentication** - No login required
❌ **Save/Bookmark Restaurants** - No persistence of user data
❌ **Email Alerts** - No notification system
❌ **Mobile App** - Web-based only
❌ **Restaurant Database** - Works on-demand with URLs only
❌ **Exporting Reports** - No PDF/CSV export
❌ **Historical Data Beyond 6 Months** - Only analyzes recent reviews
❌ **Multi-language Support** - English reviews only
❌ **Historical Data Tracking** - No database of past scans
❌ **All-Time Statistics** - Focus on recent 6-month period only

### Future Versions May Include:
- AI-powered detection for better accuracy
- Batch processing of multiple restaurants
- Email alerts for new mentions
- Database to track restaurants over time
- More sophisticated review fetching (pagination)

---

## Testing Strategy

### Testing Approach
Build and test incrementally in phases. Each phase must pass testing before moving to the next.

### Phase-by-Phase Testing

#### Phase 1: URL Parsing & Validation
**What to Test:**
- Valid Google Maps URLs parse correctly
- Invalid URLs show appropriate error
- Place ID is extracted accurately

**Test Cases:**
```
Test 1: Standard Google Maps URL
Input: https://www.google.com/maps/place/Restaurant/...
Expected: Place ID extracted successfully

Test 2: Shortened URL
Input: https://goo.gl/maps/abc123
Expected: Place ID extracted successfully

Test 3: Invalid URL
Input: https://www.example.com
Expected: Error message displayed

Test 4: URL without place ID
Input: https://www.google.com/maps
Expected: Error message displayed
```

#### Phase 2: Review Fetching
**What to Test:**
- API connection works
- Reviews are fetched successfully
- Data is structured correctly

**Test Cases:**
```
Test 1: Restaurant with reviews
Input: Valid place ID for restaurant with reviews
Expected: Reviews returned in correct format

Test 2: Restaurant without reviews
Input: Valid place ID for new restaurant (no reviews)
Expected: Graceful handling, message shown

Test 3: Invalid place ID
Input: Non-existent place ID
Expected: API error handled, user-friendly message
```

#### Phase 3: Detection Engine
**What to Test:**
- Keywords are detected correctly
- Case-insensitive matching works
- No false negatives

**Test Cases:**
```
Test 1: Clear food poisoning mention
Review: "We got food poisoning after eating here"
Expected: Flagged ✅

Test 2: Multiple keywords
Review: "Had terrible stomach ache and vomiting"
Expected: Flagged ✅, both keywords logged

Test 3: Case variation
Review: "GOT SICK after the meal"
Expected: Flagged ✅

Test 4: No keywords
Review: "Amazing food, loved everything!"
Expected: Not flagged ❌

Test 5: Partial match (edge case)
Review: "The food made me miss home" (contains "sick" in "miss")
Expected: Test to determine if this should match (define in keywords spec)
```

#### Phase 4: Dashboard Display
**What to Test:**
- All components render correctly
- Data is accurate
- "Show More" works

**Test Cases:**
```
Test 1: Restaurant with flagged reviews
Input: Restaurant with 3 food poisoning mentions
Expected:
  - KPI shows "3" for total
  - KPI shows correct number for last 6 months
  - Timeline shows correct distribution
  - Review list shows flagged reviews

Test 2: Restaurant with no flagged reviews
Input: Restaurant with no matches
Expected:
  - KPIs show "0"
  - Timeline shows no data
  - Message: "No food poisoning mentions found"

Test 3: "Show More" functionality
Input: Restaurant with more than 5 flagged reviews
Expected:
  - First 5 shown initially
  - "Show More" button visible
  - Clicking shows additional reviews
```

### Manual Testing Checklist
Before considering V1 complete:

- [ ] Test with at least 5 different restaurants
- [ ] Test with restaurant that has known food safety issues
- [ ] Test with highly-rated restaurant (should show few/no flags)
- [ ] Test with brand new restaurant (no reviews)
- [ ] Test all error scenarios
- [ ] Verify dashboard is readable and intuitive
- [ ] Confirm all calculations are accurate

---

## Timeline & Phases

### Recommended Development Approach

**Phase 1: Foundation (Week 1)**
- Set up project structure
- Implement URL parsing and validation
- Test with various URL formats
- **Deliverable:** Working URL parser

**Phase 2: API Integration (Week 1)**
- Implement review fetching
- Handle API responses
- Test with real restaurants
- **Deliverable:** Can fetch and display reviews

**Phase 3: Detection Engine (Week 2)**
- Implement regex keyword matching
- Create keyword patterns (see food_poisoning_keywords.md)
- Test detection accuracy
- **Deliverable:** Working detection engine

**Phase 4: Dashboard (Week 2-3)**
- Choose dashboard technology (Flask/Streamlit/CLI)
- Build KPI cards
- Build timeline chart
- Build review list with "Show More"
- **Deliverable:** Complete dashboard

**Phase 5: Integration & Testing (Week 3)**
- Connect all components
- End-to-end testing
- Bug fixes
- **Deliverable:** Working MVP

### Total Estimated Timeline: 3 weeks

---

## Questions & Decisions

### Open Questions
1. **Dashboard Technology:** Which framework should we use?
   - Option A: Flask + HTML/CSS/JavaScript (most flexible)
   - Option B: Streamlit (fastest, best for data dashboards)
   - Option C: Command-line with ASCII charts (simplest)

2. **Review Limit:** Should we work with the 5-review API limit or try to fetch more?
   - Current decision: Accept 5-review limit for V1
   - Future: Implement pagination or multiple API calls

3. **Date Parsing:** How to handle reviews without exact dates?
   - Google API provides "relativePublishTimeDescription" (e.g., "2 months ago")
   - Need to convert to approximate dates for timeline

### Decisions Made
✅ **Use Apify API** - Gets all reviews, not limited to 5
✅ **6-month time window** - Focus on recent, relevant data
✅ **1000 review cap** - Balance comprehensiveness with cost
✅ **Use regex for V1** - Simple and sufficient for MVP
✅ **One restaurant at a time** - Keeps scope manageable
✅ **No user authentication** - Reduces complexity
✅ **Display raw reviews** - No modification of review content

### Cost Considerations
**API Costs (Apify):**
- Free tier: $5 in credits per month (~10,000 reviews)
- Paid tier: $0.35 per 1,000 reviews

**Estimated Usage:**
- Testing phase: FREE (within free tier)
- Light usage (5 restaurants/day × 300 avg reviews): ~$16/month
- Medium usage (20 restaurants/day × 300 avg reviews): ~$64/month

**Cost Control Measures:**
- 1000 review cap per restaurant prevents runaway costs
- 6-month filter reduces data volume
- Pay-per-use pricing (no monthly minimum)

---

## Appendix

### Related Documents
- `technical_spec_v1.md` - Technical implementation details
- `food_poisoning_keywords.md` - Complete keyword list and regex patterns

### References
- Apify Google Maps Reviews Scraper API Documentation
- Existing test scripts: `test_api.py`, `search_restaurant.py`

### Revision History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-05 | Initial PRD created | Product Team |
| 1.1 | 2025-10-05 | Updated to use Apify API, 6-month focus, 1000 review cap | Product Team |

---

**Document End**
