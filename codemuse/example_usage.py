#!/usr/bin/env python3
"""
Simple example of using the Amazon scraper
"""

from amazon_scraper import AmazonScraper
import json

def main():
    # Initialize scraper
    scraper = AmazonScraper()
    
    # Example Amazon product URL (replace with actual product URL)
    product_url = "https://www.amazon.com/dp/B08N5WRWNW"  # Replace with real Amazon product URL
    
    print("🛒 Amazon Product Scraper")
    print("=" * 50)
    print(f"Scraping: {product_url}")
    print()
    
    # Scrape the product
    result = scraper.scrape_product(product_url)
    
    # Display results
    if 'error' in result:
        print("❌ Error occurred:")
        print(f"   {result['error']}: {result['message']}")
    else:
        print("✅ Product scraped successfully!")
        print()
        print("📋 Product Details:")
        print("-" * 30)
        print(f"Title: {result['title']}")
        print(f"Price: {result['price']}")
        print(f"Image: {result['image'][:50]}..." if result['image'] else "Image: Not found")
        print(f"Ratings: {result['ratings']}")
        print(f"Description: {result['description'][:100]}..." if result['description'] else "Description: Not found")
        print(f"URL: {result['url']}")
        print(f"Scraped at: {result['scraped_at']}")
        
        # Save to JSON file
        scraper.save_to_json(result, 'scraped_product.json')
        print()
        print("💾 Data saved to 'scraped_product.json'")

if __name__ == "__main__":
    main()
