"""
Build the Bay Area trip planner.
Reads events.json + app.html, injects data, writes index.html.

Usage: python3 build.py
"""
import json, random
from pathlib import Path

ROOT = Path(__file__).parent
EVENTS_PATH = ROOT / "events.json"
TEMPLATE_PATH = ROOT / "app.html"
OUTPUT_PATH = ROOT / "index.html"

with EVENTS_PATH.open() as f:
    events = json.load(f)

# Mock friends shown in the "interested" stack so the social UI is populated
# out of the box. Real friends would replace these once a backend is wired up.
random.seed(42)
friends = [
    {"id": "alex",   "name": "Alex",   "emoji": "🦊", "color": "#f59e0b"},
    {"id": "priya",  "name": "Priya",  "emoji": "🌸", "color": "#ec4899"},
    {"id": "mira",   "name": "Mira",   "emoji": "🌟", "color": "#8b5cf6"},
    {"id": "raj",    "name": "Raj",    "emoji": "🎨", "color": "#06b6d4"},
    {"id": "leo",    "name": "Leo",    "emoji": "🐧", "color": "#3b82f6"},
    {"id": "sara",   "name": "Sara",   "emoji": "🌻", "color": "#f97316"},
]

def pick_for(audience, n):
    pool = [e for e in events
            if audience == "any" or e["audience"] == audience or e["audience"] == "both"]
    return random.sample(pool, min(n, len(pool)))

profiles = [
    ("alex",   "adults", 10),
    ("priya",  "any",     8),
    ("mira",   "kids",    9),
    ("raj",    "adults",  8),
    ("leo",    "kids",    7),
    ("sara",   "adults",  9),
]
friend_interests = {}
for fid, aud, n in profiles:
    friend_interests.setdefault(fid, [])
    for e in pick_for(aud, n):
        if e["id"] not in friend_interests[fid]:
            friend_interests[fid].append(e["id"])

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
