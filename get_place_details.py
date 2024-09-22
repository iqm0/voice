import os
from dotenv import load_dotenv
from requests import RequestException

# Import functions from the other scripts
from get_calendar_events import get_calendar_events, classify_reservation, extract_possible_business_name
from search_places import search_for_place, get_place_details

# Load environment variables
load_dotenv()
MAPS_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

if __name__ == '__main__':
    events = get_calendar_events()

    api_key = MAPS_KEY
    if not api_key:
        print("Please set your Google Maps API key in the GOOGLE_MAPS_API_KEY environment variable.")
    else:
        print(f"Using Google Maps API key: {api_key}")

    for event in events:
        summary = event['summary']
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        print(f"Event: {summary} - {start_time}")

        reservation_type = classify_reservation(summary)
        print(f"  Type: {reservation_type}")

        if api_key and reservation_type != "Unknown":
            place_name = extract_possible_business_name(summary)
            print(f"  Restaurant: {place_name}")

            if place_name:
                try:
                    search_results = search_for_place(place_name, api_key)
                    if search_results:
                        print("Multiple places found:")
                        for idx, result in enumerate(search_results):
                            print(f"{idx + 1}. {result['name']} - {result.get('formatted_address', 'No address provided')}")

                        choice = int(input(f"Enter the number of the place you mean for {place_name}: ")) - 1

                        if 0 <= choice < len(search_results):
                            place_id = search_results[choice]['place_id']
                            place_details = get_place_details(place_id, api_key)
                            if place_details:
                                print("  Place Details:")
                                print(f"    Name: {place_details.get('name')}")
                                print(f"    Address: {place_details.get('formatted_address')}")
                                print(f"    Phone: {place_details.get('international_phone_number')}")
                            else:
                                print(f"    No details found for place ID: {place_id}")
                        else:
                            print(f"    Invalid selection for {place_name}")
                    else:
                        print(f"    No search results found for {place_name}")
                except RequestException as e:
                    print(f"HTTP Request failed: {e}")
            else:
                print(f"    Could not extract a business name from the event summary: {summary}")