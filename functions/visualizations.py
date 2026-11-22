import matplotlib.pyplot as plt
import numpy as np

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
