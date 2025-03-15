#!/usr/bin/env bash

set -euo pipefail

ON_CINEMA_DIR="./on_cinema_at_the_cinema"
DECKER_FILE="./decker/parsed_episodes.json"
ON_CINEMA_PODCAST_FILE="./on_cinema_podcast/podcasts.json"
HEI_NETWORK_NEWS_FILE="./hei_network_news/articles.json"
OUTPUT_FILE="./all_media.json"

LATEST_ON_CINEMA_FILE=$(ls -t "${ON_CINEMA_DIR}"/*.json | head -n 1)

echo "Combining:"
echo "  - ${LATEST_ON_CINEMA_FILE}"
echo "  - ${ON_CINEMA_PODCAST_FILE}"
echo "  - ${DECKER_FILE}"
echo "  - ${HEI_NETWORK_NEWS_FILE}"
echo "→ into ${OUTPUT_FILE}"

jq -s '
  flatten | map({
    media_type: (.media_type // "episode"),
    collection: (.collection // null),
    title: (.episode_title // .article_title // .title // null),
    description: (.episode_description // .description // null),
    date_published: (.aired_at // .posted_at // .date_published // null),
    url: (.episode_url // .article_url // .url // null),
    poster_url: (.poster_url // null),
    show: (.show // null)
  })
' "$LATEST_ON_CINEMA_FILE" "$ON_CINEMA_PODCAST_FILE" "$DECKER_FILE" "$HEI_NETWORK_NEWS_FILE" > "$OUTPUT_FILE"

echo "✅ Done. Clean, unified JSON written to ${OUTPUT_FILE}"
