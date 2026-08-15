# Round Zero — Scope, Data Model & Dashboard Layout

This fills the gap between the theory doc and actual implementation: exactly what gets built for v1, what data it's built on, and what the screens look like.

---

## 1. V1 Scope Checklist

### In scope — v1 (the actual deliverable)

- [ ] Pull your own recent match history from the Valorant API (a handful of matches — enough for real screenshots, not a live feed)
- [ ] Store raw match data
- [ ] Process raw matches into aggregated stats across those matches (not just per-match — the trend/aggregate view is the actual point)
- [ ] Rule-based coaching insights — plain conditional logic flagging real patterns in your own stats, each one traceable to the number that triggered it
- [ ] A dashboard (web page) showing the match list, the aggregated stats, and the coaching insights
- [ ] Infra defined in Terraform, deployed via a Jenkins pipeline with a manual approval gate before apply
- [ ] Basic infra observability (CloudWatch/Grafana) — enough to screenshot pipeline health, not a full monitoring suite
- [ ] Cost guardrails (budget alert) deployed before anything else
- [ ] A short load test against your own API layer, with before/after numbers (latency, throughput) — proves the infra holds up, doesn't require the LLM or real users

### Stretch goals — only after v1 fully works, in this order

- [ ] AI-generated natural-language coaching summary (Anthropic API), grounded strictly in your aggregated stats
- [ ] A separate infra-observability dashboard, distinct from the product dashboard
- [ ] CI for the ingestion/processing code (tests + lint in Jenkins), not just infra plan/apply
- [ ] Historical trend view across more matches, if you end up pulling more over time

### Explicitly out of scope — don't build these, on purpose

- Live/real-time match data (only historical, post-match data is available anyway)
- Other players' data, leaderboards, or anything requiring RSO/production API access
- A persistent always-on service — this is meant to be demoed then torn down
- User accounts/auth/multi-user support — it's your own single-player dashboard
- Mobile app, notifications, or anything beyond a single web dashboard

---

## 2. Data Model (plain terms, no schema syntax yet)

Two levels of data: **raw** (as Riot gives it to you) and **processed** (what you actually compute and show).

### Raw match data (per match, as pulled from the API)

For each match you pull, you keep:
- Match ID, map played, game mode, date/time played, match length
- Your agent picked
- Final score (rounds won/lost), and which team won
- Per-round breakdown: round number, outcome (win/loss), how it ended (elimination, spike detonated, defused, time expired), your loadout value that round, credits spent
- Your per-match totals: kills, deaths, assists, damage dealt, headshots vs. total shots, first bloods, plants/defuses

This is stored close to exactly as Riot returns it — it's your source of truth, and everything else is derived from it.

### Processed / aggregated data (computed across your pulled matches)

This is what actually gets shown and reasoned over:

- **Overall performance trend**: K/D ratio, average damage per round, headshot % — each as a single current number *and* a trend across your pulled matches (going up, flat, going down)
- **Per-agent breakdown**: win rate, K/D, headshot % — split out per agent you've played, so patterns per-agent are visible
- **Per-map breakdown**: win rate, average round loss margin — split out per map
- **Economy pattern**: win rate when you had a "full buy" round vs. an "eco/force buy" round — this is the clearest, most defensible coaching signal, since it's a direct behavior-to-outcome link
- **Round-outcome pattern**: how often your losses come from being outgunned (loadout value mismatch) vs. other causes, where the data allows that distinction

### Coaching insights (derived from the processed data, not stored separately — computed on read)

Each insight is a simple rule with three parts: **the pattern detected → the specific stat behind it → a plain-language flag**. Example shapes (not literal output, just the structure):
- "Win rate drops meaningfully in rounds where you're outgunned in loadout value — a possible economy-timing issue"
- "Headshot % on [agent] is below your overall average — possible aim or positioning gap on that agent specifically"
- "Performance (damage/round) trends downward across the second half of matches — possible fatigue or tilt pattern"

Every insight must point back to the exact aggregated number that triggered it — no insight should exist that isn't traceable to something visible elsewhere on the dashboard.

---

## 3. Dashboard Layout

One web page, three sections, top to bottom — this is deliberately simple: it needs to demo cleanly in a screenshot or a 30-second recording, not require a tour.

### Section 1 — Overview (top of page)
- Your Riot ID, and the date range of matches pulled (e.g., "Last 3 matches, Aug 10–13")
- Three or four headline stat cards: current K/D, win rate, average headshot %, average damage/round — each with a small up/down trend indicator
- This section answers "how am I doing overall" in five seconds

### Section 2 — Breakdown (middle of page)
- A per-agent table or chart: agent, matches played, win rate, K/D
- A per-map table or chart: map, matches played, win rate
- An economy chart: win rate on full-buy rounds vs. eco/force-buy rounds, side by side
- This section answers "where specifically is this coming from"

### Section 3 — Coaching Insights (bottom of page)
- A short list (2–5 items) of the plain-language insights described above
- Each insight shown as a card: the flag itself, plus the specific stat it's based on right next to it (so it's visibly grounded, not a black box)
- If the AI-generated stretch goal is built, its output replaces or sits alongside this section as a short written paragraph — still required to cite the same underlying numbers

### What's deliberately NOT on this dashboard
- No infra/ops metrics (latency, cost, pipeline health) — those live on the separate Grafana/CloudWatch view, kept apart from this product-facing page on purpose
- No match-by-match deep dive (round-by-round replay view) — v1 shows aggregates and trends, not a full match browser; that'd be a reasonable v2 addition, not v1

---

## 4. Visual Style — making it actually look good

This is what turns "a table of stats" into something worth screenshotting. None of this changes the data model above — it's purely about presentation.

### Where imagery comes from
Riot exposes official game assets (agent portraits, agent icons, map images, weapon icons) through a free, public, no-auth-required asset API — this is separate from the match-data API and has no rate-limit/key concerns, so it can be used freely for visuals with zero added cost or complexity.

### Where visuals replace plain data, per section

**Overview section**
- Headline stat cards get a small icon per stat (crosshair for K/D, a shield for win rate, etc.) instead of being plain numbers in boxes
- Trend indicators shown as tiny sparkline charts (a thin line showing the last few matches' trend), not just an up/down arrow

**Breakdown section**
- Per-agent table becomes a **row of agent portrait cards** instead of a plain table — each card shows the agent's official portrait, name, win rate, and K/D, laid out like a roster rather than a spreadsheet
- Per-map data shown as **map callout cards** using official map images as the card background, stats overlaid
- Economy comparison shown as a **grouped bar chart** (full-buy vs. eco/force-buy win rate side by side) rather than two numbers in text
- Overall trend numbers get **line charts** across your pulled matches (K/D trend, damage/round trend), not just single current values

**Coaching Insights section**
- Each insight card gets a small icon indicating its category (economy, aim/accuracy, consistency) so the list is visually scannable, not a wall of text
- The specific stat behind each insight shown as a small inline chart or highlighted number, not just prose

### Overall visual direction
- Dark theme fits the subject matter (matches Valorant's own aesthetic) and makes agent portraits and map imagery pop rather than compete with a white background
- One accent color used consistently for anything "good" (win rate up, positive trend) and a second for anything flagged as a coaching concern — makes the page scannable at a glance, before reading any text
- Keep it to the three sections already defined — the visual upgrade is about *how* each section is presented, not adding more sections or more data than what's in the data model above

---

Once you're comfortable with this, the next planning piece (if anything still feels unfinished) or we move into implementation — your call.
