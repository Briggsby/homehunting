import re

import requests

from Property import Property
from Station import Station, PredefinedStations
from common import get_postcode_from_location, RIGHTMOVE_NAME
from Agent import Agent


class Rightmove:
    ACCESS_URI = "https://www.rightmove.co.uk/api/"
    PROPERTY_URL = "https://www.rightmove.co.uk/properties/"
    HOUSE_TYPES = ["Semi-Detached", "Detached", "Terraced"]
    FLOORPLAN_REGEX = re.compile(r"(https://media\.rightmove\.co\.uk/[^\"]*FLP[^\"(max)]*\.(png|jpg|jpeg|bmp))")

    ACTIONS = {
        "search": "_search"
    }

    @staticmethod
    def get_floorplan(property_id):
        if not property_id:
            return None
        response = requests.get(Rightmove.PROPERTY_URL + str(property_id) + "#/floorplan?activePlan=1")

        matches = Rightmove.FLOORPLAN_REGEX.findall(response.text)
        if not matches:
            return None
        return matches[0][0]

    @staticmethod
    def get_property_search_response_dicts(**params):
        response = requests.get(Rightmove.ACCESS_URI + Rightmove.ACTIONS["search"], params)
        if response.status_code != 200:
            return []
        return response.json().get("properties")

    @staticmethod
    def search_properties_near_station(station: Station, distance: float, **params):
        station_id = station.ids.get(RIGHTMOVE_NAME)
        if not station_id:
            raise ValueError("No Rightmove id for station")

        params = {**params, "locationIdentifier": station_id, "radius": distance}
        return [
            Rightmove.to_property(property_dict, station)
            for property_dict in Rightmove.get_property_search_response_dicts(**params)
        ]

    @staticmethod
    def split_address(address_string):
        if not address_string or not isinstance(address_string, str):
            return None, None

        possible_splitters = ('\r\n', ', ', ',')

        for splitter in possible_splitters:
            if splitter in address_string:
                street = address_string.split(splitter)[0] or None
                town = address_string.split(splitter)[1] or None
                return street, town

        street = address_string
        town = address_string
        return street, town

    @staticmethod
    def is_new_home(property_dict):
        lozenge_model = property_dict.get("lozengeModel")
        if not isinstance(lozenge_model, dict):
            return False
        matching_lozenges = lozenge_model.get("matchingLozenges")
        if not matching_lozenges or not isinstance(matching_lozenges, list):
            return False

        return matching_lozenges[0].get("type") == "NEW_HOME"

    @staticmethod
    def to_property(property_dict: dict, station: Station):
        property_id = property_dict.get("id")
        longitude = property_dict.get("location", dict()).get("longitude")
        latitude = property_dict.get("location", dict()).get("latitude")
        street, town = Rightmove.split_address(property_dict.get("displayAddress"))

        return Property(
            source=RIGHTMOVE_NAME,
            id=property_id,
            url=Rightmove.PROPERTY_URL + str(property_dict.get("id")),
            house=property_dict.get("propertySubType") in Rightmove.HOUSE_TYPES,
            postcode=get_postcode_from_location(
                longitude=longitude,
                latitude=latitude,
            ),
            street=street,
            town=town,
            floorplan=Rightmove.get_floorplan(property_id),
            station=station,
            price=property_dict.get("price", dict()).get("amount"),
            agent=Agent(
                name=property_dict.get("customer", dict()).get("branchDisplayName"),
                phone=property_dict.get("customer", dict()).get("contactTelephone"),
            ),
            bedrooms=property_dict.get("bedrooms"),
            bathrooms=property_dict.get("bathrooms"),
            images=[
                image.get("srcUrl") for image
                in property_dict.get("propertyImages", dict()).get("images", list())
                if image.get("srcUrl")
            ],
            longitude=longitude,
            latitude=latitude,
            new_home=Rightmove.is_new_home(property_dict),
        )


if __name__ == '__main__':
    test_station = PredefinedStations.HIGHAMS_PARK
    test_distance = 1
    test_params = {
        "numberofPropertiesPerPage": 20,
        "sortType": 2,
        "index": 0,
        "includeSSTC": False,
        "viewType": "LIST",
        "channel": "BUY",
        "areaSizeUnit": "sqft",
        "currencyCode": "GBP",
        "isFetching": False,
        "minPrice": 400000,
        "maxPrice": 450000,
        "minBedrooms": 2,
    }

    properties = Rightmove.search_properties_near_station(test_station, test_distance, **test_params)

    print(properties)