"""
pull_matches.py

Milestone 2: pull your own recent Valorant match history and save the raw
JSON locally. Deliberately 100% local, no AWS involved yet - isolates
"does my API logic work" from "does my cloud infra work" (see
docs/prerequisites-and-build-order.md).

Uses HenrikDev's community Valorant API rather than Riot's directly - see
valorant_client.py for why.

Usage:
    python pull_matches.py
    python pull_matches.py --count 10
"""

import argparse
import json
from pathlib import Path

from valorant_client import get_matches, ValorantAPIError

DATA_DIR = Path(__file__).parent / "data"


def main(count: int):
    DATA_DIR.mkdir(exist_ok=True)

    print("Fetching recent matches...")
    try:
        matches = get_matches()
    except ValorantAPIError as e:
        print(f"Failed to fetch matches: {e}")
        return

    if not matches:
        print("  No matches found. Have you played any Valorant matches recently?")
        return

    matches = matches[:count]
    print(f"  Found {len(matches)} matches.")

    saved = 0
    for i, match in enumerate(matches, start=1):
        match_id = match.get("metadata", {}).get("match_id", f"unknown_{i}")
        out_path = DATA_DIR / f"{match_id}.json"

        if out_path.exists():
            print(f"  [{i}/{len(matches)}] {match_id} already saved, skipping.")
            saved += 1
            continue

        with open(out_path, "w") as f:
            json.dump(match, f, indent=2)

        map_name = match.get("metadata", {}).get("map", {}).get("name", "?")
        print(f"  [{i}/{len(matches)}] {match_id} ({map_name}) saved -> {out_path}")
        saved += 1

    print(f"\nDone. {saved}/{len(matches)} matches saved to {DATA_DIR}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull recent Valorant match history.")
    parser.add_argument("--count", type=int, default=5, help="Number of recent matches to pull (default: 5)")
    args = parser.parse_args()
    main(args.count)
