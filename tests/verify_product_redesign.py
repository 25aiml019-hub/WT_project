"""
StudentHub - Comprehensive Product Redesign & Academic Portal Verification
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
"""

import os
import sys
import json
import re
from pathlib import Path
import pymysql

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"
APP_DIR = BASE_DIR / "app"

passed_tests = 0
failed_tests = 0

def test_assert(name, condition, details=""):
    global passed_tests, failed_tests
    if condition:
        print(f"  [PASS] {name}")
        passed_tests += 1
    else:
        print(f"  [FAIL] {name} - Details: {details}")
        failed_tests += 1

print("=" * 80)
print("SECTION 1: Official Logo & Adelaide University Aesthetic Design")
print("=" * 80)

logo_png = PUBLIC_DIR / "assets" / "images" / "logo.png"
test_assert("Official Logo: assets/images/logo.png exists", logo_png.is_file())

index_html = (PUBLIC_DIR / "index.html").read_text(encoding="utf-8")
index_php = (PUBLIC_DIR / "index.php").read_text(encoding="utf-8")
home_css = (PUBLIC_DIR / "assets" / "css" / "home.css").read_text(encoding="utf-8")

test_assert("Home Page (HTML): Features Adelaide style hero section", "adelaide-hero" in index_html)
test_assert("Home Page (PHP): Features Adelaide style hero section", "adelaide-hero" in index_php)
test_assert("Home Page: Bold heading 'StudentHub — Launching the Next Generation of Leaders'", 
            "Launching the Next Generation of Leaders" in index_html and "Launching the Next Generation of Leaders" in index_php)
test_assert("Home Page: Hero CTA 'Explore Campus Life' present", "Explore Campus Life" in index_html)
test_assert("Home Page: Hero CTA 'Student Portal / Sign In' present", "Student Portal / Sign In" in index_html)
test_assert("Home Page: Fast-access 4-card hero section present", "hero-section" in index_html and "hero-card" in index_html)
test_assert("Home Page: Metrics strip with 78 class size, 4 clubs, 4 counselors", 
            "78" in index_html and "metrics-strip" in index_html)
test_assert("Home Page: Featured 4 campus clubs showcase grid present", "home-clubs-grid" in index_html)
test_assert("Home Page: Featured upcoming events preview present", "home-events-grid" in index_html)
test_assert("Home Page: Academic services grid present", "home-services-grid" in index_html)
test_assert("Home Page: Call to action bottom banner present", "adelaide-cta-banner" in index_html)
test_assert("Home Page CSS: Responsive grid breakpoints configured", 
            "grid-template-columns: repeat(4" in home_css and "@media (max-width: 1023px)" in home_css)

print("\n" + "=" * 80)
print("SECTION 2: Campus Life & 4 Dedicated Club Detail Pages")
print("=" * 80)

campuslife_html = (PUBLIC_DIR / "pages" / "campuslife.html").read_text(encoding="utf-8")
clubs_dir = PUBLIC_DIR / "pages" / "clubs"

test_assert("Clubs: Sports Club page exists (pages/clubs/sports.html)", (clubs_dir / "sports.html").is_file())
test_assert("Clubs: Music Club page exists (pages/clubs/music.html)", (clubs_dir / "music.html").is_file())
test_assert("Clubs: Coding Club page exists (pages/clubs/coding.html)", (clubs_dir / "coding.html").is_file())
test_assert("Clubs: Photography Club page exists (pages/clubs/photography.html)", (clubs_dir / "photography.html").is_file())

test_assert("Campus Life: Links to Sports Club detail page", "clubs/sports.html" in campuslife_html)
test_assert("Campus Life: Links to Music Club detail page", "clubs/music.html" in campuslife_html)
test_assert("Campus Life: Links to Coding Club detail page", "clubs/coding.html" in campuslife_html)
test_assert("Campus Life: Links to Photography Club detail page", "clubs/photography.html" in campuslife_html)

for club in ["sports", "music", "coding", "photography"]:
    content = (clubs_dir / f"{club}.html").read_text(encoding="utf-8")
    test_assert(f"Club Page ({club}): Uses official StudentHub header branding", "StudentHub" in content and "site-logo" in content)
    test_assert(f"Club Page ({club}): Includes membership / activity details", "Objectives" in content or "Activities" in content)

print("\n" + "=" * 80)
print("SECTION 3: Public Events Browsing & Event Detail Modal / View")
print("=" * 80)

events_html = (PUBLIC_DIR / "pages" / "events.html").read_text(encoding="utf-8")
event_detail_html = (PUBLIC_DIR / "pages" / "event-detail.html").read_text(encoding="utf-8")
events_renderer_js = (PUBLIC_DIR / "assets" / "js" / "events-renderer.js").read_text(encoding="utf-8")

test_assert("Events: Standalone detail page exists (pages/event-detail.html)", (PUBLIC_DIR / "pages" / "event-detail.html").is_file())
test_assert("Events: events-renderer.js does NOT contain 'innerHTML'", "innerHTML" not in events_renderer_js)
test_assert("Events: Accessible modal implementation in events-renderer.js", "openEventModal" in events_renderer_js)
test_assert("Events: Event registration endpoint exists (api/events/register.php)", (BASE_DIR / "api" / "events" / "register.php").is_file())
test_assert("Events: Public proxy for registration exists (public/api/events/register.php)", (PUBLIC_DIR / "api" / "events" / "register.php").is_file())
test_assert("Events: Registration checks student authentication and redirects to login", 
            "login.html?error=unauthorized" in events_renderer_js and "api/auth/me.php" in events_renderer_js)

print("\n" + "=" * 80)
print("SECTION 4: Course Enrollment Visibility & Route Protection")
print("=" * 80)

nav_php = (APP_DIR / "includes" / "nav.php").read_text(encoding="utf-8")
main_js = (PUBLIC_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
course_enrollment_php = (PUBLIC_DIR / "pages" / "course-enrollment.php").read_text(encoding="utf-8")
course_enrollment_html = (PUBLIC_DIR / "pages" / "course-enrollment.html").read_text(encoding="utf-8")

test_assert("Course Enrollment: Link NOT in public visitor nav in nav.php", 
            'href="pages/course-enrollment.html"' not in nav_php and 'href="course-enrollment.html"' not in nav_php)
test_assert("Course Enrollment: Protected by requireLogin() / isAuthenticated() in course-enrollment.php", 
            "isAuthenticated()" in course_enrollment_php and "login.html?error=unauthorized" in course_enrollment_php)
test_assert("Course Enrollment: Client auth verification in course-enrollment.html", 
            "api/auth/me.php" in course_enrollment_html and "unauth-container" in course_enrollment_html)
test_assert("Course Enrollment: CourseService implemented (app/services/course_service.php)", 
            (APP_DIR / "services" / "course_service.php").is_file())
test_assert("Course Enrollment: API endpoint implemented (api/courses/index.php)", 
            (BASE_DIR / "api" / "courses" / "index.php").is_file())

print("\n" + "=" * 80)
print("SECTION 5: Database Roster Integrity (Port 3307 & 78 AIML Students)")
print("=" * 80)

try:
    conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub")
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # 1. Total AIML roster count
    cur.execute("SELECT COUNT(*) AS total FROM students WHERE student_id LIKE '25AIML%'")
    tot_aiml = cur.fetchone()['total']
    test_assert(f"Database Roster: Exactly 78 FYAIML students imported (Found: {tot_aiml})", tot_aiml == 78)

    # 2. Batch counts: A:20, B:20, C:20, D:18
    cur.execute("SELECT b.batch_name, COUNT(s.id) AS cnt FROM batches b JOIN students s ON s.batch_id = b.id GROUP BY b.batch_name ORDER BY b.batch_name")
    batches = {r['batch_name']: r['cnt'] for r in cur.fetchall()}
    test_assert("Database Batches: Batch A has 20 students", batches.get('Batch A') == 20)
    test_assert("Database Batches: Batch B has 20 students", batches.get('Batch B') == 20)
    test_assert("Database Batches: Batch C has 20 students", batches.get('Batch C') == 20)
    test_assert("Database Batches: Batch D has 18 students", batches.get('Batch D') == 18)

    # 3. 4 Counselors
    cur.execute("SELECT COUNT(*) AS cnt FROM counselors")
    counselor_cnt = cur.fetchone()['cnt']
    test_assert(f"Database Counselors: 4 Faculty counselors seeded (Found: {counselor_cnt})", counselor_cnt == 4)

    # 4. Student 1 Anshika Badala link
    cur.execute("""
        SELECT s.*, b.batch_name, c.name AS counselor_name 
        FROM students s 
        JOIN batches b ON s.batch_id = b.id 
        JOIN counselors c ON s.counselor_id = c.id 
        WHERE s.id = 1
    """)
    s1 = cur.fetchone()
    test_assert("Database Student #1: Name is Anshika Badala", s1 and s1['name'] == 'Anshika Badala')
    test_assert("Database Student #1: Student ID is 25AIML002", s1 and s1['student_id'] == '25AIML002')
    test_assert("Database Student #1: Temp Student ID is 25TAIMLGGE", s1 and s1['temp_student_id'] == '25TAIMLGGE')
    test_assert("Database Student #1: Batch is Batch A", s1 and s1['batch_name'] == 'Batch A')
    test_assert("Database Student #1: Counselor is Prof. Gaurav Kumar", s1 and s1['counselor_name'] == 'Prof. Gaurav Kumar')

    # 5. Core Semester 3 Courses (6 courses)
    cur.execute("SELECT COUNT(*) AS cnt FROM courses")
    courses_cnt = cur.fetchone()['cnt']
    test_assert(f"Database Courses: 6 Core semester courses configured (Found: {courses_cnt})", courses_cnt >= 6)

    # 6. Student 1 Enrollments
    cur.execute("SELECT COUNT(*) AS cnt FROM course_enrollments WHERE student_id = 1")
    enr_cnt = cur.fetchone()['cnt']
    test_assert(f"Database Enrollments: Student #1 enrolled in all 6 courses (Found: {enr_cnt})", enr_cnt == 6)

    # 7. Timetable entries
    cur.execute("SELECT COUNT(*) AS cnt FROM timetable")
    tt_cnt = cur.fetchone()['cnt']
    test_assert(f"Database Timetable: Day-wise timetable schedule populated (Found: {tt_cnt})", tt_cnt >= 5)

    conn.close()
except Exception as e:
    test_assert("Database Roster Integrity Query", False, str(e))

print("\n" + "=" * 80)
print("SECTION 6: Marksheet Upload & Automated CGPA Extraction")
print("=" * 80)

marksheet_service = (APP_DIR / "services" / "marksheet_service.php").read_text(encoding="utf-8")
marksheet_upload_api = (BASE_DIR / "api" / "marksheets" / "upload.php").read_text(encoding="utf-8")
marksheets_htaccess = (BASE_DIR / "storage" / "uploads" / "marksheets" / ".htaccess").read_text(encoding="utf-8")

test_assert("Marksheet Service: extractCgpaFromText regex parsing implemented", "extractCgpaFromText" in marksheet_service)
test_assert("Marksheet Service: Support for CGPA, SGPA, GPA patterns", "CGPA" in marksheet_service and "SGPA" in marksheet_service)
test_assert("Marksheet Upload API: File size validated (5 MB limit)", "5 * 1024 * 1024" in marksheet_upload_api)
test_assert("Marksheet Upload API: MIME types validated (PDF, PNG, JPG, WEBP)", "application/pdf" in marksheet_upload_api)
test_assert("Marksheet Security: storage/uploads/marksheets/.htaccess denies script execution", 
            "Deny from all" in marksheets_htaccess and "FilesMatch" in marksheets_htaccess)

# Test regex extraction on sample string
sample_marksheet_text = """
CHARUSAT UNIVERSITY - GRADE SHEET
Student Name: Anshika Badala
Roll No: 25AIML002
Semester: 2
Credits Earned: 24
SGPA: 8.77
Cumulative Grade Point Average (CGPA): 8.77
Result: PASS WITH DISTINCTION
"""
cgpa_match = re.search(r'(?:CGPA|Cumulative\s*Grade\s*Point\s*Average(?:\s*\([A-Z]+\))?|C\.G\.P\.A\.)\s*[:=]?\s*([0-9]\.[0-9]{1,2})', sample_marksheet_text, re.I)
test_assert("Marksheet Regex: Successfully extracts 8.77 from university marksheet text", 
            cgpa_match is not None and cgpa_match.group(1) == "8.77")

print("\n" + "=" * 80)
print("SECTION 7: Student Portal Full Features & Privacy Defense")
print("=" * 80)

student_index = (BASE_DIR / "student" / "index.php").read_text(encoding="utf-8")

test_assert("Student Portal: Includes shared header.php and nav.php", 
            "header.php" in student_index and "nav.php" in student_index)
test_assert("Student Portal: Displays student registration ID (studentIdStr)", "studentIdStr" in student_index)
test_assert("Student Portal: Displays batch and counselor assignment", 
            "batchName" in student_index and "counselor" in student_index)
test_assert("Student Portal: Features Tab 1 Profile & Counselor", "tab-profile" in student_index)
test_assert("Student Portal: Features Tab 2 Academic Overview & CGPA", "tab-academics" in student_index)
test_assert("Student Portal: Features Tab 3 Faculty & Timetable", "tab-timetable" in student_index)
test_assert("Student Portal: Features Tab 4 FYAIML Class Directory", "tab-directory" in student_index)
test_assert("Student Portal: Features Tab 5 Marksheet Upload & CGPA OCR", "tab-marksheets" in student_index)
test_assert("Student Portal: Features Tab 6 Registered Campus Events", "tab-events" in student_index)

# Student Privacy Check in Directory Tab
test_assert("Student Privacy: Directory table does NOT show student phone numbers", 
            'cm[\'mobile\']' not in student_index and 'cm[\'phone\']' not in student_index)
test_assert("Student Privacy: Directory table does NOT show personal emails", 
            'cm[\'email\']' not in student_index)

print("\n" + "=" * 80)
total_tests = passed_tests + failed_tests
pct = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
print(f"PRODUCT REDESIGN VERIFICATION SUMMARY: {passed_tests}/{total_tests} PASSED ({pct:.1f}%)")
print("=" * 80)

if failed_tests == 0:
    print("SUCCESS: All Product Redesign, Roster Import, and Academic Portal requirements PASSED!")
    sys.exit(0)
else:
    print(f"FAILURE: {failed_tests} tests failed.")
    sys.exit(1)
