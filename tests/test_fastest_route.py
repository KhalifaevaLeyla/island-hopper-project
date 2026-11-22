"""
Check that the fastest route considers customs delays.
"""

import pandas as pd
from functions.flight_routes import find_fastest_route

# Create a network with two possible routes
example_airports = pd.DataFrame({
    "ident": ["AAA", "BBB", "CCC", "DDD"],
    "latitude_deg": [0, 0, 0, 0],
    "longitude_deg": [0, 1, 0.5, 2],
    "iso_country": ["IT", "FR", "IT", "IT"]
})

connections = {
    "AAA": ["BBB", "CCC"],
    "BBB": ["AAA", "DDD"],
    "CCC": ["AAA", "DDD"],
    "DDD": ["BBB", "CCC"]
}

# The route through CCC avoids crossing country borders
route = find_fastest_route(
    connections,
    example_airports,
    "AAA",
    "DDD",
    500,
    1,
    2
)

print("Fastest example route:")
print(route)

assert route == ["AAA", "CCC", "DDD"]

print("Fastest route test passed!")
