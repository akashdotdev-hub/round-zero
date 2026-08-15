# ROUND ZERO — Tech Stack

This covers every tool in the project, what it's actually doing, and why it's the right choice for a cost-conscious, portfolio-grade cloud pipeline. Read this alongside `project-brief.md`.

---

## 1. Infrastructure as Code — **Terraform**

**What it does:** defines every AWS resource (Lambda functions, DynamoDB tables, API Gateway, S3 buckets, IAM roles, budgets) as code, in version-controlled files, instead of clicking through the AWS console.

**Why it's here:** this is non-negotiable for a cloud engineer portfolio — "I clicked buttons in the console" is not a credible story. Terraform also gives you `terraform destroy`, which is your main cost-safety tool: tear everything down between sessions, spin it back up in minutes.

**How it's structured:**
- Split into modules (`networking`, `ingestion`, `storage`, `api`, `frontend`, `monitoring`) rather than one giant file — this is the difference between "I wrote Terraform" and "I wrote *maintainable* Terraform," and it's something interviewers specifically probe for.
- Remote state (an S3 bucket + DynamoDB table for state locking) instead of local state files — this is standard practice and worth doing even solo, because it's a genuinely common interview question ("how do you manage Terraform state in a team").

---

## 2. Compute / Ingestion & Processing — **AWS Lambda**

**What it does:** two Lambda functions do the actual work —
- **Ingestion Lambda:** triggered on a schedule (or manually for demo purposes), calls the Riot API, pulls your match history, handles auth (API key) and rate-limit backoff, writes raw match data to storage.
- **Processing Lambda:** triggered after new raw data lands, transforms it — aggregates stats across matches, computes trends, runs the rule-based coaching logic.

**Why it's here (over EC2/containers for this part):** Lambda is pay-per-invocation, not pay-per-hour — for a workload that runs a handful of times for demo purposes, this is close to free, and it matches the actual traffic pattern (bursty, infrequent) instead of paying for an idle server. It's also the "correct" architectural choice here, not just the cheap one — that distinction matters when you explain it in an interview.

**Trigger mechanism:** **Amazon EventBridge** — handles the "on a schedule" part (e.g., a cron rule) or event-based triggering (e.g., "new object landed in S3, kick off processing"). This is the standard AWS-native way to wire serverless workflows together without polling.

---

## 3. Storage — **Amazon DynamoDB**

**What it does:** stores both raw match data and processed/aggregated stats.

**Why DynamoDB over RDS (relational):** your access patterns here are simple lookups — "give me all matches for this player," "give me aggregated stats for this player" — not complex multi-table joins. DynamoDB fits key-value/document access patterns naturally, has a genuinely free-forever tier (25GB, 25 RCU/WCU), and scales without you managing a database server. Being able to explain *why* NoSQL fit this specific access pattern (not just "it's free") is the actual interview-worthy part.

**Table design:** partition key on player PUUID, sort key on match ID/timestamp — lets you efficiently query "all matches for me, most recent first" which is exactly your dashboard's main query.

---

## 4. API Layer — **Amazon API Gateway**

**What it does:** exposes HTTP endpoints (e.g., `GET /matches`, `GET /stats`, `GET /coaching`) that your frontend dashboard calls, which route to Lambda functions that read from DynamoDB and return JSON.

**Why it's here:** this is the standard, idiomatic way to expose serverless compute as a web API on AWS — REST API Gateway + Lambda is one of the most common patterns you'll be expected to know for a cloud role.

---

## 5. Frontend — **A static React dashboard, hosted on S3**

**What it does:** the actual visual dashboard — match list, stat trends, coaching insights — calling your API Gateway endpoints and rendering the results.

**Why static + S3 instead of a server:** it's a client-rendered app with no server-side logic of its own — S3 static website hosting (optionally fronted by CloudFront for HTTPS/CDN) is free-tier eligible and is the correct, minimal-cost way to serve this. No EC2, no server to patch or pay for.

---

## 6. AI Coaching Layer — **Anthropic API (Claude)**

**What it does:** takes your aggregated stats (already computed by the Processing Lambda) and generates a short, natural-language coaching summary — grounded strictly in the numbers it's given, not general Valorant advice.

**Why it's here:** this is the "current, real-market-value tech" piece you wanted — LLM integration into a data pipeline is a genuinely in-demand skill right now, distinct from the core infra skills, and it's cheap at your usage volume (a handful of calls for demo purposes).

**How it's used correctly:** the prompt is engineered to only reason over the specific stats passed in (few-shot structure: "here is this player's data, generate coaching insights *only* from this data") — this is worth explicitly designing and explaining, since "prevent the model from hallucinating advice not grounded in the data" is a real, demonstrable engineering decision, not just an API call.

---

## 7. CI/CD — **Jenkins**

**What it does:** automates two pipelines —
- **Infra pipeline:** on a Terraform change, automatically runs `terraform fmt -check`, `terraform validate`, `terraform plan` — with `terraform apply` gated behind manual approval in the Jenkins UI.
- **App pipeline:** on a code change (Lambda function code, frontend code), runs tests/linting, builds the deployable artifact (zip for Lambda, static build for the frontend), and — if approved — deploys it.

**Why Jenkins specifically (vs. GitHub Actions):** it's still heavily used in enterprise environments, and having hands-on experience with pipeline-as-code (`Jenkinsfile`) and manual approval gates is a directly relevant, still-commonly-asked-about skill for cloud/DevOps roles.

**Where it runs:** a single EC2 instance (`t3.small`), started only during active work sessions and stopped afterward — this is the one piece of the stack with a real hourly cost, so it's the one you're most deliberate about not leaving on.

---

## 8. Containerization — **Docker**

**What it does:** packages the Lambda function code (and its dependencies) into a consistent, reproducible build artifact, and is used to containerize the Riot API ingestion script for local development/testing so "works on my machine" isn't a risk.

**Why it's here even though Lambda doesn't strictly require containers:** demonstrating Docker is one of your explicit goals, and it has a genuinely legitimate role here — Lambda supports container-image deployment as an alternative to zip packaging, and using Docker for local dev/test parity (running the same ingestion logic locally in a container before it's deployed) is standard, defensible practice, not shoehorned in.

---

## 9. Observability — **Amazon CloudWatch + Grafana**

**What it does:**
- **CloudWatch:** collects logs and metrics from every Lambda invocation automatically (invocation count, duration, errors, throttles) — this is your infrastructure health layer.
- **Grafana** (self-hosted, free, on the same or a separate small EC2 instance — or Grafana Cloud's free tier): builds dashboards on top of CloudWatch metrics — a visual, screenshot-able view of pipeline health, separate from the *product* dashboard (the React app showing match stats).

**Why the split matters:** having a distinct **infra observability dashboard** (Grafana/CloudWatch — "is my pipeline healthy, fast, and cheap") separate from the **product dashboard** (React app — "here's my Valorant coaching insights") mirrors how real engineering orgs separate these concerns, and it's a detail worth explicitly pointing out in an interview.

---

## 10. Cost Control — **AWS Budgets + CloudWatch Billing Alarms**

**What it does:** the very first Terraform resource you deploy, before anything else — a budget alert (e.g., at $20 and $50 against your $160 credit) and a billing alarm, so any runaway cost gets caught immediately rather than discovered later.

**Why it's first, not last:** deploying cost guardrails before any billable resource exists is itself a demonstrable good practice — "I set up budget alerts before provisioning anything" is a small detail that signals real operational maturity.

---

## How it all connects (data flow, no diagram needed yet)

```
EventBridge (schedule/trigger)
        ↓
Ingestion Lambda → calls Riot API → writes raw match data
        ↓
DynamoDB (raw matches)
        ↓
Processing Lambda → aggregates stats, runs coaching logic, calls Anthropic API
        ↓
DynamoDB (processed stats + coaching insights)
        ↓
API Gateway ← React dashboard (S3-hosted) queries this
```

Running alongside all of it: **Terraform** defines everything above, **Jenkins** deploys changes to it, **Docker** packages the Lambda code consistently, **CloudWatch/Grafana** watches it, and **AWS Budgets** watches the money.

---

## What's deliberately excluded, and why

- **No NAT Gateway** — not needed since Lambda functions here don't require VPC placement (no private resources they need to reach), and NAT Gateway has no free tier and a real hourly cost.
- **No ElastiCache/Redis** — no need for a caching/leaderboard layer at this data volume; would add cost with no real benefit here.
- **No RDS** — the access pattern doesn't need relational joins; DynamoDB is both cheaper and architecturally more correct for this use case.

---

Next step from here: repo scaffolding and the actual first Terraform files (provider config + budget alarm), followed by the Riot API ingestion script.
