"""Daily check of the Microsoft deprecation pages listed in watchlist.yml.

- source "github": new commits to the Markdown file since the last seen SHA
- source "learn":  compare a text snapshot of the rendered Learn page with the stored one

Changes are (optionally) summarized by Claude and filtered for relevance.
For each page with relevant changes, a GitHub issue is created in this repo;
the full diff is stored under reports/ and linked from the issue.
State lives in state/ and is committed back to the repo by the workflow.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
STATE_FILE = ROOT / "state" / "state.json"
SNAPSHOT_DIR = ROOT / "state" / "snapshots"
REPORTS_DIR = ROOT / "reports"  # full diffs, linked from the issue

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPORT_REPO = os.environ.get("GITHUB_REPOSITORY", "")  # owner/name, set by Actions
# Test mode: treat GitHub sources as if the last check was N commits ago. Forces DRY_RUN.
TEST_REWIND = int(os.environ.get("TEST_REWIND") or 0)
DRY_RUN = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes") or TEST_REWIND > 0
ISSUE_LABEL = "deprecation-watch"

CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL") or "claude-opus-5"  # empty repo variable -> default
# Upper limit for the diff sent to Claude. Larger diffs are truncated – this is stated in
# the prompt and in the issue so nothing gets lost silently.
MAX_DIFF_CHARS_FOR_CLAUDE = 150_000

# Language of the issues (Claude's summary and the fixed texts around it). Logs stay English.
TEXTS = {
    "en": {
        "language": "English",
        "date_format": "YYYY-MM-DD or YYYY-MM",
        "kinds": {"new": "New", "changed": "Changed", "removed": "Removed", "clarified": "Clarified"},
        "date": "Date",
        "editorial": "Also editorial",
        "learn_page": "Learn page",
        "page_changed": "Page content changed",
        "change_detected": "Change detected",
        "no_ai": "without AI summary",
        "ai_failed": "AI summary failed",
        "missed": "The last seen version was not among the latest 30 commits; only these 30 are shown.",
        "truncated": "The diff was very large and was truncated for the summary.",
        "errors_title": "errors during check",
    },
    "de": {
        "language": "German",
        "date_format": "DD.MM.YYYY or MM/YYYY",
        "kinds": {"new": "Neu", "changed": "Geändert", "removed": "Entfernt", "clarified": "Klargestellt"},
        "date": "Termin",
        "editorial": "Außerdem redaktionell",
        "learn_page": "Learn-Seite",
        "page_changed": "Seiteninhalt geändert",
        "change_detected": "Änderung erkannt",
        "no_ai": "ohne KI-Zusammenfassung",
        "ai_failed": "KI-Zusammenfassung fehlgeschlagen",
        "missed": "Die zuletzt gesehene Version war nicht unter den letzten 30 Commits; gezeigt werden nur diese 30.",
        "truncated": "Der Diff war sehr groß und wurde für die Zusammenfassung gekürzt.",
        "errors_title": "Fehler beim Check",
    },
}
REPORT_LANGUAGE = (os.environ.get("REPORT_LANGUAGE") or "en").strip().lower()  # empty repo variable -> default
if REPORT_LANGUAGE not in TEXTS:
    sys.exit(f"REPORT_LANGUAGE must be one of {', '.join(TEXTS)}, got '{REPORT_LANGUAGE}'")
T = TEXTS[REPORT_LANGUAGE]

session = requests.Session()
session.headers["User-Agent"] = "ms-deprecation-watch"


@dataclass
class Change:
    page: dict
    diff: str
    commits: list[dict] = field(default_factory=list)  # {sha, message, url, date}
    note: str = ""
    relevant: bool = True
    headline: str = ""
    items: list[dict] = field(default_factory=list)  # {kind, feature, date, impact, action}
    editorial: str = ""


# --------------------------------------------------------------------------- state


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


# --------------------------------------------------------------------------- github source


def gh_get(url: str, **params) -> requests.Response:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    r = session.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r


def check_github(page: dict, page_state: dict) -> Change | None:
    repo, branch, path = page["repo"], page.get("branch", "main"), page["path"]
    commits = gh_get(f"{GITHUB_API}/repos/{repo}/commits", sha=branch, path=path, per_page=30).json()
    if not commits:
        raise RuntimeError(f"No commits found for {repo}:{path} – was the file moved?")

    last_sha = page_state.get("sha")
    page_state["sha"] = commits[0]["sha"]
    if last_sha is None:
        print(f"  Baseline set to {commits[0]['sha'][:7]}")
        return None

    shas = [c["sha"] for c in commits]
    if TEST_REWIND:
        last_sha = shas[min(TEST_REWIND, len(shas) - 1)]
    # Last seen SHA not among the latest 30 commits (e.g. force push or a large number of commits)
    missed = last_sha not in shas
    new = commits if missed else commits[: shas.index(last_sha)]
    if not new:
        return None

    new = list(reversed(new))  # oldest first
    patches, commit_infos = [], []
    for c in new:
        detail = gh_get(f"{GITHUB_API}/repos/{repo}/commits/{c['sha']}").json()
        for f in detail.get("files", []):
            if f["filename"] == path or f.get("previous_filename") == path:
                patch = f.get("patch") or "(Diff too large – GitHub returns no patch; see commit link)"
                patches.append(f"### Commit {c['sha'][:7]}: {first_line(c['commit']['message'])}\n{patch}")
        commit_infos.append(
            {
                "sha": c["sha"],
                "message": first_line(c["commit"]["message"]),
                "url": c["html_url"],
                "date": c["commit"]["committer"]["date"],
            }
        )
    change = Change(page=page, diff="\n\n".join(patches), commits=commit_infos)
    if missed:
        change.note = T["missed"]
    return change


def first_line(s: str) -> str:
    return s.strip().splitlines()[0] if s.strip() else ""


# --------------------------------------------------------------------------- learn source


def learn_page_text(url: str) -> str:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"  # Learn serves UTF-8; otherwise requests guesses ISO-8859-1
    soup = BeautifulSoup(r.text, "html.parser")
    main = soup.select_one("main")
    if main is None:
        raise RuntimeError(f"No <main> found on {url} – page layout changed?")
    blocks = main.select("div.content") or [main]

    for block in blocks:
        for tag in block.select("script, style, button, form, nav, .feedback-section, .display-none"):
            tag.decompose()
        for level in range(1, 7):
            for h in block.find_all(f"h{level}"):
                h.insert_before("\n" + "#" * level + " ")
                h.insert_after("\n")
        for li in block.find_all("li"):
            li.insert_before("\n- ")
        for row in block.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
            row.replace_with("\n| " + " | ".join(cells) + " |\n")
        for p in block.find_all(["p", "div"]):
            p.insert_after("\n")

    text = "\n".join(b.get_text("") for b in blocks)
    lines = [re.sub(r"[ \t\xa0]+", " ", ln).strip() for ln in text.splitlines()]
    out, blank = [], False
    for ln in lines:
        if not ln:
            if not blank and out:
                out.append("")
            blank = True
        else:
            out.append(ln)
            blank = False
    return "\n".join(out).strip() + "\n"


def check_learn(page: dict, page_state: dict) -> Change | None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snap = SNAPSHOT_DIR / f"{page['id']}.md"
    current = learn_page_text(page["url"])
    if not snap.exists():
        if not DRY_RUN:
            snap.write_text(current, encoding="utf-8")
        print("  Baseline snapshot saved")
        return None
    previous = snap.read_text(encoding="utf-8")
    if previous == current:
        return None
    diff = "".join(
        difflib.unified_diff(
            previous.splitlines(keepends=True),
            current.splitlines(keepends=True),
            fromfile="previous",
            tofile="current",
            n=3,
        )
    )
    if not DRY_RUN:
        snap.write_text(current, encoding="utf-8")
    return Change(page=page, diff=diff)


# --------------------------------------------------------------------------- claude summary

KINDS = ["new", "changed", "removed", "clarified"]
KIND_ICON = {"new": "🆕", "changed": "✏️", "removed": "🗑️", "clarified": "ℹ️"}

SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "relevant": {
            "type": "boolean",
            "description": "true if the substance of deprecations/retirements/dates/impact has changed",
        },
        "headline": {
            "type": "string",
            "description": "Key message for the issue title, max. ~10 words, without the page name",
        },
        "items": {
            "type": "array",
            "description": "One entry per substantively relevant change; empty if not relevant",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "enum": KINDS},
                    "feature": {"type": "string", "description": "Affected feature/product, short"},
                    "date": {"type": "string", "description": "Next actionable date (removal/end of support takes precedence over announcement date), " + T["date_format"] + "; empty if none is given"},
                    "impact": {"type": "string", "description": "What changes / what goes away, 1 sentence"},
                    "action": {"type": "string", "description": "Recommended action or replacement, 1 sentence; empty if none"},
                },
                "required": ["kind", "feature", "date", "impact", "action"],
                "additionalProperties": False,
            },
        },
        "editorial": {
            "type": "string",
            "description": "Purely editorial changes summarized in one short sentence, empty if none",
        },
    },
    "required": ["relevant", "headline", "items", "editorial"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You monitor Microsoft Learn pages about deprecations for a \
Dynamics 365 / Power Platform consultant. You receive the diff of a page since the last check. \
The result is sent as a GitHub issue by email and must be graspable within a few seconds.

Decide whether the change is substantively relevant:
- relevant: new deprecation or retirement, changed/new dates, changed scope or \
impact, new or changed replacement feature, required actions, removed entries, \
clarifications that change the meaning.
- not relevant: typos, rewording without change in meaning, formatting, \
link/anchor fixes, metadata (ms.date, author, ms.reviewer), translation or style fixes.

Write in {language}, concise and factual. Keep product and feature names exactly as Microsoft spells them \
(do not translate them). Do not invent anything that is not in the diff. Non-relevant parts belong only \
in "editorial".""".format(language=T["language"])


def fallback_summary(ch: Change, reason: str) -> None:
    ch.relevant = True
    ch.headline = f"{T['change_detected']} ({reason})"
    ch.items = []
    ch.editorial = ""


def summarize(changes: list[Change]) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set – no AI summary, all changes are treated as relevant.")
        for ch in changes:
            fallback_summary(ch, T["no_ai"])
        return

    import anthropic

    client = anthropic.Anthropic()
    for ch in changes:
        diff = ch.diff
        truncated = len(diff) > MAX_DIFF_CHARS_FOR_CLAUDE
        if truncated:
            diff = diff[:MAX_DIFF_CHARS_FOR_CLAUDE]
        commit_lines = "\n".join(f"- {c['date']} {c['message']}" for c in ch.commits) or "(Learn snapshot, no commits)"
        user = (
            f"Page: {ch.page['name']}\nURL: {ch.page['url']}\n\nCommits:\n{commit_lines}\n\n"
            + ("NOTE: The diff was truncated because of its size.\n\n" if truncated else "")
            + f"Diff:\n```diff\n{diff}\n```"
        )
        try:
            response = client.beta.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=16000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user}],
                output_config={"format": {"type": "json_schema", "schema": SUMMARY_SCHEMA}},
                betas=["server-side-fallback-2026-07-01"],
                extra_body={"fallbacks": "default"},
            )
            if response.stop_reason == "refusal":
                raise RuntimeError("Request was refused (refusal)")
            text = "".join(b.text for b in response.content if b.type == "text")
            data = json.loads(text)
            ch.relevant = bool(data["relevant"])
            ch.headline = data["headline"].strip().rstrip(".")
            ch.items = data["items"]
            ch.editorial = data["editorial"].strip()
        except Exception as e:  # the summary is optional – when in doubt, rather report the change
            print(f"  Claude summary for {ch.page['id']} failed: {e}")
            fallback_summary(ch, T["ai_failed"])
        if truncated:
            ch.note = (ch.note + " " if ch.note else "") + T["truncated"]


# --------------------------------------------------------------------------- report


def diff_link(ch: Change, today: str) -> str:
    return f"https://github.com/{REPORT_REPO}/blob/main/reports/{today}/{ch.page['id']}.diff"


def issue_title(ch: Change) -> str:
    return f"{ch.page.get('short', ch.page['name'])}: {ch.headline}"


def issue_body(ch: Change, today: str) -> str:
    """Compact and email-friendly: no embedded diff (<details> does not collapse in emails)."""
    parts = []
    if ch.note:
        parts.append(f"> ⚠️ {ch.note}\n")
    for it in ch.items:
        icon = KIND_ICON.get(it["kind"], "•")
        kind = T["kinds"].get(it["kind"], it["kind"].capitalize())
        meta = f"**{kind}**" + (f" · **{T['date']}: {it['date']}**" if it["date"] else "")
        lines = [f"### {icon} {it['feature']}", meta, "", it["impact"]]
        if it["action"]:
            lines += ["", f"➡️ {it['action']}"]
        parts.append("\n".join(lines) + "\n")
    if not ch.items:  # fallback without AI: commit titles as a pointer
        parts.append("\n".join(f"- {c['message']}" for c in ch.commits) or f"- {T['page_changed']}")
        parts.append("")
    if ch.editorial:
        parts.append(f"*{T['editorial']}:* {ch.editorial}\n")

    links = [f"[{T['learn_page']}]({ch.page['url']})", f"[Diff]({diff_link(ch, today)})"]
    links += [f"[`{c['sha'][:7]}`]({c['url']})" for c in ch.commits]
    parts.append("---\n" + " · ".join(links))
    return "\n".join(parts)


def write_diff_file(ch: Change, today: str) -> None:
    path = REPORTS_DIR / today / f"{ch.page['id']}.diff"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ch.diff + "\n", encoding="utf-8", newline="\n")


def gh_headers() -> dict:
    return {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}


def ensure_label(name: str, color: str, description: str) -> None:
    r = session.post(
        f"{GITHUB_API}/repos/{REPORT_REPO}/labels",
        headers=gh_headers(),
        json={"name": name, "color": color, "description": description},
        timeout=30,
    )
    if r.status_code not in (201, 422):  # 422 = already exists
        r.raise_for_status()


def create_issue(title: str, body: str, labels: list[str]) -> str:
    ensure_label(ISSUE_LABEL, "d93f0b", "Automated deprecation report")
    for label in labels:
        if label != ISSUE_LABEL:
            ensure_label(label, "0e8a16", "Product area")
    r = session.post(
        f"{GITHUB_API}/repos/{REPORT_REPO}/issues",
        headers=gh_headers(),
        json={"title": title, "body": body, "labels": labels},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["html_url"]


def publish(title: str, body: str, labels: list[str]) -> None:
    write_job_summary(f"## {title}\n\n{body}\n")
    if DRY_RUN or not (GITHUB_TOKEN and REPORT_REPO):
        print(f"\n=== {title} ===\n{body}")
    else:
        print("Issue created:", create_issue(title, body, labels))


def write_job_summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")


# --------------------------------------------------------------------------- main


def main() -> int:
    watchlist = yaml.safe_load((ROOT / "watchlist.yml").read_text(encoding="utf-8"))
    state = load_state()
    pages_state = state.setdefault("pages", {})

    changes: list[Change] = []
    errors: list[str] = []
    for page in watchlist["pages"]:
        print(f"Checking {page['id']} ({page['source']}) …")
        page_state = pages_state.setdefault(page["id"], {})
        try:
            if page["source"] == "github":
                ch = check_github(page, page_state)
            elif page["source"] == "learn":
                ch = check_learn(page, page_state)
            else:
                raise ValueError(f"Unknown source '{page['source']}'")
        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append(f"[{page['name']}]({page['url']}): {e}")
            continue
        if ch:
            print(f"  Change detected ({len(ch.commits)} commits, {len(ch.diff)} chars of diff)")
            changes.append(ch)

    if changes:
        summarize(changes)
    relevant = [c for c in changes if c.relevant]
    trivial = [c for c in changes if not c.relevant]

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    state["last_run"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for ch in relevant:
        if not DRY_RUN:
            write_diff_file(ch, today)
        labels = [ISSUE_LABEL] + ([ch.page["short"]] if ch.page.get("short") else [])
        publish(issue_title(ch), issue_body(ch, today), labels)

    if errors:
        publish(f"Deprecation Watch {today}: {T['errors_title']}", "\n".join(f"- {e}" for e in errors), [ISSUE_LABEL])

    if trivial:
        lines = "\n".join(f"- {c.page.get('short', c.page['name'])}: {c.headline}" for c in trivial)
        print(f"Not substantively relevant (no issue):\n{lines}")
        write_job_summary(f"**Not substantively relevant (no issue):**\n\n{lines}\n")
    if not relevant and not errors:
        print("No relevant changes.")
        write_job_summary("No relevant changes.")

    if not DRY_RUN:
        save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
