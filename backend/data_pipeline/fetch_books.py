import requests
import json
from pathlib import Path

BASE_URL = "https://openlibrary.org/search.json"

FIELDS = [
    "key",
    "title",
    "author_key",
    "author_name",
    "first_publish_year",
    "language",
    "edition_count",
    "cover_i",
    "cover_edition_key",
    "ebook_access",
    "has_fulltext"
]

def fetch_books(query="fantasy",limit = 20):

    params = {
        "q":query,
        "limit":limit,
        "fields":",".join(FIELDS)
    }

    headers = {
        "user-Agent" : "BookVerse/0.1"
    }

    response = requests.get(
        BASE_URL,
        params = params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.json()

def save_raw_data(data, filename="openlibrary_fantasy.json"):

    output_dir = Path("data/raw/openlibrary")
    output_dir.mkdir(parents=True , exist_ok=True)

    output_file = output_dir / filename

    with open(output_file, "w" , encoding="utf-8") as file:

        json.dump(data,file,ensure_ascii= False , indent = 2)

    print(f"Saved data to:{output_file}")


if __name__ == "__main__":

    data = fetch_books("fantasy", limit=20)
    save_raw_data(data)

    print(f"Books fetched: {len(data.get('docs',[]))}")





