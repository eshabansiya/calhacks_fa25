// Content script for scraping Amazon product information
(function() {
  'use strict';

  // Check if we're on Amazon
  function isAmazonPage() {
    return window.location.hostname.includes('amazon.com') || 
           window.location.hostname.includes('amazon.ca') ||
           window.location.hostname.includes('amazon.co.uk') ||
           window.location.hostname.includes('amazon.de') ||
           window.location.hostname.includes('amazon.fr');
  }

  // Function to extract Amazon product data
  function scrapeProductData() {
    if (!isAmazonPage()) {
      return {
        title: 'Not an Amazon page',
        price: '',
        image: '',
        ratings: '',
        description: 'This extension currently only works on Amazon product pages.',
        url: window.location.href,
        domain: window.location.hostname,
        scrapedAt: new Date().toISOString(),
        error: 'Not Amazon'
      };
    }

    const data = {
      title: '',
      price: '',
      image: '',
      ratings: '',
      description: '',
      url: window.location.href,
      domain: window.location.hostname,
      scrapedAt: new Date().toISOString()
    };

    // Amazon-specific scraping
    data.title = scrapeAmazonTitle();
    data.price = scrapeAmazonPrice();
    data.image = scrapeAmazonImage();
    data.ratings = scrapeAmazonRatings();
    data.description = scrapeAmazonDescription();

    return data;
  }

  // Amazon title selectors (based on Medium article)
  function scrapeAmazonTitle() {
    const titleSelectors = [
      '#title',                    // Primary selector from article
      '#productTitle',             // Backup selector
      'h1[data-automation-id="product-title"]',
      '.product-title',
      'h1.a-size-large',
      'h1.a-size-medium'
    ];
    
    for (const selector of titleSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent && element.textContent.trim()) {
        return element.textContent.trim();
      }
    }
    
    // Fallback to page title
    return document.title.replace('Amazon.com: ', '').replace('Amazon.ca: ', '').replace('Amazon.co.uk: ', '');
  }

  // Amazon price selectors (based on Medium article)
  function scrapeAmazonPrice() {
    const priceSelectors = [
      '#priceblock_ourprice',        // Primary selector from article
      '#priceblock_dealprice',       // Deal price selector from article
      '.a-price-whole',
      '.a-price .a-offscreen',
      '.a-price-range',
      '.a-price .a-text-price',
      '[data-automation-id="product-price"]'
    ];
    
    for (const selector of priceSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent && element.textContent.trim()) {
        const price = element.textContent.trim();
        if (price.includes('$') || price.includes('€') || price.includes('£')) {
          return price;
        }
      }
    }
    
    // Try to find price in parent elements
    const priceContainers = document.querySelectorAll('[class*="price"], [id*="price"]');
    for (const container of priceContainers) {
      const priceText = container.textContent;
      const priceMatch = priceText.match(/[\$€£]\s*\d+[\.,]\d+|\d+[\.,]\d+\s*[\$€£]/);
      if (priceMatch) {
        return priceMatch[0];
      }
    }
    
    return 'Price not found';
  }

  // Amazon image selectors (based on Medium article)
  function scrapeAmazonImage() {
    const imageSelectors = [
      '#imgTagWrapperId img',         // Primary selector from article
      '#landingImage',
      '#imgBlkFront',
      '.a-dynamic-image',
      '[data-old-hires]',
      '.a-button-selected img',
      '#main-image-container img'
    ];
    
    for (const selector of imageSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        const src = element.src || element.getAttribute('data-old-hires') || element.getAttribute('data-src');
        if (src && !src.includes('data:image')) {
          return src;
        }
      }
    }
    
    return '';
  }

  // Amazon ratings selectors (based on Medium article)
  function scrapeAmazonRatings() {
    const ratingSelectors = [
      '#acrPopover',                  // Primary selector from article
      '.a-icon-alt',
      '[data-automation-id="product-rating"]',
      '.a-icon-star',
      '.a-star-mini'
    ];
    
    for (const selector of ratingSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        // Try to get title attribute first (as suggested in article)
        const titleAttr = element.getAttribute('title');
        if (titleAttr && (titleAttr.includes('out of') || titleAttr.includes('stars'))) {
          return titleAttr.trim();
        }
        
        // Fallback to text content
        if (element.textContent) {
          const ratingText = element.textContent.trim();
          if (ratingText.includes('out of') || ratingText.includes('stars')) {
            return ratingText;
          }
        }
      }
    }
    
    // Try to find review count
    const reviewSelectors = [
      '#acrCustomerReviewText',
      '[data-automation-id="review-count"]',
      '.a-size-base'
    ];
    
    for (const selector of reviewSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent && element.textContent.includes('ratings')) {
        return element.textContent.trim();
      }
    }
    
    return '';
  }

  // Amazon description selectors (based on Medium article)
  function scrapeAmazonDescription() {
    const descriptionSelectors = [
      '#productDescription',          // Primary selector from article
      '#feature-bullets ul',
      '.a-unordered-list',
      '.a-list-item',
      '[data-automation-id="product-description"]'
    ];
    
    for (const selector of descriptionSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent && element.textContent.trim()) {
        const text = element.textContent.trim();
        if (text.length > 50) { // Only return substantial descriptions
          return text.substring(0, 500) + (text.length > 500 ? '...' : ''); // Limit length
        }
      }
    }
    
    return '';
  }

  // Listen for messages from the extension popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scrapeProduct') {
      try {
        const productData = scrapeProductData();
        sendResponse({ success: true, data: productData });
      } catch (error) {
        sendResponse({ success: false, error: error.message });
      }
    }
    return true; // Keep message channel open for async response
  });

})();
