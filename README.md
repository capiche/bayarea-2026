# Bay Area Summer & Fall 2026

A trip planner / event guide for the Bay Area, shared with my friend group.

Live: _(add Vercel URL once deployed)_

## Deploy

```bash
./deploy.sh "What changed"
```

That's it. Runs the build, commits, pushes to GitHub, Vercel deploys within 30 seconds.

## Local development

```bash
python3 build.py    # regenerates index.html from events.json + app.html
open index.html     # preview in default browser
```

## Project layout

| File | What it is |
| --- | --- |
| `events.json` | All event data (296 entries). Single source of truth. |
| `app.html` | The page template — HTML/CSS/JS with `__EVENTS_DATA__` placeholders. |
| `build.py` | Generates `index.html` by injecting data into `app.html`. |
| `index.html` | The built site. Committed — Vercel serves this. |
| `deploy.sh` | Build + commit + push. |
| `CLAUDE.md` | Project context for Claude Code. |

## Working with Claude Code

This project has a `CLAUDE.md` with the full schema, file map, and common tasks. Open this folder in Claude Code and it'll pick up the context automatically. Good prompts:

- "Add three more events to events.json: <details>"
- "Change the page header color from blue to teal"
- "Tag these five events as concert in events.json"
- "Build and show me what changed in the output"
