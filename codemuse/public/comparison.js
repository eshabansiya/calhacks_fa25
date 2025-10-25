// Comparison page logic - Updated for Python backend
document.addEventListener('DOMContentLoaded', function() {
    loadAndDisplayProducts();
});

const API_BASE_URL = 'http://localhost:5000';

function loadAndDisplayProducts() {
    const contentDiv = document.getElementById('content');
    
    // Check if we can connect to the Python server
    fetch(`${API_BASE_URL}/api/health`)
        .then(response => {
            if (response.ok) {
                return fetch(`${API_BASE_URL}/api/products`);
            } else {
                throw new Error('Server not responding');
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayProducts(data.products);
            } else {
                contentDiv.innerHTML = '<div class="error">Failed to load products from server</div>';
            }
        })
        .catch(error => {
            console.error('Error loading products:', error);
            contentDiv.innerHTML = `
                <div class="error">
                    <h2>Python Server Not Running</h2>
                    <p>Please start the Flask server first:</p>
                    <pre>python flask_server.py</pre>
                    <p>Then reload this page.</p>
                </div>
            `;
        });
}

function displayProducts(products) {
    const contentDiv = document.getElementById('content');
    
    if (products.length === 0) {
        contentDiv.innerHTML = `
            <div class="no-products">
                <h2>No Products to Compare</h2>
                <p>Add some products using the extension popup to see them compared here.</p>
                <p><strong>Note:</strong> Make sure the Python server is running!</p>
            </div>
        `;
        return;
    }

    let html = `
        <div class="comparison-table">
            <div class="table-header">
                <h2>Comparing ${products.length} Product${products.length > 1 ? 's' : ''}</h2>
                <p>Powered by Python + BeautifulSoup</p>
            </div>
            <div class="products-grid">
    `;

    products.forEach(product => {
        html += `
            <div class="product-column">
                <div class="product-image-container">
                    ${product.image ? 
                        `<img src="${product.image}" alt="${product.title}" class="product-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                         <div class="no-image" style="display:none;">No Image Available</div>` :
                        `<div class="no-image">No Image Available</div>`
                    }
                </div>
                
                <h3 class="product-title">${escapeHtml(product.title || 'Unknown Product')}</h3>
                
                <div class="product-price">${escapeHtml(product.price || 'Price not available')}</div>
                
                ${product.ratings ? `<div class="product-ratings">${escapeHtml(product.ratings)}</div>` : ''}
                
                <div class="product-domain">${escapeHtml(product.domain || 'Unknown Store')}</div>
                
                ${product.description ? `<div class="product-description">${escapeHtml(product.description)}</div>` : ''}
                
                <div class="product-url">
                    <a href="${product.url}" target="_blank" rel="noopener">View Original Product</a>
                </div>
                
                <div class="scraped-info">
                    <small>Scraped: ${new Date(product.scraped_at).toLocaleString()}</small>
                </div>
            </div>
        `;
    });

    html += `
            </div>
        </div>
    `;

    contentDiv.innerHTML = html;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Listen for storage changes to update the comparison in real-time
// Note: This won't work with the Python backend, but we can add polling if needed
setInterval(() => {
    // Optional: Poll for updates every 30 seconds
    // loadAndDisplayProducts();
}, 30000);
