"""
Island Hopper

A project to explore how far a plane can travel when its flight range is limited.

Starting point is Milan Malpensa Airport, Italy.
Main destination is Sydney Airport, Australia.
"""
import matplotlib.pyplot as plt
from functions.airport_data import load_airports, clean_airports
from functions.calculations import calculate_distance, calculate_travel_time
from functions.flight_routes import find_reachable_airports, build_connections, find_route, find_fastest_route, find_airports_within_stops
from functions.visualizations import plot_airport_types, plot_travel_times, plot_flight_route

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
    airports = load_airports() # Load the dataset
    
    if airports is None:
        return
    print(f"Total airports in dataset: {len(airports)}")

    cleaned_airports = clean_airports(airports)
    print(f"\nAirports in dataset: {len(airports)}")
    print(f"Airports after cleaning: {len(cleaned_airports)}")


    # Сoordinates of Milan and Sydney, distance between them
    milan = cleaned_airports[cleaned_airports["ident"] == "LIMC"].iloc[0]
    sydney = cleaned_airports[cleaned_airports["ident"] == "YSSY"].iloc[0]
    distance = calculate_distance(
        milan["latitude_deg"],
        milan["longitude_deg"],
        sydney["latitude_deg"],
        sydney["longitude_deg"]
    )
    print(f"\nDistance from Milan to Sydney: {distance:,.2f} km")

    if distance <= max_range_km:
        print("Our plane can fly directly to Sydney.")
    else:
        print("Our plane needs intermediate stops to reach Sydney.")


    # Airports we can reach from Milan in one flight
    reachable_airports = find_reachable_airports(
        cleaned_airports,
        "LIMC",
        max_range_km
    )
    if reachable_airports is not None:
        print(f"Direct flights from Milan: {len(reachable_airports)}")


    # Airports connected by flights within 3000 km
    connections = build_connections(cleaned_airports, max_range_km)
    print(f"Airports in network: {len(connections)}")


    # Route with the smallest number of stops
    route = find_route(connections, "LIMC", "YSSY")
    if route is None:
        print("\nSydney cannot be reached with the current aircraft range.")
    else:
        flights = len(route) - 1
        stops = max(0, len(route) - 2)
        travel_time = calculate_travel_time(
              route,
              cleaned_airports,
              flight_speed_kmh,
              refuel_time_hours,
              customs_time_hours
          )
        print("\nRoute with the fewest stops:")
        print(" -> ".join(route))
        print(f"Flights: {flights} | Stops: {stops}")
        print(f"Total travel time: {travel_time['total_hours']:.2f} hours")


    # Route with the fewest stops
    fastest_route = find_fastest_route(
        connections,
        cleaned_airports,
        "LIMC",
        "YSSY",
        flight_speed_kmh,
        refuel_time_hours,
        customs_time_hours
    )

    if fastest_route is None:
        print("\nNo possible route was found.")
    else:
        fastest_time = calculate_travel_time(
            fastest_route,
            cleaned_airports,
            flight_speed_kmh,
            refuel_time_hours,
            customs_time_hours
        )
        print("\nFastest route:")
        print(" -> ".join(fastest_route))
        print(f"Flights: {len(fastest_route) - 1} | " f"Stops: {max(0, len(fastest_route) - 2)}")
        print(f"Total travel time: {fastest_time['total_hours']:.2f} hours")   


    # Destinations reachable with no more than 10 stops
    reachable = find_airports_within_stops(
        connections,
        "LIMC",
        10
    )
    possible_destinations = cleaned_airports[cleaned_airports["ident"].isin(reachable)].copy()
    possible_destinations = possible_destinations[possible_destinations["ident"] != "LIMC"].copy()

    if possible_destinations.empty:
        print("\nNo airports found within the stop limit.")
    else:
        possible_destinations["distance_from_milan"] = calculate_distance(
            milan["latitude_deg"],
            milan["longitude_deg"],
            possible_destinations["latitude_deg"].to_numpy(),
            possible_destinations["longitude_deg"].to_numpy()
        )

    
    # Route to the farthest airport
    farthest = possible_destinations.sort_values(
        "distance_from_milan",
        ascending=False
    ).iloc[0]

    airport_code = farthest["ident"]
    flights = reachable[airport_code]
    print("\nFarthest reachable airport (max 10 stops):")
    print(f"{farthest['name']} ({airport_code})")
    print(f"Country: {farthest['iso_country']}")
    print(f"Distance from Milan: {farthest['distance_from_milan']:.2f} km")
    print(f"Flights: {flights} | Stops: {flights - 1}")
    
    farthest_route = find_route(connections, "LIMC", airport_code)
    if farthest_route is not None:
        print("\nRoute to the farthest airport:")
        print(" -> ".join(farthest_route))
        assert len(farthest_route) - 2 <= 10


    # Vizualizing results
    airport_chart = plot_airport_types(cleaned_airports)

    if route is not None:
        route_chart = plot_flight_route(
            route,
            cleaned_airports,
            "Milan to Sydney - Fewest Stops"
        )

    if fastest_route is not None:
        fastest_chart = plot_flight_route(
            fastest_route,
            cleaned_airports,
            "Milan to Sydney - Fastest Route"
        )

    if travel_time is not None and fastest_time is not None:
        plot_travel_times(travel_time, fastest_time)

    plt.show()


if __name__ == "__main__":
    main()
