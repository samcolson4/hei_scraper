#!/usr/bin/env bash

set -euo pipefail

ON_CINEMA_DIR="./on_cinema_at_the_cinema"
DECKER_FILE="./decker/parsed_episodes.json"
ON_CINEMA_PODCAST_FILE="./on_cinema_podcast/podcasts.json"
OUTPUT_FILE="./all_media.json"

# Find most recently modified JSON file in on_cinema
LATEST_ON_CINEMA_FILE=$(ls -t "${ON_CINEMA_DIR}"/*.json | head -n 1)

echo "Combining:"
echo "  - ${LATEST_ON_CINEMA_FILE}"
echo "  - ${ON_CINEMA_PODCAST_FILE}"
echo "  - ${DECKER_FILE}"
echo "→ into ${OUTPUT_FILE}"

# Combine the two arrays into one
jq -s 'add' "$LATEST_ON_CINEMA_FILE" "$ON_CINEMA_PODCAST_FILE" "$DECKER_FILE" > "$OUTPUT_FILE"

echo "✅ Done. Combined JSON written to ${OUTPUT_FILE}"
