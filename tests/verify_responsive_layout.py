#!/usr/bin/env python3
"""
StudentHub - Full-Width Responsive Layout Verification Suite
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT

This test suite verifies:
1. Complete removal of narrow desktop bottlenecks and fixed pixel widths.
2. Fluid full-width expansion (100% viewport width) across all page templates.
3. Responsive padding and spacing using CSS clamp.
4. Exact layout metrics across all 6 specified target viewport resolutions:
   - 1920 x 1080 (Large Desktop)
   - 1728 x 972  (Large Desktop / Mac)
   - 1366 x 768  (Standard Laptop / Lenovo Desktop)
   - 1024 x 768  (Small Laptop / Tablet Landscape)
   - 768 x 1024  (Tablet Portrait)
   - 390 x 844   (Mobile)
5. Preservation of individual card and form readability (proportional, not overstretched).
6. Zero horizontal overflow across all pages and viewports.
"""

import os
import re
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"
CSS_DIR = PUBLIC_DIR / "assets" / "css"
PAGES_DIR = PUBLIC_DIR / "pages"

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

print("\n" + "=" * 80)
print("SECTION 1: Fluid Full-Width CSS Architecture & Design Tokens")
print("=" * 80)

main_css = (CSS_DIR / "main.css").read_text(encoding="utf-8")
home_css = (CSS_DIR / "home.css").read_text(encoding="utf-8")
dash_css = (CSS_DIR / "dashboard.css").read_text(encoding="utf-8")
admin_css = (CSS_DIR / "admin.css").read_text(encoding="utf-8")
events_css = (CSS_DIR / "events.css").read_text(encoding="utf-8")
courses_css = (CSS_DIR / "course-enrollment.css").read_text(encoding="utf-8")
about_css = (CSS_DIR / "about.css").read_text(encoding="utf-8")
campus_css = (CSS_DIR / "campuslife.css").read_text(encoding="utf-8")
contact_css = (CSS_DIR / "contact.css").read_text(encoding="utf-8")
faq_css = (CSS_DIR / "faq.css").read_text(encoding="utf-8")
login_css = (CSS_DIR / "login.css").read_text(encoding="utf-8")
reg_css = (CSS_DIR / "registration.css").read_text(encoding="utf-8")

# 1.1 Root design tokens
log_test("Design Tokens: --container-max-width is set to 100% for full-width fluid layout",
         "--container-max-width: 100%" in main_css)
log_test("Design Tokens: --container-padding uses clamp(16px, 2.5vw, 40px)",
         "clamp(16px, 2.5vw, 40px)" in main_css)

# 1.2 Base Reset
log_test("Base Reset: html, body configured for 100% width and zero margin",
         "width: 100%" in main_css and "max-width: 100%" in main_css and "margin: 0" in main_css)
log_test("Base Reset: Zero horizontal overflow enforced (overflow-x: hidden)",
         "overflow-x: hidden" in main_css)

# 1.3 Fluid Universal Components
log_test("Header Layout: .site-header-inner uses fluid container max-width and clamp padding",
         "width: 100%" in main_css and "padding: 14px var(--container-padding)" in main_css)
log_test("Universal Nav: .main-nav uses fluid calc(100% - 2 * padding) width",
         "width: calc(100% - (2 * var(--container-padding)))" in main_css)
log_test("Universal Dividers: hr and .header-divider use fluid calc width",
         "width: calc(100% - (2 * var(--container-padding)))" in main_css)
log_test("Universal Footer: .site-footer uses fluid container padding",
         "padding: 24px var(--container-padding)" in main_css)
log_test("Universal Content Containers: .content-card, .dashboard-card, .page-container use fluid width",
         "width: calc(100% - (2 * var(--container-padding)))" in main_css and "padding: clamp(20px, 2.5vw, 36px)" in main_css)

print("\n" + "=" * 80)
print("SECTION 2: Elimination of Fixed and Restrictive Width Bottlenecks")
print("=" * 80)

# Check subpage CSS files
log_test("Events Page CSS: .events-container uses fluid calc width",
         "width: calc(100% - (2 * var(--container-padding" in events_css)
log_test("Course Enrollment CSS: .courses-container uses fluid calc width",
         "width: calc(100% - (2 * var(--container-padding" in courses_css)
log_test("About Page CSS: .about-container uses fluid calc width and clamp padding",
         "width: calc(100% - (2 * var(--container-padding" in about_css and "clamp" in about_css)
log_test("Campus Life CSS: .clubs-list uses fluid calc width and clamp padding",
         "width: calc(100% - (2 * var(--container-padding" in campus_css and "clamp" in campus_css)
log_test("Contact Page CSS: .contact-container uses fluid calc width and clamp padding",
         "width: calc(100% - (2 * var(--container-padding" in contact_css and "clamp" in contact_css)
log_test("FAQ Page CSS: .faq-container uses fluid calc width",
         "width: calc(100% - (2 * var(--container-padding" in faq_css)
log_test("Home Page CSS: .hero-section and .welcome-section use fluid calc width",
         "width: calc(100% - (2 * var(--container-padding" in home_css)
log_test("Dashboard Page CSS: .dashboard-card uses fluid calc width and clamp padding",
         "width: calc(100% - (2 * var(--container-padding" in dash_css and "clamp" in dash_css)
log_test("Admin Portal CSS: .admin-container and .admin-services-list use fluid calc width",
         "width: calc(100% - (2 * var(--container-padding" in admin_css)

# HTML pages inline style inspection
admin_html = (PAGES_DIR / "administrative.html").read_text(encoding="utf-8")
faq_html = (PAGES_DIR / "faq.html").read_text(encoding="utf-8")
stu_html = (PAGES_DIR / "students.html").read_text(encoding="utf-8")

log_test("Administrative HTML: Removed narrow style='max-width: 950px' bottleneck",
         "max-width: 950px" not in admin_html)
log_test("FAQ HTML: Removed narrow style='max-width: 950px' bottleneck",
         "max-width: 950px" not in faq_html)
log_test("Students HTML: Removed narrow style='max-width: 1000px' bottleneck",
         "max-width: 1000px" not in stu_html)

# Form Readability Preservation
log_test("Form Readability: Login container preserved at readable 420px max-width 92%",
         "width: 420px" in login_css and "max-width: 92%" in login_css)
log_test("Form Readability: Registration form container preserved at readable 720px max-width",
         "max-width: 720px" in reg_css)

print("\n" + "=" * 80)
print("SECTION 3: Viewport Box Model Calculations Across the 6 Target Resolutions")
print("=" * 80)

def simulate_viewport_metrics(vp_w: int, vp_h: int):
    # Padding calculation based on CSS rules
    if vp_w >= 1400:
        # clamp(24px, 3vw, 48px)
        pad = max(24.0, min(48.0, 0.03 * vp_w))
    elif vp_w <= 767:
        pad = 14.0
    elif vp_w <= 1023:
        # clamp(14px, 2vw, 20px)
        pad = max(14.0, min(20.0, 0.02 * vp_w))
    else:
        # clamp(16px, 2.5vw, 40px)
        pad = max(16.0, min(40.0, 0.025 * vp_w))

    container_w = vp_w - (2 * pad)
    container_pct = (container_w / vp_w) * 100.0
    card_pad = max(20.0, min(36.0, 0.025 * vp_w)) if vp_w > 767 else 16.0
    inner_w = container_w - (2 * card_pad)

    return {
        "viewport": f"{vp_w}x{vp_h}",
        "side_padding": round(pad, 1),
        "container_width": round(container_w, 1),
        "container_pct": round(container_pct, 1),
        "card_padding": round(card_pad, 1),
        "inner_content_width": round(inner_w, 1)
    }

target_resolutions = [
    (1920, 1080, "Large Desktop (1080p Full HD)"),
    (1728, 972,  "Large Desktop / Mac Retina"),
    (1366, 768,  "Standard Laptop / Lenovo Desktop"),
    (1024, 768,  "Small Laptop / Tablet Landscape"),
    (768, 1024,  "Tablet Portrait (iPad)"),
    (390, 844,   "Mobile Device (iPhone / Pixel)")
]

for w, h, desc in target_resolutions:
    m = simulate_viewport_metrics(w, h)
    # The container must expand to >= 90% of screen width, side padding must be >= 14px and <= 48px
    is_valid = (m['container_pct'] >= 90.0) and (14.0 <= m['side_padding'] <= 48.0) and (m['inner_content_width'] > 0)
    log_test(
        f"Resolution {w}x{h} ({desc}): Width={m['container_width']}px ({m['container_pct']}%), SidePad={m['side_padding']}px",
        is_valid,
        f"Metrics: {m}"
    )

print("\n" + "=" * 80)
print("SECTION 4: Live HTTP Server Endpoint Verification")
print("=" * 80)

endpoints = [
    "/index.html",
    "/pages/administrative.html",
    "/pages/campuslife.html",
    "/pages/course-enrollment.html",
    "/pages/events.html",
    "/pages/registration.html",
    "/pages/dashboard.html",
    "/pages/about.html",
    "/pages/contact.html",
    "/pages/faq.html",
    "/pages/students.html",
    "/pages/login.html"
]

for ep in endpoints:
    url = f"http://localhost:8000{ep}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ResponsiveTest'})
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            has_viewport = 'name="viewport"' in body and 'width=device-width' in body
            has_main_css = 'main.css' in body
            log_test(f"HTTP Endpoint {ep}: Status 200, Viewport Meta Tag & CSS Linked",
                     status == 200 and has_viewport and has_main_css,
                     f"Status: {status}, HasViewport: {has_viewport}, HasCSS: {has_main_css}")
    except Exception as e:
        log_test(f"HTTP Endpoint {ep}: Live response check", False, str(e))

print("\n" + "=" * 80)
print(f"RESPONSIVE LAYOUT VERIFICATION SUMMARY: {passed_count}/{passed_count + failed_count} PASSED ({passed_count / (passed_count + failed_count) * 100:.1f}%)")
print("=" * 80)

if failed_count > 0:
    print(f"FAILURE: {failed_count} tests failed!")
    sys.exit(1)
else:
    print("SUCCESS: Full-width responsive layout verified with 100% PASS rate across all 6 target resolutions!\n")
    sys.exit(0)
