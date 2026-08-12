import json
import pandas as pd
from pathlib import Path 

RAW_FILE = Path(
    "data/raw/openlibrary/openlibrary_fantasy.json"
)

OUTPUT_FILE = Path(
    "data/processed/openlibrary_fantasy_cleaned.csv"
)

def load_data():

    """load raw open library json data."""

    with open(RAW_FILE,"r", encoding="utf-8") as file:

        data=json.load(file)

    return data["docs"]

def create_dataframe(books):

    """Convert book records into pandas dataframe."""

    df = pd.DataFrame(books)

    return df

def clean_data(df):

    """Clean and select required book fileds."""

    #Keep only columns that currently exist
    required_columns = [
        "title",
        "author_name",
        "first_publish_year",
        "subject",
        "language",
        "isbn"
    ]

    existing_columns = [
        column for column in required_columns
        if column in df.columns 
    ]

    df = df[existing_columns].copy()

    #Rename columns

    df.rename(
        columns = {
            "author-name":"authors",
            "first_publish_year":"publication_year",
            "subject":"subjects",
            "language":"languages"
        },
        inplace = True
    )

    #remove books without title

    df.dropna(
        subset = ["title"],
        inplace = True
    )

    #Clean title
    df["title"]=(
        df["title"].astype(str).str.strip()
    )

    #Remove duplicate title or this initial experimet

    df.drop_duplicates(
        subset=["title"],
        inplace = True
    )

    #Reset index
    df.reset_index(drop=True, inplace= True)

    return df

def save_data(df):
    """Save cleaned data"""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index = False
    )

    print(f"Saved cleaned data to: {OUTPUT_FILE}")


if __name__ == "__main__":

    books = load_data()

    print(f"Raw books : {len(books)}")

    df = create_dataframe(books)

    print(f"Initial DataFrame shape {df.shape}")

    df = clean_data(df)

    print(f"Cleaned Dataframe shape : {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 books:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    save_data(df)
    