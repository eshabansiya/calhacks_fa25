# CodeMuse Browser Extension

A React-based browser extension that demonstrates how to convert a React app into a functional browser extension.

## Features

- ✅ React-powered interface
- ✅ Modern browser extension (Manifest V3)
- ✅ Developer-friendly
- ✅ Chrome API integration
- ✅ Responsive popup design

## How to Load the Extension

### Step 1: Build the Extension
```bash
npm run build:extension
```

### Step 2: Load in Chrome/Edge
1. Open Chrome or Edge browser
2. Navigate to `chrome://extensions/` (or `edge://extensions/` for Edge)
3. Enable "Developer mode" (toggle in the top-right corner)
4. Click "Load unpacked"
5. Select the `build` folder from your project directory
6. The extension should now appear in your extensions list

### Step 3: Test the Extension
1. Look for the CodeMuse icon in your browser toolbar
2. Click the icon to open the extension popup
3. Try the "Get Current Tab Info" button to test Chrome API integration

## Project Structure

```
codemuse/
├── public/
│   ├── manifest.json          # Extension manifest
│   ├── icons/                 # Extension icons
│   └── index.html            # Main HTML file
├── src/
│   ├── App.js                # Main React component
│   ├── App.css               # Extension-specific styles
│   └── index.js              # React entry point
├── build/                    # Built extension files
└── package.json              # Dependencies and scripts
```

## Key Files

- **`manifest.json`**: Defines the extension's metadata, permissions, and behavior
- **`App.js`**: Main React component with extension functionality
- **`App.css`**: Styled for extension popup dimensions (400x600px)
- **`.eslintrc.js`**: ESLint configuration with Chrome API globals

## Extension Capabilities

The extension includes:
- **Popup Interface**: React-based UI that opens when clicking the extension icon
- **Chrome API Access**: Can query current tab information
- **Storage Permission**: Ready for data persistence
- **Active Tab Permission**: Can interact with the current tab

## Development

### Available Scripts

- `npm start`: Start development server
- `npm run build`: Build for production
- `npm run build:extension`: Build optimized for browser extension
- `npm test`: Run tests

### Building for Extension

The `build:extension` script:
- Disables inline runtime chunks (required for extensions)
- Disables source maps (reduces file size)
- Creates optimized production build

## Customization

### Adding New Features
1. Modify `src/App.js` to add new functionality
2. Update `manifest.json` permissions if needed
3. Rebuild with `npm run build:extension`
4. Reload the extension in your browser

### Styling
- Modify `src/App.css` for styling changes
- The popup is sized at 400x600px for optimal display

### Chrome API Integration
- Add new permissions to `manifest.json`
- Use Chrome APIs in your React components
- Remember to check for API availability

## Troubleshooting

### Extension Won't Load
- Ensure you're selecting the `build` folder, not the root project folder
- Check that Developer mode is enabled
- Verify the manifest.json is valid

### Chrome API Not Working
- Check that required permissions are in manifest.json
- Ensure you're testing in the extension popup, not a regular web page
- Use `typeof chrome !== 'undefined'` checks

### Build Errors
- Run `npm install` to ensure dependencies are installed
- Check for ESLint errors and fix them
- Ensure all required files are present

## Next Steps

Consider adding:
- Content scripts for page interaction
- Background scripts for continuous operation
- Options page for settings
- More Chrome API integrations
- Data persistence with chrome.storage
- Cross-browser compatibility

## Resources

- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [Manifest V3 Migration Guide](https://developer.chrome.com/docs/extensions/migrating/)
- [React Documentation](https://reactjs.org/docs/)
