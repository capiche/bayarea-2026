# Bay Area 2026 — Trip Planner

A single-page filterable event guide for Bay Area summer/fall 2026, deployed as a static site on Vercel and shared with a friend group.

## File map

- `index.html` — the built deliverable that Vercel serves. **Generated; do not edit directly.**
- `app.html` — the source template (HTML/CSS/JS). Has three placeholders: `__EVENTS_DATA__`, `__FRIENDS_DATA__`, `__FRIEND_INTERESTS_DATA__`.
- `events.json` — the single source of truth for events. ~296 entries.
- `build.py` — injects events + friends + interests into `app.html`, writes `index.html`.
- `deploy.sh` — one-command build + commit + push (triggers Vercel auto-deploy).
- `.wiki-cache.json` — cached Wikipedia image lookups, keyed by query. Persisted so re-running image scripts doesn't re-hit the API.

## How to deploy

```bash
./deploy.sh "What I changed"
```

That's it. The script runs `build.py`, commits anything changed, pushes to GitHub, and Vercel auto-deploys within ~30 seconds.

If you only want to test the build without deploying:
```bash
python3 build.py
open index.html  # or just refresh your browser
```

## Event schema

Each entry in `events.json` is:

```json
{
  "id": "stable-slug-bay",
  "name": "Outside Lands Music Festival",
  "region": "bayarea",
  "start": "2026-08-07",         // ISO date or null (null = anytime)
  "end": "2026-08-09",           // ISO date or null
  "dates_display": "Aug 7-9, 2026",
  "recurring_weekday": null,     // 0-6 (Sun-Sat) for weekly events; null otherwise
  "anytime": false,              // true for year-round venues
  "location": "Golden Gate Park, SF",
  "audience": "adults",          // "kids" | "adults" | "both"
  "category": "festive",         // "festive"|"outdoor"|"arts"|"kid"|"novel"|"food"|"getaway"
  "description": "Iconic SF music festival with...",
  "cost": "$$$",                 // "free"|"$"|"$$"|"$$$"
  "url": "https://sfoutsidelands.com/",
  "image_keywords": "outside lands festival",  // for Wikipedia image lookup
  "img": "https://upload.wikimedia.org/...",   // resolved image URL or null
  "show_type": "concert"         // "concert"|"comedy"|null — tagged for the Show filter
}
```

## Common tasks

### Add a new event
Open `events.json`, append an entry with all required fields, save, then `./deploy.sh "Added X"`. Use an existing similar entry as a template.

### Update event dates or text
Edit the entry in `events.json` directly. Don't touch `index.html`.

### Change the page header / title / colors
Edit `app.html` (CSS in `<style>` block, header HTML in the `.topbar` section). Then run build.

### Replace a fallback image
Add a real URL to the event's `img` field in `events.json`. If `img` is null, the app falls back to a category-themed Unsplash photo (defined in `app.html` as `CAT_FALLBACK_IMGS`).

### Add a new category, audience option, or show type
You'll need to update three places: (1) the option in `events.json` entries, (2) the filter chip in `app.html`'s `.filters` section, (3) the corresponding `CAT_LABEL`/`AUD_LABEL`/`CAT_GRADIENT`/`CAT_EMOJI` maps in the `<script>` block.

### Tag more events as concert/comedy
The tagging was done by a one-off Python script. To re-tag (e.g. after adding new events), the rules live in the conversation history but can also be added here. Simplest path: hand-edit the `show_type` field on new events.

### Change mock friends
Edit the `friends` and `profiles` arrays in `build.py`. Run build.

## Deploy stack

- **Hosting**: Vercel (free tier — 100GB/month bandwidth, more than enough)
- **Source**: GitHub repo, auto-deploys on every push to `main`
- **State**: localStorage in each user's browser (interests, done, profile, custom events)

## What's not yet built

- **Shared interests across friends.** Currently each browser is its own island; mock friends (Alex, Priya, Mira, Raj, Leo, Sara) are baked in for demo. To make interests sync, wire up Supabase or Vercel Postgres — write code reads/writes to a `interests` table keyed by event_id + user_id, replace the `state.myInterest` / `FRIEND_INTERESTS` localStorage code in `app.html`.
- **Custom events shared across friends.** Same fix — write `customEvents` to the same backend.

## Conventions

- ASCII single quotes in JSON, never smart quotes.
- ISO dates everywhere (`YYYY-MM-DD`). `dates_display` is freeform human text.
- `id` must be unique and stable — used as key for done/interest state in localStorage. If you rename an event, keep the id the same.
- Don't commit `node_modules`, `.vercel`, `__pycache__`, or `.DS_Store` (`.gitignore` handles these).
- `index.html` IS committed — Vercel serves it. Don't add it to gitignore.
