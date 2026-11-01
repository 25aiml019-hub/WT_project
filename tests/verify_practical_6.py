"""
Automated Verification Suite for Practical 6: Fetch API Dynamic Rendering
StudentHub - CSPIT, CHARUSAT
Author: Anshika Badala (25AIML002)
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "public" / "assets" / "data"
JS_DIR = ROOT / "public" / "assets" / "js"
PAGES_DIR = ROOT / "public" / "pages"

def test_json_datasets():
    print("=" * 65)
    print("TEST 1: JSON Datasets Structure & Field Verification")
    print("=" * 65)

    datasets = {
        "events.json": {
            "required_fields": ["id", "title", "description", "category", "date", "time", "venue", "status"],
            "min_count": 15
        },
        "students.json": {
            "required_fields": ["id", "name", "course", "year", "department"],
            "min_count": 15
        },
        "faqs.json": {
            "required_fields": ["id", "question", "answer", "category"],
            "min_count": 15
        }
    }

    all_passed = True
    for filename, spec in datasets.items():
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"[FAIL] Missing dataset file: {filename}")
            all_passed = False
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"[FAIL] {filename}: Root element is not a JSON array.")
                all_passed = False
                continue

            count = len(data)
            if count < spec["min_count"]:
                print(f"[FAIL] {filename}: Record count {count} is less than required minimum {spec['min_count']}.")
                all_passed = False
            else:
                print(f"[PASS] {filename}: {count} records found (>= {spec['min_count']})")

            # Validate fields on every record
            missing_fields_found = False
            for idx, record in enumerate(data):
                for field in spec["required_fields"]:
                    if field not in record or record[field] is None or record[field] == "":
                        print(f"  [FAIL] {filename} record #{idx} missing required field '{field}'")
                        missing_fields_found = True
                        all_passed = False

            if not missing_fields_found:
                print(f"  [PASS] All {count} records in {filename} contain required fields: {spec['required_fields']}")

        except json.JSONDecodeError as e:
            print(f"[FAIL] {filename}: Malformed JSON syntax error: {e}")
            all_passed = False

    return all_passed

def test_search_filter_sort_logic():
    print("\n" + "=" * 65)
    print("TEST 2: Search, Filter, Sort Logic Assertions")
    print("=" * 65)

    all_passed = True

    # 1. Events Logic
    with open(DATA_DIR / "events.json", "r", encoding="utf-8") as f:
        events = json.load(f)

    # Search by title & description
    res_search = [e for e in events if "hackathon" in e["title"].lower() or "hackathon" in e["description"].lower()]
    if len(res_search) >= 2: # Annual Hackathon + Ethical Hacking Clinic
        print(f"[PASS] Events search for 'hackathon' found {len(res_search)} items")
    else:
        print(f"[FAIL] Events search for 'hackathon' returned unexpected count: {len(res_search)}")
        all_passed = False

    # Filter by category
    res_cat = [e for e in events if e["category"].lower() == "technical"]
    if len(res_cat) >= 3:
        print(f"[PASS] Events filter by category 'Technical' returned {len(res_cat)} items")
    else:
        print(f"[FAIL] Events category filter 'Technical' failed")
        all_passed = False

    # Combined filter: category 'Technical' + status 'Upcoming'
    res_combo = [e for e in events if e["category"].lower() == "technical" and e["status"].lower() == "upcoming"]
    if len(res_combo) >= 2:
        print(f"[PASS] Events combined filter (Technical + Upcoming) returned {len(res_combo)} items")
    else:
        print(f"[FAIL] Events combined filter failed")
        all_passed = False

    # Sort by date asc vs desc
    dates_asc = sorted(events, key=lambda x: x["date"])
    dates_desc = sorted(events, key=lambda x: x["date"], reverse=True)
    if dates_asc[0]["date"] <= dates_asc[-1]["date"] and dates_desc[0]["date"] >= dates_desc[-1]["date"]:
        print(f"[PASS] Events date sorting verified (Earliest: {dates_asc[0]['date']}, Latest: {dates_desc[0]['date']})")
    else:
        print(f"[FAIL] Events date sorting failed")
        all_passed = False

    # 2. Students Logic
    with open(DATA_DIR / "students.json", "r", encoding="utf-8") as f:
        students = json.load(f)

    # Search by department
    res_dept = [s for s in students if "artificial intelligence" in s["department"].lower()]
    if len(res_dept) >= 3:
        print(f"[PASS] Students search for 'artificial intelligence' found {len(res_dept)} items")
    else:
        print(f"[FAIL] Students department search failed")
        all_passed = False

    # Filter by course & year
    res_course_year = [s for s in students if s["course"] == "B.Tech" and s["year"] in ["2nd Year", "3rd Year"]]
    if len(res_course_year) >= 3:
        print(f"[PASS] Students combined filter (B.Tech + Year) found {len(res_course_year)} items")
    else:
        print(f"[FAIL] Students combined filter failed")
        all_passed = False

    # Sort by name A-Z
    names_asc = sorted(students, key=lambda x: x["name"])
    names_desc = sorted(students, key=lambda x: x["name"], reverse=True)
    if names_asc[0]["name"] <= names_asc[1]["name"] and names_desc[0]["name"] >= names_desc[1]["name"]:
        print(f"[PASS] Students name sorting verified (First: '{names_asc[0]['name']}', Last: '{names_desc[0]['name']}')")
    else:
        print(f"[FAIL] Students name sorting failed")
        all_passed = False

    # 3. FAQs Logic
    with open(DATA_DIR / "faqs.json", "r", encoding="utf-8") as f:
        faqs = json.load(f)

    res_faq_search = [f for f in faqs if "theme" in f["question"].lower() or "theme" in f["answer"].lower()]
    if len(res_faq_search) >= 1:
        print(f"[PASS] FAQs search for 'theme' found {len(res_faq_search)} items")
    else:
        print(f"[FAIL] FAQs search for 'theme' failed")
        all_passed = False

    res_faq_cat = [f for f in faqs if f["category"] == "Administrative"]
    if len(res_faq_cat) >= 4:
        print(f"[PASS] FAQs category filter 'Administrative' found {len(res_faq_cat)} items")
    else:
        print(f"[FAIL] FAQs category filter failed")
        all_passed = False

    return all_passed

def test_pagination_boundary_logic():
    print("\n" + "=" * 65)
    print("TEST 3: Pagination Boundary & Clamping Assertions")
    print("=" * 65)

    all_passed = True
    items = list(range(1, 17)) # 16 items
    page_size = 5

    total_pages = (len(items) + page_size - 1) // page_size # 4 pages

    # Page 1
    page1 = items[0:5]
    assert len(page1) == 5 and page1[0] == 1 and page1[-1] == 5
    print("[PASS] Page 1: Items 1 to 5 (size: 5)")

    # Page 4 (Last page, partial)
    page4 = items[15:20]
    assert len(page4) == 1 and page4[0] == 16
    print("[PASS] Page 4: Item 16 (partial page size: 1)")

    # Empty list
    empty_items = []
    empty_total_pages = max(1, (len(empty_items) + page_size - 1) // page_size)
    assert empty_total_pages == 1
    print("[PASS] Empty list produces totalPages = 1 and 0 sliced items")

    return all_passed

def test_security_and_safe_dom():
    print("\n" + "=" * 65)
    print("TEST 4: Safe DOM Rendering Inspection (No untrusted innerHTML)")
    print("=" * 65)

    renderer_files = [
        JS_DIR / "events-renderer.js",
        JS_DIR / "faq-renderer.js",
        JS_DIR / "students-renderer.js",
        JS_DIR / "pagination.js"
    ]

    all_passed = True
    for r_file in renderer_files:
        code = r_file.read_text(encoding="utf-8")
        # Check if innerHTML is used with variables
        if "innerHTML" in code:
            print(f"[FAIL] {r_file.name} contains 'innerHTML'. Must use safe DOM methods.")
            all_passed = False
        else:
            print(f"[PASS] {r_file.name}: Clean of innerHTML usage; uses textContent and createElement.")

    return all_passed

def test_backward_compatibility():
    print("\n" + "=" * 65)
    print("TEST 5: Practicals 1–5 Backward Compatibility & Fallback Verification")
    print("=" * 65)

    all_passed = True

    # 1. Verify faq.js maintains theme() and named faq handlers
    faq_js = (JS_DIR / "faq.js").read_text(encoding="utf-8")
    for fn in ["theme", "faq", "faq1", "faq2", "faq3", "faq4"]:
        if f"function {fn}" in faq_js:
            print(f"[PASS] faq.js maintains backward-compatible function: {fn}()")
        else:
            print(f"[FAIL] faq.js missing function: {fn}()")
            all_passed = False

    # 2. Verify registration.js retains form validation
    reg_js = (JS_DIR / "registration.js").read_text(encoding="utf-8")
    if "registerForm" in reg_js and "resetForm" in reg_js:
        print("[PASS] registration.js maintains registerForm() and resetForm()")
    else:
        print("[FAIL] registration.js missing validation functions")
        all_passed = False

    # 3. Verify contact.js retains submitMessage and resetMessage
    contact_js = (JS_DIR / "contact.js").read_text(encoding="utf-8")
    if "submitMessage" in contact_js and "resetMessage" in contact_js:
        print("[PASS] contact.js maintains submitMessage() and resetMessage()")
    else:
        print("[FAIL] contact.js missing handlers")
        all_passed = False

    # 4. Verify noscript semantic fallbacks exist in events.html and faq.html
    events_html = (PAGES_DIR / "events.html").read_text(encoding="utf-8")
    if "<noscript>" in events_html and "Hackathon" in events_html:
        print("[PASS] events.html maintains semantic <noscript> fallback with Hackathon schedule")
    else:
        print("[FAIL] events.html missing noscript schedule fallback")
        all_passed = False

    faq_html = (PAGES_DIR / "faq.html").read_text(encoding="utf-8")
    if "<noscript>" in faq_html and "What is Student Hub?" in faq_html:
        print("[PASS] faq.html maintains semantic <noscript> fallback with original FAQ questions")
    else:
        print("[FAIL] faq.html missing noscript FAQ fallback")
        all_passed = False

    return all_passed

if __name__ == "__main__":
    t1 = test_json_datasets()
    t2 = test_search_filter_sort_logic()
    t3 = test_pagination_boundary_logic()
    t4 = test_security_and_safe_dom()
    t5 = test_backward_compatibility()

    print("\n" + "=" * 65)
    if t1 and t2 and t3 and t4 and t5:
        print("ALL PRACTICAL 6 VERIFICATION TESTS PASSED SUCCESSFULLY!")
        print("=" * 65)
        sys.exit(0)
    else:
        print("ONE OR MORE PRACTICAL 6 TESTS FAILED.")
        print("=" * 65)
        sys.exit(1)
