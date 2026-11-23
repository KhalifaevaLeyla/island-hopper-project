import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_airport_types(airports):
    """
    Create a bar chart showing the number of airports by type.
    """
    airport_counts = airports["type"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        ["Medium airports", "Large airports"],
        [
            airport_counts.get("medium_airport", 0),
            airport_counts.get("large_airport", 0)
        ],
        color=["steelblue", "darkseagreen"]
    )

    ax.set_title("Airports Available for Our Aircraft")
    ax.set_ylabel("Number of airports")
    fig.tight_layout()
    return fig


def plot_travel_times(min_stops_time, fastest_time):
    """
    Compare the travel time components of two routes.
    """
    categories = ["Flying", "Refuelling", "Customs"]

    min_stops_values = [
        min_stops_time["flying_hours"],
        min_stops_time["refuelling_hours"],
        min_stops_time["customs_hours"]
    ]

    fastest_values = [
        fastest_time["flying_hours"],
        fastest_time["refuelling_hours"],
        fastest_time["customs_hours"]
    ]

    positions = np.arange(len(categories))
    bar_width = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        positions - bar_width / 2,
        min_stops_values,
        bar_width,
        label="Fewest stops",
        color="steelblue"
    )

    ax.bar(
        positions + bar_width / 2,
        fastest_values,
        bar_width,
        label="Fastest route",
        color="darkseagreen"
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_ylabel("Hours")
    ax.set_title("Travel Time Comparison")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_flight_route(route, airports, title):
    """
    Plot airport locations along a selected flight route.
    """
    route_airports = airports.set_index("ident").loc[route]
    latitudes = route_airports["latitude_deg"]
    longitudes = route_airports["longitude_deg"]
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        longitudes,
        latitudes,
        marker="o",
        color="steelblue",
        linewidth=2
    )

    for code, longitude, latitude in zip(
        route,
        longitudes,
        latitudes
    ):
        ax.annotate(
            code,
            (longitude, latitude),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9
        )

    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_route_comparison(route, fastest_route, airports):
    """Compare the two flight routes on the same graph."""

    airport_info = airports.set_index("ident")
    fig, ax = plt.subplots(figsize=(13, 7))

    # Draw the two routes using different colors
    for selected_route, color, label in [
        (route, "steelblue", "Fewest stops"),
        (fastest_route, "darkorange", "Fastest route")
    ]:
        route_airports = airport_info.loc[selected_route]

        ax.plot(
            route_airports["longitude_deg"],
            route_airports["latitude_deg"],
            marker="o",
            linewidth=2,
            color=color,
            label=label
        )

    # Label each airport only once, even if it appears in both routes
    all_codes = list(dict.fromkeys(route + fastest_route))

    for code in all_codes:
        airport = airport_info.loc[code]

        city = airport["municipality"]
        country = airport["iso_country"]

        # Some airports may not have a city in the dataset
        if pd.isna(city):
            city = airport["name"]

        ax.annotate(
            f"{code} - {city}, {country}",
            (airport["longitude_deg"], airport["latitude_deg"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8
        )

    ax.set_title("Milan to Sydney Route Comparison")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()

    return fig



def plot_farthest_route(route, airports):
    """Show the route to the farthest reachable airport."""

    airport_info = airports.set_index("ident")
    route_airports = airport_info.loc[route]
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        route_airports["longitude_deg"],
        route_airports["latitude_deg"],
        marker="o",
        color="darkgreen",
        linewidth=2
    )

    # Show the airport code, city and country at each stop
    for code in route:
        airport = airport_info.loc[code]

        city = airport["municipality"]
        country = airport["iso_country"]

        if pd.isna(city):
            city = airport["name"]

        ax.annotate(
            f"{code} - {city}, {country}",
            (airport["longitude_deg"], airport["latitude_deg"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8
        )

    ax.set_title("Route to the Farthest Reachable Airport")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig
