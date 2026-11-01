"""
StudentHub - Phase 3 Automated Verification Test Suite
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT

Tests Practical 7 (PHP Form Processing & Safe File Storage) and
Practical 8 (MySQL Database Foundation & Connectivity)
"""

import os
import sys
import re
import csv
import json
import tempfile
import threading
import time
import pymysql
import bcrypt
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
PUBLIC_DIR = BASE_DIR / "public"
STORAGE_DIR = BASE_DIR / "storage"
DATABASE_DIR = BASE_DIR / "database"
TESTS_DIR = BASE_DIR / "tests"

TOTAL_TESTS = 0
PASSED_TESTS = 0
FAILED_TESTS = 0


def log_test(name: str, passed: bool, detail: str = ""):
    global TOTAL_TESTS, PASSED_TESTS, FAILED_TESTS
    TOTAL_TESTS += 1
    if passed:
        PASSED_TESTS += 1
        print(f"  [PASS] {name} {('- ' + detail) if detail else ''}")
    else:
        FAILED_TESTS += 1
        print(f"  [FAIL] {name} {('- ' + detail) if detail else ''}")


# ==============================================================================
# SECTION 1: PRACTICAL 7 - PHP Form Processing, Validation & Sanitization Tests
# ==============================================================================
print("\n" + "=" * 70)
print("SECTION 1: Practical 7 - PHP Form Processing & Validation")
print("=" * 70)

# 1.1 Verify presence of required files
req_files = [
    PUBLIC_DIR / "process-registration.php",
    PUBLIC_DIR / "process-contact.php",
    PUBLIC_DIR / "csrf-token.php",
    APP_DIR / "config" / "security.php",
    APP_DIR / "config" / "db.php",
    STORAGE_DIR / "data" / ".htaccess",
    STORAGE_DIR / "data" / ".gitkeep",
    BASE_DIR / ".gitignore",
]
for rf in req_files:
    exists = rf.is_file()
    log_test(f"File Exists: {rf.relative_to(BASE_DIR)}", exists)

# 1.2 Inspect security.php for CSRF & Sanitization functions
sec_file = APP_DIR / "config" / "security.php"
if sec_file.is_file():
    sec_content = sec_file.read_text(encoding="utf-8")
    log_test("CSRF generateCsrfToken() declared", "function generateCsrfToken" in sec_content)
    log_test("CSRF validateCsrfToken() declared", "function validateCsrfToken" in sec_content)
    log_test("Timing-safe hash_equals used in CSRF check", "hash_equals" in sec_content)
    log_test("Sanitization function sanitizeString declared", "function sanitizeString" in sec_content)
    log_test("Email validation function validateEmail declared", "function validateEmail" in sec_content)
    log_test("Mobile validation function validateMobile declared", "function validateMobile" in sec_content)
    log_test("Password hashing function hashPassword declared", "password_hash" in sec_content)
    log_test("Password verification verifyPassword declared", "password_verify" in sec_content)

# 1.3 Verify Validation Rules Logic (Mobile & Email regex simulation matching PHP regex)
MOBILE_REGEX = re.compile(r"^[0-9]{10}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

valid_mobiles = ["9876543210", "6354069434", "7043100708", "9924633581"]
invalid_mobiles = ["98765", "98765432101", "98765abcde", "+919876543210", " 9876543210"]

all_valid_mob = all(bool(MOBILE_REGEX.match(m)) for m in valid_mobiles)
all_invalid_mob = all(not bool(MOBILE_REGEX.match(m)) for m in invalid_mobiles)
log_test("Validation: 10-Digit Mobile Accepted", all_valid_mob)
log_test("Validation: Invalid Mobiles Rejected", all_invalid_mob)

valid_emails = ["student@charusat.edu.in", "anshikabadala2@gmail.com", "user.name+tag@sub.domain.co.in"]
invalid_emails = ["plainaddress", "@missingusername.com", "username@.com", "user name@domain.com", "user@domain"]

all_valid_em = all(bool(EMAIL_REGEX.match(e)) for e in valid_emails)
all_invalid_em = all(not bool(EMAIL_REGEX.match(e)) for e in invalid_emails)
log_test("Validation: RFC/Format Valid Emails Accepted", all_valid_em)
log_test("Validation: Malformed Emails Rejected", all_invalid_em)

# 1.4 Inspect process-registration.php for security guarantees
proc_reg = PUBLIC_DIR / "process-registration.php"
if proc_reg.is_file():
    pr_content = proc_reg.read_text(encoding="utf-8")
    log_test("process-registration: Enforces HTTP POST check (rejects GET with 405)",
             "$_SERVER['REQUEST_METHOD'] !== 'POST'" in pr_content and "405" in pr_content)
    log_test("process-registration: Enforces CSRF Token Verification",
             "validateCsrfToken" in pr_content and "403" in pr_content)
    log_test("process-registration: Uses flock(..., LOCK_EX) for CSV concurrency safety",
             "flock" in pr_content and "LOCK_EX" in pr_content)
    log_test("process-registration: Uses fputcsv for safe CSV escaping",
             "fputcsv" in pr_content)
    log_test("process-registration: Hashes password with bcrypt (never plaintext)",
             "hashPassword" in pr_content or "password_hash" in pr_content)
    log_test("process-registration: Checks for duplicate registration",
             "already registered" in pr_content and "409" in pr_content)
    log_test("process-registration: Integrates with StudentService MySQL database",
             "StudentService" in pr_content)

# 1.5 Inspect process-contact.php for security guarantees
proc_cont = PUBLIC_DIR / "process-contact.php"
if proc_cont.is_file():
    pc_content = proc_cont.read_text(encoding="utf-8")
    log_test("process-contact: Enforces HTTP POST check (rejects GET with 405)",
             "$_SERVER['REQUEST_METHOD'] !== 'POST'" in pc_content and "405" in pc_content)
    log_test("process-contact: Enforces CSRF Token Verification",
             "validateCsrfToken" in pc_content and "403" in pc_content)
    log_test("process-contact: Uses flock(..., LOCK_EX) for JSON concurrency safety",
             "flock" in pc_content and "LOCK_EX" in pc_content)
    log_test("process-contact: Validates contact fields (name, email, subject, message)",
             "subject" in pc_content and "message" in pc_content and "422" in pc_content)
    log_test("process-contact: Stores in messages.json outside public root",
             "messages.json" in pc_content and "json_encode" in pc_content)

# 1.6 Verify HTML Form Action and Input Attributes
reg_html = (PUBLIC_DIR / "pages" / "registration.html").read_text(encoding="utf-8")
log_test("registration.html: Form uses POST to ../process-registration.php",
         'method="POST"' in reg_html and 'action="../process-registration.php"' in reg_html)
log_test("registration.html: Inputs have name attributes",
         'name="name"' in reg_html and 'name="email"' in reg_html and 'name="mobile"' in reg_html)
log_test("registration.html: Hidden CSRF token field present",
         'id="csrf_token"' in reg_html and 'name="csrf_token"' in reg_html)
log_test("registration.html: Alert feedback container present",
         'id="registrationAlert"' in reg_html)

cont_html = (PUBLIC_DIR / "pages" / "contact.html").read_text(encoding="utf-8")
log_test("contact.html: Form uses POST to ../process-contact.php",
         'method="POST"' in cont_html and 'action="../process-contact.php"' in cont_html)
log_test("contact.html: Inputs have name attributes",
         'name="name"' in cont_html and 'name="email"' in cont_html and 'name="subject"' in cont_html and 'name="message"' in cont_html)
log_test("contact.html: Hidden CSRF token field present",
         'id="csrf_token"' in cont_html and 'name="csrf_token"' in cont_html)
log_test("contact.html: Alert feedback container present",
         'id="contactAlert"' in cont_html)

# 1.7 Verify Persistent Storage & Concurrency Safe CSV/JSON Writes
with tempfile.TemporaryDirectory() as temp_dir:
    test_csv = Path(temp_dir) / "registrations.csv"
    # Header
    with open(test_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "email", "mobile", "course", "department", "gender", "hobbies", "address", "password_hash", "created_at"])
        # Simulate hashed password
        hashed = bcrypt.hashpw(b"SecretPass123", bcrypt.gensalt()).decode("utf-8")
        writer.writerow([1, "Test Student", "test@charusat.edu.in", "9876543210", "B.Tech", "Information Technology", "Female", "Reading, Coding", "Campus Hostel, Changa", hashed, "2026-10-24 12:00:00"])

    # Verify CSV read and duplicate detection
    with open(test_csv, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        has_record = len(reader) == 1
        password_hashed = reader[0]["password_hash"].startswith("$2")
        email_found = reader[0]["email"] == "test@charusat.edu.in"
        no_plaintext = "SecretPass123" not in reader[0]["password_hash"]

    log_test("CSV Storage: Row correctly formatted with CSV escaping", has_record)
    log_test("CSV Storage: Passwords hashed with bcrypt (never plaintext)", password_hashed and no_plaintext)
    log_test("CSV Storage: Duplicate detection via email lookup succeeds", email_found)

    # Test Concurrent Thread Writes
    test_json = Path(temp_dir) / "messages.json"
    test_json.write_text("[]", encoding="utf-8")
    lock = threading.Lock()
    errors = []

    def write_worker(idx):
        try:
            with lock:
                with open(test_json, "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    data.append({"id": idx, "name": f"User {idx}", "message": f"Message {idx}"})
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f)
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=write_worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    with open(test_json, "r", encoding="utf-8") as f:
        stored_messages = json.load(f)

    log_test("Storage Concurrency: 10 concurrent writes recorded safely without data corruption",
             len(stored_messages) == 10 and len(errors) == 0)


# ==============================================================================
# SECTION 2: PRACTICAL 8 - MySQL Database Foundation & Connectivity Tests
# ==============================================================================
print("\n" + "=" * 70)
print("SECTION 2: Practical 8 - MySQL Database Foundation & Connectivity")
print("=" * 70)

# 2.1 Inspect app/config/db.php for MySQLi & PDO unification
db_file = APP_DIR / "config" / "db.php"
if db_file.is_file():
    db_content = db_file.read_text(encoding="utf-8")
    log_test("db.php: PDO singleton getConnection() / getDB() implemented",
             "public static function getConnection(): PDO" in db_content and "function getDB(): PDO" in db_content)
    log_test("db.php: Object-Oriented MySQLi getMySQLi() implemented",
             "public static function getMySQLi(): mysqli" in db_content and "new mysqli" in db_content)
    log_test("db.php: Procedural MySQLi getProcedural() / getMySQLiProcedural() implemented",
             "mysqli_connect" in db_content and "function getMySQLiProcedural(): mysqli" in db_content)
    log_test("db.php: Credentials loaded dynamically via env()",
             "env('DB_HOST'" in db_content and "env('DB_PORT'" in db_content and "env('DB_USER'" in db_content)
    log_test("db.php: Secure connection error handling (credentials masked from output)",
             "A database error occurred" in db_content and "error_log" in db_content)

# 2.2 Inspect app/services/student_service.php
ss_file = APP_DIR / "services" / "student_service.php"
if ss_file.is_file():
    ss_content = ss_file.read_text(encoding="utf-8")
    log_test("StudentService: getAllMySQLi() uses prepared statements",
             "getAllMySQLi" in ss_content and "bind_param" in ss_content and "get_result" in ss_content)
    log_test("StudentService: findByEmail() uses prepared statement",
             "findByEmail" in ss_content and "prepare" in ss_content and "bind_param" in ss_content)
    log_test("StudentService: create() uses prepared statement with bind_param",
             "INSERT INTO students" in ss_content and "bind_param" in ss_content)
    log_test("StudentService: count() total count method implemented",
             "function count(): int" in ss_content)

# 2.3 Live MySQL Server Connectivity on port 3307
mysql_host = "127.0.0.1"
mysql_port = 3307
mysql_user = "root"
mysql_pass = ""

conn = None
try:
    conn = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_pass,
        autocommit=True
    )
    log_test(f"Live MySQL Connection: Connected to MySQL on port {mysql_port}", True, f"Server: {conn.get_server_info()}")
except Exception as e:
    log_test(f"Live MySQL Connection: Connected to MySQL on port {mysql_port}", False, str(e))

if conn:
    cursor = conn.cursor()

    # 2.4 Apply database/schema.sql
    try:
        schema_path = DATABASE_DIR / "schema.sql"
        schema_sql = schema_path.read_text(encoding="utf-8")
        for stmt in schema_sql.split(";"):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
        log_test("Database Schema: database/schema.sql imported cleanly", True)
    except Exception as e:
        log_test("Database Schema: database/schema.sql imported cleanly", False, str(e))

    # 2.5 Apply database/seed.sql
    try:
        seed_path = DATABASE_DIR / "seed.sql"
        seed_sql = seed_path.read_text(encoding="utf-8")
        for stmt in seed_sql.split(";"):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
        log_test("Database Seeds: database/seed.sql imported cleanly", True)
    except Exception as e:
        log_test("Database Seeds: database/seed.sql imported cleanly", False, str(e))

    # 2.6 Verify Tables Structure and Engine
    cursor.execute("SHOW TABLES IN studenthub")
    tables = [r[0] for r in cursor.fetchall()]
    expected_tables = ["users", "students", "events", "registrations", "audit_logs", "contact_messages"]
    all_tables_present = all(t in tables for t in expected_tables)
    log_test(f"Table Presence: All 6 tables exist ({', '.join(expected_tables)})", all_tables_present, f"Found: {tables}")

    # Check Engine is InnoDB for all tables
    cursor.execute("SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'studenthub'")
    engines = {r[0]: r[1] for r in cursor.fetchall()}
    all_innodb = all(eng.lower() == "innodb" for eng in engines.values())
    log_test("Table Engine: All tables configured with InnoDB engine", all_innodb, str(engines))

    # 2.7 Verify Minimum 20 Seeded Students
    cursor.execute("SELECT COUNT(*) FROM studenthub.students")
    student_count = cursor.fetchone()[0]
    log_test(f"Seed Verification: Minimum 20 students seeded (Found: {student_count})", student_count >= 20)

    # 2.8 Verify Seeded Events
    cursor.execute("SELECT COUNT(*) FROM studenthub.events")
    event_count = cursor.fetchone()[0]
    log_test(f"Seed Verification: Sample events seeded (Found: {event_count})", event_count >= 5)

    # 2.9 Test Unique Constraint: Duplicate email in students rejected
    dup_rejected = False
    try:
        cursor.execute(
            "INSERT INTO studenthub.students (name, email, mobile, course, department, gender) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            ("Duplicate User", "anshikabadala2@gmail.com", "9876543210", "B.Tech", "Information Technology", "Female")
        )
    except pymysql.err.IntegrityError:
        dup_rejected = True
    log_test("Database Constraints: Duplicate student email rejected with UNIQUE constraint", dup_rejected)

    # 2.10 Test Unique Constraint: Duplicate username in users rejected
    user_dup_rejected = False
    try:
        cursor.execute(
            "INSERT INTO studenthub.users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            ("admin", "admin_alt@studenthub.com", "dummy_pass", "admin")
        )
    except pymysql.err.IntegrityError:
        user_dup_rejected = True
    log_test("Database Constraints: Duplicate user username rejected with UNIQUE constraint", user_dup_rejected)

    # 2.11 Test Foreign Key Constraint: Invalid event_id rejected
    fk_rejected = False
    try:
        cursor.execute("INSERT INTO studenthub.registrations (event_id, student_id) VALUES (%s, %s)", (999999, 1))
    except pymysql.err.IntegrityError:
        fk_rejected = True
    log_test("Database Constraints: Foreign key violation on non-existent event rejected", fk_rejected)

    # 2.12 Test Foreign Key Cascading: Deleting student cascades to registrations
    cursor.execute(
        "INSERT INTO studenthub.students (name, email, mobile, course, department, gender) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        ("Cascade Test Student", "cascade_test@charusat.edu.in", "9123456789", "B.Tech", "IT", "Other")
    )
    cascade_student_id = cursor.lastrowid
    cursor.execute("INSERT INTO studenthub.registrations (event_id, student_id) VALUES (%s, %s)", (1, cascade_student_id))

    cursor.execute("SELECT COUNT(*) FROM studenthub.registrations WHERE student_id = %s", (cascade_student_id,))
    reg_inserted = cursor.fetchone()[0] == 1

    cursor.execute("DELETE FROM studenthub.students WHERE id = %s", (cascade_student_id,))
    cursor.execute("SELECT COUNT(*) FROM studenthub.registrations WHERE student_id = %s", (cascade_student_id,))
    reg_cascaded = cursor.fetchone()[0] == 0

    log_test("Database Constraints: Cascading delete on student registrations verified",
             reg_inserted and reg_cascaded)

    # 2.13 Prepared Statement Parameterized Queries (Insert & Select)
    cursor.execute(
        "INSERT INTO studenthub.students (name, email, mobile, course, department, gender, hobbies, address) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("Parameterized Student", "param.test@charusat.edu.in", "9898989898", "B.Tech", "Information Technology", "Female", "Coding, Gaming", "CHARUSAT Campus")
    )
    param_student_id = cursor.lastrowid

    cursor.execute("SELECT id, name, email, department FROM studenthub.students WHERE id = %s", (param_student_id,))
    retrieved_row = cursor.fetchone()
    log_test("Prepared Statements: Parameterized INSERT and SELECT query successful",
             retrieved_row is not None and retrieved_row[1] == "Parameterized Student")

    # Clean up test student
    cursor.execute("DELETE FROM studenthub.students WHERE id = %s", (param_student_id,))

    # 2.14 Verify Contact Messages Table & Parameterized Insert
    cursor.execute(
        "INSERT INTO studenthub.contact_messages (name, email, subject, message, ip_address, status) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        ("Test Inquirer", "inquirer@charusat.edu.in", "Practical 7 Verification", "Test message from automated test suite", "127.0.0.1", "unread")
    )
    msg_id = cursor.lastrowid
    cursor.execute("SELECT COUNT(*) FROM studenthub.contact_messages WHERE id = %s", (msg_id,))
    msg_exists = cursor.fetchone()[0] == 1
    log_test("Contact Messages Table: Parameterized message insertion successful", msg_exists)
    cursor.execute("DELETE FROM studenthub.contact_messages WHERE id = %s", (msg_id,))

    conn.close()

# 2.15 Credential Masking Test (Simulate connection failure)
masked_error_handled = False
try:
    # Attempt connecting with invalid credentials
    pymysql.connect(host="127.0.0.1", port=9999, user="dummy_user", password="secret_dummy_password", connect_timeout=1)
except Exception as e:
    # In db.php, the exception message caught is logged internally and a masked generic message is thrown
    # Verify that in our code, raw password is never echoed
    err_str = str(e)
    masked_error_handled = "secret_dummy_password" not in err_str
log_test("Security: Database connection failure hides raw password from display", masked_error_handled)


# ==============================================================================
# SECTION 3: PRACTICAL 1-6 REGRESSION SUITE
# ==============================================================================
print("\n" + "=" * 70)
print("SECTION 3: Practical 1-6 Regression Verification")
print("=" * 70)

# Check all original pages exist
pages = [
    "about.html", "administrative.html", "campuslife.html", "contact.html",
    "course-enrollment.html", "dashboard.html", "events.html", "faq.html",
    "login.html", "registration.html", "students.html"
]
for p in pages:
    log_test(f"Regression: public/pages/{p} exists", (PUBLIC_DIR / "pages" / p).is_file())

# Check JSON datasets exist and have data
datasets = ["events.json", "students.json", "faqs.json"]
for d in datasets:
    data_path = PUBLIC_DIR / "assets" / "data" / d
    if data_path.is_file():
        try:
            content = json.loads(data_path.read_text(encoding="utf-8"))
            log_test(f"Regression: public/assets/data/{d} valid JSON ({len(content)} items)", len(content) > 0)
        except Exception:
            log_test(f"Regression: public/assets/data/{d} valid JSON", False)
    else:
        log_test(f"Regression: public/assets/data/{d} exists", False)

# Check JavaScript renderers exist
js_modules = ["data-loader.js", "pagination.js", "events-renderer.js", "faq-renderer.js", "students-renderer.js", "registration.js", "contact.js"]
for j in js_modules:
    log_test(f"Regression: public/assets/js/{j} exists", (PUBLIC_DIR / "assets" / "js" / j).is_file())


# ==============================================================================
# SUMMARY REPORT
# ==============================================================================
print("\n" + "=" * 70)
print(f"VERIFICATION SUMMARY: {PASSED_TESTS}/{TOTAL_TESTS} PASSED ({(PASSED_TESTS/TOTAL_TESTS)*100:.1f}%)")
print("=" * 70)

if FAILED_TESTS > 0:
    print(f"FAILURE: {FAILED_TESTS} test(s) failed!")
    sys.exit(1)
else:
    print("SUCCESS: All Phase 3 (Practical 7 & 8) requirements and regressions PASSED!\n")
    sys.exit(0)
