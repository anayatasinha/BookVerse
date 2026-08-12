import json
import pandas as pd
from pathlib import Path 

RAW_FILE = Path(
    "data/raw/openlibrary/openlibrary_fantasy.json"
)

OUTPUT_FILE = Path(
    "data/processed/openlibrary_fantasy_cleaned.parquet"
)

def load_data():

    """load raw open library json data."""

    with open(RAW_FILE,"r", encoding="utf-8") as file:

        data=json.load(file)

    return data["docs"]

# def create_dataframe(books):

#     """Convert book records into pandas dataframe."""

#     df = pd.DataFrame(books)

#     return df

def clean_data(books):

    """Clean and select required book fileds."""

    df = pd.DataFrame(books)

    # #Keep only columns that currently exist
    # required_columns = [
    #     "title",
    #     "author_name",
    #     "first_publish_year",
    #     "subject",
    #     "language",
    #     "isbn"
    # ]

    # existing_columns = [
    #     column for column in required_columns
    #     if column in df.columns 
    # ]

    # df = df[existing_columns].copy()

    #Rename columns

    df.rename(
        columns = {
            "key": "work_id",
            "author_key": "author_ids",
            "author-name":"authors",
            "first_publish_year":"publication_year",
            "language":"languages",
            "cover_i": "cover_id"
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

    #Remove duplicate 

    # df.drop_duplicates(inplace=True)

    #Reset index
    df.reset_index(drop=True, inplace= True)

    return df

def save_data(df):
    """Save cleaned data"""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_FILE,
        index = False
    )

    print(f"Saved cleaned data to: {OUTPUT_FILE}")


if __name__ == "__main__":

    books = load_data()

    df = clean_data(books)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist)

    print("\nFirst record:")
    print(df.iloc[0])

    save_data(df)
    