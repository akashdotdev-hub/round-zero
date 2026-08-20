import json
from decimal import Decimal
from pathlib import Path

import boto3


TABLE_NAME = "round-zero-matches"
AWS_REGION = "ap-south-1"
PROCESSED_DIR = Path("processed_data")


def convert_floats(value):
    """Convert Python floats to Decimal for DynamoDB."""

    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, dict):
        return {
            key: convert_floats(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [convert_floats(item) for item in value]

    return value


def build_item(match):
    """Convert a processed match into a DynamoDB item."""

    puuid = match["puuid"]
    match_id = match["match_id"]
    started_at = match["started_at"]

    item = {
        "PK": f"PLAYER#{puuid}",
        "SK": f"MATCH#{started_at}#{match_id}",
        **match,
    }

    return convert_floats(item)


def main():
    json_files = sorted(PROCESSED_DIR.glob("*.json"))

    if not json_files:
        print("No processed match files found.")
        return

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
    )

    table = dynamodb.Table(TABLE_NAME)

    loaded_count = 0

    print(f"Found {len(json_files)} processed match files.")
    print(f"Loading into: {TABLE_NAME}")

    for file in json_files:

        try:
            with open(file, "r", encoding="utf-8") as f:
                match = json.load(f)

            item = build_item(match)

            table.put_item(Item=item)

            loaded_count += 1

            print(
                f"Loaded: {match['match_id']} "
                f"| {match['map']} "
                f"| {match['agent']}"
            )

        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"\nError processing {file.name}")
            print(f"  {error}")

    print("\n------------------------------")
    print(f"Loaded: {loaded_count}")
    print(f"Total:  {len(json_files)}")
    print("------------------------------")


if __name__ == "__main__":
    main()