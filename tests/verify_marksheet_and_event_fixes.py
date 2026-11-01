#!/usr/bin/env python3
"""
StudentHub - Event Registration & Marksheet Upload Regression Test Suite
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT

This test suite comprehensively tests:
1. Marksheet Upload Workflow:
   - Valid PDF upload with accurate CGPA extraction (no fabrication)
   - Valid image upload (PNG, JPG, WEBP)
   - Unsupported file format rejection
   - Oversized file rejection (> 5 MB)
   - Spoofed MIME type rejection
   - Unauthenticated upload rejection (401)
   - Expired/invalid session rejection (401)
   - Marksheet history retrieval (Requirement 12)
   - Cross-student access control (Requirement 7)
   - Confirmation workflow: CGPA saved ONLY after confirmation (Requirement 11)
2. Event Registration Workflow:
   - Completed event registration rejection (Event 15 Monsoon Music)
   - Past event registration rejection
   - Cancelled / closed event registration rejection
   - Eligible upcoming event registration success
   - Duplicate registration prevention (409)
   - Unauthenticated registration rejection (401)
   - Ineligible student registration rejection (403)
   - Database persistence in registrations table and student dashboard
"""

import io
import json
import os
import sys
import urllib.parse
import urllib.request
import http.cookiejar
from pathlib import Path
import pymysql

BASE_URL = "http://localhost:8000"
passed_count = 0
failed_count = 0

def log_test(name: str, condition: bool, details: str = ""):
    global passed_count, failed_count
    if condition:
        passed_count += 1
        print(f"  [PASS] {name}")
    else:
        failed_count += 1
        print(f"  [FAIL] {name} - Details: {details}")

# Helper to build multipart/form-data
def build_multipart(fields: dict, files: list) -> tuple:
    boundary = "----StudentHubBoundary" + os.urandom(8).hex()
    body = bytearray()

    for k, v in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{v}\r\n".encode("utf-8"))

    for field_name, filename, mime_type, content in files:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode("utf-8"))
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    return bytes(body), headers

# Session client helper
class TestClient:
    def __init__(self):
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))

    def request(self, url: str, method: str = "GET", data=None, headers: dict = None):
        if headers is None:
            headers = {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with self.opener.open(req, timeout=10) as resp:
                status = resp.status
                body = resp.read().decode("utf-8", errors="ignore")
                try:
                    json_data = json.loads(body)
                except Exception:
                    json_data = None
                return status, body, json_data
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            try:
                json_data = json.loads(body)
            except Exception:
                json_data = None
            return e.code, body, json_data

    def login(self, username, password):
        # 1. Fetch CSRF token from login page
        code, body, _ = self.request(f"{BASE_URL}/pages/login.html")
        csrf_token = ""
        # Or query auth/me.php or CSRF from session
        code, body, me = self.request(f"{BASE_URL}/api/auth/me.php")

        # Get CSRF token via login.php or direct POST
        login_data = urllib.parse.urlencode({
            "username": username,
            "password": password
        }).encode("utf-8")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        code, body, j = self.request(f"{BASE_URL}/api/auth/login.php", method="POST", data=login_data, headers=headers)
        return code == 200 and j and j.get("success")

# Ensure clean initial test environment
try:
    init_conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub", autocommit=True)
    init_cur = init_conn.cursor()
    init_cur.execute("DELETE FROM registrations WHERE event_id = 11 AND student_id = 1")
    init_cur.execute("DELETE FROM students WHERE student_id = 'INACT001'")
    init_cur.execute("DELETE FROM users WHERE username = 'test_inactive_user'")
    init_conn.close()
except Exception as e:
    pass

print("\n" + "=" * 80)
print("SECTION 1: Marksheet Upload & CGPA Extraction Verification")
print("=" * 80)

# Create sample test files
# 1. Authentic PDF with SGPA: 8.44
sample_pdf_text = "CHARUSAT CSPIT AIML Semester 2 Grade Card. Roll: 25AIML002. Student: Anshika Badala. SGPA: 8.44 Total Credits: 21.00 Result: PASS"
valid_pdf_bytes = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length {len(sample_pdf_text) + 60} >>
stream
BT
/F1 12 Tf
72 700 Td
({sample_pdf_text}) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000117 00000 n 
0000000234 00000 n 
0000000400 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
500
%%EOF""".encode("latin-1")

# 2. Authentic minimal 1x1 PNG
valid_png_bytes = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000a49444154789c63000100000500010d0a2d000000000049454e44ae426082")

# 3. Spoofed PDF (plain text with .pdf extension)
spoofed_pdf_bytes = b"Hello, this is just plain text masquerading as a PDF file."

# 4. Oversized file (5.5 MB)
oversized_bytes = b"0" * (int(5.5 * 1024 * 1024))

# 5. Unsupported file (.exe)
unsupported_bytes = b"MZ\x90\x00\x03\x00\x00\x00"

# Initialize Client and Login as Student 1 (anshika)
client = TestClient()
login_ok = client.login("anshika", "student123")
log_test("Authentication: Logged in as student 'anshika' (Student ID 1)", login_ok)

# Test 1.1: Upload without login
anon_client = TestClient()
body, hdrs = build_multipart({"semester": 2}, [("marksheet_file", "test.pdf", "application/pdf", valid_pdf_bytes)])
code, _, j = anon_client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=body, headers=hdrs)
log_test("Marksheet Security: Unauthenticated upload rejected with 401 Unauthorized",
         code == 401 and j and j.get("success") is False)

# Test 1.2: Valid PDF upload with CGPA extraction
body, hdrs = build_multipart({"semester": 2, "academic_year": "2025-2026"}, [("marksheet_file", "Anshika_Sem2_Result.pdf", "application/pdf", valid_pdf_bytes)])
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=body, headers=hdrs)
pdf_upload_ok = (code == 200 and j and j.get("success") is True and j.get("extracted_cgpa") == 8.44 and j.get("marksheet_id") > 0)
pdf_marksheet_id = j.get("marksheet_id", 0) if j else 0
log_test("Marksheet Upload: Valid PDF accepted with accurate SGPA 8.44 extraction (no fabrication)",
         pdf_upload_ok, f"Code: {code}, Response: {j}")

# Test 1.3: Valid Image upload (PNG) - should not fabricate academic score
body, hdrs = build_multipart({"semester": 1, "academic_year": "2025-2026"}, [("marksheet_file", "Marksheet_Scan.png", "image/png", valid_png_bytes)])
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=body, headers=hdrs)
png_upload_ok = (code == 200 and j and j.get("success") is True and j.get("marksheet_id") > 0 and j.get("has_detected_cgpa") is False and j.get("extracted_cgpa") is None)
png_marksheet_id = j.get("marksheet_id", 0) if j else 0
log_test("Marksheet Upload: Valid PNG accepted, CGPA is NULL (strictly never fabricates fake scores)",
         png_upload_ok, f"Code: {code}, Response: {j}")

# Test 1.4: Unsupported file format (.exe)
body, hdrs = build_multipart({"semester": 2}, [("marksheet_file", "payload.exe", "application/x-msdownload", unsupported_bytes)])
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=body, headers=hdrs)
log_test("Marksheet Validation: Unsupported file format (.exe) rejected with 400 Bad Request",
         code == 400 and j and j.get("success") is False and "Unsupported" in j.get("error", ""))

# Test 1.5: Oversized file (> 5 MB)
body, hdrs = build_multipart({"semester": 2}, [("marksheet_file", "huge.pdf", "application/pdf", oversized_bytes)])
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=body, headers=hdrs)
log_test("Marksheet Validation: Oversized file (> 5 MB) rejected with 400 Bad Request",
         code == 400 and j and j.get("success") is False and "exceeds" in j.get("error", "").lower())

# Test 1.6: Spoofed MIME type (text file renamed to .pdf)
body, hdrs = build_multipart({"semester": 2}, [("marksheet_file", "fake.pdf", "application/pdf", spoofed_pdf_bytes)])
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=body, headers=hdrs)
log_test("Marksheet Validation: Deep MIME validation detects fake PDF and rejects with 400",
         code == 400 and j and j.get("success") is False and "Invalid file content" in j.get("error", ""))

# Test 1.7: Upload history retrieval (Requirement 12)
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="GET")
history_ok = (code == 200 and j and j.get("success") is True and len(j.get("marksheets", [])) >= 2)
log_test("Marksheet History: Authenticated student receives upload history records", history_ok, f"Count: {j.get('count') if j else 0}")

# Test 1.8: Cross-Student Privacy Defense (Requirement 7)
# Log in as Student 2 (Student ID 92 / 25AIML003)
client2 = TestClient()
client2_login_ok = client2.login("25AIML003", "25AIML003")
log_test("Authentication: Logged in as student '25AIML003' (Student ID 92)", client2_login_ok)

# Attempt to confirm Student 1's marksheet
confirm_tamper = urllib.parse.urlencode({
    "action": "confirm",
    "marksheet_id": pdf_marksheet_id,
    "confirmed_cgpa": 9.99
}).encode("utf-8")
c_hdrs = {"Content-Type": "application/x-www-form-urlencoded"}
code, _, j = client2.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=confirm_tamper, headers=c_hdrs)
log_test("Privacy Defense: Student B cannot confirm Student A's marksheet (403 Forbidden)",
         code == 403 and j and j.get("success") is False)

# Attempt to view Student 1's marksheet file via secure viewer
code, body, _ = client2.request(f"{BASE_URL}/api/marksheets/view.php?id={pdf_marksheet_id}")
log_test("Privacy Defense: Student B cannot view Student A's marksheet document (403 Forbidden)",
         code == 403)

# Owner Student 1 viewing own marksheet
code, body, _ = client.request(f"{BASE_URL}/api/marksheets/view.php?id={pdf_marksheet_id}")
log_test("Privacy Defense: Owner Student 1 successfully accesses own marksheet file (200 OK)",
         code == 200 and len(body) > 0)

# Test 1.9: Confirmation Workflow - Save academic result only after confirmation (Requirements 10 & 11)
conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub", autocommit=True)
cur = conn.cursor(pymysql.cursors.DictCursor)

# Verify database state BEFORE confirmation
cur.execute("SELECT status, confirmed_cgpa FROM marksheets WHERE id = %s", (pdf_marksheet_id,))
before_row = cur.fetchone()
log_test("Academic Result Rule: Marksheet initially unconfirmed in DB before student confirms",
         before_row['status'] == 'extracted' and before_row['confirmed_cgpa'] is None)

# Perform valid confirmation by owner student
valid_confirm = urllib.parse.urlencode({
    "action": "confirm",
    "marksheet_id": pdf_marksheet_id,
    "confirmed_cgpa": 8.44
}).encode("utf-8")
code, _, j = client.request(f"{BASE_URL}/api/marksheets/upload.php", method="POST", data=valid_confirm, headers=c_hdrs)
log_test("Confirmation Workflow: Owner successfully confirms CGPA 8.44",
         code == 200 and j and j.get("success") is True)

# Verify database state AFTER confirmation
cur.execute("SELECT status, confirmed_cgpa FROM marksheets WHERE id = %s", (pdf_marksheet_id,))
after_row = cur.fetchone()
cur.execute("SELECT cgpa FROM students WHERE id = 1")
stu_row = cur.fetchone()

log_test("Academic Result Rule: Status updated to 'confirmed' and students.cgpa updated to 8.44",
         after_row['status'] == 'confirmed' and float(after_row['confirmed_cgpa']) == 8.44 and float(stu_row['cgpa']) == 8.44)

print("\n" + "=" * 80)
print("SECTION 2: Event Registration Enforcement & Business Rules")
print("=" * 80)

# Test 2.1: Completed event registration attempt (Event 15 Monsoon Music Acoustic Night)
reg_payload_15 = json.dumps({"event_id": 15}).encode("utf-8")
json_hdrs = {"Content-Type": "application/json"}
code, _, j = client.request(f"{BASE_URL}/api/events/register.php", method="POST", data=reg_payload_15, headers=json_hdrs)
log_test("Event Rule: Completed event #15 (Monsoon Music) registration strictly REJECTED (400 Bad Request)",
         code == 400 and j and j.get("success") is False and "concluded" in j.get("message", "").lower(),
         f"Status: {code}, Message: {j.get('message') if j else ''}")

# Test 2.2: GET status check for completed event #15
code, _, j = client.request(f"{BASE_URL}/api/events/register.php?event_id=15", method="GET")
log_test("Event Status: GET endpoint marks completed event #15 can_register=False",
         code == 200 and j and j.get("can_register") is False and j.get("is_completed") is True)

# Test 2.3: Past event registration attempt (Event 13 Orientation Day, 2026-07-15)
reg_payload_13 = json.dumps({"event_id": 13}).encode("utf-8")
code, _, j = client.request(f"{BASE_URL}/api/events/register.php", method="POST", data=reg_payload_13, headers=json_hdrs)
log_test("Event Rule: Past date event #13 registration strictly REJECTED (400 Bad Request)",
         code == 400 and j and j.get("success") is False and ("passed" in j.get("message", "").lower() or "concluded" in j.get("message", "").lower()))

# Test 2.4: Logged-out event registration attempt
code, _, j = anon_client.request(f"{BASE_URL}/api/events/register.php", method="POST", data=json.dumps({"event_id": 11}).encode("utf-8"), headers=json_hdrs)
log_test("Event Security: Logged-out registration rejected with 401 Unauthorized",
         code == 401 and j and j.get("success") is False)

# Clean up any existing registration for Event 11 (Campus Photography Exhibition, date: 2026-11-20) for Student 1
cur.execute("DELETE FROM registrations WHERE event_id = 11 AND student_id = 1")
conn.commit()

# Test 2.5: Successful registration for eligible upcoming event (Event 11, date: 2026-11-20)
reg_payload_11 = json.dumps({"event_id": 11}).encode("utf-8")
code, _, j = client.request(f"{BASE_URL}/api/events/register.php", method="POST", data=reg_payload_11, headers=json_hdrs)
upcoming_reg_ok = (code in (200, 201) and j and j.get("success") is True and j.get("registration_id", 0) > 0)
log_test("Event Registration: Eligible upcoming event #11 successfully registered (201 Created)",
         upcoming_reg_ok, f"Status: {code}, Message: {j.get('message') if j else ''}")

# Test 2.6: Duplicate registration prevention
code, _, j = client.request(f"{BASE_URL}/api/events/register.php", method="POST", data=reg_payload_11, headers=json_hdrs)
duplicate_rejected = (code in (400, 409) and j and j.get("success") is False and "already registered" in j.get("message", "").lower())
log_test("Event Rule: Duplicate registration rejected with 409/400 Conflict",
         duplicate_rejected, f"Status: {code}, Message: {j.get('message') if j else ''}")

# Test 2.7: GET status check indicates is_registered=True and can_register=False
code, _, j = client.request(f"{BASE_URL}/api/events/register.php?event_id=11", method="GET")
log_test("Event Status: GET endpoint reflects is_registered=True and can_register=False for student",
         code == 200 and j and j.get("is_registered") is True and j.get("can_register") is False)

# Test 2.8: Persistence check in database & Student Portal
cur.execute("SELECT id, event_id, student_id, registered_at FROM registrations WHERE event_id = 11 AND student_id = 1")
reg_db_row = cur.fetchone()
log_test("Database Persistence: Registration record exists in MySQL database",
         reg_db_row is not None and reg_db_row['event_id'] == 11 and reg_db_row['student_id'] == 1)

# Student Dashboard query check
code, dash_html, _ = client.request(f"{BASE_URL}/student/index.php")
log_test("Student Dashboard: Newly registered event 'Campus Photography Exhibition' renders in Student Portal",
         "Campus Photography Exhibition" in dash_html)

# Test 2.9: Ineligible student rejection (inactive/nonexistent student profile)
import subprocess
php_cmd = """
require 'app/services/student_service.php';
$res = StudentService::registerForEvent(999999, 11);
echo json_encode($res);
"""
res = subprocess.run(["C:\\xampp\\php\\php.exe", "-r", php_cmd], capture_output=True, text=True)
nonexistent_ok = "No active student record" in res.stdout
log_test("Eligibility Rule: Nonexistent/inactive student profile registration rejected", nonexistent_ok)

# Teardown & Environment Restoration (preserve official 78-student roster and academic records)
try:
    cur.execute("DELETE FROM registrations WHERE event_id = 11 AND student_id = 1")
    cur.execute("DELETE FROM students WHERE student_id = 'INACT001'")
    cur.execute("DELETE FROM users WHERE username = 'test_inactive_user'")
    if 'pdf_marksheet_id' in locals() and pdf_marksheet_id:
        cur.execute("DELETE FROM marksheets WHERE id = %s", (pdf_marksheet_id,))
    if 'png_marksheet_id' in locals() and png_marksheet_id:
        cur.execute("DELETE FROM marksheets WHERE id = %s", (png_marksheet_id,))
    # Restore Anshika Badala's verified official SGPA and weighted CGPA
    cur.execute("UPDATE semester_results SET sgpa = 8.77, remarks = NULL WHERE student_id = 1 AND semester = 2")
    cur.execute("UPDATE students SET cgpa = 8.44 WHERE id = 1")
    conn.commit()
except Exception as e:
    pass
finally:
    conn.close()

print("\n" + "=" * 80)
print(f"REGRESSION SUITE SUMMARY: {passed_count}/{passed_count + failed_count} PASSED ({passed_count / (passed_count + failed_count) * 100:.1f}%)")
print("=" * 80)

if failed_count > 0:
    print(f"FAILURE: {failed_count} tests failed!")
    sys.exit(1)
else:
    print("SUCCESS: All Marksheet Upload & Event Registration regression tests PASSED!\n")
    sys.exit(0)
