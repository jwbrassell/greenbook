# Chapter 1: HTML Foundations

## Introduction

Think about building a house - you start with the foundation and framework before adding decorations and utilities. HTML is like the structural framework of a webpage. It defines what elements exist and how they relate to each other, providing the foundation that CSS will style and JavaScript will make interactive. In this chapter, we'll learn how to create well-structured, semantic HTML documents.

## 1. HTML Basics

### The Building Blocks Metaphor

Think of HTML elements like building blocks:
- Tags are like different types of blocks
- Attributes are like block properties
- Nesting is like stacking blocks
- Document structure is like building plans

### Basic Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First Webpage</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    <p>This is my first webpage.</p>
</body>
</html>
```

### Common Elements

```html
<!-- Headings (like section titles) -->
<h1>Main Title</h1>
<h2>Subtitle</h2>
<h3>Section Title</h3>

<!-- Paragraphs (like text blocks) -->
<p>This is a paragraph of text.</p>

<!-- Links (like doorways to other pages) -->
<a href="https://example.com">Visit Example</a>

<!-- Images (like pictures on walls) -->
<img src="photo.jpg" alt="A beautiful sunset">

<!-- Lists (like bullet points) -->
<ul>
    <li>Unordered item 1</li>
    <li>Unordered item 2</li>
</ul>

<ol>
    <li>Ordered item 1</li>
    <li>Ordered item 2</li>
</ol>
```

### Hands-On Exercise: First Webpage

Create a simple personal page:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Me</title>
</head>
<body>
    <h1>About [Your Name]</h1>
    
    <h2>Introduction</h2>
    <p>Welcome to my webpage! I'm learning web development.</p>
    
    <h2>My Hobbies</h2>
    <ul>
        <li>Reading</li>
        <li>Coding</li>
        <li>Photography</li>
    </ul>
    
    <h2>Contact Me</h2>
    <p>Email: <a href="mailto:you@example.com">you@example.com</a></p>
</body>
</html>
```

## 2. Semantic HTML

### The Newspaper Layout Metaphor

Think of semantic HTML like organizing a newspaper:
- Header is like the masthead
- Nav is like the menu
- Main is like the main story
- Aside is like sidebars
- Footer is like the publication info

### Semantic Elements

```html
<!-- Page structure -->
<header>
    <h1>Website Title</h1>
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
        <h2>Article Title</h2>
        <p>Article content...</p>
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
    <p>&copy; 2024 Your Website</p>
</footer>
```

### Why Use Semantic HTML?

```html
<!-- Non-semantic (bad) -->
<div class="header">
    <div class="nav">
        <div class="nav-item">Home</div>
    </div>
</div>

<!-- Semantic (good) -->
<header>
    <nav>
        <ul>
            <li>Home</li>
        </ul>
    </nav>
</header>

Benefits:
- Better accessibility
- Clearer code structure
- Improved SEO
- Easier maintenance
```

### Hands-On Exercise: Semantic Blog Post

Create a blog post structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog Post</title>
</head>
<body>
    <header>
        <h1>My Blog</h1>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#posts">Posts</a></li>
                <li><a href="#about">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <header>
                <h2>My First Blog Post</h2>
                <time datetime="2024-01-15">January 15, 2024</time>
            </header>

            <section>
                <h3>Introduction</h3>
                <p>Welcome to my first blog post...</p>
            </section>

            <section>
                <h3>Main Content</h3>
                <p>Here's what I want to share...</p>
            </section>

            <footer>
                <p>Posted in: Web Development</p>
                <p>Author: Your Name</p>
            </footer>
        </article>

        <aside>
            <h3>Recent Posts</h3>
            <ul>
                <li><a href="#post1">Another Post</a></li>
                <li><a href="#post2">Yet Another Post</a></li>
            </ul>
        </aside>
    </main>

    <footer>
        <p>&copy; 2024 My Blog. All rights reserved.</p>
    </footer>
</body>
</html>
```

## 3. Forms and Input

### The Paper Form Metaphor

Think of HTML forms like paper forms:
- Input fields are like blank spaces
- Labels are like field descriptions
- Submit button is like "Send" button
- Validation is like checking requirements

### Basic Form Structure

```html
<form action="/submit" method="POST">
    <!-- Text input (like blank line) -->
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>

    <!-- Email input -->
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>

    <!-- Password field -->
    <label for="password">Password:</label>
    <input type="password" id="password" name="password">

    <!-- Radio buttons (like multiple choice) -->
    <fieldset>
        <legend>Subscription Type:</legend>
        <input type="radio" id="basic" name="plan" value="basic">
        <label for="basic">Basic</label>
        <input type="radio" id="premium" name="plan" value="premium">
        <label for="premium">Premium</label>
    </fieldset>

    <!-- Checkboxes (like yes/no boxes) -->
    <input type="checkbox" id="newsletter" name="newsletter">
    <label for="newsletter">Subscribe to newsletter</label>

    <!-- Dropdown (like options list) -->
    <label for="country">Country:</label>
    <select id="country" name="country">
        <option value="">Select a country</option>
        <option value="us">United States</option>
        <option value="uk">United Kingdom</option>
        <option value="ca">Canada</option>
    </select>

    <!-- Text area (like comment box) -->
    <label for="message">Message:</label>
    <textarea id="message" name="message" rows="4"></textarea>

    <!-- Submit button -->
    <button type="submit">Send</button>
</form>
```

### Form Validation

```html
<!-- Built-in validation -->
<input type="email" required>           <!-- Must be valid email -->
<input type="text" minlength="3">       <!-- Minimum length -->
<input type="number" min="0" max="100"> <!-- Number range -->
<input type="text" pattern="[A-Za-z]+"> <!-- Pattern matching -->

<!-- Custom validation messages -->
<input type="text" required
       oninvalid="this.setCustomValidity('Please enter your name')"
       oninput="this.setCustomValidity('')">
```

### Hands-On Exercise: Contact Form

Create a contact form:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>
</head>
<body>
    <h1>Contact Us</h1>
    
    <form action="/submit" method="POST">
        <div>
            <label for="name">Full Name:</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div>
            <label for="email">Email Address:</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div>
            <label for="subject">Subject:</label>
            <select id="subject" name="subject" required>
                <option value="">Select a subject</option>
                <option value="general">General Inquiry</option>
                <option value="support">Technical Support</option>
                <option value="feedback">Feedback</option>
            </select>
        </div>

        <div>
            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="5" required></textarea>
        </div>

        <div>
            <input type="checkbox" id="copy" name="copy">
            <label for="copy">Send me a copy of this message</label>
        </div>

        <button type="submit">Send Message</button>
    </form>
</body>
</html>
```

## Practical Exercises

### 1. Personal Portfolio
Build portfolio page with:
1. Header with navigation
2. About section
3. Projects showcase
4. Skills list
5. Contact information

### 2. Blog Template
Create blog template with:
1. Header with site title
2. Navigation menu
3. Article sections
4. Sidebar content
5. Footer information

### 3. Survey Form
Develop survey with:
1. Personal information
2. Multiple choice questions
3. Rating scales
4. Comment sections
5. Submit functionality

## Review Questions

1. **HTML Basics**
   - What's the purpose of DOCTYPE?
   - Why use semantic elements?
   - How to structure a basic page?

2. **Semantic HTML**
   - When use article vs section?
   - Why use nav element?
   - How to organize content?

3. **Forms**
   - When use different input types?
   - How handle validation?
   - Best practices for forms?

## Additional Resources

### Online Tools
- HTML validators
- Accessibility checkers
- Code formatters

### Further Reading
- HTML5 specification
- Accessibility guidelines
- Form best practices

### Video Resources
- HTML tutorials
- Semantic HTML guides
- Form building examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Create structured webpages
2. Build semantic documents
3. Implement interactive forms

Remember: Good HTML structure is the foundation of every great website!

## Common Questions and Answers

Q: When should I use divs vs semantic elements?
A: Use semantic elements when they match the content's meaning, divs for non-semantic grouping.

Q: How do I make my forms accessible?
A: Use proper labels, provide clear instructions, and ensure keyboard navigation works.

Q: Should I use tables for layout?
A: No, tables should only be used for tabular data. Use CSS for layout.

## Glossary

- **Element**: HTML component with start/end tags
- **Attribute**: Additional element information
- **Semantic**: Meaningful markup
- **Form**: Interactive input collection
- **Validation**: Input checking
- **DOCTYPE**: Document type declaration
- **Tag**: Element marker
- **Metadata**: Data about the document
- **Block**: Full-width element
- **Inline**: Flow element

Remember: Clear, semantic HTML makes websites more accessible and maintainable!
