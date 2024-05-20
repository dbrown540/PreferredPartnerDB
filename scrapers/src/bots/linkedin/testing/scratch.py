import re
import pycountry
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from .scratch2 import state_abbreviations

class LocationFormatter:
    def __init__(self):
        self.user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/124.0.0.0 "
                           "Safari/537.36"
        )
        self.geolocator = Nominatim(user_agent=self.user_agent)

    def clean_location(self, location):
        words_to_remove = ["Metropolitan", "Area", "Greater", "Metro"]
        cleaned_location = re.sub(r'\b(?:{})\b'.format('|'.join(words_to_remove)), '', location)
        return cleaned_location.strip()

    def reformat_location(self, location, max_retries=3):
        if location is not None:
            cleaned_location = self.clean_location(location)
            filtered_loc = cleaned_location.split("-")[0]

            retry_count = 0
            while retry_count < max_retries:
                try:
                    geolocation = self.geolocator.geocode(filtered_loc, timeout=10)
                    if geolocation:
                        address = geolocation.address
                        print(f"Geolocation address: {address}")  # Debugging statement

                        split_address = address.split(", ")
                        city = None
                        state = None
                        country = None

                        # Check for city, state, and country
                        for element in split_address:
                            if not city:
                                city = element
                            if element in state_abbreviations:
                                state = state_abbreviations[element]
                            elif element == 'District of Columbia':
                                state = 'DC'
                            if not state and not country:
                                country = pycountry.countries.get(name=element)
                                if country:
                                    country = country.name

                        if city and state:
                            return f'{city}, {state}'
                        elif city and country:
                            return f'{city}, {country}'
                        else:
                            print("Unknown location: ", location)
                            return 'Unknown Location'
                    else:
                        return 'No geolocation found.'
                except GeocoderTimedOut:
                    retry_count += 1
                    print(f"Connection timed out. Retrying attempt {retry_count}.")
        
        return location

locator = LocationFormatter()
result = locator.reformat_location("Los Angeles Metropolitan Area")
print(result)
