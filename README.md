# ms-deprecation-watch

Prüft täglich die Microsoft-Learn-Seiten zu Abkündigungen (Power Platform, Dynamics 365 CE,
Copilot Studio) und legt ein **GitHub Issue** an, wenn sich dort inhaltlich etwas getan hat.
GitHub benachrichtigt dich dann per Mail/App. An ruhigen Tagen kommt nichts.

## So funktioniert's

1. `watchlist.yml` listet die Seiten. Zwei Quelltypen:
   - `github`: neue Commits auf die Markdown-Datei im öffentlichen `MicrosoftDocs/*`-Repo
     (exakter Diff + Commit-Links). Als Merker dient die zuletzt gesehene Commit-SHA, deshalb
     gehen auch bei ausgefallenen Läufen keine Änderungen verloren.
   - `learn`: für Seiten ohne öffentliches Repo (z. B. Copilot Studio). Der Text der
     gerenderten Seite wird als Snapshot in `state/snapshots/` gespeichert und verglichen.
2. Claude (`claude-opus-5`) fasst jeden Diff auf Deutsch zusammen und filtert
   Kleinkram (Tippfehler, `ms.date`, Links, Formatierung) heraus.
3. Gibt es relevante Änderungen oder Fehler, wird ein Issue mit dem Label `deprecation-watch`
   angelegt. Es enthält Zusammenfassung, Commit-Links und den Diff zum Aufklappen.
4. Der Zustand (`state/`) wird vom Workflow zurück ins Repo committed. Durch den täglichen
   Commit bleibt der Repo aktiv, GitHub deaktiviert Schedules sonst nach 60 Tagen Inaktivität.

Beim **ersten Lauf** wird nur die Baseline gesetzt und kein Issue angelegt.

## Einrichtung

1. Secret `ANTHROPIC_API_KEY` anlegen (Settings → Secrets and variables → Actions).
   Ohne Key läuft alles weiter, dann aber ohne Zusammenfassung und Relevanzfilter.
2. Optional: Repo-Variable `CLAUDE_MODEL` setzen, um ein anderes Modell zu verwenden
   (z. B. `claude-sonnet-5`, günstiger).
3. Benachrichtigungen: Repo auf **Watch → All Activity** (oder Custom → Issues) stellen,
   damit neue Issues per Mail kommen.
4. Einmal manuell starten: Actions → *Deprecation Watch* → *Run workflow*
   (das setzt die Baseline).

## Seite hinzufügen

Auf der Learn-Seite den Bearbeiten-Stift anklicken. Er führt zur Datei im GitHub-Repo, daraus
`repo`, `branch` und `path` übernehmen. Führt der Link in ein privates `…-pr`-Repo,
das Suffix `-pr` weglassen und `main` statt `live` verwenden. Existiert kein öffentliches Repo,
`source: learn` verwenden.

## Lokal testen

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
DRY_RUN=1 .venv/Scripts/python watch.py
```

Mit `DRY_RUN=1` wird weder ein Issue angelegt noch der Zustand gespeichert.
