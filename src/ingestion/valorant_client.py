"""
valorant_client.py

Thin wrapper around HenrikDev's unofficial Valorant API
(https://docs.henrikdev.xyz/valorant).

Why not Riot's API directly? Riot explicitly does not offer personal API
keys for Valorant (confirmed directly on their product registration form:
"We do not offer personal API keys for VALORANT.") - match data requires a
Production API key, which needs a working demo and a review process, and
additionally gates most player data behind RSO (Riot Sign On) consent.

HenrikDev's API is a well-known, actively maintained community wrapper
around the same underlying Valorant data, free to use with a Discord-issued
key, and doesn't require Riot's production approval process. This is a
documented, deliberate architectural decision - see docs/tech-stack.md.
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HENRIKDEV_API_KEY = os.getenv("HENRIKDEV_API_KEY")
GAME_NAME = os.getenv("RIOT_GAME_NAME")
TAG_LINE = os.getenv("RIOT_TAG_LINE")
REGION = os.getenv("RIOT_REGION", "ap")  # ap | na | eu | kr | latam | br

BASE_URL = "https://api.henrikdev.xyz"


class ValorantAPIError(Exception):
    """Raised when the HenrikDev API returns a non-recoverable error."""
    pass


def _headers():
    if not HENRIKDEV_API_KEY:
        raise ValorantAPIError(
            "HENRIKDEV_API_KEY not set. Check src/ingestion/.env exists and "
            "has a valid key from the HenrikDev Discord dashboard."
        )
    return {"Authorization": HENRIKDEV_API_KEY}


def _get(url: str, max_retries: int = 3) -> dict:
    """GET with basic rate-limit backoff."""
    for attempt in range(1, max_retries + 1):
        response = requests.get(url, headers=_headers())

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            wait_seconds = int(response.headers.get("Retry-After", 5))
            print(f"  Rate limited. Waiting {wait_seconds}s (attempt {attempt}/{max_retries})...")
            time.sleep(wait_seconds)
            continue

        if response.status_code == 401:
            raise ValorantAPIError(
                "401 Unauthorized - check HENRIKDEV_API_KEY in .env is correct."
            )

        if response.status_code == 404:
            raise ValorantAPIError(
                f"404 Not Found for {url} - check Riot ID / region are correct."
            )

        raise ValorantAPIError(f"Unexpected status {response.status_code} for {url}: {response.text}")

    raise ValorantAPIError(f"Gave up after {max_retries} retries on {url}")


def get_matches(
    game_name: str = GAME_NAME,
    tag_line: str = TAG_LINE,
    region: str = REGION,
    platform: str = "pc",
) -> list[dict]:
    """
    Fetch recent match history (with full match details already included -
    HenrikDev's v4 matches endpoint returns full data per match, so unlike
    Riot's raw API, there's no separate "get match IDs, then fetch each one"
    step needed here).
    """
    url = f"{BASE_URL}/valorant/v4/matches/{region}/{platform}/{game_name}/{tag_line}"
    data = _get(url)
    return data.get("data", [])
