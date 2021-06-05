from common import RIGHTMOVE_NAME


class Station:
    def __init__(self, postcode: str, ids: dict[str, str]):
        self.postcode = postcode
        self.ids = ids


class PredefinedStations:
    HIGHAMS_PARK = Station(
        postcode='E4 9LA',
        ids={
            RIGHTMOVE_NAME: "STATION^4577"
        }
    )