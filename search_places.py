import requests

def search_for_place(query, api_key):
    """Searches for a place using the Google Maps Places Text Search API and returns a list of possible results."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'results' in data and data['results']:
        return data['results']  # Return all matches
    else:
        return []

def get_place_details(place_id, api_key):
    """Fetches place details using the Google Maps Places Details API."""
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,international_phone_number,rating,opening_hours,geometry",
        "key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data['status'] == 'OK':
        return data['result']
    else:
        return None