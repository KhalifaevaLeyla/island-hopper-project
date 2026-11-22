
"""
Check that flights can be added in both directions by using created add_connection function.
"""
from functions.flight_routes import add_connection, find_route, find_airports_within_stops

connections = {}

add_connection(connections, "LIMC", "airport_a")
add_connection(connections, "airport_a", "airport_b")
add_connection(connections, "airport_b", "YSSY")

print("Our example connections:")
print(connections)

# Check that connections work in both directions
assert "airport_a" in connections["LIMC"]
assert "LIMC" in connections["airport_a"]

# Check that duplicate connections are not added
add_connection(connections, "LIMC", "airport_a")
assert connections["LIMC"].count("airport_a") == 1

print("All connection checks passed!")

# Test the route search using our example airports
shortest_route = find_route(connections, "LIMC", "YSSY")

print("\nRoute found:")
print(shortest_route)

assert shortest_route == ["LIMC", "airport_a", "airport_b", "YSSY"]

# Test a destination that does not exist
assert find_route(connections, "LIMC", "unknown") is None

# Test a journey starting and ending at the same airport
assert find_route(connections, "LIMC", "LIMC") == ["LIMC"]

print("All route tests passed!")


# Check how far we can travel with one intermediate stop
reachable = find_airports_within_stops(connections, "LIMC", 1)

assert reachable["LIMC"] == 0
assert reachable["airport_a"] == 1
assert reachable["airport_b"] == 2
assert "YSSY" not in reachable

print("Stop limit tests passed!")



