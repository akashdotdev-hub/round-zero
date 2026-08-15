# ROUND ZERO
### *a cloud pipeline that turns your Valorant matches into a coach that's actually paying attention*

---

## What this document is

This is the full theory/plan for a personal cloud engineering portfolio project, written with zero technology-stack detail on purpose. It exists so this project can be picked back up in a brand-new conversation and immediately understood — what it is, why it exists, and what "done" looks like — before a single tool gets chosen.

---

## The honest problem statement

There isn't a market gap being filled here, and this project doesn't pretend otherwise. The real starting point is two separate, genuine needs that happen to solve each other:

1. **A personal one:** improving at Valorant requires noticing patterns across many matches — economy discipline, agent performance, accuracy trends, tilt patterns — and nobody reviews their own match history rigorously enough to actually see those patterns. Riot's own client shows you raw stats per match, but never aggregated, trended, or interpreted.

2. **A professional one:** building convincing cloud infrastructure experience requires working against something with real constraints — a real external API with authentication and rate limits, real messy nested data that needs genuine transformation, and a system that needs to be reliable, observable, and cost-aware, not just "runs once and works." Toy projects with fake data don't create these constraints. A real project does.

The project exists at the intersection: **use a real personal need (get better at the game) as the reason to build real infrastructure (a small but properly engineered cloud data pipeline)**, and be upfront that the "problem being solved" is self-directed, not a business case.

---

## The plan, in plain terms

1. **Pull your own match history** from Valorant's public API — your own account, your own data, nothing that requires anyone else's consent.
2. **Turn raw match data into aggregated stats** — trends across matches, not just single-match numbers: win rates by agent and map, economy efficiency, accuracy trends, performance drift over a session.
3. **Surface pattern-based coaching insights** — simple, explainable logic that flags real patterns in the data ("your win rate drops when you skip full armor buys," "your headshot percentage on this agent trails your average"). Every insight should be traceable back to the number that triggered it — no black box.
4. **(Stretch) Turn those insights into a written coaching summary** using an AI model to generate natural-language advice grounded strictly in your own aggregated stats — not generic Valorant tips, not invented advice.
5. **Show it all in a visually clean personal dashboard** — this is the proof-of-concept surface: a handful of real screenshots showing real matches, real stats, and real coaching output, not synthetic placeholder data.
6. **Treat the infrastructure itself as the actual subject of the project** — how it's built, deployed, tested, made observable, and kept cheap is the part meant to hold up under real interview scrutiny, separate from the dashboard/coaching feature itself.

---

## What "done" actually looks like

Not a persistent, always-on live service. The goal is **1–3 clean, real, working examples** — your own matches pulled, processed, visualized, and (ideally) coached — captured as screenshots/recordings, with the infrastructure behind it built and documented properly, then torn down. Proof it works end-to-end and correctly, built the right way, not a running product.

---

## What this project is *not*, on purpose

- Not a business, not a startup idea, not something solving an industry-wide problem
- Not a live/real-time system — it works with historical match data, pulled after a match ends
- Not built for other people's data or accounts — personal, self-contained
- Not meant to run continuously — meant to be demonstrated, then shut down

---

## The honest one-line pitch

*"I built a small, real cloud data pipeline — using my own Valorant match history as genuinely messy, rate-limited, real-world data — to turn raw match stats into pattern-based coaching insights, and used the project as a deliberate excuse to practice real infrastructure discipline: proper deployment, observability, and cost control, not just a working demo."*

---

## Alternate names considered

- **TILT CHECK** — *"a cloud pipeline that tells you the truth about your last ten rounds"*
- **ROUND ZERO** — *"where your next match starts, if you actually looked at your last one"*
- **FULL BUY** — *"invest in the data, not just the loadout"*
