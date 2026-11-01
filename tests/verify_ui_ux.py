#!/usr/bin/env python3
"""
StudentHub - UI/UX Consistency, Layout Responsiveness & Path Verification Suite
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
"""

import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"
APP_DIR = BASE_DIR / "app"
ADMIN_DIR = BASE_DIR / "admin"
STUDENT_DIR = BASE_DIR / "student"
CSS_DIR = PUBLIC_DIR / "assets" / "css"

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

print("\n" + "=" * 75)
print("SECTION 1: Responsive Layout & Elimination of Narrow Desktop Bottlenecks")
print("=" * 75)

main_css = (CSS_DIR / "main.css").read_text(encoding="utf-8")
home_css = (CSS_DIR / "home.css").read_text(encoding="utf-8")
dash_css = (CSS_DIR / "dashboard.css").read_text(encoding="utf-8")
admin_css = (CSS_DIR / "admin.css").read_text(encoding="utf-8")
about_css = (CSS_DIR / "about.css").read_text(encoding="utf-8")
campus_css = (CSS_DIR / "campuslife.css").read_text(encoding="utf-8")
contact_css = (CSS_DIR / "contact.css").read_text(encoding="utf-8")
events_css = (CSS_DIR / "events.css").read_text(encoding="utf-8")
faq_css = (CSS_DIR / "faq.css").read_text(encoding="utf-8")

# 1.1 Responsive container variables in main.css
log_test("Design Tokens: --container-max-width is defined (>= 1200px)",
         "--container-max-width: 1240px" in main_css or "--container-max-width: 1280px" in main_css)
log_test("Design Tokens: --container-padding is defined",
         "--container-padding" in main_css)
log_test("Design Tokens: Modern sans-serif font stack configured",
         "--font-stack" in main_css and "-apple-system" in main_css and "sans-serif" in main_css)

# 1.2 Multi-column wide hero grid on desktop in home.css
log_test("Home Page: Hero section configured with 4-column desktop grid",
         "grid-template-columns: repeat(4, 1fr)" in home_css)
log_test("Home Page: Welcome section matches wide container max-width",
         "max-width: var(--container-max-width" in home_css)

# 1.3 Dashboard / Student portal container width
log_test("Dashboard / Student Portal: Container matches responsive container width",
         "max-width: var(--container-max-width" in dash_css)
log_test("Dashboard / Student Portal: Free of rigid 800px max-width bottleneck",
         "max-width: 800px" not in dash_css)

# 1.4 Admin services & portal container width
log_test("Admin Services: List matches wide responsive container",
         "max-width: var(--container-max-width" in admin_css)
log_test("Admin Services: Free of rigid 750px/800px bottlenecks",
         "max-width: 800px" not in admin_css and "max-width: 750px" not in admin_css)
log_test("Admin Portal: .admin-container matches responsive container max-width",
         "max-width: var(--container-max-width" in admin_css)

# 1.5 Subpage containers use 1240px max width
log_test("About Page: Container matches responsive container max-width",
         "max-width: var(--container-max-width" in about_css)
log_test("Campus Life: Clubs list matches responsive container max-width",
         "max-width: var(--container-max-width" in campus_css)
log_test("Contact Page: Container matches responsive container max-width",
         "max-width: var(--container-max-width" in contact_css)
log_test("Events Page: Container matches responsive container max-width",
         "max-width: var(--container-max-width" in events_css)
log_test("FAQ Page: Container matches responsive container max-width",
         "max-width: var(--container-max-width" in faq_css)

# 1.6 Responsive Viewport Breakpoints
log_test("Responsive Breakpoint: Big PC screen optimization (>= 1400px)",
         "@media (min-width: 1400px)" in main_css)
log_test("Responsive Breakpoint: Tablet optimization (max-width: 1023px)",
         "1023px" in main_css)
log_test("Responsive Breakpoint: Mobile optimization (< 768px)",
         "767px" in main_css or "768px" in main_css)

print("\n" + "=" * 75)
print("SECTION 2: Unified Design System & Common UI Components")
print("=" * 75)

# 2.1 Color Consistency
log_test("Color Palette: Primary navy blue #1E3A8A defined in main.css",
         "#1E3A8A" in main_css)
log_test("Color Palette: Accent royal blue #2563EB defined in main.css",
         "#2563EB" in main_css)
log_test("Color Palette: Unified page background #F4F7FC defined in main.css",
         "#F4F7FC" in main_css)

# 2.2 Header Component & Brand Bar
header_php = (APP_DIR / "includes" / "header.php").read_text(encoding="utf-8")
log_test("Header Component: App header includes site-header class",
         "site-header" in header_php)
log_test("Header Component: Includes authentic StudentHub logo image",
         "site-logo" in header_php and "studenthub_co_logo" in header_php)
log_test("Header Component: Includes StudentHub brand title and campus subtitle",
         "StudentHub" in header_php and "CSPIT, CHARUSAT" in header_php)
log_test("Header Component: Includes user-header-status container for login state",
         "user-header-status" in header_php)
log_test("Header Component: Displays user avatar circle when authenticated",
         "user-avatar-circle" in header_php)
log_test("Header Component: Displays user role badge (Student/Admin)",
         "user-role-badge" in header_php)
log_test("Header Component: Renders Sign In & Register controls for guests",
         "btn-header-login" in header_php and "btn-header-register" in header_php)
log_test("Header Component: Includes mobile navigation toggle button",
         "nav-toggle-btn" in header_php)

# 2.3 Navigation Bar Component
nav_php = (APP_DIR / "includes" / "nav.php").read_text(encoding="utf-8")
log_test("Navigation Component: Uses main-nav class with primary color styling",
         "main-nav" in nav_php)
log_test("Navigation Component: Links all standard public pages",
         all(p in nav_php for p in ['administrative', 'campuslife', 'course-enrollment', 'events', 'registration', 'dashboard', 'about', 'contact', 'faq']))
log_test("Navigation Component: Dynamically displays Admin Portal for admins",
         "Admin Portal" in nav_php and "admin" in nav_php)
log_test("Navigation Component: Dynamically displays My Portal for students",
         "My Portal" in nav_php and "student" in nav_php)
log_test("Navigation Component: Dynamically displays Logout link for authenticated sessions",
         "process-logout.php" in nav_php and "Logout" in nav_php)

# 2.4 Admin Subnavigation Bar Component
admin_subnav_file = APP_DIR / "includes" / "admin_subnav.php"
log_test("Admin Subnav Component: app/includes/admin_subnav.php exists", admin_subnav_file.is_file())
admin_subnav_php = admin_subnav_file.read_text(encoding="utf-8") if admin_subnav_file.is_file() else ""
log_test("Admin Subnav Component: Links to Dashboard (index.php)", "index.php" in admin_subnav_php)
log_test("Admin Subnav Component: Links to Student Management (students.php)", "students.php" in admin_subnav_php)
log_test("Admin Subnav Component: Links to Event Management (events.php)", "events.php" in admin_subnav_php)
log_test("Admin Subnav Component: Links back to Public Portal", "public/index.html" in admin_subnav_php)

# 2.5 Admin Pages Integration
admin_idx = (ADMIN_DIR / "index.php").read_text(encoding="utf-8")
admin_stu = (ADMIN_DIR / "students.php").read_text(encoding="utf-8")
admin_ev = (ADMIN_DIR / "events.php").read_text(encoding="utf-8")

log_test("Admin Dashboard: Includes shared header.php", "header.php" in admin_idx)
log_test("Admin Dashboard: Includes shared nav.php", "nav.php" in admin_idx)
log_test("Admin Dashboard: Includes shared admin_subnav.php", "admin_subnav.php" in admin_idx)
log_test("Admin Dashboard: Includes shared footer.php", "footer.php" in admin_idx)

log_test("Admin Students: Includes shared header.php", "header.php" in admin_stu)
log_test("Admin Students: Includes shared nav.php", "nav.php" in admin_stu)
log_test("Admin Students: Includes shared admin_subnav.php", "admin_subnav.php" in admin_stu)

log_test("Admin Events: Includes shared header.php", "header.php" in admin_ev)
log_test("Admin Events: Includes shared nav.php", "nav.php" in admin_ev)
log_test("Admin Events: Includes shared admin_subnav.php", "admin_subnav.php" in admin_ev)

print("\n" + "=" * 75)
print("SECTION 3: URL Integrity & Relative Link Resolution (No Nested/Broken URLs)")
print("=" * 75)

contexts = {
    'public_root': PUBLIC_DIR,
    'public_pages': PUBLIC_DIR / 'pages',
    'admin': ADMIN_DIR,
    'student': STUDENT_DIR
}

for ctx_name, ctx_path in contexts.items():
    if ctx_name == 'public_root':
        bp = ''
        home = 'index.html'
        pages_pfx = 'pages/'
        admin_url = '../admin/index.php'
        student_url = '../student/index.php'
        logout_url = 'process-logout.php'
        login_url = 'pages/login.html'
    elif ctx_name == 'public_pages':
        bp = '../'
        home = '../index.html'
        pages_pfx = ''
        admin_url = '../../admin/index.php'
        student_url = '../../student/index.php'
        logout_url = '../process-logout.php'
        login_url = 'login.html'
    elif ctx_name == 'admin':
        bp = '../public/'
        home = '../public/index.html'
        pages_pfx = '../public/pages/'
        admin_url = 'index.php'
        student_url = '../student/index.php'
        logout_url = '../public/process-logout.php'
        login_url = '../public/pages/login.html'
    elif ctx_name == 'student':
        bp = '../public/'
        home = '../public/index.html'
        pages_pfx = '../public/pages/'
        admin_url = '../admin/index.php'
        student_url = 'index.php'
        logout_url = '../public/process-logout.php'
        login_url = '../public/pages/login.html'

    targets = {
        f"{ctx_name} -> home": ctx_path / home,
        f"{ctx_name} -> administrative": ctx_path / (pages_pfx + 'administrative.html'),
        f"{ctx_name} -> campuslife": ctx_path / (pages_pfx + 'campuslife.html'),
        f"{ctx_name} -> course-enrollment": ctx_path / (pages_pfx + 'course-enrollment.html'),
        f"{ctx_name} -> events": ctx_path / (pages_pfx + 'events.html'),
        f"{ctx_name} -> registration": ctx_path / (pages_pfx + 'registration.html'),
        f"{ctx_name} -> dashboard": ctx_path / (pages_pfx + 'dashboard.html'),
        f"{ctx_name} -> about": ctx_path / (pages_pfx + 'about.html'),
        f"{ctx_name} -> contact": ctx_path / (pages_pfx + 'contact.html'),
        f"{ctx_name} -> faq": ctx_path / (pages_pfx + 'faq.html'),
        f"{ctx_name} -> login": ctx_path / login_url,
        f"{ctx_name} -> admin": ctx_path / admin_url,
        f"{ctx_name} -> student": ctx_path / student_url,
        f"{ctx_name} -> logout": ctx_path / logout_url,
        f"{ctx_name} -> css": ctx_path / (bp + 'assets/css/main.css')
    }

    all_exist = True
    missing_items = []
    for lbl, t_path in targets.items():
        if not t_path.resolve().exists():
            all_exist = False
            missing_items.append(f"{lbl}: {t_path.resolve()}")

    log_test(f"URL Integrity: All 15 navigation paths resolve from {ctx_name} context",
             all_exist, ", ".join(missing_items))

# 3.2 Ensure no double-nested /pages/pages/ in any codebase files
nested_matches = []
for p in PUBLIC_DIR.glob("**/*.html"):
    text = p.read_text(encoding="utf-8")
    if "pages/pages" in text:
        nested_matches.append(str(p))
for p in ADMIN_DIR.glob("**/*.php"):
    text = p.read_text(encoding="utf-8")
    if "pages/pages" in text or "admin/pages" in text:
        nested_matches.append(str(p))

log_test("URL Hygiene: Zero instances of double-nested 'pages/pages' paths", len(nested_matches) == 0, str(nested_matches))

print("\n" + "=" * 75)
print("SECTION 4: Logged-In Student State & Real MySQL Data Integration")
print("=" * 75)

student_idx = (STUDENT_DIR / "index.php").read_text(encoding="utf-8")
log_test("Student Portal: Includes shared header.php", "header.php" in student_idx)
log_test("Student Portal: Includes shared nav.php", "nav.php" in student_idx)
log_test("Student Portal: Includes shared footer.php", "footer.php" in student_idx)
log_test("Student Portal: Queries authentic student profile via StudentService",
         "StudentService::getById" in student_idx or "StudentService::findByUserId" in student_idx or "StudentService::findByEmail" in student_idx)
log_test("Student Portal: Queries authentic registered events via StudentService",
         "StudentService::getRegisteredEvents" in student_idx)
log_test("Student Portal: Displays student registration ID", "studentIdStr" in student_idx)
log_test("Student Portal: Displays registered events table", "Registered Campus Events" in student_idx and "<table" in student_idx)
log_test("Student Portal: Displays responsive profile details grid", "student-info-grid" in student_idx)
log_test("Student Portal: Enforces authentication via checkAuth() guard", "checkAuth(" in student_idx)
log_test("Student Portal: Displays Sign Out link to process-logout.php", "process-logout.php" in student_idx)

# Live Database Query Verification
try:
    import pymysql
    conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub")
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Check student with user_id = 2 (Anshika Badala)
    cur.execute("SELECT s.*, u.username FROM students s JOIN users u ON s.user_id = u.id WHERE u.username = 'anshika' LIMIT 1")
    stu_record = cur.fetchone()
    log_test("Database Student Record: Anshika Badala student profile linked to active user",
             stu_record is not None and stu_record['name'] == 'Anshika Badala' and stu_record['department'] == 'Information Technology')

    # Check registered events for student #1
    cur.execute("SELECT r.id, e.title, e.event_date FROM registrations r JOIN events e ON r.event_id = e.id WHERE r.student_id = 1")
    regs = cur.fetchall()
    log_test("Database Registered Events: Student #1 has real event registrations (Found: %d)" % len(regs),
             len(regs) >= 2 and any('Hackathon' in r['title'] for r in regs))
    conn.close()
except Exception as e:
    log_test("Database Student Query Verification", False, str(e))

print("\n" + "=" * 75)
print("SECTION 5: REST API Current User Identity & JavaScript Controller")
print("=" * 75)

me_php_file = BASE_DIR / "api" / "auth" / "me.php"
log_test("REST API: api/auth/me.php endpoint exists", me_php_file.is_file())
me_php = me_php_file.read_text(encoding="utf-8") if me_php_file.is_file() else ""
log_test("REST API: Handles unauthenticated sessions cleanly", "authenticated" in me_php and "isAuthenticated()" in me_php)
log_test("REST API: Returns current user role and displayName", "displayName" in me_php and "role" in me_php)
log_test("REST API: Resolves student profile from database", "StudentService::" in me_php)

main_js = (PUBLIC_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
log_test("Client JS: Active link highlighting implemented", "link.classList.add(\"active\")" in main_js or "classList.add('active')" in main_js)
log_test("Client JS: Mobile nav toggle listener implemented", "navToggleBtn" in main_js and "nav-open" in main_js)
log_test("Client JS: Automatically synchronizes header user authentication state", "syncUserAuthenticationState" in main_js)
log_test("Client JS: Dynamically wraps tables in .table-responsive", "table-responsive" in main_js)
log_test("Client JS: Auto-populates CSRF token field", "csrf_token" in main_js)

print("\n" + "=" * 75)
print(f"UI/UX CORRECTION VERIFICATION SUMMARY: {passed_count}/{passed_count + failed_count} PASSED ({passed_count / (passed_count + failed_count) * 100:.1f}%)")
print("=" * 75)

if failed_count > 0:
    print(f"FAILURE: {failed_count} tests failed!")
    sys.exit(1)
else:
    print("SUCCESS: All UI/UX consistency, responsiveness, and path verification tests PASSED!\n")
    sys.exit(0)
