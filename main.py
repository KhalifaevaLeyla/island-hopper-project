
"""
Island Hopper

A project to explore how far a plane can travel when its flight range is limited.

Starting point is Milan Malpensa Airport, Italy.
Main destination is Sydney Airport, Australia.
"""

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
    """Run the Island Hopper program."""
    show_trip_details()


if __name__ == "__main__":
    main()
