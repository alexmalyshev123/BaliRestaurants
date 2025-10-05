"""
Test script to verify Google Maps API connection and functionality
This script uses the NEW Places API (not legacy)

This script will:
1. Connect to Google Maps API (New)
2. Search for restaurants in Bali using Text Search (New)
3. Fetch reviews for a specific restaurant using Place Details (New)
"""

import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env file
load_dotenv()

# New Places API endpoints
TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
PLACE_DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"

def get_api_key():
    """Get and validate API key from environment"""
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_MAPS_API_KEY not found in .env file")
        return None
    return api_key

def test_restaurant_search(api_key):
    """
    Test searching for restaurants using the NEW Text Search API

    The new API uses HTTP POST requests with JSON bodies
    and field masks to specify what data to return
    """
    print("\n" + "=" * 60)
    print("Testing Restaurant Search (New Places API)")
    print("=" * 60)

    query = "restaurants in Seminyak, Bali"
    print(f"Searching for: '{query}'")

    # Request body for Text Search (New)
    # textQuery: what we're searching for
    # locationBias: focuses results on a specific area (Bali coordinates)
    request_body = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": -8.6705,
                    "longitude": 115.2126
                },
                "radius": 10000.0  # 10km radius
            }
        }
    }

    # Headers required by the new API
    # X-Goog-Api-Key: your API key
    # X-Goog-FieldMask: specifies which fields you want in the response
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount"
    }

    try:
        response = requests.post(TEXT_SEARCH_URL, headers=headers, json=request_body)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            places = data.get('places', [])

            print(f"✓ Found {len(places)} restaurants")
            print("\nFirst 3 restaurants:")

            for i, place in enumerate(places[:3], 1):
                print(f"\n{i}. {place.get('displayName', {}).get('text', 'N/A')}")
                print(f"   Address: {place.get('formattedAddress', 'N/A')}")
                print(f"   Rating: {place.get('rating', 'N/A')} ({place.get('userRatingCount', 0)} reviews)")
                print(f"   Place ID: {place.get('id', 'N/A')}")

            # Return the first place for detailed testing
            return places[0] if places else None
        else:
            print(f"❌ Search failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error during search: {e}")
        return None

def test_fetch_reviews(api_key, place):
    """
    Test fetching reviews using the NEW Place Details API

    This uses a different endpoint and field mask format
    """
    print("\n" + "=" * 60)
    print("Testing Review Fetching (New Places API)")
    print("=" * 60)

    if not place:
        print("❌ No place provided to fetch reviews")
        return False

    try:
        place_id = place.get('id')
        place_name = place.get('displayName', {}).get('text', 'Unknown')

        print(f"Fetching detailed info for: {place_name}")
        print(f"Place ID: {place_id}")

        # Build the URL with place_id
        url = PLACE_DETAILS_URL.format(place_id=place_id)

        # Headers with field mask specifying we want reviews
        # The field mask tells the API exactly which data to return
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "id,displayName,rating,userRatingCount,reviews"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            reviews = result.get('reviews', [])

            print(f"\n✓ Successfully fetched details")
            print(f"Restaurant: {result.get('displayName', {}).get('text', 'N/A')}")
            print(f"Rating: {result.get('rating', 'N/A')}")
            print(f"Total Reviews: {result.get('userRatingCount', 0)}")
            print(f"Reviews returned by API: {len(reviews)}")

            if reviews:
                print("\n" + "-" * 60)
                print("Sample Review:")
                print("-" * 60)
                review = reviews[0]

                # New API has slightly different field names
                author = review.get('authorAttribution', {})
                print(f"Author: {author.get('displayName', 'Anonymous')}")
                print(f"Rating: {review.get('rating', 'N/A')} stars")
                print(f"Time: {review.get('relativePublishTimeDescription', 'N/A')}")

                # The review text is in originalText or text
                review_text = review.get('originalText', {}).get('text',
                             review.get('text', {}).get('text', 'No text provided'))
                print(f"Review Text:\n{review_text}")

                return True
            else:
                print("⚠️  No reviews found for this restaurant")
                print("Note: The API may return limited reviews by default")
                return True
        else:
            print(f"❌ Failed to fetch details: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error fetching reviews: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("\n🔍 GOOGLE MAPS API TEST SCRIPT (NEW PLACES API)")
    print("This will test the NEW Places API connection and functionality\n")

    # Get API key
    print("=" * 60)
    print("Loading API Key")
    print("=" * 60)
    api_key = get_api_key()
    if not api_key:
        print("\n❌ API key not found. Please check your .env file.")
        return

    print(f"✓ API key loaded: {api_key[:10]}..." + "*" * 20)

    # Test 1: Restaurant Search
    place = test_restaurant_search(api_key)
    if not place:
        print("\n❌ Restaurant search failed.")
        print("\nTroubleshooting:")
        print("1. Make sure 'Places API (New)' is enabled in Google Cloud Console")
        print("2. Check that your API key has the correct permissions")
        print("3. Verify your API key isn't restricted to specific domains/IPs")
        return

    # Test 2: Fetch Reviews
    success = test_fetch_reviews(api_key, place)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    if success:
        print("✅ All tests passed!")
        print("Your Google Maps API (New) is configured correctly and working.")
        print("\nYou can now proceed to build the full application.")
        print("\n📝 Note: The new API provides up to 5 reviews by default.")
        print("You may need to make multiple requests or use pagination for more.")
    else:
        print("⚠️  Some tests had issues. Please review the output above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
