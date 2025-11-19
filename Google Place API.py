import requests
import os
import pandas as pd

# Set your API key here or use environment variable
# os.environ['GOOGLE_PLACES_API_KEY'] = 'your_api_key_here'
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
# ============================================
#3. Send a GET request
# ============================================

# API endpoint
endpoint = "https://places.googleapis.com/v1/places:searchNearby"

# Request body. Google Places API New uses POST with JSON body, not GET
request_body = {
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": 40.8075,    # Columbia University latitude
                "longitude": -73.9626   # Columbia University longitude
            },
            "radius": 2000.0            # 2km radius
        }
    },
    "includedTypes": ["supermarket"],  #i'm looking for supermarkets around Columbia University
    "languageCode": "en",
    "maxResultCount": 3
}

# Headers with API key for authentication
headers = {
    "Content-Type": "application/json", #tells API to send request in JSON format
    "X-Goog-Api-Key": API_KEY, #API key for authentication
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.rating,places.id,places.reviews" 
    #fields to return in response. Name, address, types, rating, reviews 
    #https://developers.google.com/maps/documentation/places/web-service/data-fields
}

# Send POST request to API
response = requests.post(endpoint, json=request_body, headers=headers)

# a) Show request URL
print(f"Request URL: {response.url}")

# b) Display the status
print(f"Status code: {response.status_code}")

# c) Identify and display response type
print(f"Response type: {response.headers.get('Content-Type')}")

# show first place result
data = response.json() #convert response to JSON format
print(f"\n results:")
print(data["places"][0]  if "places" in data else "No places found")


# ============================================
# 4: Parse Response and Create Dataset
# ============================================

# a) Convert API response into a pandas DataFrame

def parse_place_data(place):
    # i want to extract these fields from the place object
    return {
        'name': place.get('displayName', {}).get('text', 'N/A'),
        'address': place.get('formattedAddress', 'N/A'),
        'rating': place.get('rating', None),
        'types': ', '.join(place.get('types', [])),
        'review_count': len(place.get('reviews', [])),
        'reviews': [review.get('text', 'N/A') for review in place.get('reviews', [])]
    }

# Loop through each place in response. Parse first 3 results into a DataFrame
# convert list of dictionaries into a pandas DataFrame
if "places" in data:
    places_list = [parse_place_data(place) for place in data["places"]]
    df_sample = pd.DataFrame(places_list)
    print(df_sample)


# b) Create dataset of > 100 sample size
print("b) Larger dataset (>100 records)")

all_places = [] #create list to store place information

# Search other neighborhoods in NYC.
locations = [
    (40.7580, -73.9855, "Midtown Manhattan"),
    (40.7282, -73.9942, "Greenwich Village"),
    (40.7614, -73.9776, "Upper West Side"),
    (40.7060, -74.0088, "Tribeca"),
    (40.7489, -73.9680, "Murray Hill"),
    (40.7831, -73.9712, "Upper East Side"),
    (40.7178, -73.9967, "SoHo"),
    (40.7308, -73.9973, "East Village")
]

# search for variant names using Google Places API types
place_types = ["supermarket", "grocery_store", "store"]

# Collect data from multiple searches. for each type of supermarket, perform a separate search. 
# in this inner loop, we are capturing the diff naming conventions. increases coverage for places on Google

def collect_places(lat, lng, location_name, ptype):
    """Make API request and collect places data"""
    request_body = {
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": 2000.0 #2km radius consistent with previous request
            }
        },
        "includedTypes": [ptype],
        "languageCode": "en",
        "maxResultCount": 20
    }
    
    response = requests.post(endpoint, json=request_body, headers=headers)
    
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', response.text)
        print(f"  Failed to collect from {location_name} - {ptype}: Status {response.status_code}")
        print(f"    Error: {error_msg}")
        return []
    
    result = response.json()
    places = result.get('places', [])
    
    for place in places:
        place_info = parse_place_data(place)
        place_info['location_searched'] = location_name
        place_info['place_type_searched'] = ptype
        all_places.append(place_info)
    
    print(f"  Collected from {location_name} - {ptype}: {len(places)} places")
    return places

for lat, lng, location_name in locations:
    for ptype in place_types:
        collect_places(lat, lng, location_name, ptype)

# Create DataFrame
df = pd.DataFrame(all_places)
print(f"\nTotal results: {len(df)}")


# c) Summary statistics
print(f"="* 60)
print(f"c) Summary Statistics:")
print(f"="* 60)

print("\nDataFrame Info:")
print(df.info())

if len(df) > 0:
    print("\nDescriptive Statistics:")
    print(df.describe())

    print("\nRating Distribution:")
    print(df['rating'].value_counts().head(10))

    print("\nTop 10 Most Common Place Types:")
    print(df['types'].value_counts().head(10))

    print("\nLocation Distribution:")
    print(df['location_searched'].value_counts())

    print("\nPlace Type Distribution:")
    print(df['place_type_searched'].value_counts())

    print("\nReview Count Distribution:")
    print(df['review_count'].value_counts())
else:   
    print(f"dataframe is empty")
# Save to CSV
df.to_csv('nyc_supermarket_data.csv', index=False)
print(f"csv file saved")

# ============================================
# 5: API Client Function 
# ============================================

def search_nearby_places(
    location, 
    radius=2000,
    place_types=None, 
    language="en", 
    max_results=20, 
    api_key=None):

    """
    Search for places near a specific location using Google Places API (New)

    This function simplifies API access by handling: 
    - Authentication setup
    - Request formatting
    - Error handling 
    - Response parsing
    
    Parameters
    ----------
    location : tuple or str
        Either a name like "Columbia University" or coordinates (lat, lng)
        Latitude and longitude as tuple (lat, lng) or string "lat,lng" 
        (e.g., (40.7580, -73.9855) or "40.7580,-73.9855")

    radius : int or float, optional
        Search radius in meters (default: 500)
        Used radius 2km to match previous request

    place_types : list of str, optional
        Types of places to search for (e.g. supermarkets)
        Note: Use underscores, not spaces (e.g., "grocery_store" not "grocery store")
        If None, searches all types (supermarket, grocery_store, store)

    language : str, optional
        Language code for results (default: "en")

    max_results : int, optional
        Maximum number of results to return (default: 20)

    api_key : str, optional
        Google Places API key. Defaults to environment variable GOOGLE_PLACES_API_KEY
    
    
    Returns
    -------
    list of dict
        List of place dictionaries with name, address, rating, types, review_count, reviews, etc
    
    Raises
    ------
    ValueError
        if location format is invalid, or API key missing

    requests.HTTPError
        If API request fails (4xx/5xx status codes)

    requests.RequestException
        If network error occurs (connection timeout, etc)
    
    Examples
    --------
    # Search by place name
    # places = search_nearby_places("Times Square", place_types=["restaurant"])
   
    # Search by coordinates
    # places = search_nearby_places((40.7580, -73.9855), radius=500)
    
    # Get all nearby places
    # places = search_nearby_places("Central Park")
    """

  # STEP 1: Handle API key (hide authentication complexity)
    if api_key is None:
        api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if not api_key:
            raise ValueError(
                "No API key provided. Either pass api_key parameter or "
                "set GOOGLE_PLACES_API_KEY environment variable. "
                "Get one at: https://console.cloud.google.com/"
            )
    # STEP 2: Parse location
    if isinstance(location, str):
        #if string, could be place name -- but would need geocoding
        # or coordinates (lat, lng)
        # split string by comma and convert to float
        if(',' in location):
            lat, lng = map(float, location.split(','))
        else: 
            raise ValueError("please provide location as 'lat,lng' or tuple (lat, lng)")
    elif isinstance(location, (tuple, list)):
        lat, lng = location
    else:
        raise ValueError("Location must be a string 'lat,lng' or tuple (lat, lng)")
    
    # STEP 3: Build request, setup endpoint and headers
    endpoint = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.rating,places.id"
    }
    
    # Build request body (Google Places API New uses POST with JSON body)
    request_body = {
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": float(radius)
            }
        },
        "languageCode": language,
        "maxResultCount": max_results
    }
    
    if place_types:
        request_body["includedTypes"] = place_types
    
    try:
        # Send POST request (not GET!)
        response = requests.post(endpoint, json=request_body, headers=headers)
        
        # Check for HTTP errors (4xx, 5xx)
        if response.status_code == 400:
            error_msg = f"Bad Request - Check your parameters\nAPI Error: {response.text}"
            raise requests.HTTPError(error_msg)
        elif response.status_code == 401:
            raise requests.HTTPError("Unauthorized - Check your API key at https://console.cloud.google.com/")
        elif response.status_code == 403:
            raise requests.HTTPError("Forbidden - API key lacks permissions. Enable places API at Google Cloud Console.")
        elif response.status_code == 429:
            raise requests.HTTPError("Rate limit exceeded - Too many requests. Slow down or upgrade billing plan")
        elif response.status_code >= 500:
            raise requests.HTTPError(f"Server error: {response.status_code}. Try again later.")
        
        # Raise for any other errors
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        places = data.get('places', [])
        
        # Transform raw data into user-friendly format
        simplified_places = []
        for place in places: 
            simplified_places.append({
                'name': place.get('displayName', {}).get('text', 'N/A'),
                'address': place.get('formattedAddress', 'N/A'),
                'rating': place.get('rating', None),
                'types': ', '.join(place.get('types', [])),
                'review_count': len(place.get('reviews', [])),
                'reviews': [review.get('text', 'N/A') for review in place.get('reviews', [])]
            })
        return simplified_places

    except requests.exceptions.ConnectionError as e:
        raise requests.RequestException(f"Network connection error: {e}")
    except requests.exceptions.Timeout as e:
        raise requests.RequestException(f"Request timeout: {e}")
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}")

#STEP 6: Test the function

# Example usage of the function
if __name__ == "__main__":
    print(f"="*50)
    print("Testing API Client Function")
    print("="*50)
    
    # Test with basic search
    try:
        print("\nTest 1: search for supermarkets near Columbia University")
        results = search_nearby_places(
            location=(40.8075, -73.9626),  # Columbia University
            radius=5000,
            place_types=["supermarket"],  # Valid place types
            max_results=5
        )
        print(f"\nFound {len(results)} places")
        if results:
            print("\nFirst result:")
            print(f"Nearest: {results[0]['name']}")
            print(f"Rating: {results[0]['rating']}")
            print(f"Types: {results[0]['types']}")
            print(f"Address: {results[0]['address']}")
            print(f"Review Count: {results[0]['review_count']}")
            print(f"Reviews: {results[0]['reviews']}")
    except Exception as e:
        print(f"Error: {e}")

#Test with multiple place types
try:
    print("\nTest 2: search for supermarkets and grocery stores near Columbia University")
    results = search_nearby_places(
        location=(40.8075, -73.9626),
        radius=5000,
        place_types=["supermarket", "grocery_store"],
        max_results=5
    )
    print(f"\nFound {len(results)} places")
    if results:
        print("\nFirst result:")
except Exception as e:  
        print(f"Test 2 error: {e}")
    
# Test wth invalid location
try: 
    print("\nTest 3: search for places near invalid location")
    results = search_nearby_places(
        location="123 Spongebob St, Underthesea, USA",
        radius=5000,
        place_types=["supermarket"],
        max_results=5
    )
except ValueError as e:
    print(f"Correctly caught error: {e}")

# Test with no place types
try:    
    print("\nTest 4: search for places near Columbia University without specifying place types")
    results = search_nearby_places(
        location=(40.8075, -73.9626),
        radius=5000,
        #missing place types parameter
        max_results=5
    )
    print(f"Found {len(results)} places of various types")
except Exception as e:
    print(f"Test 3 failed: {e}")