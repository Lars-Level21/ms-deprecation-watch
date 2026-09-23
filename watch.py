"""Täglicher Check der Microsoft-Deprecation-Seiten aus watchlist.yml.

- source "github": neue Commits auf die Markdown-Datei seit der zuletzt gesehenen SHA
- source "learn":  Text-Snapshot der gerenderten Learn-Seite gegen den gespeicherten vergleichen

Änderungen werden (optional) von Claude zusammengefasst und nach Relevanz gefiltert.
Pro Seite mit relevanten Änderungen wird ein GitHub Issue im eigenen Repo angelegt;
der vollständige Diff liegt unter reports/ und ist im Issue verlinkt.
Der Zustand liegt in state/ und wird vom Workflow zurück ins Repo committed.
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
REPORTS_DIR = ROOT / "reports"  # vollständige Diffs, im Issue verlinkt

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPORT_REPO = os.environ.get("GITHUB_REPOSITORY", "")  # owner/name, von Actions gesetzt
# Testmodus: GitHub-Quellen so behandeln, als wäre der letzte Check N Commits her. Erzwingt DRY_RUN.
TEST_REWIND = int(os.environ.get("TEST_REWIND") or 0)
DRY_RUN = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes") or TEST_REWIND > 0
ISSUE_LABEL = "deprecation-watch"

CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL") or "claude-opus-5"  # leere Repo-Variable -> Default
# Obergrenze für den Diff, der an Claude geht. Größere Diffs werden gekürzt – das wird im
# Prompt und im Issue ausgewiesen, damit nichts stillschweigend verloren geht.
MAX_DIFF_CHARS_FOR_CLAUDE = 150_000

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
        raise RuntimeError(f"Keine Commits für {repo}:{path} gefunden – wurde die Datei verschoben?")

    last_sha = page_state.get("sha")
    page_state["sha"] = commits[0]["sha"]
    if last_sha is None:
        print(f"  Baseline gesetzt auf {commits[0]['sha'][:7]}")
        return None

    shas = [c["sha"] for c in commits]
    if TEST_REWIND:
        last_sha = shas[min(TEST_REWIND, len(shas) - 1)]
    # Zuletzt gesehene SHA nicht unter den letzten 30 Commits (z. B. Force-Push oder sehr viele Commits)
    missed = last_sha not in shas
    new = commits if missed else commits[: shas.index(last_sha)]
    if not new:
        return None

    new = list(reversed(new))  # älteste zuerst
    patches, commit_infos = [], []
    for c in new:
        detail = gh_get(f"{GITHUB_API}/repos/{repo}/commits/{c['sha']}").json()
        for f in detail.get("files", []):
            if f["filename"] == path or f.get("previous_filename") == path:
                patch = f.get("patch") or "(Diff zu groß – GitHub liefert keinen Patch; siehe Commit-Link)"
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
        change.note = "Die zuletzt gesehene Version war nicht unter den letzten 30 Commits; gezeigt werden nur diese 30."
    return change


def first_line(s: str) -> str:
    return s.strip().splitlines()[0] if s.strip() else ""


# --------------------------------------------------------------------------- learn source


def learn_page_text(url: str) -> str:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"  # Learn liefert UTF-8; requests rät sonst ISO-8859-1
    soup = BeautifulSoup(r.text, "html.parser")
    main = soup.select_one("main")
    if main is None:
        raise RuntimeError(f"Kein <main> auf {url} gefunden – Seitenlayout geändert?")
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
        print("  Baseline-Snapshot gespeichert")
        return None
    previous = snap.read_text(encoding="utf-8")
    if previous == current:
        return None
    diff = "".join(
        difflib.unified_diff(
            previous.splitlines(keepends=True),
            current.splitlines(keepends=True),
            fromfile="gestern",
            tofile="heute",
            n=3,
        )
    )
    if not DRY_RUN:
        snap.write_text(current, encoding="utf-8")
    return Change(page=page, diff=diff)


# --------------------------------------------------------------------------- claude summary

KINDS = ["neu", "geändert", "entfernt", "klargestellt"]
KIND_ICON = {"neu": "🆕", "geändert": "✏️", "entfernt": "🗑️", "klargestellt": "ℹ️"}

SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "relevant": {
            "type": "boolean",
            "description": "true, wenn sich inhaltlich etwas an Abkündigungen/Retirements/Terminen/Auswirkungen geändert hat",
        },
        "headline": {
            "type": "string",
            "description": "Kernaussage für den Issue-Titel, max. ~10 Wörter, ohne Seitennamen",
        },
        "items": {
            "type": "array",
            "description": "Eine Zeile pro inhaltlich relevanter Änderung; leer, wenn nicht relevant",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "enum": KINDS},
                    "feature": {"type": "string", "description": "Betroffenes Feature/Produkt, kurz"},
                    "date": {"type": "string", "description": "Relevanter Termin (TT.MM.JJJJ oder 'MM/JJJJ'), leer wenn keiner genannt"},
                    "impact": {"type": "string", "description": "Was ändert sich / was fällt weg, 1 Satz"},
                    "action": {"type": "string", "description": "Empfohlene Maßnahme bzw. Ersatz, 1 Satz; leer wenn keine"},
                },
                "required": ["kind", "feature", "date", "impact", "action"],
                "additionalProperties": False,
            },
        },
        "editorial": {
            "type": "string",
            "description": "Rein redaktionelle Änderungen in einem kurzen Satz zusammengefasst, leer wenn keine",
        },
    },
    "required": ["relevant", "headline", "items", "editorial"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """Du überwachst Microsoft-Learn-Seiten zu Abkündigungen (Deprecations) für einen \
Dynamics-365-/Power-Platform-Berater. Du bekommst den Diff einer Seite seit dem letzten Check. \
Das Ergebnis wird als GitHub Issue per E-Mail verschickt und muss in wenigen Sekunden erfassbar sein.

Entscheide, ob die Änderung inhaltlich relevant ist:
- relevant: neue Abkündigung oder Retirement, geänderte/neue Termine, geänderter Umfang oder \
Auswirkungen, neue oder geänderte Ersatzfunktion, erforderliche Maßnahmen, entfernte Einträge, \
Klarstellungen, die die Bedeutung ändern.
- nicht relevant: Tippfehler, Formulierungen ohne Bedeutungsänderung, Formatierung, \
Link-/Anker-Korrekturen, Metadaten (ms.date, author, ms.reviewer), Übersetzungs- oder Stilkorrekturen.

Schreibe auf Deutsch, knapp und sachlich. Englische Produkt- und Featurenamen bleiben englisch. \
Erfinde nichts, was nicht im Diff steht. Nicht relevante Anteile gehören nur in "editorial"."""


def fallback_summary(ch: Change, reason: str) -> None:
    ch.relevant = True
    ch.headline = f"Änderung erkannt ({reason})"
    ch.items = []
    ch.editorial = ""


def summarize(changes: list[Change]) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY nicht gesetzt – keine KI-Zusammenfassung, alle Änderungen gelten als relevant.")
        for ch in changes:
            fallback_summary(ch, "ohne KI-Zusammenfassung")
        return

    import anthropic

    client = anthropic.Anthropic()
    for ch in changes:
        diff = ch.diff
        truncated = len(diff) > MAX_DIFF_CHARS_FOR_CLAUDE
        if truncated:
            diff = diff[:MAX_DIFF_CHARS_FOR_CLAUDE]
        commit_lines = "\n".join(f"- {c['date']} {c['message']}" for c in ch.commits) or "(Learn-Snapshot, keine Commits)"
        user = (
            f"Seite: {ch.page['name']}\nURL: {ch.page['url']}\n\nCommits:\n{commit_lines}\n\n"
            + ("HINWEIS: Der Diff wurde wegen seiner Größe gekürzt.\n\n" if truncated else "")
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
                raise RuntimeError("Anfrage wurde abgelehnt (refusal)")
            text = "".join(b.text for b in response.content if b.type == "text")
            data = json.loads(text)
            ch.relevant = bool(data["relevant"])
            ch.headline = data["headline"].strip().rstrip(".")
            ch.items = data["items"]
            ch.editorial = data["editorial"].strip()
        except Exception as e:  # Zusammenfassung ist optional – im Zweifel lieber melden
            print(f"  Claude-Zusammenfassung für {ch.page['id']} fehlgeschlagen: {e}")
            fallback_summary(ch, "KI-Zusammenfassung fehlgeschlagen")
        if truncated:
            ch.note = (ch.note + " " if ch.note else "") + "Der Diff war sehr groß und wurde für die Zusammenfassung gekürzt."


# --------------------------------------------------------------------------- report


def diff_link(ch: Change, today: str) -> str:
    return f"https://github.com/{REPORT_REPO}/blob/main/reports/{today}/{ch.page['id']}.diff"


def issue_title(ch: Change) -> str:
    return f"{ch.page.get('short', ch.page['name'])}: {ch.headline}"


def issue_body(ch: Change, today: str) -> str:
    """Kompakt und mail-tauglich: kein eingebetteter Diff (<details> klappt in Mails nicht ein)."""
    parts = []
    if ch.note:
        parts.append(f"> ⚠️ {ch.note}\n")
    for it in ch.items:
        icon = KIND_ICON.get(it["kind"], "•")
        meta = f"**{it['kind'].capitalize()}**" + (f" · **Termin: {it['date']}**" if it["date"] else "")
        lines = [f"### {icon} {it['feature']}", meta, "", it["impact"]]
        if it["action"]:
            lines += ["", f"➡️ {it['action']}"]
        parts.append("\n".join(lines) + "\n")
    if not ch.items:  # Fallback ohne KI: Commit-Titel als Anhaltspunkt
        parts.append("\n".join(f"- {c['message']}" for c in ch.commits) or "- Seiteninhalt geändert")
        parts.append("")
    if ch.editorial:
        parts.append(f"*Außerdem redaktionell:* {ch.editorial}\n")

    links = [f"[Learn-Seite]({ch.page['url']})", f"[Diff]({diff_link(ch, today)})"]
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
    if r.status_code not in (201, 422):  # 422 = existiert bereits
        r.raise_for_status()


def create_issue(title: str, body: str, labels: list[str]) -> str:
    ensure_label(ISSUE_LABEL, "d93f0b", "Automatischer Deprecation-Report")
    for label in labels:
        if label != ISSUE_LABEL:
            ensure_label(label, "0e8a16", "Produktbereich")
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
        print("Issue angelegt:", create_issue(title, body, labels))


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
        print(f"Prüfe {page['id']} ({page['source']}) …")
        page_state = pages_state.setdefault(page["id"], {})
        try:
            if page["source"] == "github":
                ch = check_github(page, page_state)
            elif page["source"] == "learn":
                ch = check_learn(page, page_state)
            else:
                raise ValueError(f"Unbekannte source '{page['source']}'")
        except Exception as e:
            print(f"  FEHLER: {e}")
            errors.append(f"[{page['name']}]({page['url']}): {e}")
            continue
        if ch:
            print(f"  Änderung erkannt ({len(ch.commits)} Commits, {len(ch.diff)} Zeichen Diff)")
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
        publish(f"Deprecation-Watch {today}: Fehler beim Check", "\n".join(f"- {e}" for e in errors), [ISSUE_LABEL])

    if trivial:
        lines = "\n".join(f"- {c.page.get('short', c.page['name'])}: {c.headline}" for c in trivial)
        print(f"Ohne inhaltliche Relevanz (kein Issue):\n{lines}")
        write_job_summary(f"**Ohne inhaltliche Relevanz (kein Issue):**\n\n{lines}\n")
    if not relevant and not errors:
        print("Keine relevanten Änderungen.")
        write_job_summary("Keine relevanten Änderungen.")

    if not DRY_RUN:
        save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
