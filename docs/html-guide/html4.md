# HTML4 Documentation and Examples

HTML4 was released in 1997 and served as the primary HTML standard until HTML5. While largely superseded by HTML5, understanding HTML4 remains important for maintaining legacy systems and understanding web development history.

## Key Features of HTML4

### Document Structure
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>HTML4 Document</title>
</head>
<body>
    <!-- Content goes here -->
</body>
</html>
```

### Common Elements

#### 1. Tables for Layout (Common in HTML4)
```html
<table border="1" cellpadding="5" cellspacing="0">
    <tr>
        <td>Header</td>
    </tr>
    <tr>
        <td>Navigation</td>
    </tr>
    <tr>
        <td>Content</td>
    </tr>
</table>
```

#### 2. Frames (HTML4 Specific)
```html
<frameset cols="25%,75%">
    <frame src="navigation.html">
    <frame src="content.html">
</frameset>
```

#### 3. Forms
```html
<form action="process.php" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <input type="submit" value="Submit">
</form>
```

### Formatting Elements
```html
<b>Bold text</b>
<i>Italic text</i>
<u>Underlined text</u>
<font face="Arial" size="3" color="red">Colored text</font>
<center>Centered text</center>
```

### Lists
```html
<ul type="disc">
    <li>Unordered list item</li>
</ul>

<ol type="1">
    <li>Ordered list item</li>
</ol>
```

### Images and Links
```html
<img src="image.jpg" alt="Description" border="0">
<a href="https://example.com" target="_blank">Link</a>
```

## HTML4 Specific Attributes

### Common Attributes
- `align`: Alignment of elements
- `bgcolor`: Background color
- `border`: Border width
- `cellpadding`: Cell padding in tables
- `cellspacing`: Cell spacing in tables
- `valign`: Vertical alignment

### Example with Multiple Attributes
```html
<table width="100%" border="1" cellpadding="5" cellspacing="0" bgcolor="#FFFFFF">
    <tr>
        <td align="center" valign="middle">
            <font color="red">Centered Content</font>
        </td>
    </tr>
</table>
```

## Complete HTML4 Page Example
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>HTML4 Example Page</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body bgcolor="#FFFFFF" text="#000000" link="#0000FF" vlink="#800080">
    <center>
        <h1><font color="navy">Welcome to My HTML4 Page</font></h1>
    </center>

    <table width="100%" border="0" cellspacing="0" cellpadding="5">
        <tr>
            <td width="20%" bgcolor="#F0F0F0" valign="top">
                <b>Navigation</b><br>
                <a href="#section1">Section 1</a><br>
                <a href="#section2">Section 2</a>
            </td>
            <td width="80%" valign="top">
                <h2><a name="section1">Section 1</a></h2>
                <p><font face="Arial" size="2">
                    This is the main content area of the page.
                </font></p>

                <h2><a name="section2">Section 2</a></h2>
                <p><font face="Arial" size="2">
                    More content here.
                </font></p>

                <form action="submit.php" method="post">
                    <table border="0" cellpadding="3">
                        <tr>
                            <td><font face="Arial" size="2">Name:</font></td>
                            <td><input type="text" name="name" size="20"></td>
                        </tr>
                        <tr>
                            <td><font face="Arial" size="2">Email:</font></td>
                            <td><input type="text" name="email" size="20"></td>
                        </tr>
                        <tr>
                            <td colspan="2" align="center">
                                <input type="submit" value="Submit">
                            </td>
                        </tr>
                    </table>
                </form>
            </td>
        </tr>
    </table>

    <hr>
    <center>
        <font size="2">&copy; 2024 My Website</font>
    </center>
</body>
</html>
```

## Important Notes

1. **Deprecated Features**:
   - `<font>` tag
   - `<center>` tag
   - `<strike>` tag
   - Frame elements
   - Many presentational attributes

2. **Browser Support**:
   - All modern browsers still support HTML4 elements
   - However, using HTML4-specific features is not recommended for new projects

3. **Limitations**:
   - Limited semantic meaning
   - Heavy mixing of content and presentation
   - No native support for audio/video
   - No form validation
   - No support for mobile devices

4. **Best Practices** (even when using HTML4):
   - Use CSS for styling instead of HTML attributes
   - Avoid deprecated elements
   - Ensure proper document structure
   - Include alt text for images
   - Use meaningful titles and metadata
