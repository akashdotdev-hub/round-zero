# Round Zero

*a cloud pipeline that turns Valorant match history into a coach that's actually paying attention*

**Status:** 🚧 in progress — built one milestone at a time, in public. See [progress](#progress) below.

---

## What this is

Round Zero pulls my own Valorant match history from Riot's API, turns raw per-match stats into aggregated trends (economy discipline, per-agent performance, accuracy drift), and surfaces rule-based coaching insights — each one traceable back to the exact number that triggered it, no black box.

It's a personal tool first. But it's also a deliberate excuse to build **real cloud infrastructure** against **real constraints**: a rate-limited external API, genuinely messy nested data, and a system built to be reliable, observable, and cost-aware — not a demo that only has to run once.

> I built a small, real cloud data pipeline — using my own Valorant match history as genuinely messy, rate-limited, real-world data — to turn raw match stats into pattern-based coaching insights, and used the project as a deliberate excuse to practice real infrastructure discipline: proper deployment, observability, and cost control, not just a working demo.

**This is a learning project first, portfolio piece second.** Nothing gets copy-pasted without understanding why it's there — the repo's growth (see below) is the actual evidence of that.

---

## Stack

`Terraform` · `AWS Lambda` · `DynamoDB` · `API Gateway` · `EventBridge` · `React` · `S3` · `Jenkins` · `Docker` · `CloudWatch` / `Grafana` · `Anthropic API` *(stretch)*

Full reasoning for every tool choice is in [`docs/tech-stack.md`](docs/tech-stack.md).

---

## Repo structure

This repo is **not** scaffolded up front — each folder appears exactly when its milestone starts, so the commit history itself is a map of the build order.

```
round-zero/
├── docs/            planning docs — problem statement, tech stack, data model
├── terraform/       infra as code (Milestone 1+)
├── src/
│   ├── ingestion/   Riot API client (Milestone 2)
│   └── processing/  aggregation + coaching logic (Milestone 4)
├── frontend/        React dashboard (Milestone 6)
└── jenkins/         CI/CD pipeline (Milestone 7)
```

---

## Progress

| # | Milestone | Status |
|---|---|---|
| 1 | Cost guardrails (Terraform budget + billing alarm) | ⬜ not started |
| 2 | Ingestion working locally against Riot API | ⬜ not started |
| 3 | Storage wired up (DynamoDB) | ⬜ not started |
| 4 | Processing + rule-based coaching logic | ⬜ not started |
| 5 | API layer (API Gateway + Lambda) | ⬜ not started |
| 6 | Dashboard (React) | ⬜ not started |
| 7 | CI/CD (Jenkins) | ⬜ not started |
| 8 | Observability + load test | ⬜ not started |
| ★ | Stretch: AI coaching layer (Claude) | ⬜ not started |

Full detail on each milestone, what's being learned, and how "done" is verified: [`docs/prerequisites-and-build-order.md`](docs/prerequisites-and-build-order.md).

---

## What this is deliberately *not*

- Not a business or a product — a personal tool, built for one account (mine)
- Not live/real-time — works with historical, post-match data only
- Not an always-on service — demoed with real screenshots, then torn down
- Not built for other people's data, leaderboards, or production Riot API access

Full scope and explicit non-goals: [`docs/scope-and-data-model.md`](docs/scope-and-data-model.md).

---

## Docs

- [`docs/project-brief.md`](docs/project-brief.md) — the full theory: problem statement, plan, what "done" looks like
- [`docs/tech-stack.md`](docs/tech-stack.md) — every tool, what it does, why it was chosen
- [`docs/scope-and-data-model.md`](docs/scope-and-data-model.md) — v1 scope, data model, dashboard layout
- [`docs/prerequisites-and-build-order.md`](docs/prerequisites-and-build-order.md) — the session-by-session build checklist

---

## License

MIT — see [`LICENSE`](LICENSE).