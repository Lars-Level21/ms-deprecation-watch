# ms-deprecation-watch

Checks the Microsoft Learn pages about deprecations (Power Platform, Dynamics 365 CE,
Copilot Studio) every day and opens a **GitHub issue** when their content has changed.
GitHub then notifies you by email or in the app. On quiet days, nothing arrives.

```mermaid
flowchart TD
    T(["⏰ Daily at 05:00 UTC<br/>or manual start"]) --> W["📋 watchlist.yml<br/>list of Learn pages"]

    W --> G["🐙 Source <b>github</b><br/>new commits since<br/>last seen SHA"]
    W --> L["🌐 Source <b>learn</b><br/>page text vs.<br/>stored snapshot"]

    G --> C{"Changed?"}
    L --> C
    C -- no --> Q(["😴 Quiet day<br/>no issue"])
    C -- "yes (first run)" --> B(["📌 Set baseline only"])
    C -- yes --> AI["🤖 Claude<br/>summarizes the diff<br/>filters out minor edits"]

    AI --> R{"Substantively<br/>relevant?"}
    R -- no --> Q
    R -- yes --> I["📝 One GitHub issue per page<br/>date · impact · action<br/>+ diff under reports/"]
    I --> M(["📬 Notification by email/app<br/>→ read, close issue"])

    Q --> S[("💾 Commit state/ to the repo<br/>keeps the schedule active")]
    B --> S
    I --> S

    classDef trigger fill:#e8f0fe,stroke:#4a6fd8,color:#1a2b5c
    classDef ai fill:#f3e8fd,stroke:#8a4fd8,color:#3b1a5c
    classDef out fill:#e6f6ea,stroke:#3a9a55,color:#14401f
    classDef quiet fill:#f2f2f2,stroke:#999,color:#444
    class T trigger
    class AI ai
    class I,M out
    class Q,B quiet
```

## How it works

1. `watchlist.yml` lists the pages. There are two source types:
   - `github`: new commits to the Markdown file in the public `MicrosoftDocs/*` repo
     (exact diff + commit links). The last seen commit SHA serves as the bookmark, so
     no changes are lost even if runs fail.
   - `learn`: for pages without a public repo (e.g. Copilot Studio). The text of the
     rendered page is stored as a snapshot in `state/snapshots/` and compared.
2. Claude (`claude-opus-5`) summarizes each diff in the configured language and filters out minor edits
   (typos, `ms.date`, links, formatting).
3. A **separate issue** is created for each page with relevant changes, labeled
   `deprecation-watch` plus the product area (e.g. `D365 Sales`). The title carries the
   key message, and the body is email-friendly: date, impact and action for each deprecation.
   The workflow stores the full diff under `reports/<date>/<id>.diff`, and the issue
   links to it. Close the issue after review.
4. The workflow commits the state (`state/`) back to the repo. The daily commit keeps the
   repo active; otherwise GitHub disables schedules after 60 days of inactivity.

On the **first run**, only the baseline is set and no issue is created.

## Setup

1. Create the secret `ANTHROPIC_API_KEY` (Settings → Secrets and variables → Actions).
   Without a key everything still runs, but without summaries or relevance filtering.
2. Optional: set the repo variable `CLAUDE_MODEL` to use a different model
   (e.g. `claude-sonnet-5`, which is cheaper).
3. Optional: set the repo variable `REPORT_LANGUAGE` to `de` to get the issues in German.
   Default is `en` (English).
4. Notifications: set the repo to **Watch → All Activity** (or Custom → Issues)
   so that new issues arrive by email.
5. Start it once manually: Actions → *Deprecation Watch* → *Run workflow*
   (this sets the baseline).

## Adding a page

Click the edit pencil on the Learn page. It leads to the file in the GitHub repo; take
`repo`, `branch` and `path` from there. If the link points to a private `…-pr` repo,
drop the `-pr` suffix and use `main` instead of `live`. If there is no public repo,
use `source: learn`.

## Testing locally

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
DRY_RUN=1 .venv/Scripts/python watch.py
```

With `DRY_RUN=1`, no issue is created and no state is saved.
`TEST_REWIND=3` checks the GitHub sources as if the last check was 3 commits ago
(forces a dry run). In Actions, the same is available as the `test_rewind` input when starting manually.
