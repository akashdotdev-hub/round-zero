import json
from pathlib import Path


MY_PUUID = "fc7c1e4e-8839-54c5-a21d-497bef293a2e"

DATA_DIR = Path("data")
PROCESSED_DIR = Path("processed_data")


def extract_player_match(raw_match, my_puuid):
    """Extract our player's relevant data from one match."""

    metadata = raw_match["metadata"]

    # Find our player using the stable PUUID
    player = next(
        (
            player
            for player in raw_match["players"]
            if player.get("puuid") == my_puuid
        ),
        None,
    )

    # Player was not present in this match
    if player is None:
        return None

    stats = player["stats"]
    damage = stats["damage"]

    return {
        # Identity
        "puuid": player["puuid"],

        # Match information
        "match_id": metadata["match_id"],
        "map": metadata["map"]["name"],
        "started_at": metadata["started_at"],
        "game_length_in_ms": metadata["game_length_in_ms"],
        "queue": metadata["queue"],
        "season": metadata["season"],
        "region": metadata["region"],
        "cluster": metadata["cluster"],

        # Player information
        "team_id": player["team_id"],
        "agent": player["agent"]["name"],

        # Combat statistics
        "score": stats["score"],
        "kills": stats["kills"],
        "deaths": stats["deaths"],
        "assists": stats["assists"],
        "headshots": stats["headshots"],
        "bodyshots": stats["bodyshots"],
        "legshots": stats["legshots"],

        # Damage
        "damage_dealt": damage["dealt"],
        "damage_received": damage["received"],

        # Economy
        "economy": player["economy"],

        # Behavior
        "behavior": player["behavior"],
    }


def main():
    json_files = sorted(DATA_DIR.glob("*.json"))

    if not json_files:
        print("No match JSON files found.")
        return

    # Create processed-data directory if needed
    PROCESSED_DIR.mkdir(exist_ok=True)

    print(f"Found {len(json_files)} match files.")

    extracted_count = 0
    skipped_count = 0

    for file in json_files:

        try:
            with open(file, "r", encoding="utf-8") as f:
                raw_match = json.load(f)

            extracted = extract_player_match(raw_match, MY_PUUID)

            if extracted is None:
                print(f"\nSkipping {file.name}")
                print("  Your player was not found in this match.")
                skipped_count += 1
                continue

            # Save extracted record
            output_file = PROCESSED_DIR / file.name

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(extracted, f, indent=2)

            extracted_count += 1

            print(f"\nProcessed: {file.name}")
            print(f"  Match: {extracted['match_id']}")
            print(f"  Map: {extracted['map']}")
            print(f"  Agent: {extracted['agent']}")
            print(
                f"  K/D/A: "
                f"{extracted['kills']}/"
                f"{extracted['deaths']}/"
                f"{extracted['assists']}"
            )
            print(
                f"  Saved: {output_file}"
            )

        except (json.JSONDecodeError, KeyError) as error:
            print(f"\nError processing {file.name}")
            print(f"  {error}")

    print("\n------------------------------")
    print(f"Extracted: {extracted_count}")
    print(f"Skipped:   {skipped_count}")
    print(f"Total:     {len(json_files)}")
    print("------------------------------")


if __name__ == "__main__":
    main()