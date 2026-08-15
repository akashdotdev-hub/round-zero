# Round Zero — Prerequisites & Build Order

Read this right before starting a session. It's the "am I actually ready" checklist and the session-by-session order — nothing here is theory, this is what you check and do, in order.

---

## 1. Prerequisites Checklist

### AWS
- [x] AWS account created
- [ ] Logged into the AWS Console right now, correct account (easy to have multiple — double check)
- [ ] Billing alerts enabled: **Billing Preferences → "Receive Billing Alerts"** — this is a manual, one-time, account-level toggle Terraform cannot set for you. Do this before deploying anything, or the CloudWatch billing alarm from `budget.tf` won't fire.
- [ ] AWS CLI installed locally, and `aws configure` run with credentials for this account (access key + secret from an IAM user — not your root account credentials)

### Riot
- [x] Riot Developer Portal account
- [x] Dev API key generated
- [ ] Confirm it's fresh — dev keys expire every 24 hours. If it's from an earlier session, regenerate it now at developer.riotgames.com before running anything

### Local tooling — confirm what's actually installed
Run these three checks in a terminal, right now, before starting:
```bash
terraform -version
docker --version
git --version
```
- [ ] Terraform installed (needed from Milestone 1)
- [ ] Docker installed (not needed until Milestone 4 — processing/Lambda packaging — so it's fine to install this later, not blocking day one)
- [ ] Git installed (needed from Milestone 1, to actually version-control this as you go)

If Terraform is the one missing, install it before your first session — everything starts there. If it's Docker missing, you have a few milestones of runway before it matters.

### Where things run
- [x] Confirmed: your own laptop/PC, not a cloud shell or sandbox

---

## 2. Build Order — one milestone per session

Each milestone ends with something real and working — never leave a session with something half-wired. Don't start the next milestone until the current one is confirmed working.

### Milestone 1 — Cost guard deployed
- Run `terraform init`, `terraform plan`, `terraform apply` on the existing `provider.tf` + `budget.tf` files
- **Confirm it worked**: check AWS Console → Billing → Budgets, see the budget listed; check CloudWatch → Alarms, see the billing alarm listed
- Nothing else gets built until this is visibly live — it's the one thing that has to exist before anything billable does

### Milestone 2 — Ingestion working locally
- Run `pull_matches.py` against your real Riot ID
- **Confirm it worked**: real match JSON files sitting in `src/ingestion/data/`, inspected by eye to make sure the data looks right (right agent, right stats, matches you actually remember playing)
- This is still 100% local — nothing touches AWS yet

### Milestone 3 — Storage wired up (DynamoDB)
- Add the DynamoDB table(s) to Terraform, apply
- Modify the ingestion script to write to DynamoDB instead of local JSON
- **Confirm it worked**: query the table in the AWS Console, see your real match data sitting there

### Milestone 4 — Processing + coaching logic
- Write the aggregation logic (per-agent, per-map, economy stats) and the rule-based coaching checks, from the data model doc
- Can run locally against the DynamoDB data first, then wrap in Lambda + Docker once the logic itself is confirmed correct
- **Confirm it worked**: aggregated stats + coaching insights, computed from your real matches, printed out correctly and by-hand-checked against what you know actually happened in those games

### Milestone 5 — API layer
- API Gateway + Lambda endpoints exposing the processed data
- **Confirm it worked**: hit the endpoint with `curl` or Postman, get real JSON back

### Milestone 6 — Dashboard
- Build the frontend against the real API from Milestone 5, following the layout doc (agent cards, charts, coaching section)
- **Confirm it worked**: this is your first real screenshot-worthy moment — the actual visual payoff

### Milestone 7 — Jenkins pipeline
- Stand up Jenkins on EC2, wire the infra pipeline (plan on change, manual-approve apply)
- **Confirm it worked**: make a small Terraform change, watch Jenkins catch it and run a plan
- Stop the EC2 instance the moment you're done for the session — this is your one real recurring cost

### Milestone 8 — Observability + load test
- CloudWatch/Grafana dashboard for pipeline health
- Synthetic load test against your API layer, capture before/after numbers
- **Confirm it worked**: real screenshots of the load test running and the metrics responding

### Stretch — AI coaching layer
- Only after all 8 milestones above are solid — wire the Anthropic API into the processing step per the tech-stack doc

---

## The rule for every session
Start of session: check the milestone you're on. End of session: either that milestone is confirmed working (checkbox-style, provable, not "probably fine"), or you stop at a clean sub-step you can pick back up — never mid-broken.
