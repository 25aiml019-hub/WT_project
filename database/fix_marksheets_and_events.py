import json
import pymysql
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_JSON_FILE = BASE_DIR / "public" / "assets" / "data" / "events.json"

conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub")
cur = conn.cursor(pymysql.cursors.DictCursor)

print("1. Updating marksheets table status ENUM...")
cur.execute("ALTER TABLE marksheets MODIFY COLUMN status ENUM('pending','extracted','confirmed','verified','rejected') NOT NULL DEFAULT 'extracted'")

print("2. Updating events table status ENUM and fields...")
cur.execute("ALTER TABLE events MODIFY COLUMN status ENUM('upcoming','ongoing','completed','cancelled','closed') NOT NULL DEFAULT 'upcoming'")
cur.execute("ALTER TABLE events MODIFY COLUMN event_time VARCHAR(60) NULL DEFAULT NULL")
cur.execute("ALTER TABLE events MODIFY COLUMN location VARCHAR(150) NOT NULL DEFAULT 'CHARUSAT Campus'")

# Check columns of events
cur.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'events' AND table_schema = 'studenthub'")
cols = [r['COLUMN_NAME'] for r in cur.fetchall()]

if 'max_participants' not in cols:
    cur.execute("ALTER TABLE events ADD COLUMN max_participants INT NOT NULL DEFAULT 100 AFTER location")
    print("Added max_participants to events")

if 'registration_deadline' not in cols:
    cur.execute("ALTER TABLE events ADD COLUMN registration_deadline DATE NULL DEFAULT NULL AFTER event_date")
    print("Added registration_deadline to events")

print("3. Syncing all 16 events from events.json into MySQL...")
with open(EVENTS_JSON_FILE, "r", encoding="utf-8") as f:
    events_data = json.load(f)

for ev in events_data:
    ev_id = int(ev['id'])
    title = ev['title']
    desc = ev.get('description', '')
    cat = ev.get('category', 'General')
    date_str = ev.get('date', '2026-10-31')
    time_str = ev.get('time', '10:00 AM')
    loc = ev.get('venue', ev.get('location', 'CHARUSAT Campus'))
    status_raw = ev.get('status', 'Upcoming').lower()
    if status_raw not in ['upcoming', 'ongoing', 'completed', 'cancelled', 'closed']:
        status_raw = 'upcoming'
    
    # Calculate registration deadline (same as event date)
    deadline = date_str

    # Upsert event
    cur.execute("""
        INSERT INTO events (id, title, description, category, event_date, registration_deadline, event_time, location, max_participants, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 100, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            description = VALUES(description),
            category = VALUES(category),
            event_date = VALUES(event_date),
            registration_deadline = VALUES(registration_deadline),
            event_time = VALUES(event_time),
            location = VALUES(location),
            status = VALUES(status)
    """, (ev_id, title, desc, cat, date_str, deadline, time_str, loc, status_raw))

conn.commit()

cur.execute("SELECT COUNT(*) AS c FROM events")
total_events = cur.fetchone()['c']
print(f"Total events in database: {total_events}")

cur.execute("SELECT id, title, event_date, status FROM events ORDER BY id ASC")
for r in cur.fetchall():
    print(f"  Event #{r['id']}: {r['title']} | Date: {r['event_date']} | Status: {r['status']}")

conn.close()
print("Events sync and schema update completed successfully!")
