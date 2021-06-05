from typing import Optional, List

from Agent import Agent
from Station import Station


class Property:
    def __init__(self,
                 source,
                 id,
                 url,
                 house: bool,
                 postcode: str,
                 street: str,
                 town: str,
                 floorplan: str,
                 station: Station,
                 price: int,
                 agent: Agent,
                 bedrooms: Optional[int] = None,
                 bathrooms: Optional[int] = None,
                 images: Optional[List[str]] = None,
                 longitude: Optional[float] = None,
                 latitude: Optional[float] = None,
                 new_home: Optional[bool] = None):
        self.source = source
        self.id = id
        self.url = url
        self.house = house
        self.postcode = postcode
        self.street = street
        self.town = town
        self.floorplan = floorplan
        self.station = station
        self.price = price
        self.agent = agent

        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.images = images or []
        self.longitude = longitude
        self.latitude = latitude
        self.new_home = new_home
