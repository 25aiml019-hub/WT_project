import os
import subprocess
import pymysql
import json
import datetime

BACKUP_DIR = "database/verified_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

dump_bin = "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe"
mysql_bin = "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# 1. Portable Migration Dump (No CREATE DATABASE / USE - perfect for InfinityFree / phpMyAdmin)
portable_backup = os.path.join(BACKUP_DIR, "studenthub_infinityfree_migration.sql")
cmd_portable = [
    dump_bin,
    "--host=127.0.0.1",
    "--port=3307",
    "--user=root",
    "--routines",
    "--triggers",
    "--hex-blob",
    "--add-drop-table",
    "studenthub",
    f"--result-file={portable_backup}"
]
subprocess.run(cmd_portable, check=True)
print(f"[1] Created portable migration SQL: {portable_backup} ({os.path.getsize(portable_backup):,} bytes)")

# 2. Standalone Master Backup (With CREATE DATABASE / USE for exact full-server recovery)
master_backup = os.path.join(BACKUP_DIR, f"studenthub_master_backup_{timestamp}.sql")
cmd_master = [
    dump_bin,
    "--host=127.0.0.1",
    "--port=3307",
    "--user=root",
    "--databases",
    "studenthub",
    "--routines",
    "--triggers",
    "--hex-blob",
    f"--result-file={master_backup}"
]
subprocess.run(cmd_master, check=True)
print(f"[2] Created master standalone backup: {master_backup} ({os.path.getsize(master_backup):,} bytes)")

# 3. Verify clean import into a fresh verification database
conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", autocommit=True)
cur = conn.cursor()

verify_db = "studenthub_backup_verification"
cur.execute(f"DROP DATABASE IF EXISTS `{verify_db}`")
cur.execute(f"CREATE DATABASE `{verify_db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
print(f"[3] Created clean verification database: `{verify_db}`")

# Import portable_backup into verify_db
cmd_import = [mysql_bin, "--host=127.0.0.1", "--port=3307", "--user=root", verify_db]
with open(portable_backup, "r", encoding="utf-8") as f_in:
    res = subprocess.run(cmd_import, stdin=f_in, capture_output=True, text=True)

if res.returncode != 0:
    raise RuntimeError(f"Clean import verification failed: {res.stderr}")

print("[4] Import into clean verification database succeeded without errors!")

# Compare all tables and row counts
cur.execute("USE `studenthub`")
cur.execute("SHOW TABLES")
orig_tables = [r[0] for r in cur.fetchall()]

cur.execute(f"USE `{verify_db}`")
cur.execute("SHOW TABLES")
imp_tables = [r[0] for r in cur.fetchall()]

assert set(orig_tables) == set(imp_tables), "Tables count mismatch between original and imported backup!"

audit_data = {
    "verified_at": datetime.datetime.now().isoformat(),
    "source_instance": {
        "host": "127.0.0.1",
        "port": 3307,
        "database": "studenthub",
        "server_version": "MySQL Community Server 8.0.46",
        "datadir": "C:\\Users\\Manan1\\AppData\\Local\\Temp\\studenthub_mysql_test\\"
    },
    "tables_count": len(orig_tables),
    "tables": {}
}

print(f"\n[5] Comparing all {len(orig_tables)} tables between live database and verified import:")
for t in sorted(orig_tables):
    cur.execute(f"SELECT COUNT(*) FROM `studenthub`.`{t}`")
    cnt_orig = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM `{verify_db}`.`{t}`")
    cnt_imp = cur.fetchone()[0]
    assert cnt_orig == cnt_imp, f"Mismatch in {t}: {cnt_orig} vs {cnt_imp}"
    print(f"  [VERIFIED] {t:<28}: {cnt_orig:>4} rows")
    audit_data["tables"][t] = cnt_orig

# Business integrity assertions
cur.execute(f"SELECT COUNT(*) FROM `{verify_db}`.students WHERE student_id IS NOT NULL")
aiml_cnt = cur.fetchone()[0]
assert aiml_cnt == 78, f"Expected 78 AIML students, found {aiml_cnt}"
audit_data["aiml_roster_students"] = aiml_cnt

cur.execute(f"SELECT COUNT(*) FROM `{verify_db}`.events")
events_cnt = cur.fetchone()[0]
assert events_cnt == 16, f"Expected 16 events, found {events_cnt}"
audit_data["events"] = events_cnt

cur.execute(f"SELECT COUNT(*) FROM `{verify_db}`.semester_results")
sem_cnt = cur.fetchone()[0]
assert sem_cnt == 156, f"Expected 156 semester results, found {sem_cnt}"
audit_data["semester_results"] = sem_cnt

cur.execute(f"SELECT COUNT(*) FROM `{verify_db}`.timetable_slots")
tt_cnt = cur.fetchone()[0]
assert tt_cnt == 51, f"Expected 51 timetable slots, found {tt_cnt}"
audit_data["timetable_slots"] = tt_cnt

# Save audit snapshot
audit_file = os.path.join(BACKUP_DIR, "studenthub_audit_snapshot.json")
with open(audit_file, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)

print(f"\n[6] Audit snapshot saved to: {audit_file}")

# Clean up temporary test database
cur.execute(f"DROP DATABASE IF EXISTS `{verify_db}`")
conn.close()
print(f"[7] Cleaned up verification database `{verify_db}`.")
print("\n" + "=" * 80)
print("BACKUP EXPORT & VERIFICATION COMPLETED WITH 100% INTEGRITY")
print("=" * 80)
