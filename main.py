"""
Island Hopper

A project to explore how far a plane can travel when its flight range is limited.

Starting point is Milan Malpensa Airport, Italy.
Main destination is Sydney Airport, Australia.
"""

from functions.airport_data import load_airports, clean_airports
from functions.calculations import calculate_distance
from functions.flight_routes import find_reachable_airports, build_connections, find_route

start_airport = "Milan Malpensa"
destination = "Sydney"

# Aircraft settings
max_range_km = 3000
flight_speed_kmh = 500
refuel_time_hours = 1
customs_time_hours = 2

def show_trip_details():
    """Print the route information and aircraft settings."""
    print("Welcome to Island Hopper!")
    print()
    print(f"Starting from: {start_airport}")
    print(f"Destination: {destination}")
    print()
    print(f"Maximum range: {max_range_km} km")
    print(f"Flying speed: {flight_speed_kmh} km/h")
    print(f"Refuelling time: {refuel_time_hours} hour(s)")
    print(f"Customs time: {customs_time_hours} hour(s)")

def main():
    """Load the airport dataset and prepare it for analysis."""
    show_trip_details()
    airports = load_airports()

    if airports is None:
        return

    print(f"Total airports in dataset: {len(airports)}")

    cleaned_airports = clean_airports(airports)
    print(f"Airports available for our plane: {len(cleaned_airports)}")
    print("\nAirport types after cleaning:")
    print(cleaned_airports["type"].value_counts())
    print("\nFirst five available airports:")
    print(
        cleaned_airports[
            ["name", "iso_country", "latitude_deg", "longitude_deg"]
        ].head()
    )

    selected_airports = cleaned_airports[
        cleaned_airports["ident"].isin(["LIMC", "YSSY"])
    ]

    print(
        selected_airports[
            ["ident", "name", "municipality", "iso_country",
             "latitude_deg", "longitude_deg"]
        ].to_string(index=False)
    )
    milan = cleaned_airports[
        cleaned_airports["ident"] == "LIMC"
    ].iloc[0]

    sydney = cleaned_airports[
        cleaned_airports["ident"] == "YSSY"
    ].iloc[0]

    distance = calculate_distance(
        milan["latitude_deg"],
        milan["longitude_deg"],
        sydney["latitude_deg"],
        sydney["longitude_deg"]
    )

    print("\nDistance between Milan and Sydney:")
    print(f"{distance:,.2f} km")

    if distance <= max_range_km:
        print("Our plane can fly directly to Sydney.")
    else:
        print("Our plane needs intermediate stops to reach Sydney.")

    reachable_airports = find_reachable_airports(
        cleaned_airports,
        "LIMC",
        max_range_km
    )

    if reachable_airports is not None:
        print(f"\nAirports within range: {len(reachable_airports)}")

        print("\nTen closest airports:")
        print(
            reachable_airports[
                ["ident", "name", "iso_country", "distance_km"]
            ].head(10).to_string(index=False)
        )

    connections = build_connections(cleaned_airports, max_range_km)
    print(f"Airports in network: {len(connections)}")
    print(f"Connections from Milan: {len(connections['LIMC'])}")
    print(f"Connections from Sydney: {len(connections['YSSY'])}")


    route = find_route(connections, "LIMC", "YSSY")

    if route is None:
        print("Sydney cannot be reached with the current aircraft range.")
    else:
        flights = len(route) - 1
        stops = max(0, len(route) - 2)

        print("\nRoute with the fewest stops:")
        print(" -> ".join(route))

        print(f"\nNumber of flights: {flights}")
        print(f"Intermediate stops: {stops}")

    for i in range(len(route) - 1):
            first = cleaned_airports[
                cleaned_airports["ident"] == route[i]
            ].iloc[0]

            second = cleaned_airports[
                cleaned_airports["ident"] == route[i + 1]
            ].iloc[0]

            distance = calculate_distance(
                first["latitude_deg"],
                first["longitude_deg"],
                second["latitude_deg"],
                second["longitude_deg"]
            )

            print(f"{route[i]} -> {route[i + 1]}: {distance:.2f} km")

            assert distance <= max_range_km

if __name__ == "__main__":
    main()
