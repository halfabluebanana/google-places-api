# Google Places API Client for Modern Data Structures
## License
MIT License - Created for Columbia University Modern Data Structures Course

## Author
halfabluebanana

A Python implementation of a Google Places API client for searching nearby places, with focus on NYC supermarkets.

## Requirements

- Python 3.7+
- `requests` library
- `pandas` library
- Google Places API key

## Installation
```bash
# Clone the repository
git clone https://github.com/QMSS-G5072-2025/Setiawan_Adeline.git
cd Setiawan_Adeline/Homework08_AS20251105

# Install dependencies
pip install requests pandas
```

## Authentication

### Getting a Google Places API Key

1. **Visit Google Cloud Console**: https://console.cloud.google.com/
2. **Create a Project** (or select an existing one)
3. **Enable the Places API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Places API (New)"
   - Click "Enable"
4. **Create Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key

### Setting Up Your API Key

Choose one of the following methods:

#### Option 1: Environment Variable (Mac/Linux)
```bash
export GOOGLE_PLACES_API_KEY='your_api_key_here'
python google_place_api_practice.py
```

#### Option 2: Environment Variable (Windows)
```cmd
set GOOGLE_PLACES_API_KEY=your_api_key_here
python google_place_api_practice.py
```

#### Option 3: For Jupyter Notebooks
```python
# Add this to the first cell of your notebook
import os
os.environ['GOOGLE_PLACES_API_KEY'] = 'your_api_key_here'
```

## Usage

### Basic Example
```python
from google_place_api_practice import search_nearby_places

# Search for supermarkets near Columbia University
results = search_nearby_places(
    location=(40.8075, -73.9626),
    radius=2000,
    place_types=["supermarket"],
    max_results=10
)

for place in results:
    print(f"{place['name']} - Rating: {place['rating']}")
```

### API Client Function
The main function `search_nearby_places()` accepts:
- `location`: Coordinates as tuple or "lat,lng" string
- `radius`: Search radius in meters (default: 2000)
- `place_types`: List of place types (e.g., ["supermarket", "grocery_store"])
- `max_results`: Maximum results to return (default: 20)
- `api_key`: Optional API key (defaults to environment variable)

## Project Structure
```
├── google_place_api_practice.py  # Main script with API client
├── nyc_supermarket_data.csv      # Sample dataset output
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## Features

- ✅ Secure API key management via environment variables
- ✅ Comprehensive error handling for API failures
- ✅ Flexible location input (coordinates or strings)
- ✅ Creates dataset with 100+ NYC supermarket records
- ✅ Exports data to CSV for analysis

## To run this API client

1. Obtain a Google Places API key using the instructions above
2. Set the API key using any of the three options provided
3. Run the script: `python google_place_api_practice.py`
4. Check the generated `<filename>.csv` for results


## API Documentation

For detailed API information, see:
- [Google Places API (New) Overview](https://developers.google.com/maps/documentation/places/web-service/op-overview)
- [Place Types Reference](https://developers.google.com/maps/documentation/places/web-service/place-types)
- [Pricing Information](https://developers.google.com/maps/billing-and-pricing/pricing#places-pricing)

