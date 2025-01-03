# HTML5 Documentation and Examples

HTML5 is the latest version of HTML, introducing new elements, attributes, and behaviors. It simplifies markup while providing rich semantic elements and support for modern web applications.

## Key Features of HTML5

### Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML5 Document</title>
</head>
<body>
    <!-- Content goes here -->
</body>
</html>
```

## New Semantic Elements

### Page Structure Elements
```html
<header>
    <nav>
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <section>
            <h1>Article Title</h1>
            <p>Article content...</p>
        </section>
    </article>
    
    <aside>
        <h2>Related Content</h2>
        <p>Sidebar content...</p>
    </aside>
</main>

<footer>
    <p>&copy; 2024 My Website</p>
</footer>
```

### Content Elements
```html
<figure>
    <img src="image.jpg" alt="Description">
    <figcaption>Image caption</figcaption>
</figure>

<time datetime="2024-01-15">January 15, 2024</time>

<mark>Highlighted text</mark>
```

## New Form Features

### Input Types
```html
<form>
    <!-- Email with validation -->
    <input type="email" required>
    
    <!-- Date picker -->
    <input type="date">
    
    <!-- Number with range -->
    <input type="number" min="0" max="100">
    
    <!-- Color picker -->
    <input type="color">
    
    <!-- Range slider -->
    <input type="range" min="0" max="100">
    
    <!-- Search field -->
    <input type="search">
    
    <!-- URL field -->
    <input type="url">
    
    <!-- Phone number -->
    <input type="tel">
</form>
```

### Form Attributes
```html
<form>
    <!-- Autocomplete -->
    <input type="text" autocomplete="name">
    
    <!-- Placeholder -->
    <input type="text" placeholder="Enter your name">
    
    <!-- Pattern validation -->
    <input type="text" pattern="[A-Za-z]{3}">
    
    <!-- Required fields -->
    <input type="text" required>
    
    <!-- Autofocus -->
    <input type="text" autofocus>
    
    <!-- Form validation -->
    <input type="submit" formnovalidate>
</form>
```

## Multimedia Elements

### Audio
```html
<audio controls>
    <source src="audio.mp3" type="audio/mpeg">
    <source src="audio.ogg" type="audio/ogg">
    Your browser does not support the audio element.
</audio>
```

### Video
```html
<video width="640" height="360" controls>
    <source src="video.mp4" type="video/mp4">
    <source src="video.webm" type="video/webm">
    Your browser does not support the video element.
</video>
```

## Canvas and SVG

### Canvas Example
```html
<canvas id="myCanvas" width="200" height="100"></canvas>
<script>
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(0, 0, 150, 75);
</script>
```

### SVG Example
```html
<svg width="100" height="100">
    <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
</svg>
```

## Storage APIs

### Local Storage
```html
<script>
    // Store data
    localStorage.setItem("username", "John");
    
    // Retrieve data
    const username = localStorage.getItem("username");
    
    // Remove data
    localStorage.removeItem("username");
</script>
```

### Session Storage
```html
<script>
    // Store session data
    sessionStorage.setItem("tempData", "123");
    
    // Retrieve session data
    const data = sessionStorage.getItem("tempData");
</script>
```

## Complete HTML5 Page Example
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern HTML5 Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        header, footer {
            background: #f4f4f4;
            padding: 20px;
        }
        main {
            max-width: 800px;
            margin: 20px auto;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <header>
                <h1>Welcome to HTML5</h1>
                <p>Posted on <time datetime="2024-01-15">January 15, 2024</time></p>
            </header>

            <section>
                <h2>Modern Features</h2>
                <p>HTML5 introduces many new features...</p>
                
                <figure>
                    <img src="example.jpg" alt="Example Image">
                    <figcaption>An example of HTML5 features</figcaption>
                </figure>
            </section>

            <section>
                <h2>Contact Form</h2>
                <form id="contactForm">
                    <label for="name">Name:</label>
                    <input type="text" id="name" required placeholder="Enter your name">

                    <label for="email">Email:</label>
                    <input type="email" id="email" required placeholder="Enter your email">

                    <label for="message">Message:</label>
                    <textarea id="message" required></textarea>

                    <button type="submit">Send</button>
                </form>
            </section>
        </article>

        <aside>
            <h3>Related Links</h3>
            <ul>
                <li><a href="#link1">Link 1</a></li>
                <li><a href="#link2">Link 2</a></li>
            </ul>
        </aside>
    </main>

    <footer>
        <p>&copy; 2024 HTML5 Example. All rights reserved.</p>
    </footer>
</body>
</html>
```

## Important Features and Improvements

1. **Semantic Elements**:
   - `<header>`, `<footer>`, `<nav>`, `<main>`
   - `<article>`, `<section>`, `<aside>`
   - `<figure>`, `<figcaption>`
   - `<time>`, `<mark>`

2. **Form Improvements**:
   - New input types (email, date, number, etc.)
   - Built-in validation
   - Placeholder text
   - Required fields
   - Pattern matching

3. **Multimedia Support**:
   - Native audio and video playback
   - Canvas for drawing
   - SVG support
   - WebGL support

4. **APIs and Storage**:
   - Local Storage
   - Session Storage
   - Web Workers
   - Geolocation
   - Drag and Drop

5. **Mobile Support**:
   - Viewport meta tag
   - Touch events
   - Mobile-friendly input types

## Best Practices

1. **Semantic Structure**:
   - Use semantic elements appropriately
   - Maintain proper heading hierarchy
   - Use landmarks for accessibility

2. **Accessibility**:
   - Include ARIA roles when needed
   - Provide alt text for images
   - Ensure keyboard navigation
   - Use semantic elements properly

3. **Performance**:
   - Optimize multimedia content
   - Use async/defer for scripts
   - Implement proper caching
   - Minimize DOM manipulation

4. **Mobile First**:
   - Use responsive design
   - Implement touch-friendly interfaces
   - Optimize for different screen sizes

5. **Cross-Browser Support**:
   - Test across different browsers
   - Provide fallbacks when needed
   - Use feature detection
