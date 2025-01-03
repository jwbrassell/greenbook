# Chapter 5: Performance and Optimization

## Introduction

Thiok abtun  unrcger  nco  arp-myzuenend tr oetidizu weivmngdfne-reducerw mghtneimprSimlyeradytami r,r ndeiresptimiieveny  omponcnt.oSimile,dy, alplication times, improneq iresficiencyingandde,ngeduceverload tymes,pi provifgh ff.  ehcy,sand finc-tanpng everyrp wt lf ahe systen. In wh s phaptet,zwe' appcaanihnwsto mptcmizaplain1endmbeatio p## The Sto.

##r1. FroLyendoOpMimiztoion

###rThSoreLyMaphor

Thkofftdopimizionlitolyout:
-Atrgazaionliroduinlactmd tmization like store layout:
ssCachang tikioinvlntoiyem nrgemeot
- Luadicgt lrntgyikumerfw
acP imicslikals-mntgice
-gUs reexper ecceus klowstmsifaction
- Performance metrics like sales metrics
###UAereteOetimiz tion

```javaslripi customer satisfaction
//webpck.cig.js
cs ph= rquie('ph');
nMiCsExtrctPugin#=#rOquiio('mini-css-exrc-plugin');
stTerPlug =rqui('trs-webpck-plugn');
csCmrssonlug = rqui('ompion-wbpk-plu');

mole.exort ={
mo:'oduton',
  enr:'//sck/igd.x.j',
contautput: {
 =(hph:pa.rv(__dirnm, 'dit'),
contiEPrfeie(amm:c'[nams].[cxct-nthash].js',plugin');
 contnrec-el:ruconst CompressionPlugin = require('compression-webpack-plugin');
 },module.exports = {
 doion',: {
   miimiz: [eTsrPlg()],    entry: './src/index.js',
  t    tpo(_nhsnk):{
 l:mn]    tcnk:'',    },
n    im  l]axIn hialRuq:essIiy,
     c'mSz: 0,
     iq itcachG pc:a{: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name(module) {
                        const packageName = module.context.match(
                            /[\\/]node_modules[\\/](.*?)([\\/]|$)/
                        )[1];
                        return `vendor.${packageName.replace('@', '')}`;
                    }
                }
            }
        }
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                        plugins: ['@babel/plugin-transform-runtime']
                    }
                }
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader'
                ]
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset',
                parser: {
                    dataUrlCondition: {
                        maxSize: 8 * 1024 // 8kb
                    }
                }
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css'
        }),
        new CompressionPlugin({
            test: /\.(js|css|html|svg)$/,
            algorithm: 'gzip'
        })
    ]
};
```

### Caching Strategy

```javascript
// service-worker.js
const CACHE_NAME = 'app-cache-v1';
const URLS_TO_CACHE = [
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/api/data'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(URLS_TO_CACHE))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                
                return fetch(event.request).then(response => {
                    if (!response || response.status !== 200) {
                        return response;
                    }
                    
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(
                                event.request,
                                responseToCache
                            );
                        });
                    
                    return response;
                });
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
```

### Hands-On Exercise: Performance Optimization

Create optimized frontend:
```javascript
// performance_optimizer.js
class PerformanceOptimizer {
    constructor() {
        this.metrics = {};
        this.observers = new Map();
        this.setupObservers();
    }
    
    setupObservers() {
        // Performance observer
        this.observers.set('performance', new PerformanceObserver(list => {
            for (const entry of list.getEntries()) {
                this.metrics[entry.name] = entry.startTime;
            }
        }));
        
        // Long task observer
        this.observers.set('longtask', new PerformanceObserver(list => {
            for (const entry of list.getEntries()) {
                console.warn('Long task detected:', entry.duration);
            }
        }));
        
        // Layout shift observer
        this.observers.set('layout-shift', new PerformanceObserver(list => {
            for (const entry of list.getEntries()) {
                if (!entry.hadRecentInput) {
                    this.metrics.cls = (this.metrics.cls || 0) + entry.value;
                }
            }
        }));
        
        // First paint observer
        this.observers.set('paint', new PerformanceObserver(list => {
            for (const entry of list.getEntries()) {
                this.metrics[entry.name] = entry.startTime;
            }
        }));
        
        // Resource timing observer
        this.observers.set('resource', new PerformanceObserver(list => {
            for (const entry of list.getEntries()) {
                if (!this.metrics.resources) {
                    this.metrics.resources = [];
                }
                this.metrics.resources.push({
                    name: entry.name,
                    duration: entry.duration,
                    size: entry.transferSize
                });
            }
        }));
        
        // Start observing
        this.observers.get('performance').observe({
            entryTypes: ['navigation', 'resource']
        });
        this.observers.get('longtask').observe({
            entryTypes: ['longtask']
        });
        this.observers.get('layout-shift').observe({
            entryTypes: ['layout-shift']
        });
        this.observers.get('paint').observe({
            entryTypes: ['paint']
        });
        this.observers.get('resource').observe({
            entryTypes: ['resource']
        });
    }
    
    lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    deferScripts() {
        const scripts = document.querySelectorAll(
            'script[data-defer]'
        );
        
        scripts.forEach(script => {
            const deferredScript = document.createElement('script');
            
            Array.from(script.attributes).forEach(attr => {
                if (attr.name !== 'data-defer') {
                    deferredScript.setAttribute(
                        attr.name,
                        attr.value
                    );
                }
            });
            
            deferredScript.textContent = script.textContent;
            script.parentNode.replaceChild(
                deferredScript,
                script
            );
        });
    }
    
    optimizeAnimations() {
        const animatedElements = document.querySelectorAll(
            '.animated'
        );
        
        animatedElements.forEach(element => {
            element.style.willChange = 'transform';
            
            element.addEventListener('animationend', () => {
                element.style.willChange = 'auto';
            });
        });
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    optimizeEventListeners() {
        // Optimize scroll handler
        const scrollHandler = this.throttle(() => {
            // Handle scroll event
        }, 100);
        
        window.addEventListener('scroll', scrollHandler);
        
        // Optimize resize handler
        const resizeHandler = this.debounce(() => {
            // Handle resize event
        }, 250);
        
        window.addEventListener('resize', resizeHandler);
    }
    
    preloadCriticalAssets() {
        const assets = [
            '/styles/main.css',
            '/scripts/app.js',
            '/images/hero.jpg'
        ];
        
        assets.forEach(asset => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = asset;
            
            if (asset.endsWith('.css')) {
                link.as = 'style';
            } else if (asset.endsWith('.js')) {
                link.as = 'script';
            } else if (asset.match(/\.(jpg|png|gif|svg)$/)) {
                link.as = 'image';
            }
            
            document.head.appendChild(link);
        });
    }
    
    optimizeFonts() {
        // Add font display swap
        const fontStyle = document.createElement('style');
        fontStyle.textContent = `
            @font-face {
                font-family: 'CustomFont';
                src: url('/fonts/custom-font.woff2') format('woff2');
                font-display: swap;
            }
        `;
        document.head.appendChild(fontStyle);
        
        // Preload critical fonts
        const fontPreload = document.createElement('link');
        fontPreload.rel = 'preload';
        fontPreload.href = '/fonts/custom-font.woff2';
        fontPreload.as = 'font';
        fontPreload.type = 'font/woff2';
        fontPreload.crossOrigin = 'anonymous';
        document.head.appendChild(fontPreload);
    }
    
    getMetrics() {
        return {
            ...this.metrics,
            // Core Web Vitals
            LCP: this.metrics['largest-contentful-paint'],
            FID: this.metrics['first-input-delay'],
            CLS: this.metrics.cls,
            // Other metrics
            TTFB: this.metrics['time-to-first-byte'],
            FCP: this.metrics['first-contentful-paint'],
            DCL: this.metrics['DOMContentLoaded'],
            Load: this.metrics['load']
        };
    }
}

// Example usage
const optimizer = new PerformanceOptimizer();

// Initialize optimizations
document.addEventListener('DOMContentLoaded', () => {
    optimizer.lazyLoadImages();
    optimizer.deferScripts();
    optimizer.optimizeAnimations();
    optimizer.optimizeEventListeners();
    optimizer.preloadCriticalAssets();
    optimizer.optimizeFonts();
});

// Monitor performance
setInterval(() => {
    const metrics = optimizer.getMetrics();
    console.log('Performance Metrics:', metrics);
}, 5000);
```

## 2. Backend Optimization

### The Warehouse Efficiency Metaphor

Think of backend optimization like warehouse efficiency:
- Database like inventory storage
- Caching like quick-access shelves
- Queries like order picking
- Indexing like organization system
- Load balancing like worker distribution

### Database Optimization

```python
# database_optimizer.py
from sqlalchemy import create_engine, text
from typing import List, Dict
import logging
import time

class DatabaseOptimizer:
    """Optimizes database performance."""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.logger = logging.getLogger('db_optimizer')
    
    def analyze_queries(self, days: int = 1) -> List[Dict]:
        """Analyze slow queries."""
        query = """
        SELECT 
            query,
            calls,
            total_time,
            mean_time,
            rows
        FROM pg_stat_statements
        WHERE last_call >= NOW() - INTERVAL ':days days'
        ORDER BY total_time DESC
        LIMIT 10
        """
        
        with self.engine.connect() as conn:
            result = conn.execute(
                text(query),
                {'days': days}
            )
            return [dict(row) for row in result]
    
    def suggest_indexes(self) -> List[Dict]:
        """Suggest missing indexes."""
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            seq_scan,
            seq_tup_read,
            idx_scan,
            idx_tup_fetch
        FROM pg_stat_user_tables
        WHERE seq_scan > idx_scan
        AND seq_tup_read > 10000
        ORDER BY seq_tup_read DESC
        """
        
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row) for row in result]
    
    def analyze_table_bloat(self) -> List[Dict]:
        """Analyze table bloat."""
        query = """
        SELECT
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size('"'||schemaname||'"."'||tablename||'"')) as total_size,
            pg_size_pretty(pg_relation_size('"'||schemaname||'"."'||tablename||'"')) as table_size,
            pg_size_pretty(pg_total_relation_size('"'||schemaname||'"."'||tablename||'"') - 
                          pg_relation_size('"'||schemaname||'"."'||tablename||'"')) as bloat_size
        FROM pg_stat_user_tables
        ORDER BY pg_total_relation_size('"'||schemaname||'"."'||tablename||'"') DESC
        """
        
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row) for row in result]
    
    def optimize_table(self, table: str) -> None:
        """Optimize single table."""
        with self.engine.connect() as conn:
            # Analyze table
            conn.execute(
                text(f"ANALYZE {table}")
            )
            
            # Vacuum table
            conn.execute(
                text(f"VACUUM ANALYZE {table}")
            )
    
    def create_index(
        self,
        table: str,
        columns: List[str],
        index_type: str = 'btree'
    ) -> None:
        """Create index on table."""
        index_name = f"idx_{table}_{'_'.join(columns)}"
        columns_str = ', '.join(columns)
        
        with self.engine.connect() as conn:
            conn.execute(text(
                f"CREATE INDEX CONCURRENTLY {index_name} "
                f"ON {table} USING {index_type} ({columns_str})"
            ))
    
    def optimize_queries(
        self,
        queries: List[str]
    ) -> List[Dict]:
        """Analyze and optimize queries."""
        results = []
        
        for query in queries:
            # Explain query
            with self.engine.connect() as conn:
                explain = conn.execute(
                    text(f"EXPLAIN ANALYZE {query}")
                )
                
                # Measure execution time
                start = time.time()
                conn.execute(text(query))
                duration = time.time() - start
                
                results.append({
                    'query': query,
                    'duration': duration,
                    'plan': [row[0] for row in explain]
                })
        
        return results
    
    def setup_partitioning(
        self,
        table: str,
        column: str,
        interval: str = '1 month'
    ) -> None:
        """Setup table partitioning."""
        with self.engine.connect() as conn:
            # Create partitioned table
            conn.execute(text(
                f"CREATE TABLE {table}_partitioned "
                f"PARTITION BY RANGE ({column})"
            ))
            
            # Create partitions
            for i in range(12):
                conn.execute(text(
                    f"CREATE TABLE {table}_y2023m{i+1} "
                    f"PARTITION OF {table}_partitioned "
                    f"FOR VALUES FROM "
                    f"('2023-{i+1}-01') TO "
                    f"('2023-{i+2}-01')"
                ))
    
    def setup_caching(
        self,
        tables: List[str]
    ) -> None:
        """Setup table caching."""
        with self.engine.connect() as conn:
            for table in tables:
                # Set cache policy
                conn.execute(text(
                    f"ALTER TABLE {table} "
                    f"SET (fillfactor = 90)"
                ))
                
                # Create cache table
                conn.execute(text(
                    f"CREATE MATERIALIZED VIEW {table}_cache "
                    f"AS SELECT * FROM {table}"
                ))
    
    def generate_report(self) -> Dict:
        """Generate optimization report."""
        return {
            'slow_queries': self.analyze_queries(),
            'missing_indexes': self.suggest_indexes(),
            'table_bloat': self.analyze_table_bloat()
        }

# Example usage
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create optimizer
    optimizer = DatabaseOptimizer(
        'postgresql://user:pass@localhost/db'
    )
    
    # Generate report
    report = optimizer.generate_report()
    
    # Optimize based on findings
    for table in report['table_bloat']:
        optimizer.optimize_table(table['tablename'])
    
    for index in report['missing_indexes']:
        optimizer.create_index(
            index['tablename'],
            [index['indexname']]
        )
```

### Caching Implementation

```python
# caching.py
from functools import wraps
import redis
import json
import time
from typing import Any, Callable, Optional

class CacheManager:
    """Manages application caching."""
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0
    ):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
    
    def cache(
        self,
        key_prefix: str,
        expire: int = 3600
    ) -> Callable:
        """Cache decorator."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Generate cache key
                key = f"{key_prefix}:{func.__name__}:"
                key += ":".join(str(arg) for arg in args)
                key += ":".join(
                    f"{k}={v}"
                    for k, v in sorted(kwargs.items())
                )
                
                # Check cache
                cached = self.redis.get(key)
                if cached:
                    return json.loads(cached)
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Cache result
                self.redis.setex(
                    key,
                    expire,
                    json.dumps(result)
                )
                
                return result
            return wrapper
        return decorator
    
    def memoize(
        self,
        func: Callable,
        key_prefix: str,
        expire: int = 3600
    ) -> Any:
        """Memoize function result."""
        key = f"{key_prefix}:{func.__name__}"
        
        # Check cache
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        # Execute function
        result = func()
        
        # Cache result
        self.redis.setex(
            key,
            expire,
            json.dumps(result)
        )
        
        return result
    
    def cache_query(
        self,
        query: str,
        params: Optional[dict] = None,
        expire: int = 3600
    ) -> Any:
        """Cache database query."""
        # Generate cache key
        key = f"query:{query}"
        if params:
            key += ":" + ":".join(
                f"{k}={v}"
                for k, v in sorted(params.items())
            )
        
        # Check cache
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        # Execute query
        with engine.connect() as conn:
            result = conn.execute(
                text(query),
                params or {}
            )
            data = [dict(row) for row in result]
        
        # Cache result
        self.redis.setex(
            key,
            expire,
            json.dumps(data)
        )
        
        return data
    
    def invalidate(self, pattern: str) -> None:
        """Invalidate cache entries."""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.redis.flushdb()

# Example usage
cache = CacheManager()

@cache.cache('user', expire=300)
def get_user(user_id: int) -> dict:
    # Simulate database query
    time.sleep(1)
    return {'id': user_id, 'name': 'Test User'}

def expensive_computation() -> int:
    # Simulate expensive computation
    time.sleep(2)
    return 42

# Cache expensive computation
result = cache.memoize(
    expensive_computation,
    'computation',
    expire=3600
)

# Cache database query
users = cache.cache_query(
    "SELECT * FROM users WHERE active = :active",
    {'active': True},
    expire=600
)
```

### Hands-On Exercise: Query Optimization

Create query optimizer:
```python
# query_optimizer.py
from sqlalchemy import create_engine, text
import time
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class QueryMetrics:
    """Query performance metrics."""
    query: str
    duration: float
    rows: int
    plan: List[str]
    timestamp: datetime

class QueryOptimizer:
    """Optimizes SQL queries."""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.logger = logging.getLogger('query_optimizer')
        self.metrics: List[QueryMetrics] = []
    
    def analyze_query(
        self,
        query: str,
        params: Dict[str, Any] = None
    ) -> QueryMetrics:
        """Analyze query performance."""
        with self.engine.connect() as conn:
            # Get execution plan
            explain = conn.execute(
                text(f"EXPLAIN ANALYZE {query}"),
                params or {}
            )
            plan = [row[0] for row in explain]
            
            # Execute query
            start = time.time()
            result = conn.execute(
                text(query),
                params or {}
            )
            duration = time.time() - start
            
            # Create metrics
            metrics = QueryMetrics(
                query=query,
                duration=duration,
                rows=result.rowcount,
                plan=plan,
                timestamp=datetime.now()
            )
            
            self.metrics.append(metrics)
            return metrics
    
    def optimize_query(
        self,
        query: str,
        params: Dict[str, Any] = None
    ) -> str:
        """Suggest query optimizations."""
        with self.engine.connect() as conn:
            # Analyze query
            explain = conn.execute(
                text(f"EXPLAIN {query}"),
                params or {}
            )
            plan = [row[0] for row in explain]
            
            suggestions = []
            
            # Check for sequential scans
            if any('Seq Scan' in line for line in plan):
                suggestions.append(
                    "Consider adding indexes to avoid sequential scans"
                )
            
            # Check for temporary files
            if any('Temporary File' in line for line in plan):
                suggestions.append(
                    "Query might benefit from increased work_mem"
                )
            
            # Check for nested loops
            if any('Nested Loop' in line for line in plan):
                suggestions.append(
                    "Consider using JOIN instead of nested loops"
                )
            
            return "\n".join(suggestions)
    
    def benchmark_queries(
        self,
        queries: List[str],
        iterations: int = 5
    ) -> Dict[str, Dict[str, float]]:
        """Benchmark multiple queries."""
        results = {}
        
        for query in queries:
            durations = []
            
            for _ in range(iterations):
                metrics = self.analyze_query(query)
                durations.append(metrics.duration)
            
            results[query] = {
                'min': min(durations),
                'max': max(durations),
                'avg': sum(durations) / len(durations)
            }
        
        return results
    
    def get_slow_queries(
        self,
        threshold: float = 1.0
    ) -> List[QueryMetrics]:
        """Get slow queries."""
        return [
            m for m in self.metrics
            if m.duration > threshold
        ]
    
    def suggest_indexes(
        self,
        query: str
    ) -> List[str]:
        """Suggest indexes for query."""
        with self.engine.connect() as conn:
            # Get table names
            tables = []
            for word in query.split():
                if word.lower() == 'from' or word.lower() == 'join':
                    tables.append(
                        next(w for w in query.split()[query.split().index(word)+1:] if w)
                    )
            
            suggestions = []
            
            # Analyze each table
            for table in tables:
                result = conn.execute(text(
                    f"SELECT * FROM pg_stat_user_tables "
                    f"WHERE relname = '{table}'"
                ))
                stats = result.fetchone()
                
                if stats:
                    if stats.seq_scan > stats.idx_scan:
                        suggestions.append(
                            f"Table {table} might benefit from an index"
                        )
            
            return suggestions
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate optimization report."""
        slow_queries = self.get_slow_queries()
        
        return {
            'total_queries': len(self.metrics),
            'slow_queries': len(slow_queries),
            'average_duration': sum(
                m.duration for m in self.metrics
            ) / len(self.metrics),
            'slowest_query': max(
                self.metrics,
                key=lambda m: m.duration
            ) if self.metrics else None,
            'queries_by_rows': sorted(
                self.metrics,
                key=lambda m: m.rows,
                reverse=True
            )[:5]
        }

# Example usage
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create optimizer
    optimizer = QueryOptimizer(
        'postgresql://user:pass@localhost/db'
    )
    
    # Analyze queries
    queries = [
        "SELECT * FROM users WHERE active = true",
        "SELECT u.*, p.* FROM users u JOIN posts p ON u.id = p.user_id",
        "SELECT COUNT(*) FROM orders GROUP BY status"
    ]
    
    for query in queries:
        # Analyze performance
        metrics = optimizer.analyze_query(query)
        print(f"Query duration: {metrics.duration:.2f}s")
        
        # Get optimization suggestions
        suggestions = optimizer.optimize_query(query)
        if suggestions:
            print("Suggestions:", suggestions)
        
        # Get index suggestions
        indexes = optimizer.suggest_indexes(query)
        if indexes:
            print("Index suggestions:", indexes)
    
    # Generate report
    report = optimizer.generate_report()
    print("Optimization Report:", report)
```

## 3. Scaling Strategies

### The Business Growth Metaphor

Think of scaling like business growth:
- Horizontal scaling like opening new stores
- Vertical scaling like store expansion
- Load balancing like customer distribution
- Caching like express checkout
- Microservices like specialized departments

### Load Balancing

```python
# load_balancer.py
import socket
import threading
import queue
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    """Server health status."""
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
    UNKNOWN = 'unknown'

@dataclass
class Server:
    """Represents a backend server."""
    host: str
    port: int
    weight: int = 1
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: float = 0
    failed_checks: int = 0

class LoadBalancer:
    """Simple load balancer implementation."""
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 8000,
        algorithm: str = 'round_robin'
    ):
        self.host = host
        self.port = port
        self.algorithm = algorithm
        self.servers: List[Server] = []
        self.current_index = 0
        self.stats: Dict[str, int] = {
            'requests': 0,
            'errors': 0,
            'health_checks': 0
        }
        self.lock = threading.Lock()
        self.logger = logging.getLogger('load_balancer')
    
    def add_server(
        self,
        host: str,
        port: int,
        weight: int = 1
    ) -> None:
        """Add backend server."""
        server = Server(host, port, weight)
        self.servers.append(server)
        self.check_server_health(server)
    
    def remove_server(
        self,
        host: str,
        port: int
    ) -> None:
        """Remove backend server."""
        self.servers = [
            s for s in self.servers
            if not (s.host == host and s.port == port)
        ]
    
    def check_server_health(self, server: Server) -> None:
        """Check server health."""
        try:
            # Try to connect
            with socket.create_connection(
                (server.host, server.port),
                timeout=5
            ):
                server.status = HealthStatus.HEALTHY
                server.failed_checks = 0
        except (socket.timeout, ConnectionRefusedError):
            server.failed_checks += 1
            if server.failed_checks >= 3:
                server.status = HealthStatus.UNHEALTHY
        
        server.last_check = time.time()
        self.stats['health_checks'] += 1
    
    def get_next_server(self) -> Optional[Server]:
        """Get next available server."""
        if not self.servers:
            return None
        
        healthy_servers = [
            s for s in self.servers
            if s.status == HealthStatus.HEALTHY
        ]
        
        if not healthy_servers:
            return None
        
        if self.algorithm == 'round_robin':
            with self.lock:
                server = healthy_servers[self.current_index]
                self.current_index = (
                    self.current_index + 1
                ) % len(healthy_servers)
                return server
        elif self.algorithm == 'weighted':
            total_weight = sum(s.weight for s in healthy_servers)
            r = random.uniform(0, total_weight)
            upto = 0
            for server in healthy_servers:
                upto += server.weight
                if upto > r:
                    return server
        
        return healthy_servers[0]
    
    def handle_request(
        self,
        client_socket: socket.socket
    ) -> None:
        """Handle client request."""
        try:
            # Get next server
            server = self.get_next_server()
            if not server:
                client_socket.close()
                self.stats['errors'] += 1
                return
            
            # Forward request
            with socket.create_connection(
                (server.host, server.port)
            ) as server_socket:
                # Forward client request
                data = client_socket.recv(4096)
                if not data:
                    return
                
                server_socket.sendall(data)
                
                # Forward server response
                while True:
                    response = server_socket.recv(4096)
                    if not response:
                        break
                    client_socket.sendall(response)
            
            self.stats['requests'] += 1
            
        except Exception as e:
            self.logger.error(f"Error handling request: {e}")
            self.stats['errors'] += 1
        finally:
            client_socket.close()
    
    def start(self) -> None:
        """Start load balancer."""
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        # Start health check thread
        health_thread = threading.Thread(
            target=self._health_check_loop
        )
        health_thread.daemon = True
        health_thread.start()
        
        self.logger.info(
            f"Load balancer running on {self.host}:{self.port}"
        )
        
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(
                target=self.handle_request,
                args=(client_socket,)
            )
            client_thread.start()
    
    def _health_check_loop(self) -> None:
        """Periodic health checks."""
        while True:
            for server in self.servers:
                self.check_server_health(server)
            time.sleep(30)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get load balancer statistics."""
        return {
            **self.stats,
            'servers': len(self.servers),
            'healthy_servers': len([
                s for s in self.servers
                if s.status == HealthStatus.HEALTHY
            ])
        }

# Example usage
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create load balancer
    balancer = LoadBalancer(
        host='localhost',
        port=8000,
        algorithm='round_robin'
    )
    
    # Add backend servers
    balancer.add_server('backend1', 8001)
    balancer.add_server('backend2', 8002)
    balancer.add_server('backend3', 8003)
    
    # Start load balancer
    balancer.start()
```

## Practical Exercises

### 1. Frontend Optimization
Implement improvements:
1. Asset bundling
2. Code splitting
3. Lazy loading
4. Caching strategy
5. Performance monitoring

### 2. Backend Optimization
Create optimizations for:
1. Database queries
2. Caching system
3. Load balancing
4. Connection pooling
5. Request handling

### 3. Scaling Implementation
Build scaling system:
1. Horizontal scaling
2. Vertical scaling
3. Load distribution
4. Service discovery
5. Health monitoring

## Review Questions

1. **Frontend**
   - How optimize assets?
   - When use caching?
   - Best practices for loading?

2. **Backend**
   - How optimize queries?
   - When use indexes?
   - Best practices for caching?

3. **Scaling**
   - How handle growth?
   - When scale services?
   - Best practices for distribution?

## Additional Resources

### Online Tools
- Performance analyzers
- Optimization tools
- Scaling platforms

### Further Reading
- Performance patterns
- Optimization strategies
- Scaling architectures

### Video Resources
- Performance tutorials
- Optimization guides
- Scaling examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Optimize applications
2. Improve performance
3. Scale systems

Remember: Performance optimization is an ongoing process!

## Common Questions and Answers

Q: When should I optimize?
A: Start with monitoring and optimize based on data.

Q: What should I optimize first?
A: Focus on the biggest bottlenecks identified through monitoring.

Q: How do I measure improvements?
A: Use metrics and benchmarks to compare before and after.

## Glossary

- **Optimization**: Performance improvement
- **Caching**: Quick data access
- **Scaling**: System growth
- **Load Balancing**: Request distribution
- **Monitoring**: Performance tracking
- **Benchmark**: Performance measure
- **Index**: Database optimization
- **Cache**: Quick storage
- **Latency**: Response time
- **Throughput**: Processing capacity

Remember: Always measure before and after optimization!
