# Chapter 4: Using curl and Tools

## Introduction

Think about having a Swiss Army knife for APIs - that's what curl and similar tools provide. They let you interact with web services directly from the command line, test APIs quickly, and debug issues efficiently. In this chapter, we'll master these essential tools, using practical examples to understand their capabilities.

## 1. curl Basics

### The Phone Call Metaphor

Think of curl like making phone calls:
- Different numbers (URLs)
- Various types of calls (HTTP methods)
- Specific messages (data)
- Special instructions (headers)
- Different responses (status codes)

### Basic curl Commands

```bash
# Simple GET request (like asking a question)
curl https://api.example.com/data

# Save response to file (like recording a call)
curl -o response.json https://api.example.com/data

# Show headers (like seeing call details)
curl -I https://api.example.com/data

# Follow redirects (like being forwarded)
curl -L https://api.example.com/data

# Show detailed info (like call log)
curl -v https://api.example.com/data
```

### Common Options

```bash
# Request Methods
-X GET                    # Specify method
-X POST
-X PUT
-X DELETE

# Headers
-H "Content-Type: application/json"
-H "Authorization: Bearer token123"

# Data
-d '{"name":"John"}'     # POST data
--data-urlencode "q=search term"

# Output Control
-s                       # Silent mode
-S                       # Show errors
-o file.txt             # Save to file
```

### Hands-On Exercise: curl Explorer

Test different API endpoints:
```bash
# GET request with headers
curl -H "Accept: application/json" \
     https://api.github.com/users/username

# POST with JSON data
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@example.com"}' \
     https://api.example.com/users

# PUT with file data
curl -X PUT \
     -H "Content-Type: application/json" \
     -d @data.json \
     https://api.example.com/users/123
```

## 2. API Testing Tools

### The Kitchen Tools Metaphor

Think of API tools like different kitchen tools:
- curl: Like a basic knife (versatile, essential)
- Postman: Like a food processor (powerful, feature-rich)
- Browser Tools: Like measuring cups (helpful for quick checks)
- jq: Like a strainer (processes JSON data)

### Postman

```
Features:
1. Collections
   - Save requests
   - Group related calls
   - Share with team

2. Environments
   - Different settings
   - Variable storage
   - Easy switching

3. Tests
   - Automated checks
   - Response validation
   - Chain requests
```

### Browser Developer Tools

```
Network Tab Features:
1. Request Details
   - Headers
   - Payload
   - Timing

2. Response Analysis
   - Status codes
   - Response body
   - Headers received

3. Filtering
   - By type
   - By domain
   - By status
```

### Hands-On Exercise: Tool Comparison

Test same API with different tools:
```bash
# Using curl
curl -v -H "Accept: application/json" \
     https://api.example.com/data

# Using httpie (modern alternative)
http GET api.example.com/data Accept:application/json

# Using wget
wget --header="Accept: application/json" \
     https://api.example.com/data

# Process with jq
curl https://api.example.com/data | jq '.items[]'
```

## 3. Response Handling

### The Mail Delivery Metaphor

Think of responses like receiving mail:
- Status codes: Like delivery status
- Headers: Like envelope information
- Body: Like letter contents
- Errors: Like delivery problems

### Status Codes

```
Common Status Codes:
2xx Success
- 200: OK (like "Delivered")
- 201: Created (like "Package Accepted")
- 204: No Content (like "Empty Package")

3xx Redirection
- 301: Moved Permanently (like "New Address")
- 302: Found (like "Temporary Forward")

4xx Client Error
- 400: Bad Request (like "Wrong Address")
- 401: Unauthorized (like "ID Required")
- 404: Not Found (like "Address Not Found")

5xx Server Error
- 500: Internal Error (like "Post Office Problem")
- 503: Service Unavailable (like "Office Closed")
```

### Response Processing

```bash
# Extract specific fields with jq
curl api.example.com/data | jq '.name'

# Format JSON output
curl api.example.com/data | jq '.'

# Filter arrays
curl api.example.com/data | jq '.items[] | select(.price > 10)'

# Transform data
curl api.example.com/data | jq '{name: .name, cost: .price}'
```

### Hands-On Exercise: Response Analyzer

Create response analysis script:
```bash
#!/bin/bash

# Function to analyze response
analyze_response() {
    local url=$1
    
    # Get response with headers
    response=$(curl -i -s $url)
    
    # Extract status code
    status=$(echo "$response" | head -n 1 | cut -d' ' -f2)
    
    # Print analysis
    echo "Status Code: $status"
    
    case $status in
        2*)
            echo "Success!"
            ;;
        3*)
            echo "Redirection detected"
            ;;
        4*)
            echo "Client error"
            ;;
        5*)
            echo "Server error"
            ;;
    esac
    
    # Show headers
    echo -e "\nHeaders:"
    echo "$response" | grep -E "^[A-Za-z-]+:"
}

# Test different endpoints
analyze_response "https://api.example.com/success"
analyze_response "https://api.example.com/error"
```

## Practical Exercises

### 1. API Test Suite
Build script that:
1. Tests multiple endpoints
2. Checks status codes
3. Validates responses
4. Handles errors
5. Generates report

### 2. Data Processor
Create tool to:
1. Fetch JSON data
2. Filter results
3. Transform format
4. Save output
5. Handle errors

### 3. Authentication Tester
Develop script that:
1. Tests different auth methods
2. Validates tokens
3. Checks permissions
4. Reports issues
5. Suggests fixes

## Review Questions

1. **curl Basics**
   - Common curl options?
   - When use different methods?
   - How handle authentication?

2. **Testing Tools**
   - When use Postman vs curl?
   - How process JSON responses?
   - Best practices for testing?

3. **Response Handling**
   - Common status codes?
   - How process different formats?
   - Error handling strategies?

## Additional Resources

### Online Tools
- curl command builders
- JSON validators
- API testing platforms

### Further Reading
- curl documentation
- HTTP status codes
- JSON processing

### Video Resources
- curl tutorials
- API testing guides
- Tool comparisons

## Next Steps

After mastering these concepts, you'll be ready to:
1. Test any API effectively
2. Debug API issues
3. Automate API testing

Remember: Good tools make API work much easier - invest time in learning them well!

## Common Questions and Answers

Q: When should I use curl vs Postman?
A: Use curl for quick tests and automation, Postman for complex testing and team collaboration.

Q: How do I debug API issues?
A: Use verbose mode (-v), check status codes, validate request format, and examine response headers.

Q: Should I learn all curl options?
A: Focus on common options first, learn others as needed for specific tasks.

## Glossary

- **curl**: Command-line tool for transfers
- **Postman**: API development platform
- **jq**: JSON processor
- **Verbose**: Detailed output mode
- **Header**: Request/response metadata
- **Payload**: Request/response data
- **Status Code**: Response indicator
- **Content-Type**: Data format indicator
- **Authentication**: Identity verification
- **Authorization**: Access control

Remember: The right tool for the job makes all the difference - master these tools to become more efficient!
