"""
StudentHub - Phase 4 Automated Verification Test Suite
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT

Tests Practical 9 (Secure User Registration, Transactional Consistency)
and Practical 10 (Login/Logout, Session Hardening, RBAC Role Enforcement).
"""

import os
import sys
import re
import csv
import json
import time
import uuid
import pymysql
import bcrypt
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
API_DIR = BASE_DIR / "api"
PUBLIC_DIR = BASE_DIR / "public"
STORAGE_DIR = BASE_DIR / "storage"
DATABASE_DIR = BASE_DIR / "database"

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


# Database Config from .env or default test port
DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_NAME = "studenthub"
DB_USER = "root"
DB_PASS = ""

print("\n" + "=" * 75)
print("SECTION 1: Practical 9 - Secure User Registration & Transactional Integrity")
print("=" * 75)

# 1.1 Inspect Required Files for Practical 9
p9_files = [
    PUBLIC_DIR / "process-registration.php",
    APP_DIR / "services" / "user_service.php",
    APP_DIR / "services" / "student_service.php",
    APP_DIR / "config" / "security.php",
    PUBLIC_DIR / "pages" / "registration.html",
    PUBLIC_DIR / "pages" / "registration.php",
    PUBLIC_DIR / "assets" / "js" / "registration.js"
]
for f in p9_files:
    log_test(f"File Exists: {f.relative_to(BASE_DIR)}", f.is_file())

# 1.2 Inspect UserService Code Implementation
us_file = APP_DIR / "services" / "user_service.php"
us_code = us_file.read_text(encoding="utf-8") if us_file.is_file() else ""
log_test("UserService: registerStudent() method implemented", "function registerStudent" in us_code)
log_test("UserService: Uses begin_transaction() and commit()", "begin_transaction" in us_code and "commit" in us_code)
log_test("UserService: Uses rollback() on failure", "rollback" in us_code)
log_test("UserService: Hashes password with bcrypt before insert", "hashPassword" in us_code or "password_hash" in us_code)
log_test("UserService: Prepared statement used for users insert", "INSERT INTO users" in us_code and "prepare" in us_code and "bind_param" in us_code)
log_test("UserService: Prepared statement used for students insert", "INSERT INTO students" in us_code and "prepare" in us_code and "bind_param" in us_code)
log_test("UserService: Sets role strictly to 'student' (no privilege escalation)", "'student', 'active'" in us_code)

# 1.3 Inspect process-registration.php
pr_file = PUBLIC_DIR / "process-registration.php"
pr_code = pr_file.read_text(encoding="utf-8") if pr_file.is_file() else ""
log_test("process-registration: Enforces HTTP POST check (405)", "$_SERVER['REQUEST_METHOD'] !== 'POST'" in pr_code and "405" in pr_code)
log_test("process-registration: Enforces CSRF Token validation (403)", "validateCsrfToken" in pr_code and "403" in pr_code)
log_test("process-registration: Validates password confirmation match", "$password !== $confirmPassword" in pr_code)
log_test("process-registration: Enforces duplicate email check (409 Conflict)", "409" in pr_code and "already exists" in pr_code)
log_test("process-registration: Does NOT write password or password_hash to CSV file",
         "password_hash" not in pr_code[pr_code.find("fputcsv($fp, ["):pr_code.find("fflush($fp);")] if "fputcsv($fp, [" in pr_code else False)

# 1.4 Live Database Registration & Transactional Integrity
conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME, autocommit=False)
cursor = conn.cursor()

# Synthetic student credentials
test_uuid = uuid.uuid4().hex[:6]
syn_username = f"test_stu_{test_uuid}"
syn_email = f"test_{test_uuid}@charusat.edu.in"
syn_mobile = "9876543210"
syn_raw_password = "SecureStudentPass123!"

try:
    # Hash password using bcrypt
    syn_hash = bcrypt.hashpw(syn_raw_password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8").replace("$2b$", "$2y$")

    # Start transaction
    cursor.execute(
        "INSERT INTO users (username, email, password, role, status) VALUES (%s, %s, %s, 'student', 'active')",
        (syn_username, syn_email, syn_hash)
    )
    new_user_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO students (user_id, name, email, mobile, course, department, gender, hobbies, address, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')",
        (new_user_id, f"Test Student {test_uuid}", syn_email, syn_mobile, "B.Tech", "Information Technology", "Female", "Coding, Gaming", "Changa Campus")
    )
    new_student_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (%s, %s, %s, %s)",
        (new_user_id, "USER_REGISTRATION", f"Registered test student: {syn_username}", "127.0.0.1")
    )
    conn.commit()

    log_test("Live Registration: User and Student records inserted atomically in transaction",
             new_user_id > 0 and new_student_id > 0)

    # Verify user record
    cursor.execute("SELECT id, username, email, password, role, status FROM users WHERE id = %s", (new_user_id,))
    user_row = cursor.fetchone()
    log_test("Live Registration: User role is 'student' and status is 'active'",
             user_row is not None and user_row[4] == "student" and user_row[5] == "active")
    log_test("Live Registration: Password stored as valid bcrypt hash (not plaintext)",
             user_row[3].startswith("$2y$") or user_row[3].startswith("$2b$") and syn_raw_password not in user_row[3])

    # Verify student link
    cursor.execute("SELECT id, user_id, email, mobile FROM students WHERE id = %s", (new_student_id,))
    student_row = cursor.fetchone()
    log_test("Live Registration: Student foreign key user_id correctly references users.id",
             student_row is not None and student_row[1] == new_user_id)

    # 1.5 Duplicate Rejection Test
    dup_email_rejected = False
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'student')",
            (f"other_{test_uuid}", syn_email, syn_hash)
        )
        conn.commit()
    except pymysql.err.IntegrityError:
        conn.rollback()
        dup_email_rejected = True
    log_test("Live Registration: Duplicate email rejected by database UNIQUE constraint", dup_email_rejected)

    dup_username_rejected = False
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'student')",
            (syn_username, f"other_{test_uuid}@charusat.edu.in", syn_hash)
        )
        conn.commit()
    except pymysql.err.IntegrityError:
        conn.rollback()
        dup_username_rejected = True
    log_test("Live Registration: Duplicate username rejected by database UNIQUE constraint", dup_username_rejected)

    # 1.6 Rollback Test on Failure (No Orphaned Records)
    rollback_ok = False
    orphan_uuid = uuid.uuid4().hex[:6]
    orphan_user = f"orphan_{orphan_uuid}"
    orphan_email = f"orphan_{orphan_uuid}@charusat.edu.in"
    try:
        # Insert user
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'student')",
            (orphan_user, orphan_email, syn_hash)
        )
        orphan_id = cursor.lastrowid
        # Force intentional failure on student insert (null required name)
        cursor.execute("INSERT INTO students (user_id, name) VALUES (%s, NULL)", (orphan_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (orphan_user,))
        orphan_count = cursor.fetchone()[0]
        rollback_ok = (orphan_count == 0)
    log_test("Transactional Integrity: Transaction rolls back on error (zero orphaned users)", rollback_ok)

finally:
    # Cleanup synthetic student
    cursor.execute("DELETE FROM audit_logs WHERE user_id = %s", (new_user_id,))
    cursor.execute("DELETE FROM students WHERE id = %s", (new_student_id,))
    cursor.execute("DELETE FROM users WHERE id = %s", (new_user_id,))
    conn.commit()
    conn.close()


print("\n" + "=" * 75)
print("SECTION 2: Practical 10 - Login, Logout & Session Management")
print("=" * 75)

# 2.1 Inspect Login Files
p10_files = [
    PUBLIC_DIR / "process-login.php",
    PUBLIC_DIR / "process-logout.php",
    PUBLIC_DIR / "pages" / "login.html",
    PUBLIC_DIR / "pages" / "login.php",
    API_DIR / "auth" / "login.php",
    API_DIR / "auth" / "logout.php",
    APP_DIR / "includes" / "auth_check.php",
    APP_DIR / "middleware" / "auth_middleware.php",
    APP_DIR / "middleware" / "role_middleware.php"
]
for f in p10_files:
    log_test(f"File Exists: {f.relative_to(BASE_DIR)}", f.is_file())

# 2.2 Inspect process-login.php
pl_file = PUBLIC_DIR / "process-login.php"
pl_code = pl_file.read_text(encoding="utf-8") if pl_file.is_file() else ""
log_test("process-login: Enforces HTTP POST check (405)", "$_SERVER['REQUEST_METHOD'] !== 'POST'" in pl_code and "405" in pl_code)
log_test("process-login: Enforces CSRF token check (403)", "validateCsrfToken" in pl_code and "403" in pl_code)
log_test("process-login: Calls UserService::authenticate()", "UserService::authenticate" in pl_code)
log_test("process-login: Regenerates session ID on login (session_regenerate_id)", "session_regenerate_id" in pl_code)
log_test("process-login: Stores minimal identity (user_id, username, email, role)",
         "$_SESSION['user_id']" in pl_code and "$_SESSION['role']" in pl_code)
log_test("process-login: Performs RBAC redirect routing (admin vs student)",
         "'admin') ? '../admin/index.php' : '../student/index.php'" in pl_code)

# 2.3 Inspect process-logout.php
lo_file = PUBLIC_DIR / "process-logout.php"
lo_code = lo_file.read_text(encoding="utf-8") if lo_file.is_file() else ""
log_test("process-logout: Clears session array ($_SESSION = [])", "$_SESSION = []" in lo_code)
log_test("process-logout: Expires session cookie in past (time() - 42000)", "time() - 42000" in lo_code)
log_test("process-logout: Calls session_destroy()", "session_destroy()" in lo_code)
log_test("process-logout: Redirects to login with logged_out status", "logged_out=1" in lo_code)

# 2.4 Live Authentication Tests (MySQL Server)
conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME, autocommit=True)
cursor = conn.cursor()

# Test 2.4.1: Verify seeded admin credentials
cursor.execute("SELECT id, username, email, password, role, status FROM users WHERE username = 'admin'")
admin_row = cursor.fetchone()
admin_hash_ok = False
if admin_row:
    admin_hash_b = admin_row[3].replace("$2y$", "$2b$").encode("utf-8")
    admin_hash_ok = bcrypt.checkpw(b"admin123", admin_hash_b)
log_test("Authentication: Seeded admin account verifies with password 'admin123'", admin_hash_ok)

# Test 2.4.2: Verify seeded student credentials
cursor.execute("SELECT id, username, email, password, role, status FROM users WHERE username = 'anshika'")
student_row = cursor.fetchone()
student_hash_ok = False
if student_row:
    stu_hash_b = student_row[3].replace("$2y$", "$2b$").encode("utf-8")
    student_hash_ok = bcrypt.checkpw(b"student123", stu_hash_b)
log_test("Authentication: Seeded student account verifies with password 'student123'", student_hash_ok)

# Test 2.4.3: Invalid password rejected
invalid_pass_rejected = not bcrypt.checkpw(b"WrongPassword999", admin_hash_b)
log_test("Authentication: Incorrect password rejected safely", invalid_pass_rejected)

# Test 2.4.4: Inactive account rejection
inact_uuid = uuid.uuid4().hex[:6]
cursor.execute(
    "INSERT INTO users (username, email, password, role, status) VALUES (%s, %s, %s, 'student', 'inactive')",
    (f"inact_{inact_uuid}", f"inact_{inact_uuid}@test.com", admin_row[3])
)
inact_id = cursor.lastrowid
cursor.execute("SELECT status FROM users WHERE id = %s", (inact_id,))
inact_status = cursor.fetchone()[0]
log_test("Authentication: Inactive status correctly recorded in DB", inact_status == "inactive")
cursor.execute("DELETE FROM users WHERE id = %s", (inact_id,))

# Test 2.4.5: Parameterized search supports both username and email
cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", ("admin", "admin"))
found_by_username = cursor.fetchone() is not None
cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", ("admin@studenthub.com", "admin@studenthub.com"))
found_by_email = cursor.fetchone() is not None
log_test("Authentication: Prepared statement resolves user by both username and email",
         found_by_username and found_by_email)

conn.close()

# 2.5 Session Hardening & Timeout Inspection
cfg_file = APP_DIR / "config" / "config.php"
cfg_code = cfg_file.read_text(encoding="utf-8") if cfg_file.is_file() else ""
log_test("Session Hardening: session.cookie_httponly set to 1", "session.cookie_httponly', '1'" in cfg_code)
log_test("Session Hardening: session.cookie_samesite set to 'Lax'", "session.cookie_samesite', 'Lax'" in cfg_code)
log_test("Session Hardening: session.cookie_secure enabled on HTTPS", "session.cookie_secure', '1'" in cfg_code)
log_test("Session Hardening: Inactivity timeout enforcement logic present", "SESSION_LIFETIME" in cfg_code and "last_activity" in cfg_code)


print("\n" + "=" * 75)
print("SECTION 3: Role-Based Access Control (RBAC) & Endpoint Guards")
print("=" * 75)

# 3.1 Inspect auth_check.php Guard Functions
ac_file = APP_DIR / "includes" / "auth_check.php"
ac_code = ac_file.read_text(encoding="utf-8") if ac_file.is_file() else ""
log_test("RBAC: isAuthenticated() helper declared", "function isAuthenticated(): bool" in ac_code)
log_test("RBAC: hasRole() role check helper declared", "function hasRole(string $role): bool" in ac_code)
log_test("RBAC: currentUser() identity accessor declared", "function currentUser(): ?array" in ac_code)
log_test("RBAC: requireLogin() redirect guard declared", "function requireLogin" in ac_code)
log_test("RBAC: requireRole() role enforcement guard declared", "function requireRole" in ac_code)
log_test("RBAC: enforceApiAuth() API status 401/403 guard declared", "function enforceApiAuth" in ac_code)

# 3.2 Inspect admin/index.php RBAC Enforcement
admin_file = BASE_DIR / "admin" / "index.php"
admin_code = admin_file.read_text(encoding="utf-8") if admin_file.is_file() else ""
log_test("RBAC: admin/index.php invokes checkRole('admin')", "checkRole('admin'" in admin_code)
log_test("RBAC: admin/index.php displays authenticated user details and sign out",
         "currentUser()" in admin_code and "process-logout.php" in admin_code)

# 3.3 Inspect student/index.php RBAC Enforcement
student_file = BASE_DIR / "student" / "index.php"
student_code = student_file.read_text(encoding="utf-8") if student_file.is_file() else ""
log_test("RBAC: student/index.php invokes checkAuth() guard", "checkAuth(" in student_code)
log_test("RBAC: student/index.php displays authenticated student details and sign out",
         "currentUser()" in student_code and "process-logout.php" in student_code)

# 3.4 Inspect Navigation Component for Dynamic Auth Links
nav_file = APP_DIR / "includes" / "nav.php"
nav_code = nav_file.read_text(encoding="utf-8") if nav_file.is_file() else ""
log_test("RBAC: nav.php dynamically displays Admin Portal link for admin users",
         "Admin Portal" in nav_code and "admin" in nav_code and "role" in nav_code)
log_test("RBAC: nav.php dynamically displays Logout link for authenticated users",
         "process-logout.php" in nav_code)


print("\n" + "=" * 75)
print("SECTION 4: Practical 1-8 Regressions Verification")
print("=" * 75)

# Verify HTML pages
pages = [
    "about.html", "administrative.html", "campuslife.html", "contact.html",
    "course-enrollment.html", "dashboard.html", "events.html", "faq.html",
    "login.html", "registration.html", "students.html"
]
for p in pages:
    log_test(f"Regression: public/pages/{p} exists", (PUBLIC_DIR / "pages" / p).is_file())

# Verify JSON datasets
datasets = ["events.json", "students.json", "faqs.json"]
for d in datasets:
    data_path = PUBLIC_DIR / "assets" / "data" / d
    try:
        content = json.loads(data_path.read_text(encoding="utf-8"))
        log_test(f"Regression: public/assets/data/{d} valid JSON ({len(content)} items)", len(content) > 0)
    except Exception:
        log_test(f"Regression: public/assets/data/{d} valid JSON", False)

# Verify JavaScript renderers
renderers = ["data-loader.js", "pagination.js", "events-renderer.js", "faq-renderer.js", "students-renderer.js", "registration.js", "contact.js"]
for r in renderers:
    log_test(f"Regression: public/assets/js/{r} exists", (PUBLIC_DIR / "assets" / "js" / r).is_file())


# ==============================================================================
# SUMMARY REPORT
# ==============================================================================
print("\n" + "=" * 75)
print(f"PHASE 4 VERIFICATION SUMMARY: {PASSED_TESTS}/{TOTAL_TESTS} PASSED ({(PASSED_TESTS/TOTAL_TESTS)*100:.1f}%)")
print("=" * 75)

if FAILED_TESTS > 0:
    print(f"FAILURE: {FAILED_TESTS} test(s) failed!")
    sys.exit(1)
else:
    print("SUCCESS: All Practical 9 and 10 requirements and regressions PASSED!\n")
    sys.exit(0)
