
import numpy as np

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two locations on Earth.

    Parameters:
        lat1, lon1: Coordinates of the first location.
        lat2, lon2: Coordinates of the second location.

    Returns:
        Distance in kilometres.
    """
    earth_radius = 6371

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    latitude_difference = lat2 - lat1
    longitude_difference = lon2 - lon1

    a = (
        np.sin(latitude_difference / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(longitude_difference / 2) ** 2
    )

    distance = 2 * earth_radius * np.arcsin(np.sqrt(a))

    return distance