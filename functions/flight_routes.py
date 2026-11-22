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


def add_connection(connections, airport_a, airport_b):
    """
    Add a possible flight between two airports.

    Parameters:
        connections: Dictionary of airport connections.
        airport_a: First airport code.
        airport_b: Second airport code.

    Returns:
        Updated connections dictionary.
    """
    if airport_a not in connections:
        connections[airport_a] = []

    if airport_b not in connections:
        connections[airport_b] = []

    if airport_b not in connections[airport_a]:
        connections[airport_a].append(airport_b)

    if airport_a not in connections[airport_b]:
        connections[airport_b].append(airport_a)

    return connections

def build_connections(airports, max_range_km):
    """
    Find possible direct flights between all eligible airports.

    Parameters:
        airports: DataFrame of cleaned airports.
        max_range_km: Maximum distance allowed for one flight.

    Returns:
        Dictionary containing airport codes and their connections.
    """
    connections = {}

    airport_codes = airports["ident"].to_numpy()
    latitudes = airports["latitude_deg"].to_numpy()
    longitudes = airports["longitude_deg"].to_numpy()

    for i in range(len(airport_codes)):
        distances = calculate_distance(
            latitudes[i],
            longitudes[i],
            latitudes,
            longitudes
        )

        within_range = (
            (distances <= max_range_km)
            & (distances > 0)
        )

        nearby_airports = airport_codes[within_range]
        connections[airport_codes[i]] = nearby_airports.tolist()

    return connections


def find_route(connections, start, destination):
    """
    Find a route with the fewest flights between two airports.

    Parameters:
        connections: Dictionary containing possible airport connections.
        start: Starting airport code.
        destination: Destination airport code.

    Returns:
        List of airport codes in the route, or None if no route exists.
    """
    if start not in connections or destination not in connections:
        return None

    routes = [[start]]
    visited = {start}

    for route in routes:
        current = route[-1]

        if current == destination:
            return route

        for airport in connections[current]:
            if airport not in visited:
                visited.add(airport)
                routes.append(route + [airport])

    return None

