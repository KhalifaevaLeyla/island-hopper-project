"""
Island Hopper App
An interactive application for exploring flight routes with different aircraft settings.
"""

import matplotlib.pyplot as plt
import streamlit as st
from functions.airport_data import load_airports, clean_airports
from functions.calculations import calculate_distance, calculate_travel_time
from functions.flight_routes import build_connections, find_route, find_fastest_route, find_airports_within_stops
from functions.visualizations import plot_travel_times, plot_farthest_route, plot_route_comparison

st.set_page_config(
    page_title="Island Hopper",
    layout="wide"
)
st.title("Island Hopper")
st.write(
    "Explore possible flight routes around the world "
    "with a small aircraft that can only use medium and large airports."
)

# Aircraft settings 
flight_speed_kmh = 500
refuel_time_hours = 1
max_stops = 10
destination_code = "YSSY"

# Aircraft settings that can be chosen
st.sidebar.header("Aircraft settings")
max_range_km = st.sidebar.slider(
    "Maximum flight range (km)",
    min_value=500,
    max_value=6000,
    value=3000,
    step=250
)

customs_time_hours = st.sidebar.number_input(
    "Customs time (hours)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5
)

st.sidebar.write(f"Flying speed: {flight_speed_kmh} km/h")
st.sidebar.write(f"Refuelling time: {refuel_time_hours} hour")
st.sidebar.write(f"Maximum intermediate stops: {max_stops}")


@st.cache_data # lets Streamlit reuse previously calculated results
def get_airports():
    """Load and clean the airport data once."""
    airports = load_airports()

    if airports is None:
        return None, None

    cleaned_airports = clean_airports(airports)

    return airports, cleaned_airports


@st.cache_data(show_spinner=False)
def get_connections(max_range_km):
    """Build the airport network for the selected flight range."""
    _, cleaned_airports = get_airports()

    return build_connections(cleaned_airports, max_range_km)


# Load the airport dataset
airports, cleaned_airports = get_airports()

if cleaned_airports is None:
    st.error("Could not load the airport data.")
    st.stop()

# Airport settings that can be chosen
airport_options = cleaned_airports.sort_values("name")
airport_codes = airport_options["ident"].tolist()

airport_names = dict(
    zip(
        airport_options["ident"],
        airport_options["name"]
    )
)

start_code = st.selectbox(
    "Starting airport",
    airport_codes,
    index=airport_codes.index("LIMC"),
    format_func=lambda code: f"{airport_names[code]} ({code})"
)


# Show the selected journey
st.subheader("Plan a journey")
st.write(f"Starting airport: {airport_names[start_code]} ({start_code})")
st.write("Destination: Sydney Kingsford Smith International Airport (YSSY)")

# Show dataset information
st.subheader("Airport dataset")
st.metric("Total airports", len(airports))
st.metric("Available airports", len(cleaned_airports))

# Run calculations whith button
if st.button("Find flight routes"):
    connections = get_connections(max_range_km)
    start = cleaned_airports[cleaned_airports["ident"] == start_code].iloc[0]
    destination = cleaned_airports[cleaned_airports["ident"] == destination_code].iloc[0]

    direct_distance = calculate_distance(
        start["latitude_deg"],
        start["longitude_deg"],
        destination["latitude_deg"],
        destination["longitude_deg"]
    )

    # Route with the fewest stops
    route = find_route(
        connections,
        start_code,
        destination_code
    )

    # Route with the shortest travel time
    fastest_route = find_fastest_route(
        connections,
        cleaned_airports,
        start_code,
        destination_code,
        flight_speed_kmh,
        refuel_time_hours,
        customs_time_hours
    )

    # Airports reachable within 10 stops
    reachable = find_airports_within_stops(
        connections,
        start_code,
        max_stops
    )

    # Show the results for Sydney
    st.subheader("Journey to Sydney")

    st.write(
        f"Direct distance to Sydney: {direct_distance:,.2f} km"
    )

    if direct_distance <= max_range_km:
        st.success("Sydney can be reached with a direct flight.")
    elif route is not None:
        st.success("Sydney can be reached with intermediate stops.")
    else:
        st.warning("Sydney cannot be reached with this aircraft range.")

    travel_time = None
    fastest_time = None

    # Route with the fewest stops
    if route is not None:
        travel_time = calculate_travel_time(
            route,
            cleaned_airports,
            flight_speed_kmh,
            refuel_time_hours,
            customs_time_hours
        )

        st.subheader("Route with the fewest stops")
        st.write(" -> ".join(route))

        st.metric("Flights", len(route) - 1)
        st.metric("Intermediate stops", max(0, len(route) - 2))
        st.metric(
            "Travel time",
            f"{travel_time['total_hours']:.2f} hours"
        )

    # Fastest route
    if fastest_route is not None:
        fastest_time = calculate_travel_time(
            fastest_route,
            cleaned_airports,
            flight_speed_kmh,
            refuel_time_hours,
            customs_time_hours
        )

        st.subheader("Fastest route")
        st.write(" -> ".join(fastest_route))

        st.metric("Flights", len(fastest_route) - 1)
        st.metric(
            "Intermediate stops",
            max(0, len(fastest_route) - 2)
        )
        st.metric(
            "Travel time",
            f"{fastest_time['total_hours']:.2f} hours"
        )
    
    # Show both routes together
    if route is not None and fastest_route is not None:
        st.subheader("Flight route comparison")

        fig = plot_route_comparison(
            route,
            fastest_route,
            cleaned_airports
        )

        st.pyplot(fig)
        plt.close(fig)


    # Compare the travel times
    if travel_time is not None and fastest_time is not None:
        st.subheader("Travel time comparison")

        fig = plot_travel_times(travel_time, fastest_time)

        st.pyplot(fig)
        plt.close(fig)

    # Find the farthest reachable airport
    st.subheader("Farthest reachable airport")

    possible_destinations = cleaned_airports[cleaned_airports["ident"].isin(reachable) & (cleaned_airports["ident"] != start_code)].copy()

    if possible_destinations.empty:
        st.warning("No other airports can be reached.")
    else:
        # Compare direct distances from the starting airport
        possible_destinations["distance_from_start"] = calculate_distance(
            start["latitude_deg"],
            start["longitude_deg"],
            possible_destinations["latitude_deg"].to_numpy(),
            possible_destinations["longitude_deg"].to_numpy()
        )

        farthest = possible_destinations.sort_values(
            "distance_from_start",
            ascending=False
        ).iloc[0]

        farthest_code = farthest["ident"]
        flights_needed = reachable[farthest_code]

        st.write(f"Airport: {farthest['name']} ({farthest_code})")
        st.write(f"Country: {farthest['iso_country']}")

        st.metric(
            "Direct distance",
            f"{farthest['distance_from_start']:,.2f} km"
        )

        st.metric(
            "Intermediate stops",
            flights_needed - 1
        )

        farthest_route = find_route(
            connections,
            start_code,
            farthest_code
        )

    if farthest_route is not None:
            st.write("Route:")
            st.write(" -> ".join(farthest_route))

            fig = plot_farthest_route(
                farthest_route,
                cleaned_airports
            )

            st.pyplot(fig)
            plt.close(fig)