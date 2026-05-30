"""
Build the Bay Area trip planner.
Reads events.json + app.html, injects data, writes index.html.

Usage: python3 build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
EVENTS_PATH = ROOT / "events.json"
TEMPLATE_PATH = ROOT / "app.html"
OUTPUT_PATH = ROOT / "index.html"

with EVENTS_PATH.open() as f:
    events = json.load(f)

# No mock friends. The "interested" stack starts empty — only the real user's
# own interest shows, until a shared backend is wired up (see CLAUDE.md).
friends = []
friend_interests = {}

events_json = json.dumps(events, separators=(",", ":"), ensure_ascii=False)
friends_json = json.dumps(friends, separators=(",", ":"), ensure_ascii=False)
friend_interests_json = json.dumps(friend_interests, separators=(",", ":"), ensure_ascii=False)

template = TEMPLATE_PATH.read_text()
html = (template
        .replace("__EVENTS_DATA__", events_json)
        .replace("__FRIENDS_DATA__", friends_json)
        .replace("__FRIEND_INTERESTS_DATA__", friend_interests_json))

OUTPUT_PATH.write_text(html)

print(f"✓ Wrote {OUTPUT_PATH.name} ({len(html):,} bytes)")
print(f"  {len(events)} events · {sum(1 for e in events if e.get('start') and not e.get('anytime'))} dated · {sum(1 for e in events if e.get('anytime'))} anytime")
