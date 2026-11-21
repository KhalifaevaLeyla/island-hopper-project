"""
Island Hopper

A project to explore how far a plane can travel when its flight range is limited.

Starting point is Milan Malpensa Airport, Italy.
Main destination is Sydney Airport, Australia.
"""

from functions.airport_data import load_airports, clean_airports

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


if __name__ == "__main__":
    main()
