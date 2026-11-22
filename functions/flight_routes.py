from functions.calculations import calculate_distance

def find_reachable_airports(airports, start_code, max_range_km):
    """
    Find airports that can be reached directly from a starting airport.

    Parameters:
        airports: DataFrame containing the cleaned airport data.
        start_code: ICAO code of the starting airport.
        max_range_km: Maximum distance the aircraft can fly.

    Returns:
        DataFrame containing reachable airports and their distances.
    """
    start = airports[airports["ident"] == start_code]

    if start.empty:
        print(f"Airport {start_code} was not found.")
        return None

    start = start.iloc[0]

    possible_flights = airports.copy()

    # Calculate the distance from our starting airport to all others
    possible_flights["distance_km"] = calculate_distance(
        start["latitude_deg"],
        start["longitude_deg"],
        possible_flights["latitude_deg"].to_numpy(),
        possible_flights["longitude_deg"].to_numpy()
    )

    # Keep only airports within range, excluding the starting airport
    possible_flights = possible_flights[
        (possible_flights["distance_km"] <= max_range_km)
        & (possible_flights["ident"] != start_code)
    ]

    return possible_flights.sort_values("distance_km")
