"""
Bali Restaurant Food Safety Checker
Main application entry point
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This pulls in your API keys securely
load_dotenv()

def main():
    """
    Main function - this is where the application starts
    """
    print("Welcome to Bali Restaurant Food Safety Checker!")

    # Check if Google Maps API key is configured
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    if not api_key:
        print("⚠️  Google Maps API key not found!")
        print("Please create a .env file and add your GOOGLE_MAPS_API_KEY")
        return

    print("✓ API key configured")
    print("\nReady to check restaurants for food safety mentions!")
    # TODO: Add restaurant search and review analysis functionality

if __name__ == "__main__":
    # This line ensures main() only runs when you execute this file directly
    # (not when it's imported as a module)
    main()
