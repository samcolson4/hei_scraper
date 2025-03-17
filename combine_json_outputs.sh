#!/usr/bin/env bash

set -euo pipefail

ON_CINEMA_DIR="./on_cinema_at_the_cinema"
HEI_NETWORK_NEWS_DIR="./hei_network_news"
DECKER_FILE="./decker/parsed_episodes.json"
ON_CINEMA_PODCAST_FILE="./on_cinema_podcast/podcasts.json"
EPHEMERA_FILE="./ephemera.json"
OUTPUT_FILE="./all_media.json"

LATEST_ON_CINEMA_FILE=$(ls -t "${ON_CINEMA_DIR}"/*.json | head -n 1)
LATEST_HEI_NETWORK_NEWS_FILE=$(ls -t "${HEI_NETWORK_NEWS_DIR}"/*.json | head -n 1)

echo "Combining:"
echo "  - ${LATEST_ON_CINEMA_FILE}"
echo "  - ${ON_CINEMA_PODCAST_FILE}"
echo "  - ${DECKER_FILE}"
echo "  - ${LATEST_HEI_NETWORK_NEWS_FILE}"
echo "  - ${EPHEMERA_FILE}"
echo "→ into ${OUTPUT_FILE}"

jq -s 'add' "$LATEST_ON_CINEMA_FILE" "$ON_CINEMA_PODCAST_FILE" "$DECKER_FILE" "$LATEST_HEI_NETWORK_NEWS_FILE" "$EPHEMERA_FILE" > "$OUTPUT_FILE"

echo "✅ Done. Combined JSON written to ${OUTPUT_FILE}"

COUNT=$(jq length "$OUTPUT_FILE")
sed -i '' "/<!-- DATA_COUNT_START -->/,/<!-- DATA_COUNT_END -->/c\\
<!-- DATA_COUNT_START -->\\
On Cinema At The Cinema item count: ${COUNT}\\
<!-- DATA_COUNT_END -->
" README.md
