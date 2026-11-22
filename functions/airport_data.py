from pathlib import Path
import pandas as pd

def load_airports():
    """Read the airport dataset and return it as a DataFrame."""
    project_folder = Path(__file__).resolve().parent.parent
    file_path = project_folder / "data" / "airports.csv"

    try:
        airports = pd.read_csv(file_path)
        return airports

    except FileNotFoundError:
        print("Airport data file was not found.")
        print("Check that airports.csv is inside the data folder.")
        return None

    except pd.errors.EmptyDataError:
        print("The airport data file is empty.")
        return None


def clean_airports(airports):
    """
    Keep airports that can be used in our flight calculations.
    Only medium and large airports with valid coordinates are included.
    """
    allowed_types = ["medium_airport", "large_airport"]

    cleaned = airports[airports["type"].isin(allowed_types)].copy()

    # Remove airports without coordinates or country information
    cleaned = cleaned.dropna(
        subset=["latitude_deg", "longitude_deg", "iso_country"]
    )

    # Remove coordinates outside the possible geographic range
    cleaned = cleaned[cleaned["latitude_deg"].between(-90, 90)& cleaned["longitude_deg"].between(-180, 180)]

    # Remove duplicate airport identifiers
    cleaned = cleaned.drop_duplicates(subset="ident")

    return cleaned
