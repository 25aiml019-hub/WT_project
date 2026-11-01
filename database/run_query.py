import sys
import pymysql

query = sys.argv[1] if len(sys.argv) > 1 else ""
if not query:
    print("No query provided")
    sys.exit(1)

conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub")
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute(query)
if query.strip().upper().startswith("SELECT"):
    for row in cur.fetchall():
        print(row)
else:
    conn.commit()
    print(f"Affected rows: {cur.rowcount}")
conn.close()
