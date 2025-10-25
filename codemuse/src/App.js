import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [isScraping, setIsScraping] = useState(false);
  const [scrapeMessage, setScrapeMessage] = useState('');
  const [serverStatus, setServerStatus] = useState('checking');

  const API_BASE_URL = 'http://localhost:5000';

  // Check server status on component mount
  useEffect(() => {
    checkServerStatus();
    loadProducts();
  }, []);

  const checkServerStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      if (response.ok) {
        setServerStatus('connected');
      } else {
        setServerStatus('error');
      }
    } catch (error) {
      setServerStatus('disconnected');
      console.error('Server connection failed:', error);
    }
  };

  const loadProducts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/products`);
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setProducts(data.products);
        }
      }
    } catch (error) {
      console.error('Failed to load products:', error);
    }
  };

  const scrapeCurrentPage = async () => {
    if (serverStatus !== 'connected') {
      setScrapeMessage('Python server is not running. Please start the Flask server first.');
      return;
    }

    setIsScraping(true);
    setScrapeMessage('Scraping product data...');

    try {
      // Get current tab URL
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send URL to Python backend
      const response = await fetch(`${API_BASE_URL}/api/scrape`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: tab.url })
      });

      const result = await response.json();
      
      if (result.success) {
        setScrapeMessage('Amazon product added successfully!');
        // Reload products to show the new one
        await loadProducts();
      } else {
        if (result.error === 'Not an Amazon URL') {
          setScrapeMessage('This extension currently only works on Amazon product pages');
        } else {
          setScrapeMessage(`Failed to scrape: ${result.message || result.error}`);
        }
      }
    } catch (error) {
      console.error('Scraping error:', error);
      setScrapeMessage('Error: Could not connect to Python server');
    } finally {
      setIsScraping(false);
      setTimeout(() => setScrapeMessage(''), 3000);
    }
  };

  const removeProduct = async (productId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/products/${productId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        await loadProducts(); // Reload products
      }
    } catch (error) {
      console.error('Failed to remove product:', error);
    }
  };

  const clearAllProducts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/clear`, {
        method: 'POST'
      });
      
      if (response.ok) {
        setProducts([]);
      }
    } catch (error) {
      console.error('Failed to clear products:', error);
    }
  };

  const openComparisonPage = () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('comparison.html') });
  };

  const getServerStatusMessage = () => {
    switch (serverStatus) {
      case 'connected':
        return '✅ Python server connected';
      case 'disconnected':
        return '❌ Python server not running';
      case 'error':
        return '⚠️ Server error';
      default:
        return '🔄 Checking server...';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Shopping Comparison</h1>
        <p className="amazon-note">Hybrid: Python + JavaScript</p>
        
        <div className="server-status">
          {getServerStatusMessage()}
        </div>
        
        <div className="action-buttons">
          <button 
            className="scrape-button"
            onClick={scrapeCurrentPage}
            disabled={isScraping || serverStatus !== 'connected'}
          >
            {isScraping ? 'Scraping...' : 'Add Amazon Product'}
          </button>
          
          {products.length > 0 && (
            <button 
              className="comparison-button"
              onClick={openComparisonPage}
            >
              View Full Comparison
            </button>
          )}
        </div>

        {scrapeMessage && (
          <div className="message">
            {scrapeMessage}
          </div>
        )}

        <div className="products-section">
          <div className="products-header">
            <h3>Saved Products ({products.length})</h3>
            {products.length > 0 && (
              <button 
                className="clear-button"
                onClick={clearAllProducts}
              >
                Clear All
              </button>
            )}
          </div>

          <div className="products-list">
            {products.length === 0 ? (
              <p className="no-products">
                {serverStatus === 'connected' 
                  ? 'No products saved yet. Visit an Amazon product page and click "Add Amazon Product" to start comparing!'
                  : 'Start the Python server first, then visit an Amazon product page to scrape products.'
                }
              </p>
            ) : (
              products.map(product => (
                <div key={product.id} className="product-card">
                  <div className="product-image">
                    {product.image ? (
                      <img src={product.image} alt={product.title} />
                    ) : (
                      <div className="no-image">No Image</div>
                    )}
                  </div>
                  <div className="product-info">
                    <h4 className="product-title">{product.title}</h4>
                    <div className="product-price">{product.price}</div>
                    {product.ratings && (
                      <div className="product-ratings">{product.ratings}</div>
                    )}
                    <div className="product-domain">{product.domain}</div>
                  </div>
                  <button 
                    className="remove-button"
                    onClick={() => removeProduct(product.id)}
                    title="Remove product"
                  >
                    ×
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
