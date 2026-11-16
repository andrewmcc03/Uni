import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "ml-latest-small"
OUTPUT_DIR = BASE_DIR / "prepared"
OUTPUT_DIR.mkdir(exist_ok=True)


def read_csv(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


movies_rows = read_csv("movies.csv")
ratings_rows = read_csv("ratings.csv")
tags_rows = read_csv("tags.csv")
links_rows = read_csv("links.csv")

ratings_by_movie = defaultdict(list)
tags_by_movie = defaultdict(list)
links_by_movie = {}

# Prepare embedded rating documents.
for row in ratings_rows:
    movie_id = row["movieId"]
    timestamp = int(row["timestamp"])

    ratings_by_movie[movie_id].append({
        "_id": f'rating_{movie_id}_{row["userId"]}',
        "sourceUserId": int(row["userId"]),
        "rating": float(row["rating"]),
        "date": datetime.fromtimestamp(
            timestamp, timezone.utc
        ).isoformat()
    })

# Prepare embedded tag documents.
for row in tags_rows:
    movie_id = row["movieId"]
    timestamp = int(row["timestamp"])

    tags_by_movie[movie_id].append({
        "_id": f'tag_{movie_id}_{row["userId"]}_{timestamp}',
        "sourceUserId": int(row["userId"]),
        "tag": row["tag"],
        "date": datetime.fromtimestamp(
            timestamp, timezone.utc
        ).isoformat()
    })

# Index external identifiers by movie ID.
for row in links_rows:
    links_by_movie[row["movieId"]] = {
        "imdbId": row["imdbId"] or None,
        "tmdbId": int(row["tmdbId"]) if row["tmdbId"] else None
    }

documents = []

for row in movies_rows:
    movie_id = row["movieId"]
    ratings = ratings_by_movie[movie_id]
    tags = tags_by_movie[movie_id]

    # Extract the year from titles ending in "(YYYY)".
    match = re.search(r"\((\d{4})\)\s*$", row["title"])
    release_year = int(match.group(1)) if match else None

    documents.append({
        "_id": f"movie_{movie_id}",
        "sourceMovieId": int(movie_id),
        "title": row["title"],
        "releaseYear": release_year,
        "genres": [
            genre for genre in row["genres"].split("|")
            if genre and genre != "(no genres listed)"
        ],
        "averageRating": (
            round(sum(r["rating"] for r in ratings) / len(ratings), 2)
            if ratings else None
        ),
        "ratingCount": len(ratings),
        "ratings": ratings,
        "tags": tags,
        "externalIds": links_by_movie.get(movie_id, {
            "imdbId": None,
            "tmdbId": None
        }),
        # User-submitted reviews will be managed by your API.
        "reviews": []
    })

output_file = OUTPUT_DIR / "movies.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(documents, file, ensure_ascii=False, indent=2)

print(f"Movies prepared: {len(documents)}")
print(f"Ratings embedded: {sum(len(m['ratings']) for m in documents)}")
print(f"Tags embedded: {sum(len(m['tags']) for m in documents)}")
print(f"Output written to: {output_file}")