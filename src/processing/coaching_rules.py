def evaluate_overall_rules(overall_stats):
    """Evaluate deterministic coaching rules."""

    insights = []

    kd_ratio = overall_stats["kd_ratio"]
    average_deaths = overall_stats["average_deaths"]
    headshot_percentage = overall_stats["headshot_percentage"]

    if kd_ratio < 1.0:
        insights.append({
            "rule_id": "KDR_BELOW_ONE",
            "category": "combat",
            "severity": "high",
            "evidence": {
                "kd_ratio": round(kd_ratio, 2),
            },
            "recommendation": (
                "Focus on reducing unnecessary deaths "
                "and improving survival during engagements."
            ),
        })

    if average_deaths > 15:
        insights.append({
            "rule_id": "HIGH_DEATH_RATE",
            "category": "survivability",
            "severity": "medium",
            "evidence": {
                "average_deaths": round(average_deaths, 2),
            },
            "recommendation": (
                "Review unnecessary engagements, "
                "positioning, and disengagement decisions."
            ),
        })

    if headshot_percentage < 20:
        insights.append({
            "rule_id": "LOW_HEADSHOT_RATE",
            "category": "aim",
            "severity": "medium",
            "evidence": {
                "headshot_percentage": round(
                    headshot_percentage,
                    2,
                ),
            },
            "recommendation": (
                "Prioritize crosshair placement "
                "and aim consistency."
            ),
        })

    return insights


def evaluate_agent_rules(agent_stats):
    """Evaluate agent-specific coaching rules."""

    insights = []

    for agent, stats in agent_stats.items():

        # Require at least two matches before
        # making an agent-specific recommendation.
        if stats["matches"] < 2:
            continue

        if stats["kd_ratio"] < 1.0:
            insights.append({
                "rule_id": "AGENT_LOW_PERFORMANCE",
                "category": "agent",
                "severity": "medium",
                "agent": agent,
                "evidence": {
                    "matches": stats["matches"],
                    "kd_ratio": round(
                        stats["kd_ratio"],
                        2,
                    ),
                },
                "recommendation": (
                    f"Review your performance on {agent} "
                    "before making it a primary pick."
                ),
            })

    return insights