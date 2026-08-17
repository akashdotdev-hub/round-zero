"""
riot_client.py

Thin wrapper around Riot's Valorant APIs.

Riot splits routing into two different schemes, and this trips people up
constantly, so it's worth being explicit about it here:

  - Account API (get PUUID from Riot ID) uses BROAD "continent" routing:
      americas | asia | europe
  - Match API (match history, match details) uses the SPECIFIC shard:
      ap | na | eu | kr | latam | br  (etc.)

Mumbai / India players are on the "ap" shard, and "ap" falls under the
"asia" continent for Account API purposes.

Docs: https://developer.riotgames.com/apis
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
GAME_NAME = os.getenv("RIOT_GAME_NAME")
TAG_LINE = os.getenv("RIOT_TAG_LINE")
REGION = os.getenv("RIOT_REGION", "ap")  # match API shard

# Account API continent for a given match-api region.
# Extend this map as needed if you ever support other shards.
_CONTINENT_FOR_REGION = {
    "ap": "asia",
    "kr": "asia",
    "na": "americas",
    "latam": "americas",
    "br": "americas",
    "eu": "europe",
}


class RiotAPIError(Exception):
    """Raised when the Riot API returns a non-recoverable error."""
    pass


def _headers():
    print(f"DEBUG: RIOT_API_KEY = {RIOT_API_KEY!r}")  # temporary debug line
    if not RIOT_API_KEY:
        raise RiotAPIError(...)
    return {"X-Riot-Token": RIOT_API_KEY}


def _get(url: str, max_retries: int = 3) -> dict:
    """
    GET with basic rate-limit backoff.

    Riot's dev API rate limit is tight (20 req / 1s, 100 req / 2min at time
    of writing). If we get a 429, Riot tells us exactly how long to wait
    via the Retry-After header - respect it rather than guessing.
    """
    for attempt in range(1, max_retries + 1):
        response = requests.get(url, headers=_headers())

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            wait_seconds = int(response.headers.get("Retry-After", 5))
            print(f"  Rate limited. Waiting {wait_seconds}s (attempt {attempt}/{max_retries})...")
            time.sleep(wait_seconds)
            continue

        if response.status_code == 403:
            raise RiotAPIError(
                "403 Forbidden - your API key is likely expired. "
                "Regenerate at developer.riotgames.com and update .env."
            )

        if response.status_code == 404:
            raise RiotAPIError(f"404 Not Found for {url} - check Riot ID / region are correct.")

        raise RiotAPIError(f"Unexpected status {response.status_code} for {url}: {response.text}")

    raise RiotAPIError(f"Gave up after {max_retries} retries on {url}")


def get_puuid(game_name: str = GAME_NAME, tag_line: str = TAG_LINE, region: str = REGION) -> str:
    """Resolve a Riot ID (name#tag) to a PUUID via the Account API."""
    continent = _CONTINENT_FOR_REGION.get(region)
    if not continent:
        raise RiotAPIError(f"No continent mapping for region '{region}'. Add it to _CONTINENT_FOR_REGION.")

    url = f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    data = _get(url)
    return data["puuid"]


def get_match_ids(puuid: str, region: str = REGION, count: int = 5) -> list[str]:
    """Get a list of recent match IDs for a PUUID."""
    url = (
        f"https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
    )
    data = _get(url)
    history = data.get("history", [])[:count]
    return [entry["matchId"] for entry in history]


def get_match_details(match_id: str, region: str = REGION) -> dict:
    """Get full match details for a single match ID."""
    url = f"https://{region}.api.riotgames.com/val/match/v1/matches/{match_id}"
    return _get(url)
