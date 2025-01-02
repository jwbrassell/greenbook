# Frontend Development Troubleshooting

## Table of Contents
- [Frontend Development Troubleshooting](#frontend-development-troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [Build Process Issues](#build-process-issues)
    - [Common Build Problems](#common-build-problems)
- [Check Node.js and npm versions](#check-nodejs-and-npm-versions)
- [Clear npm cache](#clear-npm-cache)
- [Check for package issues](#check-for-package-issues)
- [Rebuild node modules](#rebuild-node-modules)
    - [Webpack Issues](#webpack-issues)
- [Check webpack configuration](#check-webpack-configuration)
- [Debug webpack build](#debug-webpack-build)
- [Analyze bundle size](#analyze-bundle-size)
- [Check for duplicate dependencies](#check-for-duplicate-dependencies)
  - [Package Management](#package-management)
    - [Dependency Issues](#dependency-issues)
- [Check for package conflicts](#check-for-package-conflicts)
- [Update packages](#update-packages)
- [Fix package issues](#fix-package-issues)
- [Check package versions](#check-package-versions)
    - [Yarn Issues](#yarn-issues)
- [Check yarn installation](#check-yarn-installation)
- [Clear cache](#clear-cache)
- [Check for outdated packages](#check-for-outdated-packages)
- [Upgrade packages](#upgrade-packages)
  - [Browser Compatibility](#browser-compatibility)
    - [Cross-Browser Testing](#cross-browser-testing)
- [Browser-sync for testing](#browser-sync-for-testing)
- [Autoprefixer check](#autoprefixer-check)
- [Check babel configuration](#check-babel-configuration)
    - [CSS Issues](#css-issues)
- [Validate CSS](#validate-css)
- [Check browser support](#check-browser-support)
- [Analyze CSS](#analyze-css)
  - [Asset Optimization](#asset-optimization)
    - [Image Optimization](#image-optimization)
- [Optimize images](#optimize-images)
- [Check image sizes](#check-image-sizes)
- [Convert image formats](#convert-image-formats)
    - [JavaScript Optimization](#javascript-optimization)
- [Analyze bundle size](#analyze-bundle-size)
- [Check for unused exports](#check-for-unused-exports)
- [Minify JavaScript](#minify-javascript)
  - [Development Server Issues](#development-server-issues)
    - [Local Server Problems](#local-server-problems)
- [Check ports in use](#check-ports-in-use)
- [Kill process using port](#kill-process-using-port)
- [Check development logs](#check-development-logs)
    - [Hot Module Replacement](#hot-module-replacement)
- [Check webpack dev server](#check-webpack-dev-server)
- [Monitor file changes](#monitor-file-changes)
- [Clear webpack cache](#clear-webpack-cache)
  - [Testing Issues](#testing-issues)
    - [Unit Test Problems](#unit-test-problems)
- [Run tests with debugging](#run-tests-with-debugging)
- [Update snapshots](#update-snapshots)
- [Check test coverage](#check-test-coverage)
- [Run specific tests](#run-specific-tests)
    - [E2E Test Issues](#e2e-test-issues)
- [Cypress debugging](#cypress-debugging)
- [Check Selenium setup](#check-selenium-setup)
- [Clear test cache](#clear-test-cache)
  - [Performance Issues](#performance-issues)
    - [Runtime Performance](#runtime-performance)
    - [Loading Performance](#loading-performance)
- [Lighthouse CLI](#lighthouse-cli)
- [WebPageTest CLI](#webpagetest-cli)
- [Bundle analysis](#bundle-analysis)
  - [Common Frontend Errors](#common-frontend-errors)
    - [JavaScript Runtime Errors](#javascript-runtime-errors)
    - [Network Request Issues](#network-request-issues)
- [Check network requests](#check-network-requests)
- [Monitor API calls](#monitor-api-calls)
- [Test CORS](#test-cors)
  - [Framework-Specific Issues](#framework-specific-issues)
    - [React Problems](#react-problems)
- [Check React version](#check-react-version)
- [Debug with React DevTools](#debug-with-react-devtools)
- [Install React Developer Tools extension](#install-react-developer-tools-extension)
- [Performance profiling](#performance-profiling)
    - [Vue.js Issues](#vuejs-issues)
- [Vue CLI troubleshooting](#vue-cli-troubleshooting)
- [Check Vue configuration](#check-vue-configuration)
- [Debug with Vue DevTools](#debug-with-vue-devtools)
- [Install Vue Developer Tools extension](#install-vue-developer-tools-extension)
  - [Best Practices](#best-practices)
    - [Development Environment](#development-environment)
    - [Code Quality](#code-quality)
  - [Monitoring and Debugging](#monitoring-and-debugging)
    - [Error Tracking](#error-tracking)
- [Setup error tracking](#setup-error-tracking)
- [Initialize Sentry](#initialize-sentry)
    - [Performance Monitoring](#performance-monitoring)
- [Web Vitals monitoring](#web-vitals-monitoring)
- [Initialize monitoring](#initialize-monitoring)
  - [Documentation](#documentation)



## Build Process Issues

### Common Build Problems

**Symptoms:**
- Build failures
- Compilation errors
- Asset processing issues
- Module resolution errors

**Node.js/npm Issues:**
```bash
# Check Node.js and npm versions
node -v
npm -v

# Clear npm cache
npm cache clean --force

# Check for package issues
npm audit
npm outdated

# Rebuild node modules
rm -rf node_modules package-lock.json
npm install
```

### Webpack Issues

**Common Problems:**
```bash
# Check webpack configuration
cat webpack.config.js

# Debug webpack build
webpack --debug --display-error-details

# Analyze bundle size
webpack-bundle-analyzer stats.json

# Check for duplicate dependencies
npm ls package-name
```

## Package Management

### Dependency Issues

**npm Troubleshooting:**
```bash
# Check for package conflicts
npm ls

# Update packages
npm update

# Fix package issues
npm audit fix
npm dedupe

# Check package versions
npm list package-name
npm view package-name versions
```

### Yarn Issues

```bash
# Check yarn installation
yarn --version

# Clear cache
yarn cache clean

# Check for outdated packages
yarn outdated

# Upgrade packages
yarn upgrade-interactive --latest
```

## Browser Compatibility

### Cross-Browser Testing

**Tools and Commands:**
```bash
# Browser-sync for testing
browser-sync start --server --files "css/*.css"

# Autoprefixer check
npx autoprefixer-info

# Check babel configuration
cat .babelrc
```

### CSS Issues

```bash
# Validate CSS
npx stylelint "src/**/*.css"

# Check browser support
npx browserslist

# Analyze CSS
npx parker css/main.css
```

## Asset Optimization

### Image Optimization

```bash
# Optimize images
npx imagemin images/* --out-dir=dist/images

# Check image sizes
du -sh images/*

# Convert image formats
convert image.jpg image.webp
```

### JavaScript Optimization

```bash
# Analyze bundle size
source-map-explorer dist/main.js

# Check for unused exports
webpack-unused-exports

# Minify JavaScript
terser input.js -o output.min.js
```

## Development Server Issues

### Local Server Problems

**Symptoms:**
- Server won't start
- Hot reload not working
- Port conflicts
- WebSocket issues

**Commands:**
```bash
# Check ports in use
lsof -i :3000
netstat -tulpn | grep LISTEN

# Kill process using port
kill -9 $(lsof -t -i:3000)

# Check development logs
tail -f npm-debug.log
```

### Hot Module Replacement

```bash
# Check webpack dev server
webpack-dev-server --progress --debug

# Monitor file changes
watchman watch-list

# Clear webpack cache
rm -rf .webpack-cache/
```

## Testing Issues

### Unit Test Problems

```bash
# Run tests with debugging
jest --debug

# Update snapshots
jest -u

# Check test coverage
jest --coverage

# Run specific tests
jest path/to/test
```

### E2E Test Issues

```bash
# Cypress debugging
cypress run --debug

# Check Selenium setup
selenium-standalone start

# Clear test cache
cypress cache clear
```

## Performance Issues

### Runtime Performance

**Chrome DevTools Commands:**
```javascript
// Performance monitoring
console.time('Operation');
// ... code ...
console.timeEnd('Operation');

// Memory leaks
console.profile('Memory Profile');
// ... actions ...
console.profileEnd();
```

### Loading Performance

```bash
# Lighthouse CLI
lighthouse http://localhost:3000

# WebPageTest CLI
webpagetest test http://localhost:3000

# Bundle analysis
webpack-bundle-analyzer stats.json
```

## Common Frontend Errors

### JavaScript Runtime Errors

**Debug Techniques:**
```javascript
// Add error boundary
window.onerror = function(msg, url, lineNo, columnNo, error) {
    console.log('Error: ' + msg);
    return false;
};

// Debug event listeners
getEventListeners(element);

// Memory leak detection
chrome.heapSnapshot();
```

### Network Request Issues

```bash
# Check network requests
curl -I http://localhost:3000

# Monitor API calls
mitmproxy

# Test CORS
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://api.example.com
```

## Framework-Specific Issues

### React Problems

```bash
# Check React version
npm list react

# Debug with React DevTools
# Install React Developer Tools extension

# Performance profiling
react-addons-perf.start();
// ... actions ...
react-addons-perf.stop();
react-addons-perf.printWasted();
```

### Vue.js Issues

```bash
# Vue CLI troubleshooting
vue inspect

# Check Vue configuration
cat vue.config.js

# Debug with Vue DevTools
# Install Vue Developer Tools extension
```

## Best Practices

### Development Environment

1. **Editor Setup:**
   ```bash
   # ESLint configuration
   npm install eslint --save-dev
   eslint --init
   
   # Prettier setup
   npm install prettier --save-dev
   echo {}> .prettierrc
   ```

2. **Version Control:**
   ```bash
   # Git hooks setup
   npm install husky --save-dev
   
   # Add pre-commit hooks
   "husky": {
     "hooks": {
       "pre-commit": "lint-staged"
     }
   }
   ```

### Code Quality

1. **Linting:**
   ```bash
   # Run ESLint
   eslint src/
   
   # Fix auto-fixable issues
   eslint src/ --fix
   
   # Run Prettier
   prettier --write src/
   ```

2. **Type Checking:**
   ```bash
   # TypeScript check
   tsc --noEmit
   
   # Flow check
   flow check
   ```

## Monitoring and Debugging

### Error Tracking

```bash
# Setup error tracking
npm install @sentry/browser
npm install @sentry/tracing

# Initialize Sentry
Sentry.init({
  dsn: "your-dsn",
  tracesSampleRate: 1.0,
});
```

### Performance Monitoring

```bash
# Web Vitals monitoring
npm install web-vitals

# Initialize monitoring
import {getCLS, getFID, getLCP} from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getLCP(console.log);
```

## Documentation

1. **Code Documentation:**
   - JSDoc comments
   - README files
   - API documentation
   - Component documentation

2. **Build Process:**
   - Build configuration
   - Environment setup
   - Deployment procedures
   - Debug procedures

3. **Testing:**
   - Test coverage reports
   - Testing strategies
   - CI/CD pipeline
   - Performance benchmarks
