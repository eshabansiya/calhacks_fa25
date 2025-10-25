#!/usr/bin/env python3
"""
Amazon Product Scraper using BeautifulSoup
Based on Medium article: https://medium.com/@joerosborne/how-to-scrape-amazon-prices-beginner-guide-a9d2b42dc1ec
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urlparse
import re

class AmazonScraper:
    def __init__(self):
        self.session = requests.Session()
        # Headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def is_amazon_url(self, url):
        """Check if URL is from Amazon"""
        parsed_url = urlparse(url)
        return 'amazon.com' in parsed_url.netloc or 'amazon.ca' in parsed_url.netloc or 'amazon.co.uk' in parsed_url.netloc
    
    def scrape_product(self, url):
        """
        Scrape Amazon product information
        Returns dictionary with product data
        """
        if not self.is_amazon_url(url):
            return {
                'error': 'Not an Amazon URL',
                'message': 'This scraper only works with Amazon product pages',
                'url': url
            }
        
        try:
            # Add random delay to be respectful
            time.sleep(random.uniform(1, 3))
            
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product data
            product_data = {
                'url': url,
                'domain': urlparse(url).netloc,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': self._scrape_title(soup),
                'price': self._scrape_price(soup),
                'image': self._scrape_image(soup),
                'ratings': self._scrape_ratings(soup),
                'description': self._scrape_description(soup)
            }
            
            return product_data
            
        except requests.RequestException as e:
            return {
                'error': 'Request failed',
                'message': str(e),
                'url': url
            }
        except Exception as e:
            return {
                'error': 'Scraping failed',
                'message': str(e),
                'url': url
            }
    
    def _scrape_title(self, soup):
        """Extract product title"""
        # Primary selector from Medium article
        title_selectors = [
            '#title',
            '#productTitle',
            'h1[data-automation-id="product-title"]',
            '.product-title',
            'h1.a-size-large',
            'h1.a-size-medium'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # Remove Amazon prefixes
            for prefix in ['Amazon.com: ', 'Amazon.ca: ', 'Amazon.co.uk: ']:
                if title_text.startswith(prefix):
                    return title_text[len(prefix):]
            return title_text
        
        return 'Title not found'
    
    def _scrape_price(self, soup):
        """Extract product price"""
        # Primary selectors from Medium article
        price_selectors = [
            '#priceblock_ourprice',
            '#priceblock_dealprice',
            '.a-price-whole',
            '.a-price .a-offscreen',
            '.a-price-range',
            '.a-price .a-text-price',
            '[data-automation-id="product-price"]'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Check if it contains currency symbols
                if re.search(r'[\$€£¥]\s*\d+[\.,]\d+|\d+[\.,]\d+\s*[\$€£¥]', price_text):
                    return price_text
        
        # Try to find price in any element with price-related classes/IDs
        price_containers = soup.find_all(['span', 'div'], class_=re.compile(r'price|cost|amount'))
        for container in price_containers:
            price_text = container.get_text(strip=True)
            price_match = re.search(r'[\$€£¥]\s*\d+[\.,]\d+|\d+[\.,]\d+\s*[\$€£¥]', price_text)
            if price_match:
                return price_match.group(0)
        
        return 'Price not found'
    
    def _scrape_image(self, soup):
        """Extract product image URL"""
        # Primary selector from Medium article
        image_selectors = [
            '#imgTagWrapperId img',
            '#landingImage',
            '#imgBlkFront',
            '.a-dynamic-image',
            '.a-button-selected img',
            '#main-image-container img'
        ]
        
        for selector in image_selectors:
            element = soup.select_one(selector)
            if element:
                # Try different attributes for image URL
                for attr in ['src', 'data-old-hires', 'data-src']:
                    img_url = element.get(attr)
                    if img_url and not img_url.startswith('data:image'):
                        return img_url
        
        return ''
    
    def _scrape_ratings(self, soup):
        """Extract product ratings"""
        # Primary selector from Medium article
        rating_selectors = [
            '#acrPopover',
            '.a-icon-alt',
            '[data-automation-id="product-rating"]',
            '.a-icon-star',
            '.a-star-mini'
        ]
        
        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                # Try title attribute first (as suggested in article)
                title_attr = element.get('title')
                if title_attr and ('out of' in title_attr or 'stars' in title_attr):
                    return title_attr.strip()
                
                # Fallback to text content
                rating_text = element.get_text(strip=True)
                if 'out of' in rating_text or 'stars' in rating_text:
                    return rating_text
        
        # Try to find review count
        review_selectors = [
            '#acrCustomerReviewText',
            '[data-automation-id="review-count"]',
            '.a-size-base'
        ]
        
        for selector in review_selectors:
            element = soup.select_one(selector)
            if element and 'ratings' in element.get_text():
                return element.get_text(strip=True)
        
        return ''
    
    def _scrape_description(self, soup):
        """Extract product description"""
        # Primary selector from Medium article
        description_selectors = [
            '#productDescription',
            '#feature-bullets ul',
            '.a-unordered-list',
            '.a-list-item',
            '[data-automation-id="product-description"]'
        ]
        
        for selector in description_selectors:
            element = soup.select_one(selector)
            if element:
                description_text = element.get_text(strip=True)
                if len(description_text) > 50:  # Only return substantial descriptions
                    # Limit length to avoid too much text
                    return description_text[:500] + ('...' if len(description_text) > 500 else '')
        
        return ''
    
    def scrape_multiple_products(self, urls):
        """Scrape multiple Amazon products"""
        results = []
        for url in urls:
            print(f"Scraping: {url}")
            result = self.scrape_product(url)
            results.append(result)
            
            # Add delay between requests
            time.sleep(random.uniform(2, 4))
        
        return results
    
    def save_to_json(self, data, filename):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")


def main():
    """Example usage"""
    scraper = AmazonScraper()
    
    # Example Amazon product URLs
    test_urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",  # Example product
        # Add more URLs here
    ]
    
    print("Amazon Product Scraper")
    print("=" * 50)
    
    # Scrape single product
    if test_urls:
        url = test_urls[0]
        print(f"Scraping single product: {url}")
        result = scraper.scrape_product(url)
        
        print("\nScraped Data:")
        print("-" * 30)
        for key, value in result.items():
            print(f"{key}: {value}")
        
        # Save to file
        scraper.save_to_json(result, 'amazon_product.json')
    
    # Scrape multiple products
    if len(test_urls) > 1:
        print(f"\nScraping {len(test_urls)} products...")
        results = scraper.scrape_multiple_products(test_urls)
        scraper.save_to_json(results, 'amazon_products.json')


if __name__ == "__main__":
    main()
