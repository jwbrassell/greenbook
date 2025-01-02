"""
Flask-Caching Example - Performance Optimization
Shows how to implement efficient caching compared to PHP's file-based approach
"""

from flask import Flask, jsonify
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Cache Configuration
cache_config = {
    "DEBUG": True,
    "CACHE_TYPE": "redis",  # Can also use 'simple' for in-memory caching
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 300  # 5 minutes
}

"""
PHP Traditional Caching:
```php
// Cache using files
function get_cached_data($key, $ttl = 300) {
    $cache_file = "cache/{$key}.json";
    
    if (file_exists($cache_file) && (time() - filemtime($cache_file) < $ttl)) {
        return json_decode(file_get_contents($cache_file), true);
    }
    
    // Get fresh data
    $data = get_fresh_data();
    file_put_contents($cache_file, json_encode($data));
    return $data;
}
```
"""

app.config.from_mapping(cache_config)
cache = Cache(app)
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# Basic Caching Examples

@app.route('/product/<int:id>')
@cache.memoize(timeout=300)
def get_product(id):
    """
    Cache individual product lookups
    
    PHP Equivalent:
    ```php
    function get_product($id) {
        $cache_file = "cache/product_{$id}.json";
        
        if (file_exists($cache_file) && (time() - filemtime($cache_file) < 300)) {
            return json_decode(file_get_contents($cache_file), true);
        }
        
        $product = fetch_from_database($id);
        file_put_contents($cache_file, json_encode($product));
        return $product;
    }
    ```
    """
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price
    })

@app.route('/products')
@cache.cached(timeout=300)
def get_all_products():
    """Cache entire product list"""
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price
    } for p in products])

# Function Caching with Parameters

@cache.memoize(timeout=300)
def get_products_by_price_range(min_price, max_price):
    """Cache function results based on parameters"""
    return Product.query.filter(
        Product.price >= min_price,
        Product.price <= max_price
    ).all()

@app.route('/products/price-range')
def products_by_price():
    min_price = float(request.args.get('min', 0))
    max_price = float(request.args.get('max', 1000))
    products = get_products_by_price_range(min_price, max_price)
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price
    } for p in products])

# Computed Values Caching

@cache.cached(timeout=3600, key_prefix='product_stats')
def get_product_stats():
    """Cache computed statistics"""
    products = Product.query.all()
    return {
        'total_products': len(products),
        'avg_price': sum(p.price for p in products) / len(products),
        'price_range': {
            'min': min(p.price for p in products),
            'max': max(p.price for p in products)
        }
    }

# Partial Caching with Template Fragments

"""
In templates:
```html
{% cache 300, 'product-list', page %}
    {% for product in products %}
        <div class="product">
            <h3>{{ product.name }}</h3>
            <p>{{ product.price }}</p>
        </div>
    {% endfor %}
{% endcache %}
```
"""

# Cache Invalidation Examples

def update_product(id, data):
    """
    Update product and invalidate related caches
    
    PHP Equivalent:
    ```php
    function update_product($id, $data) {
        update_database($id, $data);
        
        // Manual cache cleanup
        unlink("cache/product_{$id}.json");
        unlink("cache/all_products.json");
        unlink("cache/product_stats.json");
    }
    ```
    """
    product = Product.query.get_or_404(id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Invalidate specific caches
    cache.delete_memoized(get_product, id)
    cache.delete('products')
    cache.delete('product_stats')

# Cache Decorators with Dynamic Timeout

def get_cache_timeout(base_timeout=300):
    """Dynamic cache timeout based on time of day"""
    hour = datetime.now().hour
    if 0 <= hour < 6:  # Less traffic at night
        return base_timeout * 2
    return base_timeout

@cache.cached(timeout=get_cache_timeout)
def get_featured_products():
    """Cache with dynamic timeout"""
    return Product.query.filter_by(featured=True).all()

# Cache Keys with Multiple Parameters

@cache.memoize()
def search_products(query, category=None, min_price=None, max_price=None):
    """
    Complex query caching
    Cache key automatically includes all parameters
    """
    products = Product.query
    
    if query:
        products = products.filter(Product.name.ilike(f'%{query}%'))
    if category:
        products = products.filter_by(category=category)
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)
        
    return products.all()

# Rate Limiting with Cache

def get_request_count(user_id):
    """Track API request count per user"""
    key = f'request_count_{user_id}'
    count = cache.get(key) or 0
    return count

def increment_request_count(user_id):
    """Increment and cache request count"""
    key = f'request_count_{user_id}'
    count = get_request_count(user_id) + 1
    cache.set(key, count, timeout=3600)  # Reset after 1 hour
    return count

@app.route('/api/data')
def api_endpoint():
    """Rate-limited endpoint using cache"""
    user_id = get_current_user_id()
    count = increment_request_count(user_id)
    
    if count > 100:  # Rate limit: 100 requests per hour
        return jsonify({'error': 'Rate limit exceeded'}), 429
        
    # Process request...
    return jsonify({'data': 'some data'})

# Best Practices

"""
1. Cache Strategy:
   - Cache expensive operations
   - Use appropriate timeouts
   - Consider cache invalidation
   - Monitor cache hit rates

2. Cache Keys:
   - Use descriptive prefixes
   - Include relevant parameters
   - Consider version numbers
   - Handle special characters

3. Cache Backends:
   - Redis for distributed caching
   - Memcached for simple caching
   - FileSystem for development
   - Simple for single-worker setups

4. Performance Tips:
   - Cache database queries
   - Cache API responses
   - Cache template fragments
   - Use memoization for functions

5. Cache Invalidation:
   - Update cache on data changes
   - Use cache versioning
   - Implement cache warming
   - Handle race conditions

Example of cache warming:
```python
def warm_cache():
    # Pre-populate cache on startup
    products = Product.query.all()
    for product in products:
        cache.set(f'product_{product.id}', product)
    cache.set('all_products', products)
```

6. Error Handling:
```python
def get_cached_data(key):
    try:
        return cache.get(key)
    except Exception as e:
        logger.error(f"Cache error: {e}")
        return None
```

7. Monitoring:
```python
def get_cache_stats():
    return {
        'hits': cache.get('stats_hits') or 0,
        'misses': cache.get('stats_misses') or 0,
        'size': len(cache.cache._cache)  # For simple cache
    }
```
"""

if __name__ == '__main__':
    app.run(debug=True)
