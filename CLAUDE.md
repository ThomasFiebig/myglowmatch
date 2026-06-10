# Start-Konvention myglowmatch

**IMMER aus diesem Verzeichnis starten:**
```
cd ~/Projekte/myglowmatch && claude
```

Alles liegt hier: Git-Repo, Daten, Backups, Credentials, Session-Archiv, Memory-Kontext.

## Wo was liegt

| Pfad | Inhalt |
|---|---|
| `~/Projekte/myglowmatch/` | Git-Repo: Next.js-Code, `test_suite.py`, `inspect_workflow.py`, `sheets_writer.py`, `HANDOVER.md`, `.env` |
| `~/Projekte/myglowmatch/chat-archive/` | Session-Dokus (jüngste: `2026-06-10_session.md`) |
| `~/Projekte/myglowmatch/produktdatenblaetter/` | 37 MONAT-PDFs (Provenienz-Quelle für Audits) |
| `~/Projekte/myglowmatch/backups/` | CSV-Backups vor Sheet-Edits |
| `~/Projekte/myglowmatch/credentials/` | Service-Account-Key für Google Sheets (gitignored) |
| `~/Projekte/myglowmatch/map_*.csv` | Sheet-Import-Vorlagen aus den 5 Migrationen |

## Wiedereinstieg

Standard-Prompt nach Start:

> Lies `chat-archive/<JJJJ-MM-TT>_session.md` der letzten Session. Sag mir den Stand und empfiehl, was wir als Nächstes machen.

`HANDOVER.md` im Git-Repo gibt die Faktografie (Workflow-Nodes, Sheet-Tabs, Migrationsstand, Konventionen, offene Punkte). Memory (User-Profil, Stil, Projekt-Kontext, MONAT-Datenblätter-Referenz, npm-Quirk) wird beim Start automatisch geladen.
