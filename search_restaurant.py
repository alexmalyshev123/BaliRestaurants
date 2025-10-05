"""
Search for a specific restaurant and view its reviews
Usage: python search_restaurant.py "Restaurant Name"
"""

import os
import sys
from dotenv import load_dotenv
import requests
import argparse

# Load environment variables
load_dotenv()

# New Places API endpoints
TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
PLACE_DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"

def get_api_key():
    """Get API key from environment"""
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_MAPS_API_KEY not found in .env file")
        sys.exit(1)
    return api_key

def search_restaurant(api_key, restaurant_name):
    """
    Search for a restaurant by name

    Args:
        api_key: Google Maps API key
        restaurant_name: Name of the restaurant to search for

    Returns:
        List of matching restaurants
    """
    print(f"\n🔍 Searching for: '{restaurant_name}'")
    print("=" * 60)

    # Request body - you can modify locationBias to search in different areas
    request_body = {
        "textQuery": restaurant_name,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": -8.6705,  # Bali coordinates
                    "longitude": 115.2126
                },
                "radius": 50000.0  # 50km radius to cover more of Bali
            }
        }
    }

    # Headers with field mask
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount"
    }

    try:
        response = requests.post(TEXT_SEARCH_URL, headers=headers, json=request_body)

        if response.status_code == 200:
            data = response.json()
            places = data.get('places', [])

            if places:
                print(f"✓ Found {len(places)} matching restaurant(s)\n")
                return places
            else:
                print("❌ No restaurants found with that name")
                return []
        else:
            print(f"❌ Search failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return []

    except Exception as e:
        print(f"❌ Error during search: {e}")
        return []

def get_restaurant_reviews(api_key, place):
    """
    Fetch detailed information and reviews for a specific restaurant

    Args:
        api_key: Google Maps API key
        place: Place object from search results

    Returns:
        Dictionary with restaurant details and reviews
    """
    place_id = place.get('id')
    place_name = place.get('displayName', {}).get('text', 'Unknown')

    print(f"\n📖 Fetching reviews for: {place_name}")
    print("=" * 60)

    url = PLACE_DETAILS_URL.format(place_id=place_id)

    # Request all review-related fields
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "id,displayName,formattedAddress,rating,userRatingCount,reviews"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch details: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error fetching reviews: {e}")
        return None

def display_restaurant_info(restaurant_data):
    """
    Display restaurant information and reviews in a readable format

    Args:
        restaurant_data: Dictionary with restaurant details
    """
    name = restaurant_data.get('displayName', {}).get('text', 'N/A')
    address = restaurant_data.get('formattedAddress', 'N/A')
    rating = restaurant_data.get('rating', 'N/A')
    total_reviews = restaurant_data.get('userRatingCount', 0)
    reviews = restaurant_data.get('reviews', [])

    print(f"\n{'=' * 60}")
    print(f"🍽️  {name}")
    print(f"{'=' * 60}")
    print(f"📍 Address: {address}")
    print(f"⭐ Rating: {rating}/5 ({total_reviews} total reviews)")
    print(f"📝 Reviews returned by API: {len(reviews)}")

    if reviews:
        print(f"\n{'=' * 60}")
        print("REVIEWS:")
        print(f"{'=' * 60}\n")

        for i, review in enumerate(reviews, 1):
            author = review.get('authorAttribution', {})
            author_name = author.get('displayName', 'Anonymous')
            rating_stars = review.get('rating', 'N/A')
            time_desc = review.get('relativePublishTimeDescription', 'N/A')

            # Get review text
            review_text = review.get('originalText', {}).get('text',
                         review.get('text', {}).get('text', 'No text provided'))

            print(f"Review #{i}")
            print(f"{'-' * 60}")
            print(f"👤 Author: {author_name}")
            print(f"⭐ Rating: {rating_stars}/5")
            print(f"🕒 Posted: {time_desc}")
            print(f"\n{review_text}\n")
            print(f"{'-' * 60}\n")
    else:
        print("\n⚠️  No reviews available for this restaurant")

def main():
    """Main function"""
    # Set up argument parser
    # This allows us to accept command-line arguments
    parser = argparse.ArgumentParser(
        description='Search for a restaurant and view its reviews',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search_restaurant.py "Naughty Nuri's Warung"
  python search_restaurant.py "Locavore Ubud"
  python search_restaurant.py "pizza restaurants in Canggu"
        """
    )

    parser.add_argument(
        'restaurant',
        type=str,
        help='Name of the restaurant to search for'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Show all matching restaurants (default: show only first match)'
    )

    # Parse arguments
    args = parser.parse_args()

    print("\n🍴 RESTAURANT SEARCH & REVIEW TOOL")
    print("=" * 60)

    # Get API key
    api_key = get_api_key()

    # Search for restaurant
    places = search_restaurant(api_key, args.restaurant)

    if not places:
        print("\nTry:")
        print("- Using a more specific restaurant name")
        print("- Including the location (e.g., 'Restaurant Name Bali')")
        print("- Checking the spelling")
        return

    # Display all matches or just the first one
    if args.all:
        # Show brief info for all matches
        for i, place in enumerate(places, 1):
            name = place.get('displayName', {}).get('text', 'N/A')
            address = place.get('formattedAddress', 'N/A')
            rating = place.get('rating', 'N/A')
            review_count = place.get('userRatingCount', 0)

            print(f"\n{i}. {name}")
            print(f"   📍 {address}")
            print(f"   ⭐ {rating}/5 ({review_count} reviews)")

        print(f"\n💡 Tip: Run without --all flag to see detailed reviews for the first match")
    else:
        # Get detailed reviews for the first match
        restaurant_data = get_restaurant_reviews(api_key, places[0])

        if restaurant_data:
            display_restaurant_info(restaurant_data)

            if len(places) > 1:
                print(f"\n💡 Tip: Found {len(places)} matches. Use --all flag to see all matches")

    print("\n" + "=" * 60)
    print("✅ Done!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
