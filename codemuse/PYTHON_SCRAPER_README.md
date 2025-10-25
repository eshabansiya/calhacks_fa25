# Amazon Product Scraper (Python)

A Python-based Amazon product scraper using BeautifulSoup, based on the Medium article: [How to Scrape Amazon Prices - Beginner Guide](https://medium.com/@joerosborne/how-to-scrape-amazon-prices-beginner-guide-a9d2b42dc1ec)

## Features

- 🛒 Scrape Amazon product information (title, price, image, ratings, description)
- 🌍 Support for multiple Amazon domains (.com, .ca, .co.uk, etc.)
- 🎯 Accurate selectors based on proven methods
- 📊 Export data to JSON format
- ⏱️ Respectful scraping with delays
- 🔄 Batch scraping for multiple products
- 🛡️ Error handling and validation

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Or install manually:**
   ```bash
   pip install requests beautifulsoup4 lxml
   ```

## Usage

### Basic Usage

```python
from amazon_scraper import AmazonScraper

# Initialize scraper
scraper = AmazonScraper()

# Scrape a single product
url = "https://www.amazon.com/dp/B08N5WRWNW"
result = scraper.scrape_product(url)

print(f"Title: {result['title']}")
print(f"Price: {result['price']}")
print(f"Image: {result['image']}")
print(f"Ratings: {result['ratings']}")
print(f"Description: {result['description']}")
```

### Batch Scraping

```python
# Scrape multiple products
urls = [
    "https://www.amazon.com/dp/B08N5WRWNW",
    "https://www.amazon.com/dp/B07XJ8C8F5",
    "https://www.amazon.com/dp/B08N5WRWNW"
]

results = scraper.scrape_multiple_products(urls)

# Save to JSON
scraper.save_to_json(results, 'products.json')
```

### Command Line Usage

1. **Run the example:**
   ```bash
   python example_usage.py
   ```

2. **Run the main scraper:**
   ```bash
   python amazon_scraper.py
   ```

## Selectors Used

Based on the Medium article, the scraper uses these proven selectors:

### Title
- `#title` (primary)
- `#productTitle` (backup)
- Various fallback selectors

### Price
- `#priceblock_ourprice` (primary)
- `#priceblock_dealprice` (deal prices)
- Class-based selectors as fallbacks

### Image
- `#imgTagWrapperId img` (primary)
- Various image container selectors

### Ratings
- `#acrPopover` (primary)
- Checks `title` attribute first
- Text content as fallback

### Description
- `#productDescription` (primary)
- Feature bullets and other containers

## Output Format

The scraper returns a dictionary with:

```json
{
  "url": "https://www.amazon.com/dp/B08N5WRWNW",
  "domain": "www.amazon.com",
  "scraped_at": "2024-01-15 14:30:25",
  "title": "Product Title",
  "price": "$29.99",
  "image": "https://images.amazon.com/image.jpg",
  "ratings": "4.5 out of 5 stars",
  "description": "Product description text..."
}
```

## Error Handling

The scraper handles various error scenarios:

- **Invalid URLs**: Returns error message
- **Non-Amazon URLs**: Returns error message
- **Network errors**: Returns request error details
- **Parsing errors**: Returns scraping error details

## Important Notes

### Legal and Ethical Considerations

⚠️ **Important**: This scraper is for educational purposes only. Please ensure you:

- Comply with Amazon's Terms of Service
- Respect robots.txt files
- Use reasonable delays between requests
- Don't overload Amazon's servers
- Consider using official APIs when available

### Rate Limiting

The scraper includes built-in delays:
- 1-3 seconds between single requests
- 2-4 seconds between batch requests
- Random delays to avoid detection

### User Agent

The scraper uses a realistic User-Agent string to mimic a real browser.

## Comparison with Browser Extension

This Python scraper complements the browser extension:

| Feature | Python Scraper | Browser Extension |
|---------|---------------|-------------------|
| **Environment** | Standalone script | Browser popup |
| **Language** | Python + BeautifulSoup | JavaScript |
| **Use Case** | Batch processing, automation | Interactive browsing |
| **Data Source** | Direct HTTP requests | Page DOM access |
| **Setup** | Requires Python installation | Load in browser |

## Troubleshooting

### Common Issues

1. **"Title not found"**: Amazon may have changed selectors
2. **"Price not found"**: Product may be out of stock or have different pricing structure
3. **Network errors**: Check internet connection and URL validity
4. **Empty results**: Amazon may be blocking requests

### Debugging

Enable debug mode by modifying the scraper:

```python
# Add debug prints
print(f"Found title element: {element}")
print(f"Title text: {element.get_text(strip=True)}")
```

## Contributing

Feel free to improve the scraper by:
- Adding new selectors
- Improving error handling
- Adding new features
- Optimizing performance

## License

This project is for educational purposes. Please respect Amazon's Terms of Service and use responsibly.
