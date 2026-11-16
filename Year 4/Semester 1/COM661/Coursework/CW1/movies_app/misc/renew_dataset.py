from pymongo import MongoClient
import bcrypt
import subprocess # for cmd commands (for mongosh)
from pathlib import Path # for cmd commands (for mongosh)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.moviesDB  # select moviesDB database
movies = db.movies    # movies collection
users = db.users      # select users collection (in moviesDB)
blacklist = db.blacklist

### WARNING - WIPES ALL COLLECTIONS IN moviesDB and re-generates & re-enters dataset

# pre-warn
warnConfirm = input(str("\n**WARNING**: This will drop all collections and renew the dataset. Do you wish to continue [y/n]? "))
if warnConfirm != "y":
    print("\nExiting...\n")
    exit()


#########################################################################################################
#########################################################################################################
#########################################################################################################

### DROP COLLECTIONS BEFORE RE-ADDING (CLEAR ALL)
movies.drop()
users.drop()
blacklist.drop()

### create users
user_list = [
          {
            "name" : "Andrew",
            "username" : "andrew",  
            "password" : b"andrewpw",
            "email" : "andrew@email.com",
            "admin" : True
          },
          {
            "name" : "Standard User",
            "username" : "standarduser",  
            "password" : b"standardpw",
            "email" : "standarduser@email.com",
            "admin" : False
          },
          {
            "name" : "Alternate User",
            "username" : "altuser",  
            "password" : b"alternatepw",
            "email" : "alternateuser@email.com",
            "admin" : False
          }
       ]

for new_user in user_list:
      new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
      users.insert_one(new_user)


### import movies

# prep_dataset_new.py (02-11-26)
import csv
import random
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS


# --------------------------------------------------
# File locations and settings
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "ml-latest-small"
OUTPUT_DIR = BASE_DIR #/ "prepared" # commented out as no longer needed 'prepared' folder

MOVIES_FILE = DATA_DIR / "movies.csv"
RATINGS_FILE = DATA_DIR / "ratings.csv"
TAGS_FILE = DATA_DIR / "tags.csv"
LINKS_FILE = DATA_DIR / "links.csv"

OUTPUT_FILE = OUTPUT_DIR.parent / "movies.json"

MOVIE_LIMIT = 500

# profit range
MIN_PROFIT = 1_000_000
MAX_PROFIT = 500_000_000

PRIOR_RATING = 3.5
PRIOR_COUNT = 20


# --------------------------------------------------
# Generated reviewer names and comments
# --------------------------------------------------

FIRST_NAMES = [
    "Alex", "Sam", "Jordan", "Taylor", "Morgan",
    "Jamie", "Charlie", "Riley", "Casey", "Drew",
    "Emily", "Oliver", "Sophie", "Harry", "Amelia",
    "Jack", "Grace", "Daniel", "Ella", "Thomas"
]

LAST_NAMES = [
    "Morgan", "Taylor", "Wilson", "Bennett", "Parker",
    "Thompson", "Reed", "Foster", "Brooks", "Hayes",
    "Mitchell", "Cooper", "Ward", "Bailey", "Collins"
]

COMMENTS = {
    "high": [
        "A fantastic film with a memorable story and excellent performances.",
        "Really enjoyed this one. The characters and storyline were brilliant.",
        "An entertaining film that I would happily watch again.",
        "Excellent from beginning to end. Definitely worth watching.",
        "A great film with plenty of memorable moments."
    ],

    "medium": [
        "An enjoyable film, although some parts could have been better developed.",
        "A decent watch with some interesting moments.",
        "I enjoyed parts of this film, but it was not particularly memorable.",
        "A solid film, although I expected a little more from it.",
        "Good overall, but there were a few things that could have been improved."
    ],

    "low": [
        "It had some interesting moments, but overall it wasn't quite what I expected.",
        "I struggled to stay interested and found the storyline disappointing.",
        "Not a particularly enjoyable film, although it had some potential.",
        "The film was below my expectations and could have been much better.",
        "Some good ideas, but the overall execution was disappointing."
    ]
}

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def read_csv(filename):
    """Read a CSV file and return a list of dictionaries."""
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def extract_title_and_year(original_title):
    """Extract the movie title and year from a MovieLens title."""
    match = re.match(r"^(.*?)\s*\((\d{4})\)\s*$", original_title)

    if match:
        return match.group(1).strip(), int(match.group(2))

    return original_title.strip(), None


def timestamp_to_datetime(timestamp):
    """Convert a Unix timestamp into a UTC datetime."""
    return datetime.fromtimestamp(
        int(timestamp),
        tz=timezone.utc
    )


def optional_int(value):
    """Convert a non-empty value into an integer."""
    if not value or not value.strip():
        return None

    return int(value)


def generate_reviewer_name(source_user_id):
    """Generate a consistent fictional name for each source user."""
    rng = random.Random(source_user_id)

    first_name = rng.choice(FIRST_NAMES)
    last_name = rng.choice(LAST_NAMES)

    return f"{first_name} {last_name}"


def generate_review_comment(rating, rng):
    """Choose a comment appropriate to the review rating."""

    if rating >= 4.0:
        category = "high"
    elif rating >= 2.5:
        category = "medium"
    else:
        category = "low"

    return rng.choice(COMMENTS[category])


def calculate_weighted_rating(average_rating, rating_count, overall_average):
    """Calculate a weighted rating using a prior average."""

    numerator = (
        average_rating * rating_count
        + overall_average * PRIOR_COUNT
    )

    denominator = rating_count + PRIOR_COUNT

    return round(numerator / denominator, 2)


def generate_profit(movie_id):
    """
    Generate repeatable synthetic profit.

    Values are in USD and are not real financial figures.
    """
    rng = random.Random(1000 + movie_id)

    return rng.randint(MIN_PROFIT, MAX_PROFIT)


# --------------------------------------------------
# Load source CSV files
# --------------------------------------------------

print("\n1 - Compiling and generating dataset...")
print("Reading MovieLens CSV files...")

movie_rows = read_csv(MOVIES_FILE)
rating_rows = read_csv(RATINGS_FILE)
tag_rows = read_csv(TAGS_FILE)
link_rows = read_csv(LINKS_FILE)


# --------------------------------------------------
# Select movies
# --------------------------------------------------

movie_rows.sort(key=lambda row: int(row["movieId"]))

selected_movies = movie_rows[:MOVIE_LIMIT]

selected_movie_ids = {
    int(movie["movieId"]) for movie in selected_movies
}

print(f"Selected {len(selected_movies)} movies.")


# --------------------------------------------------
# Group ratings and convert them into reviews
# --------------------------------------------------

reviews_by_movie = defaultdict(list)

for row in rating_rows:

    movie_id = int(row["movieId"])

    if movie_id not in selected_movie_ids:
        continue

    source_user_id = int(row["userId"])

    # MovieLens ratings can start at 0.5.
    # Ensure imported review ratings are within 1-5.
    rating = max(1.0, float(row["rating"]))

    # Consistent comment generation for each source rating.
    rng = random.Random(movie_id * 100000 + source_user_id)

    # reviewer username generator
    reviewer_name = generate_reviewer_name(source_user_id)

    username_base = re.sub(
        r"[^a-z0-9]",
        "",
        reviewer_name.lower()
    )

    username_rng = random.Random(source_user_id + 50000)
    username = f"{username_base}{username_rng.randint(10, 9999)}"

    review = {
        "_id": ObjectId(),
        "sourceUserId": source_user_id,
        "name": reviewer_name,
        "username": username,
        "comment": generate_review_comment(rating, rng),
        "rating": rating,
        "createdAt": timestamp_to_datetime(row["timestamp"]).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    reviews_by_movie[movie_id].append(review)


# --------------------------------------------------
# Group tags by movie
# --------------------------------------------------

tags_by_movie = defaultdict(list)

for row in tag_rows:

    movie_id = int(row["movieId"])

    if movie_id not in selected_movie_ids:
        continue

    source_user_id = int(row["userId"])

    # Generate consistent fictional name for each source user.
    tagger_name = generate_reviewer_name(source_user_id)

    # Generate consistent username for each source user.
    username_base = re.sub(
        r"[^a-z0-9]",
        "",
        tagger_name.lower()
    )

    username_rng = random.Random(source_user_id + 50000)
    username = f"{username_base}{username_rng.randint(10, 9999)}"

    tags_by_movie[movie_id].append({
        "_id": ObjectId(),
        "sourceUserId": source_user_id,
        "name": tagger_name,
        "username": username,
        "tag": row["tag"].strip(),
        "createdAt": timestamp_to_datetime(row["timestamp"]).strftime("%Y-%m-%dT%H:%M:%SZ")
    })


# --------------------------------------------------
# Link external movie identifiers
# --------------------------------------------------

links_by_movie = {}

for row in link_rows:

    movie_id = int(row["movieId"])

    if movie_id not in selected_movie_ids:
        continue

    external_ids = {}

    imdb_id = row.get("imdbId", "").strip()
    tmdb_id = row.get("tmdbId", "").strip()

    if imdb_id:
        external_ids["imdbId"] = imdb_id

    if tmdb_id:
        external_ids["tmdbId"] = optional_int(tmdb_id)

    links_by_movie[movie_id] = external_ids


# --------------------------------------------------
# Calculate overall average review rating
# --------------------------------------------------

all_ratings = [
    review["rating"]
    for movie_reviews in reviews_by_movie.values()
    for review in movie_reviews
]

if all_ratings:
    overall_average = sum(all_ratings) / len(all_ratings)
else:
    overall_average = PRIOR_RATING


# --------------------------------------------------
# Build movie documents
# --------------------------------------------------

movies = []

for row in selected_movies:

    movie_id = int(row["movieId"])

    title, release_year = extract_title_and_year(row["title"])

    movie_reviews = reviews_by_movie[movie_id]
    movie_tags = tags_by_movie[movie_id]

    review_count = len(movie_reviews)

    if review_count > 0:
        average_rating = sum(
            review["rating"] for review in movie_reviews
        ) / review_count
    else:
        average_rating = 0.0

    weighted_rating = calculate_weighted_rating(
        average_rating,
        review_count,
        overall_average
    )

    genres = [
        genre
        for genre in row["genres"].split("|")
        if genre and genre != "(no genres listed)"
    ]

    movie_document = {
        "_id": ObjectId(),

        "sourceMovieId": movie_id,
        "title": title,
        "releaseYear": release_year,
        "genres": genres,

        # Synthetic financial data.
        "grossProfits": generate_profit(movie_id),

        # Rating statistics calculated from embedded reviews.
        "averageRating": round(average_rating, 2),
        "weightedRating": weighted_rating,
        "reviewCount": review_count,

        "tagCount": len(movie_tags),

        # Embedded reviews and tags.
        "reviews": movie_reviews,
        "tags": movie_tags,

        # External database identifiers.
        "externalIds": links_by_movie.get(movie_id, {})
    }

    movies.append(movie_document)


# --------------------------------------------------
# Export as MongoDB Extended JSON
# --------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write(
        dumps(
            movies,
            json_options=RELAXED_JSON_OPTIONS,
            indent=2
        )
    )

print()
print(f"Successfully prepared {len(movies)} movie documents.")
print(f"Total embedded reviews: {sum(len(m['reviews']) for m in movies)}")
print(f"Total embedded tags: {sum(len(m['tags']) for m in movies)}")
print(f"Output saved to: {OUTPUT_FILE}")

print()


### fix titles

import json
import re

input_file = BASE_DIR.parent / "movies.json"
#output_file = "movies_fixed.json"
output_file = BASE_DIR.parent / "movies.json"

print("2 - Fixing movie titles...")

with open(input_file, "r", encoding="utf-8") as f:
    movies = json.load(f)

fixed_count = 0

for movie in movies:
    title = movie.get("title", "")

    # Move ", The", ", A", or ", An" to the beginning
    match = re.match(r"^(.*),\s+(The|A|An)(\s*\(.*)?$", title, re.IGNORECASE)

    if match:
        movie["title"] = (
            match.group(2) + " " +
            match.group(1) +
            (match.group(3) or "")
        ).strip()

        fixed_count += 1

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(movies, f, indent=2, ensure_ascii=False)

print(f"Finished! Fixed {fixed_count} movie titles.")

print()


### mongosh import

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR.parent / "movies.json"

print("3 - Importing movies into moviesDB...")

command = [
    "mongoimport",
    "--db", "moviesDB",
    "--collection", "movies",
    "--file", str(JSON_FILE),
    "--jsonArray"
]

try:
    subprocess.run(command, check=True)

    print("\nSuccessfully imported movies into MongoDB!\n")

except subprocess.CalledProcessError as error:
    print(f"\nMongoDB import failed: {error}\n")

except FileNotFoundError:
    print("\nError: mongoimport could not be found. Check that MongoDB Database Tools are installed.\n")