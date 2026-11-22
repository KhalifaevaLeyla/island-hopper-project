from functions.calculations import calculate_distance

def find_reachable_airports(airports, start_code, max_range_km):
    """
    Find airports that can be reached directly from a starting airport.
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
    """
    connections = {}

    airport_codes = airports["ident"].to_numpy()
    latitudes = airports["latitude_deg"].to_numpy()
    longitudes = airports["longitude_deg"].to_numpy()

    # For each airport, find all other airports within flying range
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


def find_fastest_route(
    connections, airports, start, destination,
    flight_speed_kmh, refuel_time_hours, customs_time_hours
):
    """
    Find the route with the shortest total travel time.
    """
    if start not in connections or destination not in connections:
        return None

    airport_info = airports.set_index("ident")

    times = {start: 0}
    previous = {start: None}
    unvisited = [start]
    visited = set()

    while unvisited:
        # Choose the airport with the lowest known travel time
        current = min(unvisited, key=lambda airport: times[airport])
        unvisited.remove(current)
        visited.add(current)

        if current == destination:
            break

        first = airport_info.loc[current]

        for next_airport in connections[current]:
            if next_airport in visited:
                continue

            second = airport_info.loc[next_airport]

            distance = calculate_distance(
                first["latitude_deg"],
                first["longitude_deg"],
                second["latitude_deg"],
                second["longitude_deg"]
            )

            flight_time = distance / flight_speed_kmh

            customs_time = 0
            if first["iso_country"] != second["iso_country"]:
                customs_time = customs_time_hours

            refuel_time = 0
            if current != start:
                refuel_time = refuel_time_hours

            new_time = (
                times[current]
                + flight_time
                + customs_time
                + refuel_time
            )

            # Update the route if we found a faster way to this airport
            if new_time < times.get(next_airport, float("inf")):
                times[next_airport] = new_time
                previous[next_airport] = current

                if next_airport not in unvisited:
                    unvisited.append(next_airport)

    if destination not in visited:
        return None

    # Follow the previous airports backwards to rebuild the route
    route = []
    current = destination

    while current is not None:
        route.append(current)
        current = previous[current]

    route.reverse()

    return route


def find_airports_within_stops(connections, start, max_stops):
    """
    Find airports reachable with a limited number of stops.
    """
    if start not in connections:
        return {}

    max_flights = max_stops + 1

    flights_needed = {start: 0}
    airports_to_check = [start]

    # Explore airports until we reach the allowed number of flights
    for current in airports_to_check:
        current_flights = flights_needed[current]

        if current_flights >= max_flights:
            continue

        for nearby in connections[current]:
            if nearby not in flights_needed:
                flights_needed[nearby] = current_flights + 1
                airports_to_check.append(nearby)

    return flights_needed

