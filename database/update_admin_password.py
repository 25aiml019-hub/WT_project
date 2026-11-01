import pymysql
import json
import subprocess
import datetime
import os

# Connect to Antigravity MySQL database on Port 3307
conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='', database='studenthub', autocommit=True)
cur = conn.cursor(pymysql.cursors.DictCursor)

# 1. Inspect existing admin record
cur.execute("SELECT * FROM users WHERE username = 'admin'")
admin_records = cur.fetchall()
print(f"Found {len(admin_records)} admin record(s).")
if len(admin_records) != 1:
    raise RuntimeError(f"Expected exactly 1 admin record, found {len(admin_records)}")

admin = admin_records[0]
print("Current admin data before modification:")
print(admin)

# 2. Create backup before modification
os.makedirs("database/backups", exist_ok=True)
backup_sql_path = "database/backups/admin_backup_pre_admin123.sql"
backup_json_path = "database/backups/admin_backup_pre_admin123.json"

# Write SQL backup
with open(backup_sql_path, "w", encoding="utf-8") as f:
    f.write("-- StudentHub Admin Account Backup\n")
    f.write(f"-- Created: {datetime.datetime.now().isoformat()}\n")
    f.write("USE `studenthub`;\n")
    vals = [
        str(admin['id']),
        repr(admin['username']),
        repr(admin['email']),
        repr(admin['password']),
        repr(admin['role']),
        repr(admin['status']),
        str(admin.get('must_change_password', 0))
    ]
    f.write(f"INSERT INTO `users` (`id`, `username`, `email`, `password`, `role`, `status`, `must_change_password`) VALUES ({', '.join(vals)}) ON DUPLICATE KEY UPDATE password = VALUES(password);\n")

# Write JSON backup
def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

with open(backup_json_path, "w", encoding="utf-8") as f:
    json.dump(admin, f, default=json_serial, indent=2)

print(f"Backup created at {backup_sql_path} and {backup_json_path}")

# 3. Generate secure PHP-compatible bcrypt hash for 'admin123'
php_cmd = "echo password_hash('admin123', PASSWORD_BCRYPT, ['cost' => 10]);"
res = subprocess.run(["C:\\xampp\\php\\php.exe", "-r", php_cmd], capture_output=True, text=True, check=True)
new_hash = res.stdout.strip()
print(f"Generated secure bcrypt hash for 'admin123': {new_hash}")

# 4. Update the actual admin account password in the database
cur.execute("UPDATE users SET password = %s, updated_at = NOW() WHERE username = 'admin'", (new_hash,))
print("Updated admin password in database.")

# 5. Verification checks
cur.execute("SELECT * FROM users WHERE username = 'admin'")
updated_admin_records = cur.fetchall()
if len(updated_admin_records) != 1:
    raise RuntimeError("Integrity check failed: duplicate admin account detected!")

updated_admin = updated_admin_records[0]
print("Updated admin user record:")
print(updated_admin)

# Verify with PHP password_verify
verify_php = f"""
$hash = '{updated_admin['password']}';
echo 'matches_admin123:' . (password_verify('admin123', $hash) ? 'YES' : 'NO') . PHP_EOL;
echo 'matches_123:' . (password_verify('123', $hash) ? 'YES' : 'NO') . PHP_EOL;
"""
res2 = subprocess.run(["C:\\xampp\\php\\php.exe", "-r", verify_php], capture_output=True, text=True, check=True)
print("PHP password verification:")
print(res2.stdout)

# Verify student accounts remain intact
cur.execute("SELECT count(*) as cnt FROM students WHERE student_id IS NOT NULL")
stu_cnt = cur.fetchone()['cnt']
print(f"Total AIML student roster count: {stu_cnt} (Must be 78)")
assert stu_cnt == 78, f"Student count changed! Expected 78, got {stu_cnt}"

conn.close()
print("Database admin password update completed successfully.")
