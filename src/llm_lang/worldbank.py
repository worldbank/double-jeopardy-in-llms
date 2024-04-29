import httpx
import pandas as pd


def fetch_gdp_per_capita(country_code, year=2022):
    """
    Fetches the GDP per capita for a given country and year.

    Parameters
    ----------
    country_code : str
        The ISO-3166-1 alpha-3 country code.
    year : int, optional
        The year for which GDP per capita is to be fetched. Defaults to 2022.

    Returns
    -------
    float or None
        The GDP per capita value for the specified country and year, or None if data is not available.
    """
    base_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.PCAP.CD?date={year}&format=json"

    with httpx.Client() as client:
        response = client.get(base_url)

        if response.status_code == 200:
            data = response.json()
            # The API returns an array with metadata and data. We want the data.
            try:
                gdp_data = data[1][0] if data[1] else None
                if gdp_data:
                    gdp_value = gdp_data["value"]
                    return gdp_value
            except IndexError:
                return pd.NA
