import re
import pycountry
import logging
import asyncio
import aiohttp

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from .states import state_abbreviations

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

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

    async def async_geocode(self, location):
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        headers = {'User-Agent': self.user_agent}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        return data[0]
                return None

    async def reformat_location(self, location, max_retries=3):
        if location is not None:
            cleaned_location = self.clean_location(location)
            filtered_loc = cleaned_location.split("-")[0]

            retry_count = 0
            while retry_count < max_retries:
                try:
                    geolocation = await self.async_geocode(filtered_loc)
                    if geolocation:
                        address = geolocation['display_name']
                        logging.info(f"Geolocation address: {address}")  # Debugging statement

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
                            logging.warning(f"Unknown location: {location}")
                            return 'United States'
                    else:
                        logging.warning(f"No geolocation found for {location}")
                        return 'United States'
                except Exception as e:
                    retry_count += 1
                    logging.warning(f"Connection error: {e}. Retrying attempt {retry_count}.")
                    await asyncio.sleep(1)  # wait a bit before retrying
        
        return 'United States'

# Asynchronous function to process multiple locations
async def process_locations(locations_worked, location_formatter):
    for i, loc in enumerate(locations_worked):
        newloc = await location_formatter.reformat_location(loc)
        locations_worked[i] = newloc
        await asyncio.sleep(1.1)

# Example usage
locations_worked = ["Washington, District of Columbia, United States"]  # Your list of locations
location_formatter = LocationFormatter()

# Run the async process
asyncio.run(process_locations(locations_worked, location_formatter))

# Print the updated locations
print(locations_worked)
