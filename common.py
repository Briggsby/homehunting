import requests

POSTCODE_URL = "https://api.postcodes.io/postcodes"
RIGHTMOVE_NAME = "Rightmove"


def get_postcode_from_location(longitude, latitude):
    response = requests.get(POSTCODE_URL, {
        "longitude": longitude,
        "latitude": latitude,
    })

    result = response.json().get('result') or [dict()]
    return result[0].get('postcode', None)
