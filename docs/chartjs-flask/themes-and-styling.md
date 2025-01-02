# Chart.js Themes and Styling with Flask

## Table of Contents
- [Chart.js Themes and Styling with Flask](#chartjs-themes-and-styling-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Theme Implementation](#basic-theme-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template with Theme](#html-template-with-theme)
  - [Example 1: Multiple Color Schemes](#example-1:-multiple-color-schemes)
    - [Flask Implementation](#flask-implementation)
    - [Color Scheme Configuration](#color-scheme-configuration)
  - [Example 2: Custom Style Presets](#example-2:-custom-style-presets)
    - [Flask Implementation](#flask-implementation)
    - [Style Preset Configuration](#style-preset-configuration)
  - [Example 3: Dynamic Theme Generator](#example-3:-dynamic-theme-generator)
    - [Flask Implementation](#flask-implementation)
    - [Dynamic Theme Configuration](#dynamic-theme-configuration)
  - [Working with Database Data](#working-with-database-data)



Themes and styling allow you to create consistent, visually appealing charts that match your application's design. This guide demonstrates how to implement custom themes and styles in Chart.js with Flask integration.

## Basic Theme Implementation

### Flask Route
```python
@app.route('/themed-chart')
def themed_chart():
    return render_template('themed_chart.html')

@app.route('/api/chart-data')
def chart_data():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Sales',
            'data': [65, 59, 80, 81, 56, 55]
        }]
    }
    return jsonify(data)
```

### HTML Template with Theme
```html
<div style="width: 800px;">
    <canvas id="themedChart"></canvas>
</div>

<script>
// Custom theme definition
const customTheme = {
    colors: {
        primary: 'rgb(75, 192, 192)',
        secondary: 'rgb(255, 99, 132)',
        background: 'rgb(255, 255, 255)',
        grid: 'rgb(230, 230, 230)',
        text: 'rgb(102, 102, 102)'
    },
    fonts: {
        base: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        size: 12
    },
    animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
    }
};

// Apply theme to Chart.js defaults
Chart.defaults.color = customTheme.colors.text;
Chart.defaults.font.family = customTheme.fonts.base;
Chart.defaults.font.size = customTheme.fonts.size;
Chart.defaults.animation.duration = customTheme.animation.duration;
Chart.defaults.animation.easing = customTheme.animation.easing;

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            // Apply theme to dataset
            data.datasets[0].backgroundColor = customTheme.colors.primary + '40';  // 40 = 25% opacity
            data.datasets[0].borderColor = customTheme.colors.primary;
            data.datasets[0].borderWidth = 2;
            
            const ctx = document.getElementById('themedChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Themed Sales Chart',
                            color: customTheme.colors.text,
                            font: {
                                size: customTheme.fonts.size * 1.5
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: customTheme.colors.grid
                            }
                        },
                        y: {
                            grid: {
                                color: customTheme.colors.grid
                            },
                            beginAtZero: true
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Multiple Color Schemes

This example shows how to implement switchable color schemes for different themes.

### Flask Implementation
```python
@app.route('/api/color-schemes')
def color_schemes():
    data = {
        'labels': ['Category A', 'Category B', 'Category C', 'Category D'],
        'datasets': [{
            'label': 'Dataset 1',
            'data': [45, 59, 80, 81]
        }, {
            'label': 'Dataset 2',
            'data': [28, 48, 40, 19]
        }]
    }
    return jsonify(data)
```

### Color Scheme Configuration
```javascript
const colorSchemes = {
    light: {
        background: 'rgb(255, 255, 255)',
        text: 'rgb(102, 102, 102)',
        grid: 'rgb(230, 230, 230)',
        colors: [
            'rgb(75, 192, 192)',
            'rgb(255, 99, 132)',
            'rgb(255, 205, 86)',
            'rgb(54, 162, 235)'
        ]
    },
    dark: {
        background: 'rgb(47, 47, 47)',
        text: 'rgb(230, 230, 230)',
        grid: 'rgb(77, 77, 77)',
        colors: [
            'rgb(0, 255, 255)',
            'rgb(255, 99, 132)',
            'rgb(255, 205, 86)',
            'rgb(54, 162, 235)'
        ]
    },
    pastel: {
        background: 'rgb(248, 249, 250)',
        text: 'rgb(73, 80, 87)',
        grid: 'rgb(233, 236, 239)',
        colors: [
            'rgb(190, 227, 219)',
            'rgb(255, 214, 214)',
            'rgb(255, 241, 214)',
            'rgb(214, 229, 255)'
        ]
    }
};

function applyColorScheme(chart, schemeName) {
    const scheme = colorSchemes[schemeName];
    
    // Update chart background
    chart.canvas.parentNode.style.backgroundColor = scheme.background;
    
    // Update datasets colors
    chart.data.datasets.forEach((dataset, i) => {
        dataset.backgroundColor = scheme.colors[i % scheme.colors.length] + '40';
        dataset.borderColor = scheme.colors[i % scheme.colors.length];
    });
    
    // Update options
    chart.options.plugins.title.color = scheme.text;
    chart.options.scales.x.grid.color = scheme.grid;
    chart.options.scales.y.grid.color = scheme.grid;
    chart.options.scales.x.ticks.color = scheme.text;
    chart.options.scales.y.ticks.color = scheme.text;
    
    chart.update();
}
```

## Example 2: Custom Style Presets

This example demonstrates how to create and apply style presets for different chart types.

### Flask Implementation
```python
@app.route('/api/styled-data')
def styled_data():
    data = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [{
            'label': 'Revenue',
            'data': [12000, 19000, 15000, 22000]
        }]
    }
    return jsonify(data)
```

### Style Preset Configuration
```javascript
const stylePresets = {
    modern: {
        fonts: {
            family: "'Inter', sans-serif",
            size: 13,
            weight: 500
        },
        colors: {
            primary: 'rgb(99, 102, 241)',
            background: 'rgb(249, 250, 251)',
            border: 'rgb(229, 231, 235)'
        },
        borderRadius: 8,
        borderWidth: 2
    },
    classic: {
        fonts: {
            family: "'Georgia', serif",
            size: 12,
            weight: 400
        },
        colors: {
            primary: 'rgb(66, 88, 110)',
            background: 'rgb(255, 255, 255)',
            border: 'rgb(204, 204, 204)'
        },
        borderRadius: 0,
        borderWidth: 1
    },
    minimal: {
        fonts: {
            family: "'SF Mono', monospace",
            size: 11,
            weight: 400
        },
        colors: {
            primary: 'rgb(0, 0, 0)',
            background: 'rgb(255, 255, 255)',
            border: 'rgb(234, 234, 234)'
        },
        borderRadius: 4,
        borderWidth: 1
    }
};

function applyStylePreset(chart, presetName) {
    const preset = stylePresets[presetName];
    
    // Update global font
    Chart.defaults.font.family = preset.fonts.family;
    Chart.defaults.font.size = preset.fonts.size;
    Chart.defaults.font.weight = preset.fonts.weight;
    
    // Update dataset styles
    chart.data.datasets.forEach(dataset => {
        dataset.backgroundColor = preset.colors.primary + '20';
        dataset.borderColor = preset.colors.primary;
        dataset.borderWidth = preset.borderWidth;
        dataset.borderRadius = preset.borderRadius;
    });
    
    // Update chart background
    chart.canvas.parentNode.style.backgroundColor = preset.colors.background;
    
    chart.update();
}
```

## Example 3: Dynamic Theme Generator

This example shows how to create dynamically generated themes based on a base color.

### Flask Implementation
```python
@app.route('/api/theme-data')
def theme_data():
    data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'datasets': [{
            'label': 'Activity',
            'data': [65, 59, 80, 81, 56]
        }]
    }
    return jsonify(data)
```

### Dynamic Theme Configuration
```javascript
function generateTheme(baseColor) {
    // Convert base color to HSL for easier manipulation
    const color = tinycolor(baseColor);
    const hsl = color.toHsl();
    
    return {
        colors: {
            primary: color.toRgbString(),
            secondary: tinycolor({ h: (hsl.h + 180) % 360, s: hsl.s, l: hsl.l }).toRgbString(),
            background: tinycolor({ h: hsl.h, s: hsl.s * 0.1, l: 0.98 }).toRgbString(),
            text: tinycolor({ h: hsl.h, s: hsl.s * 0.2, l: 0.3 }).toRgbString(),
            grid: tinycolor({ h: hsl.h, s: hsl.s * 0.1, l: 0.9 }).toRgbString()
        },
        gradients: {
            primary: {
                start: color.lighten(20).toRgbString(),
                end: color.darken(10).toRgbString()
            }
        },
        shadows: {
            small: `0 2px 4px ${color.setAlpha(0.1).toRgbString()}`,
            medium: `0 4px 6px ${color.setAlpha(0.1).toRgbString()}`
        }
    };
}

function applyDynamicTheme(chart, baseColor) {
    const theme = generateTheme(baseColor);
    
    // Create gradient
    const ctx = chart.ctx;
    const gradient = ctx.createLinearGradient(0, 0, 0, chart.height);
    gradient.addColorStop(0, theme.gradients.primary.start);
    gradient.addColorStop(1, theme.gradients.primary.end);
    
    // Apply theme
    chart.data.datasets.forEach(dataset => {
        dataset.backgroundColor = gradient;
        dataset.borderColor = theme.colors.primary;
        dataset.borderWidth = 2;
    });
    
    // Update options
    chart.options.plugins.title.color = theme.colors.text;
    chart.options.scales.x.grid.color = theme.colors.grid;
    chart.options.scales.y.grid.color = theme.colors.grid;
    chart.options.scales.x.ticks.color = theme.colors.text;
    chart.options.scales.y.ticks.color = theme.colors.text;
    
    // Apply background and shadow
    chart.canvas.parentNode.style.backgroundColor = theme.colors.background;
    chart.canvas.parentNode.style.boxShadow = theme.shadows.medium;
    
    chart.update();
}
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database and apply themes based on data categories:

```python
class ChartTheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    primary_color = db.Column(db.String(50))
    background_color = db.Column(db.String(50))
    font_family = db.Column(db.String(100))
    
    @staticmethod
    def get_theme_config(theme_name):
        theme = ChartTheme.query.filter_by(name=theme_name).first()
        if not theme:
            return default_theme_config()
            
        return {
            'colors': {
                'primary': theme.primary_color,
                'background': theme.background_color
            },
            'fonts': {
                'family': theme.font_family,
                'size': 12
            }
        }

@app.route('/api/themed-data/<theme_name>')
def get_themed_data(theme_name):
    theme = ChartTheme.get_theme_config(theme_name)
    data = generate_chart_data()  # Your data generation function
    
    # Apply theme to data
    for dataset in data['datasets']:
        dataset['backgroundColor'] = theme['colors']['primary'] + '40'
        dataset['borderColor'] = theme['colors']['primary']
    
    return jsonify({
        'data': data,
        'theme': theme
    })
```

This documentation provides three distinct examples of Chart.js themes and styling with varying complexity and features. Each example demonstrates different aspects of theme implementation when integrated with Flask, from basic color schemes to dynamic theme generation.
