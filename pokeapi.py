# Reflection Questions:
#
# 1. Which API did I choose and why?
# I chose the PokéAPI (https://pokeapi.co) because it is publicly accessible, does not require an API key,
# and provides structured JSON data that is easy to work with using Python and Pandas.

# 2. What challenges did I encounter while working with the API?
# One challenge was navigating nested JSON data such as Pokémon types and abilities.
# Another challenge was making sure API requests were not sent too quickly.

# 3. How did I overcome these challenges?
# I inspected the JSON responses to understand their structure and extracted only the fields I needed.
# I also added a short delay between requests to respect API rate limits.

# 4. What did I learn about making API requests and handling JSON data?
# I learned how to use Python’s requests library to make API calls, parse JSON responses,
# and organize API data into a Pandas DataFrame for analysis and storage.


import time
import requests
import pandas as pd
from urllib.parse import urljoin

# Base URL for the PokéAPI
BASE_URL = "https://pokeapi.co/api/v2/"

# Endpoint for retrieving Pokémon listings
POKEMON_ENDPOINT = urljoin(BASE_URL, "pokemon/")


# Sends a GET request and returns parsed JSON data
def fetch_json(url, params=None):
    headers = {"User-Agent": "CMCC-API-Assignment/1.0"}
    response = requests.get(url, headers=headers, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


# Extracts and flattens relevant Pokémon fields from the API response
def parse_pokemon_details(details):
    types = [t["type"]["name"] for t in details.get("types", [])]
    abilities = [a["ability"]["name"] for a in details.get("abilities", [])]

    return {
        "id": details.get("id"),
        "name": details.get("name"),
        "height_dm": details.get("height"),
        "weight_hg": details.get("weight"),
        "base_experience": details.get("base_experience"),
        "types": ", ".join(types),
        "abilities": ", ".join(abilities),
    }


# Retrieves Pokémon data and stores it in a Pandas DataFrame
def scrape_pokemon(limit=60, offset=0):
    rows = []

    # Get a list of Pokémon names and URLs
    listing = fetch_json(POKEMON_ENDPOINT, {"limit": limit, "offset": offset})
    results = listing.get("results", [])

    for index, pokemon in enumerate(results, start=1):
        name = pokemon.get("name")
        url = pokemon.get("url")

        try:
            details = fetch_json(url)
            rows.append(parse_pokemon_details(details))
        except Exception as e:
            print(f"Error fetching {name}: {repr(e)}")

        # Delay between requests to respect API usage limits
        time.sleep(0.2)

    return pd.DataFrame(rows)


# Main execution function
def main():
    # Number of Pokémon to retrieve
    LIMIT = 150

    # Fetch Pokémon data
    df = scrape_pokemon(limit=LIMIT)

    # Display a preview of the data
    print("Data Preview:")
    print(df.head(15))

    # Basic summary output
    print("\nTotal Pokémon Retrieved:", len(df))
    print("Average Base Experience:", round(df["base_experience"].dropna().mean(), 2))

    # Save data to CSV
    output_file = "pokemon_api_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved {len(df)} rows to {output_file}")


# Ensures the script runs only when executed directly
if __name__ == "__main__":
    main()
