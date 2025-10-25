# Hybrid Amazon Scraper System

A powerful hybrid system combining **Python BeautifulSoup scraping** with a **JavaScript browser extension** for the best of both worlds.

## 🏗️ **System Architecture**

```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│   Browser       │◄─────────────►│   Python Flask  │
│   Extension     │                │   Server        │
│   (JavaScript)  │                │   (BeautifulSoup)│
└─────────────────┘                └─────────────────┘
         │                                   │
         │                                   │
    Chrome APIs                         Amazon.com
    (Get current tab)                    (Web scraping)
```

## ✨ **Key Features**

- 🐍 **Python Backend**: Robust BeautifulSoup scraping
- 🌐 **JavaScript Frontend**: Interactive browser extension
- 🔄 **Real-time Communication**: HTTP API between components
- 📊 **Persistent Storage**: Server-side product storage
- 🎯 **Amazon-Focused**: Optimized selectors for Amazon
- 🛡️ **Error Handling**: Comprehensive error management
- 📱 **Responsive UI**: Works in extension popup and full page

## 🚀 **Quick Start**

### **Option 1: Automated Setup**
```bash
cd codemuse
python start_system.py
```

### **Option 2: Manual Setup**

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Start Python Server:**
   ```bash
   python flask_server.py
   ```

3. **Build Extension:**
   ```bash
   npm run build:extension
   ```

4. **Load Extension:**
   - Go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `build` folder

## 📁 **File Structure**

```
codemuse/
├── flask_server.py              # Python Flask API server
├── amazon_scraper.py            # Standalone Python scraper
├── start_system.py              # Automated startup script
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
├── public/
│   ├── manifest.json            # Extension configuration
│   ├── comparison.html          # Full comparison page
│   └── comparison.js            # Comparison page logic
├── src/
│   ├── App.js                   # Main extension UI
│   └── App.css                  # Extension styling
└── build/                       # Built extension files
```

## 🔧 **How It Works**

### **1. User Interaction**
- User visits Amazon product page
- Clicks extension icon
- Extension gets current tab URL

### **2. Communication**
- Extension sends URL to Python server via HTTP API
- Server validates URL and scrapes product data
- Server returns structured product information

### **3. Data Storage**
- Products stored in Python server memory
- Extension fetches products via API
- Real-time updates between components

### **4. Comparison View**
- Extension opens comparison page in new tab
- Page fetches products from Python server
- Side-by-side product comparison

## 🌐 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scrape` | POST | Scrape product from URL |
| `/api/products` | GET | Get all scraped products |
| `/api/products/<id>` | DELETE | Remove specific product |
| `/api/clear` | POST | Clear all products |
| `/api/health` | GET | Server health check |

### **Example API Usage**

```bash
# Scrape a product
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/dp/B08N5WRWNW"}'

# Get all products
curl http://localhost:5000/api/products

# Health check
curl http://localhost:5000/api/health
```

## 🎯 **Amazon Selectors**

The Python scraper uses proven selectors from the Medium article:

### **Title**
- Primary: `#title`
- Backup: `#productTitle`

### **Price**
- Primary: `#priceblock_ourprice`
- Deal: `#priceblock_dealprice`

### **Image**
- Primary: `#imgTagWrapperId img`
- Backup: `#landingImage`

### **Ratings**
- Primary: `#acrPopover`
- Method: Check `title` attribute first

### **Description**
- Primary: `#productDescription`
- Backup: Feature bullets

## 🔄 **Extension Workflow**

1. **Check Server Status**: Extension verifies Python server is running
2. **Get Current Tab**: Extension gets URL of current Amazon page
3. **Send to Server**: URL sent to Python server for scraping
4. **Receive Data**: Server returns scraped product information
5. **Update UI**: Extension displays new product in list
6. **Persist Data**: Product stored in server memory

## 🛠️ **Development**

### **Python Server Development**
```bash
# Run in debug mode
python flask_server.py

# Test API endpoints
python -c "
import requests
response = requests.get('http://localhost:5000/api/health')
print(response.json())
"
```

### **Extension Development**
```bash
# Build extension
npm run build:extension

# Start development server
npm start
```

### **Testing**
```bash
# Test Python scraper standalone
python amazon_scraper.py

# Test extension with server
python flask_server.py &
npm run build:extension
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **"Python server not running"**
   - Start Flask server: `python flask_server.py`
   - Check if port 5000 is available

2. **"Failed to scrape"**
   - Verify URL is Amazon product page
   - Check Python server logs
   - Ensure internet connection

3. **Extension won't load**
   - Check manifest.json permissions
   - Verify build folder exists
   - Enable Developer mode in Chrome

4. **CORS errors**
   - Flask-CORS is installed and configured
   - Check browser console for specific errors

### **Debug Mode**

Enable debug logging:
```python
# In flask_server.py
app.run(host='localhost', port=5000, debug=True)
```

Check browser console:
```javascript
// In extension
console.log('Server status:', serverStatus);
console.log('API response:', result);
```

## 📊 **Performance**

- **Scraping Speed**: 1-2 seconds per product
- **Memory Usage**: ~50MB for Python server
- **Storage**: In-memory (can be upgraded to database)
- **Concurrent Users**: Single-user system (can be scaled)

## 🔒 **Security Considerations**

- **Local Only**: Server runs on localhost only
- **No Authentication**: Single-user system
- **Rate Limiting**: Built-in delays between requests
- **User Agent**: Realistic browser headers

## 🚀 **Future Enhancements**

- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Multiple website support
- [ ] User authentication
- [ ] Product price tracking
- [ ] Email notifications
- [ ] Mobile app integration

## 📝 **License**

This project is for educational purposes. Please respect Amazon's Terms of Service and use responsibly.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section
2. Review server logs
3. Check browser console
4. Verify all dependencies are installed
5. Ensure Python server is running

---

**Happy Scraping! 🛒✨**
