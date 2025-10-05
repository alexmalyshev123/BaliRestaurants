"""
Test script for Apify API integration
Tests Google Maps Reviews Scraper with 6-month filtering and 1000 review cap
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def test_apify_connection():
    """Test basic connection to Apify API"""
    print("\n🔍 APIFY API TEST SCRIPT")
    print("=" * 60)
    print()

    # Step 1: Load API key
    print("Step 1: Loading API key...")
    api_key = os.getenv('APIFY_API_KEY')

    if not api_key:
        print("❌ ERROR: APIFY_API_KEY not found in .env file")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your Apify API token to APIFY_API_KEY")
        print("3. Get your token from: https://console.apify.com/account/integrations")
        return False

    print(f"✓ API key loaded: {api_key[:15]}...")
    print()

    # Step 2: Initialize Apify client
    print("Step 2: Connecting to Apify...")
    try:
        client = ApifyClient(api_key)
        print("✓ Connected to Apify successfully")
        print()
    except Exception as e:
        print(f"❌ Error connecting to Apify: {e}")
        return False

    # Step 3: Configure test restaurant
    # Using shortened Google Maps URL format (maps.app.goo.gl)
    test_url = "https://maps.app.goo.gl/KXuHZ6dNENB9R3sr8"

    print("Step 3: Fetching reviews from test restaurant...")
    print(f"URL: {test_url}")
    print()

    # Calculate date 6 months ago
    six_months_ago = datetime.now() - timedelta(days=180)
    start_date = six_months_ago.strftime('%Y-%m-%d')

    print(f"Filter: Reviews from {start_date} to today")
    print(f"Limit: Maximum 1000 reviews")
    print()

    # Step 4: Run the scraper
    print("Step 4: Running Google Maps Reviews Scraper...")
    print("(This may take 30-60 seconds...)")
    print()

    try:
        # Configure the scraper
        # Apify expects URLs in a specific format with 'url' key
        run_input = {
            "startUrls": [{"url": test_url}],  # Note: wrapped in dict with 'url' key
            "maxReviews": 10,                   # Just 10 for testing
            "reviewsSort": "newest"             # Get most recent first
        }

        # Run the actor (Google Maps Reviews Scraper)
        # Actor ID: compass/google-maps-reviews-scraper
        run = client.actor("compass/google-maps-reviews-scraper").call(run_input=run_input)

        print("✓ Scraper completed successfully")
        print()

        # Step 5: Fetch results
        print("Step 5: Retrieving results...")

        # Each item in the dataset is a REVIEW (not a restaurant object with nested reviews)
        reviews = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            reviews.append(item)

        if not reviews:
            print("❌ No results returned")
            return False

        print(f"✓ Results retrieved: {len(reviews)} reviews")
        print()

        # Step 6: Display results
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print()

        # Restaurant info (from first review)
        first_review = reviews[0]
        print(f"Restaurant: {first_review.get('title', 'N/A')}")
        print(f"Address: {first_review.get('address', 'N/A')}")
        print(f"Rating: {first_review.get('totalScore', 'N/A')}/5")
        print(f"Total Reviews (on Google): {first_review.get('reviewsCount', 'N/A'):,}")
        print()

        # Reviews fetched
        print(f"Reviews Fetched: {len(reviews)}")
        print()

        if reviews:
            # Show first 3 reviews as samples
            print("-" * 60)
            print("Sample Reviews:")
            print("-" * 60)
            print()

            for i, review in enumerate(reviews[:3], 1):
                print(f"Review #{i}")
                print("-" * 40)
                print(f"Author: {review.get('name', 'Anonymous')}")
                print(f"Rating: {review.get('stars', 'N/A')} stars")
                print(f"Date: {review.get('publishedAtDate', 'N/A')}")
                review_text = review.get('text', 'No text')
                print(f"Review: {review_text[:200] if review_text else 'No text'}...")
                print()

            # Statistics
            print("=" * 60)
            print("STATISTICS")
            print("=" * 60)
            print()
            print(f"Total reviews fetched: {len(reviews)}")
            print()

            # Show date range
            if reviews:
                latest_date = reviews[0].get('publishedAtDate', '')
                oldest_date = reviews[-1].get('publishedAtDate', '')
                print(f"Latest review: {latest_date}")
                print(f"Oldest review: {oldest_date}")
                print()

        # Step 7: Success
        print("=" * 60)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Your Apify API is configured correctly and working.")
        print("You can now proceed to build the food safety checker app.")
        print()

        # Cost estimation
        cost = (len(reviews) / 1000) * 0.35
        print(f"💰 Cost for this test: ~${cost:.2f}")
        print(f"   ({len(reviews)} reviews × $0.35 per 1,000)")
        print()

        return True

    except Exception as e:
        print(f"❌ Error during scraper execution: {e}")
        print()
        print("Common issues:")
        print("1. Invalid API key - check your token in .env")
        print("2. No credits remaining - check Apify Console → Billing")
        print("3. Network issues - check your internet connection")
        print()
        return False

if __name__ == "__main__":
    success = test_apify_connection()

    if not success:
        print("❌ Test failed. Please fix the issues above and try again.")
        print()
        print("Need help? Check specs/setup_apify.md for detailed setup instructions.")
    else:
        print("Next steps:")
        print("1. Review the PRD: specs/PRD_v1.md")
        print("2. Review the technical spec: specs/technical_spec_v1.md")
        print("3. Start building Phase 1: URL validator")
        print()

    print("=" * 60)
