import json
from pathlib import Path

from coaching_rules import (
    evaluate_agent_rules,
    evaluate_overall_rules,
)


PROCESSED_DIR = Path("../ingestion/processed_data")


def load_matches():
    """Load all processed match records."""

    matches = []

    for file in sorted(PROCESSED_DIR.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            matches.append(json.load(f))

    return matches


def calculate_overall_stats(matches):
    """Calculate overall performance statistics."""

    total_matches = len(matches)

    if total_matches == 0:
        return {}

    total_kills = sum(match["kills"] for match in matches)
    total_deaths = sum(match["deaths"] for match in matches)
    total_assists = sum(match["assists"] for match in matches)

    total_headshots = sum(match["headshots"] for match in matches)
    total_bodyshots = sum(match["bodyshots"] for match in matches)
    total_legshots = sum(match["legshots"] for match in matches)

    total_damage = sum(match["damage_dealt"] for match in matches)

    total_shots = (
        total_headshots
        + total_bodyshots
        + total_legshots
    )

    return {
        "matches": total_matches,
        "average_kills": total_kills / total_matches,
        "average_deaths": total_deaths / total_matches,
        "average_assists": total_assists / total_matches,
        "kd_ratio": (
            total_kills / total_deaths
            if total_deaths > 0
            else 0
        ),
        "average_damage": total_damage / total_matches,
        "headshot_percentage": (
            (total_headshots / total_shots) * 100
            if total_shots > 0
            else 0
        ),
    }


def calculate_agent_stats(matches):
    """Calculate performance statistics grouped by agent."""

    agents = {}

    for match in matches:
        agent = match["agent"]

        if agent not in agents:
            agents[agent] = {
                "matches": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "damage": 0,
            }

        agents[agent]["matches"] += 1
        agents[agent]["kills"] += match["kills"]
        agents[agent]["deaths"] += match["deaths"]
        agents[agent]["assists"] += match["assists"]
        agents[agent]["damage"] += match["damage_dealt"]

    results = {}

    for agent, data in agents.items():
        matches_played = data["matches"]

        results[agent] = {
            "matches": matches_played,
            "average_kills": data["kills"] / matches_played,
            "average_deaths": data["deaths"] / matches_played,
            "average_assists": data["assists"] / matches_played,
            "kd_ratio": (
                data["kills"] / data["deaths"]
                if data["deaths"] > 0
                else 0
            ),
            "average_damage": data["damage"] / matches_played,
        }

    return results


def calculate_map_stats(matches):
    """Calculate performance statistics grouped by map."""

    maps = {}

    for match in matches:
        map_name = match["map"]

        if map_name not in maps:
            maps[map_name] = {
                "matches": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "damage": 0,
            }

        maps[map_name]["matches"] += 1
        maps[map_name]["kills"] += match["kills"]
        maps[map_name]["deaths"] += match["deaths"]
        maps[map_name]["assists"] += match["assists"]
        maps[map_name]["damage"] += match["damage_dealt"]

    results = {}

    for map_name, data in maps.items():
        matches_played = data["matches"]

        results[map_name] = {
            "matches": matches_played,
            "average_kills": data["kills"] / matches_played,
            "average_deaths": data["deaths"] / matches_played,
            "average_assists": data["assists"] / matches_played,
            "kd_ratio": (
                data["kills"] / data["deaths"]
                if data["deaths"] > 0
                else 0
            ),
            "average_damage": data["damage"] / matches_played,
        }

    return results


def main():
    matches = load_matches()

    print(f"Loaded {len(matches)} processed matches.")

    if not matches:
        print("No processed matches found.")
        return

    # Overall statistics
    overall_stats = calculate_overall_stats(matches)

    print("\n=== Overall Performance ===")

    print(f"Matches: {overall_stats['matches']}")
    print(f"Average Kills: {overall_stats['average_kills']:.2f}")
    print(f"Average Deaths: {overall_stats['average_deaths']:.2f}")
    print(f"Average Assists: {overall_stats['average_assists']:.2f}")
    print(f"K/D Ratio: {overall_stats['kd_ratio']:.2f}")
    print(f"Average Damage: {overall_stats['average_damage']:.2f}")
    print(
        f"Headshot %: "
        f"{overall_stats['headshot_percentage']:.2f}%"
    )

    # Agent statistics
    agent_stats = calculate_agent_stats(matches)

    print("\n=== Agent Performance ===")

    for agent, stats in agent_stats.items():
        print(f"\n{agent}")
        print(f"  Matches: {stats['matches']}")
        print(f"  Average Kills: {stats['average_kills']:.2f}")
        print(f"  Average Deaths: {stats['average_deaths']:.2f}")
        print(f"  Average Assists: {stats['average_assists']:.2f}")
        print(f"  K/D Ratio: {stats['kd_ratio']:.2f}")
        print(f"  Average Damage: {stats['average_damage']:.2f}")

    map_stats = calculate_map_stats(matches)

    print("\n=== Map Performance ===")

    for map_name, stats in map_stats.items():
        print(f"\n{map_name}")
        print(f"  Matches: {stats['matches']}")
        print(f"  Average Kills: {stats['average_kills']:.2f}")
        print(f"  Average Deaths: {stats['average_deaths']:.2f}")
        print(f"  Average Assists: {stats['average_assists']:.2f}")
        print(f"  K/D Ratio: {stats['kd_ratio']:.2f}")
        print(f"  Average Damage: {stats['average_damage']:.2f}")

    overall_insights = evaluate_overall_rules(overall_stats)
    agent_insights = evaluate_agent_rules(agent_stats) 

    print("\n=== Coaching Insights ===")

    all_insights = overall_insights + agent_insights

    if not all_insights:
        print("No coaching rules triggered.")
    else:
        for insight in all_insights:
            print(f"\nRule: {insight['rule_id']}")
            print(f"Category: {insight['category']}")
            print(f"Severity: {insight['severity']}")

        if "agent" in insight:
            print(f"Agent: {insight['agent']}")

        print(f"Evidence: {insight['evidence']}")
        print(f"Recommendation: {insight['recommendation']}")


if __name__ == "__main__":
    main()