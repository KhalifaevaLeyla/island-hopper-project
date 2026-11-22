import numpy as np

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth
    using their latitude and longitude.
    """

    # Convert degrees to radians
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


def calculate_travel_time(
    route, airports, flight_speed_kmh, refuel_time_hours, customs_time_hours
):
    """
    Caalculate flying, refuelling and customs time for a route.
    """
    if not route:
        return None

    if flight_speed_kmh <= 0:
        raise ValueError("Flight speed must be positive.")

    if refuel_time_hours < 0 or customs_time_hours < 0:
        raise ValueError("Stop durations cannot be negative.")

    # Compute flying time for each flight in the route
    airport_info = airports.set_index("ident")
    flying_hours = 0
    customs_hours = 0

    for i in range(len(route) - 1):
        first = airport_info.loc[route[i]]
        second = airport_info.loc[route[i + 1]]
        distance = calculate_distance(
            first["latitude_deg"],
            first["longitude_deg"],
            second["latitude_deg"],
            second["longitude_deg"]
        )
        flying_hours += distance / flight_speed_kmh

        if first["iso_country"] != second["iso_country"]:
            customs_hours += customs_time_hours

    stops = max(0, len(route) - 2)
    refuelling_hours = stops * refuel_time_hours
    total_hours = flying_hours + refuelling_hours + customs_hours

    return {
        "flying_hours": flying_hours,
        "refuelling_hours": refuelling_hours,
        "customs_hours": customs_hours,
        "total_hours": total_hours
    }
