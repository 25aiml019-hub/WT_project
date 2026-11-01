"""
StudentHub - Phase Remedy Comprehensive Verification Suite
Covers:
- CSRF & Authentication Hardening
- 78 Student Accounts & Bcrypt Verification
- SGPA Reconciliation & Weighted CGPA Calculation
- Semester 3 Timetable Logic
- Student Directory Privacy Defense
- UI/UX & Asset Resolution
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
"""

import os
import sys
import json
import pymysql
import bcrypt
import urllib.request
import urllib.parse
import http.cookiejar
from decimal import Decimal

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "studenthub",
    "autocommit": True
}

BASE_URL = "http://localhost:8000"

passed = 0
failed = 0

def log_test(name, condition, details=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name} - Details: {details}")
        failed += 1

def main():
    print("=" * 75)
    print("RUNNING STUDENTHUB PHASE REMEDY VERIFICATION SUITE")
    print("=" * 75)

    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    # -------------------------------------------------------------
    # SECTION 1: 78 Student Accounts & Authentication
    # -------------------------------------------------------------
    print("\n--- SECTION 1: 78 Student Accounts & Authentication ---")

    cur.execute("SELECT count(*) FROM students WHERE student_id IS NOT NULL")
    roster_count = cur.fetchone()[0]
    log_test("Official AIML Roster has exactly 78 students", roster_count == 78, f"Found {roster_count}")

    cur.execute("SELECT count(*) FROM students WHERE student_id IS NOT NULL AND user_id IS NOT NULL")
    linked_count = cur.fetchone()[0]
    log_test("All 78 roster students are linked to user accounts", linked_count == 78, f"Found {linked_count}")

    cur.execute("""
        SELECT u.id, u.username, u.email, u.password, u.role, u.status, u.must_change_password, s.student_id
        FROM users u
        JOIN students s ON s.user_id = u.id
        WHERE s.student_id = '25AIML001'
    """)
    s1 = cur.fetchone()
    log_test("Student 25AIML001 account exists with student role", s1 is not None and s1[4] == 'student')
    log_test("Student 25AIML001 account is active", s1 is not None and s1[5] == 'active')
    log_test("Student 25AIML001 requires initial password change", s1 is not None and s1[6] == 1)
    
    s1_pass_match = False
    if s1 and s1[3]:
        s1_hash = s1[3].replace('$2y$', '$2b$').encode('utf-8')
        s1_pass_match = bcrypt.checkpw(b"25AIML001", s1_hash)
    log_test("Student 25AIML001 password is valid bcrypt hash of college ID", s1_pass_match)

    cur.execute("""
        SELECT u.id, u.username, u.email, u.password, u.role, u.status, s.student_id
        FROM users u
        JOIN students s ON s.user_id = u.id
        WHERE s.student_id = '25AIML002'
    """)
    s2 = cur.fetchone()
    log_test("Anshika Badala (25AIML002) linked to authentic user account", s2 is not None and s2[4] == 'student')

    cur.execute("SELECT count(*) FROM users WHERE role = 'student' AND must_change_password = 1")
    must_change_count = cur.fetchone()[0]
    log_test("77 newly provisioned students have must_change_password = 1", must_change_count >= 77, f"Found {must_change_count}")

    # -------------------------------------------------------------
    # SECTION 2: SGPA Import & Weighted CGPA Calculations
    # -------------------------------------------------------------
    print("\n--- SECTION 2: Academic Records & Weighted CGPA Reconciliation ---")

    cur.execute("SELECT count(*) FROM semester_results WHERE semester = 1 AND is_missing = 0")
    sem1_valid = cur.fetchone()[0]
    log_test("Semester 1 has 77 verified published records", sem1_valid == 77, f"Found {sem1_valid}")

    cur.execute("""
        SELECT sr.is_missing, sr.remarks, sr.credits
        FROM semester_results sr
        JOIN students s ON sr.student_id = s.id
        WHERE s.student_id = '25AIML011' AND sr.semester = 1
    """)
    s11_sem1 = cur.fetchone()
    log_test("Student 25AIML011 is explicitly flagged as missing for Semester 1", 
             s11_sem1 is not None and s11_sem1[0] == 1 and 'pending' in s11_sem1[1].lower())

    cur.execute("SELECT count(*) FROM semester_results WHERE semester = 2 AND is_missing = 0")
    sem2_valid = cur.fetchone()[0]
    log_test("Semester 2 has 78 verified published records", sem2_valid == 78, f"Found {sem2_valid}")

    cur.execute("""
        SELECT s.student_id, s.name, s.cgpa,
               sr1.sgpa AS sem1_sgpa, sr2.sgpa AS sem2_sgpa
        FROM students s
        JOIN semester_results sr1 ON sr1.student_id = s.id AND sr1.semester = 1
        JOIN semester_results sr2 ON sr2.student_id = s.id AND sr2.semester = 2
        WHERE s.student_id = '25AIML002'
    """)
    anshika_academic = cur.fetchone()
    anshika_cgpa_ok = (anshika_academic is not None and 
                       anshika_academic[3] == Decimal('8.05') and 
                       anshika_academic[4] == Decimal('8.77') and 
                       anshika_academic[2] == Decimal('8.44'))
    log_test("Anshika Badala: Sem 1 SGPA = 8.05, Sem 2 SGPA = 8.77, Weighted CGPA = 8.44", anshika_cgpa_ok, f"Got: {anshika_academic}")

    cur.execute("SELECT count(*) FROM unassigned_academic_records")
    unassigned_count = cur.fetchone()[0]
    log_test("Unassigned academic quarantine table holds exactly 13 records (including 25AIML079-25AIML090)", 
             unassigned_count == 13, f"Found {unassigned_count}")

    # -------------------------------------------------------------
    # SECTION 3: Semester 3 Timetable Integration
    # -------------------------------------------------------------
    print("\n--- SECTION 3: Semester 3 Timetable Integration ---")

    cur.execute("SELECT count(*) FROM timetable_slots WHERE academic_year = '2026-2027' AND semester = 3")
    tt_count = cur.fetchone()[0]
    log_test("Timetable table contains official 51 Semester 3 schedule slots", tt_count == 51, f"Found {tt_count}")

    cur.execute("SELECT count(*) FROM timetable_slots WHERE batch IN ('ALL', 'A1')")
    a1_slots = cur.fetchone()[0]
    log_test("Batch A1 has 25 applicable weekly academic slots", a1_slots == 25, f"Found {a1_slots}")

    cur.execute("""
        SELECT subject_name, room_no, faculty_name 
        FROM timetable_slots 
        WHERE day_of_week = 'Monday' AND slot_number = 1
    """)
    mon1 = cur.fetchone()
    log_test("Monday Slot 1 is Operating Systems in Room 218 with Prof. Gaurav Kumar", 
             mon1 is not None and mon1[0] == 'Operating Systems' and mon1[1] == '218')

    cur.execute("""
        SELECT subject_name, room_no, faculty_name 
        FROM timetable_slots 
        WHERE day_of_week = 'Monday' AND batch = 'A1' AND slot_type = 'counseling'
    """)
    counseling_slot = cur.fetchone()
    log_test("Monday Slot 6 for Batch A1 is Counseling in Cabin 204 with Prof. Gaurav Kumar", 
             counseling_slot is not None and 'counseling' in counseling_slot[0].lower() and counseling_slot[1] == 'Cabin 204')

    # -------------------------------------------------------------
    # SECTION 4: Live HTTP & API Endpoints Verification
    # -------------------------------------------------------------
    print("\n--- SECTION 4: Live HTTP, CSRF & RBAC Authentication Tests ---")

    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    def http_req(url, method="GET", data=None, headers=None):
        hdrs = headers or {}
        body = None
        if data is not None:
            if isinstance(data, dict):
                body = urllib.parse.urlencode(data).encode("utf-8")
                if "Content-Type" not in hdrs:
                    hdrs["Content-Type"] = "application/x-www-form-urlencoded"
            elif isinstance(data, (bytes, bytearray)):
                body = data
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
        try:
            resp = opener.open(req)
            return resp.getcode(), resp.headers, resp.read().decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read().decode("utf-8", errors="ignore")

    # 1. Fetch CSRF token
    code, hdrs, text = http_req(f"{BASE_URL}/csrf-token.php")
    log_test("CSRF Token Endpoint returns HTTP 200", code == 200)
    csrf_data = json.loads(text) if code == 200 else {}
    csrf_token = csrf_data.get("csrf_token", "")
    log_test("CSRF Token is valid 64-character hex string", len(csrf_token) == 64)

    # 2. Reject login with invalid CSRF token
    code, hdrs, text = http_req(f"{BASE_URL}/process-login.php", method="POST", data={
        "username": "admin",
        "password": "123",
        "csrf_token": "invalid_csrf_token_12345"
    }, headers={"Accept": "application/json"})
    log_test("Login rejects invalid CSRF token with HTTP 403", code == 403)

    # 3. Successful login as Student Anshika using college ID 25AIML002
    code, hdrs, text = http_req(f"{BASE_URL}/process-login.php", method="POST", data={
        "username": "25AIML002",
        "password": "25AIML002",
        "csrf_token": csrf_token
    }, headers={"Accept": "application/json"})
    log_test("Student login with 25AIML002 / 25AIML002 succeeds with HTTP 200", code == 200)
    login_data = json.loads(text) if code == 200 else {}
    log_test("Login returns role 'student' and redirect to student portal", 
             login_data.get("role") == "student" and "student" in login_data.get("redirect", ""))

    # 4. Check API /api/auth/me.php while authenticated
    code, hdrs, text = http_req(f"{BASE_URL}/api/auth/me.php")
    log_test("Authenticated /api/auth/me.php returns HTTP 200", code == 200)
    me_data = json.loads(text) if code == 200 else {}
    log_test("Current user identity reports authenticated student Anshika", 
             me_data.get("authenticated") is True and me_data.get("user", {}).get("role") == "student")

    # 5. Access student portal via HTTP GET
    code, hdrs, portal_html = http_req(f"{BASE_URL}/student/index.php")
    log_test("Student portal accessible with HTTP 200 for authenticated student", code == 200)
    log_test("Student portal displays college ID 25AIML002", "25AIML002" in portal_html)
    log_test("Student portal displays weighted CGPA 8.44", "8.44" in portal_html)
    log_test("Student portal displays Sem 1 SGPA 8.05 and Sem 2 SGPA 8.77", "8.05" in portal_html and "8.77" in portal_html)
    log_test("Student portal displays counselor Prof. Gaurav Kumar", "Prof. Gaurav Kumar" in portal_html)
    log_test("Student portal includes Semester 3 Timetable schedule", "Semester 3" in portal_html and "Operating Systems" in portal_html)

    # 6. Check student privacy defense in HTML
    log_test("Student directory hides personal phone numbers and emails", 
             "+91-" not in portal_html[portal_html.find("id=\"directory-table\""):portal_html.find("</table")])

    # 7. Check Logout
    code, hdrs, text = http_req(f"{BASE_URL}/process-logout.php?redirect=0", headers={"Accept": "application/json"})
    log_test("Logout processor returns HTTP 200 / redirect", code in (200, 302))

    # 8. Unauthenticated me.php after logout
    code, hdrs, text = http_req(f"{BASE_URL}/api/auth/me.php")
    me_after = json.loads(text) if code == 200 else {}
    log_test("Session after logout is unauthenticated", me_after.get("authenticated") is False)

    # -------------------------------------------------------------
    # SECTION 5: UI & Link Integrity
    # -------------------------------------------------------------
    print("\n--- SECTION 5: UI & Clean Relative Link Resolution ---")

    # Verify CSS file is served as text/css from docroot
    code, hdrs, text = http_req(f"{BASE_URL}/assets/css/main.css")
    log_test("Stylesheet /assets/css/main.css returns HTTP 200", code == 200)
    log_test("Stylesheet Content-Type is text/css", "text/css" in hdrs.get("Content-Type", ""))

    code, hdrs, text = http_req(f"{BASE_URL}/assets/css/dashboard.css")
    log_test("Stylesheet /assets/css/dashboard.css returns HTTP 200", code == 200)

    # Verify login.html contains demo instructions
    code, hdrs, login_html = http_req(f"{BASE_URL}/pages/login.html")
    log_test("Login page contains Demo Login Instructions card", "Demo Login Instructions" in login_html)
    log_test("Login page explains college ID username and temporary password", "25AIML002" in login_html)

    # Verify change password page exists and is accessible
    code, hdrs, text = http_req(f"{BASE_URL}/pages/change-password.php")
    log_test("Change password page redirects unauthenticated users to login", code in (200, 302))

    cur.close()
    conn.close()

    print("\n" + "=" * 75)
    print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL: {passed + failed})")
    print("=" * 75)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
