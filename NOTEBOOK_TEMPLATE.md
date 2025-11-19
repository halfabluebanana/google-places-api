# Template for Jupyter Notebook Markdown Cells

## Cell 1: Title and Setup Instructions

```markdown
# API Assignment - Google Places API

**Student Name**: [Your Name]  
**Date**: [Date]

---

## Setup Instructions

This notebook uses the **Google Places API** which requires authentication via API key.

### For Graders: How to Get an API Key

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the "Places API (New)"
4. Go to "Credentials" and create an API key
5. Set the API key using one of the methods below

### Setting Up Your API Key

**Option 1: Environment Variable (Recommended)**
```bash
export GOOGLE_PLACES_API_KEY='your_api_key_here'
jupyter notebook
```

**Option 2: In the notebook (see next cell)**

Uncomment and edit the setup line in the next code cell.

⚠️ **Note**: This submission does NOT include an actual API key for security reasons.
```

## Cell 2: API Key Setup (Code Cell)

```python
import requests
import os
import pandas as pd

# ============================================
# SETUP: API Key Configuration
# ============================================
# For testing/grading: Uncomment the line below and add your API key
# os.environ['GOOGLE_PLACES_API_KEY'] = 'your_api_key_here'

# Load API key from environment variable
API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')

if not API_KEY:
    raise ValueError(
        "API key not found! Please set the GOOGLE_PLACES_API_KEY environment variable.\n"
        "Options:\n"
        "1. Set in terminal: export GOOGLE_PLACES_API_KEY='your_key'\n"
        "2. Uncomment the line above and add your key"
    )

print("✓ API key loaded successfully")
```

## Cell 3: Question 2 - Authentication

```markdown
## 2. Authentication

### 2a) How the API Authenticates Users

The Google Places API uses **API Key authentication**. The API key is passed in the request headers using the `X-Goog-Api-Key` header field. This key identifies your Google Cloud project and provides access to enabled APIs.

Authentication flow:
1. Client includes API key in request header: `X-Goog-Api-Key: YOUR_API_KEY`
2. Google validates the key against their records
3. If valid, checks if the key has permissions for the Places API
4. If authorized, processes the request and returns data

### 2b) How to Obtain an API Key

**Step-by-step instructions:**

1. **Create Google Cloud Account**
   - Visit: https://console.cloud.google.com/
   - Sign in with Google account

2. **Create or Select a Project**
   - Click on project dropdown (top left)
   - Click "New Project"
   - Name your project and click "Create"

3. **Enable Places API**
   - Go to "APIs & Services" > "Library"
   - Search for "Places API (New)"
   - Click on it and press "Enable"

4. **Create API Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "+ CREATE CREDENTIALS"
   - Select "API Key"
   - Copy the generated key
   - (Optional) Restrict the key to specific APIs and IP addresses for security

5. **Set Up Billing** (Note: Google provides free tier credits)
   - Some API features may require billing to be enabled
   - New users get $300 in free credits

**Official Documentation**: https://developers.google.com/maps/documentation/places/web-service/get-api-key
```

## Cell 4: Question 3 - Simple GET Request

```markdown
## 3. Send a Simple GET Request

### 3a) GET Request with Query Parameters

Let's search for cafes near Times Square, NYC using several query parameters.
```

## Cell 5: Question 3a Code

```python
# API endpoint
endpoint = "https://places.googleapis.com/v1/places:searchNearby"

# Query parameters explained:
# - location: Latitude/longitude coordinates (Times Square)
# - radius: Search radius in meters
# - types: Filter by place types
# - languageCode: Language for returned results
# - maxResultCount: Limit number of results

params = {
    "location": "40.7580,-73.9855",    # Times Square, NYC
    "radius": 500,                     # 500 meters
    "types": ["cafe"],                 # Looking for cafes
    "languageCode": "en",              # English results
    "maxResultCount": 5                # Limit to 5 results
}

# Headers with API key
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY
}

# Send GET request
response = requests.get(endpoint, params=params, headers=headers)

# Display request details
print("Request Details:")
print(f"URL: {response.url}")
print(f"\nQuery Parameters Used:")
for key, value in params.items():
    print(f"  - {key}: {value}")
```

## Cell 6: Question 3b - Status Code

```markdown
### 3b) Check and Display Request Status
```

```python
# Check status code
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    print("✓ Request successful!")
elif response.status_code == 400:
    print("✗ Bad Request - Check parameters")
elif response.status_code == 401:
    print("✗ Unauthorized - Check API key")
elif response.status_code == 403:
    print("✗ Forbidden - API key may lack permissions")
elif response.status_code == 429:
    print("✗ Rate limit exceeded")
else:
    print(f"✗ Request failed with status: {response.status_code}")
```

## Cell 7: Question 3c - Response Type

```markdown
### 3c) Identify Response Type and Display Snippet
```

```python
# Identify response type
content_type = response.headers.get("Content-Type", "")
print(f"Content-Type Header: {content_type}")

if "json" in content_type:
    print("\n✓ Response Type: JSON")
    
    # Parse JSON
    data = response.json()
    
    # Display snippet
    if "places" in data and data["places"]:
        print(f"\nFound {len(data['places'])} places")
        print("\nFirst place result:")
        print("-" * 50)
        first_place = data["places"][0]
        
        # Display key information
        for key, value in first_place.items():
            if not isinstance(value, (dict, list)):  # Simple fields only
                print(f"{key}: {value}")
    else:
        print("No places found in response")
else:
    print(f"Response Type: {content_type}")
    print(response.text[:500])
```

## For Question 4 and 5

Continue with similar structured markdown and code cells for:
- Question 4: Parse response and create dataset
- Question 5: API client function

The function from the .py file can be copied into a notebook cell with proper documentation.

