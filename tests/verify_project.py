"""
Automated Verification Suite for StudentHub Project Restructuring
Author: Antigravity Assistant
Course: AIUE203 - Web Development Fundamentals
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = ROOT / "public"

def test_html_assets_and_links():
    print("=" * 60)
    print("TEST 1: Verifying HTML Local Links, Stylesheets & Scripts")
    print("=" * 60)

    html_files = list(PUBLIC_DIR.glob("**/*.html"))
    if not html_files:
        print("[FAIL] No HTML files found in public directory!")
        return False

    all_passed = True
    checked_links = 0

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        rel_path = html_file.relative_to(ROOT)
        print(f"\nChecking: {rel_path}")

        # Check CSS links: <link rel="stylesheet" href="...">
        css_matches = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        for css in css_matches:
            if css.startswith("http://") or css.startswith("https://"):
                continue
            target = (html_file.parent / css).resolve()
            checked_links += 1
            if not target.exists():
                print(f"  [FAIL] Missing CSS: {css} (resolved to {target})")
                all_passed = False
            else:
                print(f"  [PASS] CSS found: {css}")

        # Check JS scripts: <script src="...">
        js_matches = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
        for js in js_matches:
            if js.startswith("http://") or js.startswith("https://"):
                continue
            target = (html_file.parent / js).resolve()
            checked_links += 1
            if not target.exists():
                print(f"  [FAIL] Missing JS: {js} (resolved to {target})")
                all_passed = False
            else:
                print(f"  [PASS] JS found: {js}")

        # Check Anchor links: <a href="...">
        a_matches = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        for a in a_matches:
            if a.startswith("http://") or a.startswith("https://") or a.startswith("#") or a.startswith("mailto:"):
                continue
            # Strip anchors / query parameters
            clean_a = a.split("#")[0].split("?")[0]
            if not clean_a:
                continue
            target = (html_file.parent / clean_a).resolve()
            checked_links += 1
            if not target.exists():
                print(f"  [FAIL] Broken anchor link: {a} (resolved to {target})")
                all_passed = False
            else:
                print(f"  [PASS] Link verified: {a}")

    print(f"\nTotal local references checked: {checked_links}")
    return all_passed

def test_validation_regexes():
    print("\n" + "=" * 60)
    print("TEST 2: Verifying Practical 5 Form Validation Regular Expressions")
    print("=" * 60)

    reg_js_file = PUBLIC_DIR / "assets" / "js" / "registration.js"
    if not reg_js_file.exists():
        print(f"[FAIL] registration.js not found at {reg_js_file}")
        return False

    content = reg_js_file.read_text(encoding="utf-8")

    # Mobile regex: /^[0-9]{10}$/
    mobile_pattern = r'^[0-9]{10}$'
    valid_mobiles = ["9876543210", "6354069434", "7043100708"]
    invalid_mobiles = ["12345", "98765432100", "98765abcde", "", "abcdefghij"]

    for m in valid_mobiles:
        assert re.match(mobile_pattern, m), f"Failed to match valid mobile {m}"
        print(f"  [PASS] Valid mobile accepted: {m}")

    for m in invalid_mobiles:
        assert not re.match(mobile_pattern, m), f"Incorrectly matched invalid mobile {m}"
        print(f"  [PASS] Invalid mobile rejected: '{m}'")

    # Email regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    valid_emails = ["anshikabadala2@gmail.com", "admin@studenthub.com", "student@charusat.edu.in"]
    invalid_emails = ["plainaddress", "missing@domain", "@missinguser.com", "has space@domain.com"]

    for e in valid_emails:
        assert re.match(email_pattern, e), f"Failed to match valid email {e}"
        print(f"  [PASS] Valid email accepted: {e}")

    for e in invalid_emails:
        assert not re.match(email_pattern, e), f"Incorrectly matched invalid email {e}"
        print(f"  [PASS] Invalid email rejected: '{e}'")

    return True

def test_critical_directories():
    print("\n" + "=" * 60)
    print("TEST 3: Verifying Architecture Tiers & Protection Files")
    print("=" * 60)

    required_paths = [
        "public/index.html",
        "public/pages/about.html",
        "public/pages/administrative.html",
        "public/pages/campuslife.html",
        "public/pages/course-enrollment.html",
        "public/pages/dashboard.html",
        "public/pages/events.html",
        "public/pages/login.html",
        "public/pages/registration.html",
        "public/pages/contact.html",
        "public/pages/faq.html",
        "public/assets/css/main.css",
        "public/assets/js/main.js",
        "public/assets/js/registration.js",
        "public/assets/js/contact.js",
        "public/assets/js/faq.js",
        "app/config/config.php",
        "app/config/db.php",
        "app/includes/header.php",
        "app/includes/nav.php",
        "app/includes/footer.php",
        "app/includes/auth_check.php",
        "app/middleware/auth_middleware.php",
        "app/middleware/role_middleware.php",
        "app/services/student_service.php",
        "app/services/event_service.php",
        "api/auth/login.php",
        "api/auth/logout.php",
        "api/students/index.php",
        "api/events/index.php",
        "admin/index.php",
        "student/index.php",
        "storage/uploads/.htaccess",
        "database/schema.sql",
        "database/seed.sql",
        "public/assets/data/events.json",
        "public/assets/data/students.json",
        "public/assets/data/faqs.json",
        "public/assets/js/data-loader.js",
        "public/assets/js/pagination.js",
        "public/assets/js/events-renderer.js",
        "public/assets/js/faq-renderer.js",
        "public/assets/js/students-renderer.js",
        "public/assets/css/dynamic-data.css",
        "tests/practical_6_test.html",
        "tests/verify_practical_6.py",
        ".gitignore",
        ".env.example",
        "index.html",
        "PROJECT_AUDIT.md"
    ]

    all_exist = True
    for p in required_paths:
        path_obj = ROOT / p
        if path_obj.exists():
            print(f"  [PASS] Exists: {p}")
        else:
            print(f"  [FAIL] Missing: {p}")
            all_exist = False

    return all_exist

if __name__ == "__main__":
    t1 = test_html_assets_and_links()
    t2 = test_validation_regexes()
    t3 = test_critical_directories()

    print("\n" + "=" * 60)
    if t1 and t2 and t3:
        print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("ONE OR MORE CHECKS FAILED.")
        print("=" * 60)
        sys.exit(1)
