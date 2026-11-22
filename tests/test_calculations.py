"""
Tests for distance and travel time calculations.
"""

import pandas as pd
from functions.calculations import calculate_distance, calculate_travel_time

# The distance between identical coordinates should be zero
assert calculate_distance(45.63, 8.73, 45.63, 8.73) == 0

# A distance should be the same in both directions
distance_a = calculate_distance(45.63, 8.73, -33.95, 151.18)
distance_b = calculate_distance(-33.95, 151.18, 45.63, 8.73)
assert abs(distance_a - distance_b) < 0.001
print("Distance calculation tests passed!")


# Example to test travel time calculations
example_airports = pd.DataFrame({
    "ident": ["AAA", "BBB", "CCC"],
    "latitude_deg": [0, 0, 0],
    "longitude_deg": [0, 1, 2],
    "iso_country": ["IT", "IT", "FR"]
})

example_route = ["AAA", "BBB", "CCC"]
result = calculate_travel_time(
    example_route,
    example_airports,
    flight_speed_kmh=500,
    refuel_time_hours=1,
    customs_time_hours=2
)

# Two flights, one refuelling stop and one border crossing
assert result["refuelling_hours"] == 1
assert result["customs_hours"] == 2

# Check that the total is the sum of all components
expected_total = (
    result["flying_hours"]
    + result["refuelling_hours"]
    + result["customs_hours"]
)

assert abs(result["total_hours"] - expected_total) < 0.001
print("Travel time tests passed!")