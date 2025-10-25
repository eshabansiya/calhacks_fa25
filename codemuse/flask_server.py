#!/usr/bin/env python3
"""
Flask Backend Server for Amazon Scraper
Communicates with the browser extension
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urlparse
import re
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for browser extension communication

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
        """Scrape Amazon product information"""
        if not self.is_amazon_url(url):
            return {
                'success': False,
                'error': 'Not an Amazon URL',
                'message': 'This scraper only works with Amazon product pages',
                'url': url
            }
        
        try:
            # Add random delay to be respectful
            time.sleep(random.uniform(1, 2))
            
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product data
            product_data = {
                'success': True,
                'url': url,
                'domain': urlparse(url).netloc,
                'scraped_at': datetime.now().isoformat(),
                'title': self._scrape_title(soup),
                'price': self._scrape_price(soup),
                'image': self._scrape_image(soup),
                'ratings': self._scrape_ratings(soup),
                'description': self._scrape_description(soup)
            }
            
            return product_data
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': 'Request failed',
                'message': str(e),
                'url': url
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'Scraping failed',
                'message': str(e),
                'url': url
            }
    
    def _scrape_title(self, soup):
        """Extract product title"""
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
            for prefix in ['Amazon.com: ', 'Amazon.ca: ', 'Amazon.co.uk: ']:
                if title_text.startswith(prefix):
                    return title_text[len(prefix):]
            return title_text
        
        return 'Title not found'
    
    def _scrape_price(self, soup):
        """Extract product price"""
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
                for attr in ['src', 'data-old-hires', 'data-src']:
                    img_url = element.get(attr)
                    if img_url and not img_url.startswith('data:image'):
                        return img_url
        
        return ''
    
    def _scrape_ratings(self, soup):
        """Extract product ratings"""
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
                # Try title attribute first
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
                if len(description_text) > 50:
                    return description_text[:500] + ('...' if len(description_text) > 500 else '')
        
        return ''

# Initialize scraper
scraper = AmazonScraper()

# In-memory storage for products (in production, use a database)
products_storage = []

@app.route('/')
def index():
    """Serve the main page"""
    return jsonify({
        'message': 'Amazon Scraper API Server',
        'status': 'running',
        'endpoints': {
            'scrape': '/api/scrape',
            'products': '/api/products',
            'clear': '/api/clear'
        }
    })

@app.route('/api/scrape', methods=['POST'])
def scrape_product():
    """Scrape a product from the provided URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'No URL provided'
            })
        
        print(f"Scraping URL: {url}")
        result = scraper.scrape_product(url)
        
        # If successful, add to storage
        if result['success']:
            result['id'] = str(int(time.time() * 1000))  # Generate unique ID
            products_storage.append(result)
            print(f"Successfully scraped: {result['title']}")
        else:
            print(f"Failed to scrape: {result['error']}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        })

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all scraped products"""
    return jsonify({
        'success': True,
        'products': products_storage
    })

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a specific product"""
    global products_storage
    products_storage = [p for p in products_storage if p.get('id') != product_id]
    return jsonify({
        'success': True,
        'message': 'Product deleted'
    })

@app.route('/api/clear', methods=['POST'])
def clear_products():
    """Clear all products"""
    global products_storage
    products_storage = []
    return jsonify({
        'success': True,
        'message': 'All products cleared'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'products_count': len(products_storage)
    })

if __name__ == '__main__':
    print("Starting Amazon Scraper API Server...")
    print("Server will be available at: http://localhost:5000")
    print("Extension should connect to: http://localhost:5000/api/scrape")
    print("=" * 60)
    
    # Run the Flask server
    app.run(host='localhost', port=5000, debug=True)
