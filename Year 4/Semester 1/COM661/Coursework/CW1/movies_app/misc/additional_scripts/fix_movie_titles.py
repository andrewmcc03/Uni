import json
import re

input_file = "movies.json"
output_file = "movies_fixed.json"

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