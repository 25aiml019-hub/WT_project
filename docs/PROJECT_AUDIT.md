# Project Audit: StudentHub (Wt_Project)

**Course:** AIUE203 - Web Development Fundamentals (WDF)  
**Student Name:** Daksh Harkhani  
**Student ID:** 25AIML019  
**Institute:** CSPIT, CHARUSAT  
**Audit Date:** October 2026  
**Auditor:** Antigravity Engineering Assistant  

---

## 1. Executive Summary

This audit document evaluates the initial state of the **StudentHub** repository prior to Phase 1 restructuring. The initial project consisted of a single folder named `Wt_Project` containing 25 loose files (HTML, CSS, JS, and README) placed in a flat directory without architectural tiers or separation of concerns.

While the fundamental requirements of Practicals 1 through 5 (semantic HTML, basic styling, responsive layout, JavaScript DOM manipulation, and registration validation) were present, the project suffered from significant structural defects, broken references, casing inconsistencies, dead code, and zero separation between public web assets and future backend/database modules.

---

## 2. Inventory of Existing Files (Initial State)

| # | File Name | Size | Type | Practical Mapping | Observations / Issues |
|---|-----------|------|------|-------------------|-----------------------|
| 1 | `index.html` | 2,382 B | HTML | Practical 2, 3 | Main landing page. Contains navigation and hero grid. Footer is present. |
| 2 | `home.css` | 3,424 B | CSS | Practical 3 | Styles for home. Contains 61 lines of commented-out legacy CSS at the top. |
| 3 | `ADMINISTRATIVE.html` | 1,017 B | HTML | Practical 2 | All-caps filename. No navigation bar or footer; user gets stranded. |
| 4 | `admin.css` | 1,997 B | CSS | Practical 3 | Table and list styling for administrative services. |
| 5 | `campuslife.html` | 775 B | HTML | Practical 2, 3 | Incomplete navigation bar with typo `ADMINSTRATIVE.html` and mixed-case `CAMPUSLIFE.html`. Embedded `<style>` tag. |
| 6 | `campuslife.css` | 2,482 B | CSS | Practical 3 | Clubs listing styling with hover effects. |
| 7 | `COURSEENROLLMENT.html` | 757 B | HTML | Practical 2 | All-caps filename. Line 5 has unclosed `<link>` tag. Navigation is commented out. Embedded `<style>` tag. |
| 8 | `COURSEENROLLMENT.css` | 1,558 B | CSS | Practical 3 | All-caps filename. Course table styles. |
| 9 | `dashboard.html` | 442 B | HTML | Practical 2 | No navigation bar. Uses outdated styling. |
| 10 | `dashboard.css` | 359 B | CSS | Practical 3 | Primitive styles (`aliceblue`, `darkblue`), inconsistent with the StudentHub brand. |
| 11 | `events.html` | 451 B | HTML | Practical 2 | Table of events. No navigation bar. Outdated styling. |
| 12 | `events.css` | 441 B | CSS | Practical 3 | Primitive styles (`aliceblue`, black borders), inconsistent with primary theme. |
| 13 | `login.html` | 972 B | HTML | Practical 2, 5 | Inline JS dummy validation (`admin`/`123`). Stray `</a>` on line 24. No navigation bar. |
| 14 | `login.css` | 592 B | CSS | Practical 3 | Form styling inconsistent with primary theme (`border: 2px solid rgb(7, 6, 74)`). |
| 15 | `about.html` | 2,859 B | HTML | Practical 2, 3 | Lines 1–28 contain obsolete commented-out HTML. No navigation bar or footer. |
| 16 | `about.css` | 2,537 B | CSS | Practical 3 | Container, card, and social link styling. |
| 17 | `contact.html` | 4,501 B | HTML | Practical 2, 3 | Lines 1–33 contain obsolete commented-out HTML. References `contact.js` which did NOT exist. |
| 18 | `contact.css` | 4,293 B | CSS | Practical 3 | Form, contact info cards, and layout styling. |
| 19 | `faq.html` | 4,848 B | HTML | Practical 2, 4 | Lines 1–74 contain obsolete commented-out HTML. Theme button and accordion buttons. No standard navigation. |
| 20 | `faq.css` | 2,971 B | CSS | Practical 3, 4 | Accordion styling and dark-theme styles. |
| 21 | `faq.js` | 1,117 B | JS | Practical 4 | Functions `theme()`, `faq()`, `faq1()`, `faq2()`, `faq3()`, `faq4()`. |
| 22 | `registration.html` | 4,157 B | HTML | Practical 2, 5 | Lines 1–71 contain obsolete commented-out HTML. No navigation bar. |
| 23 | `reg.css` | 2,390 B | CSS | Practical 3, 5 | Form layout and inputs styling. Filename abbreviation (`reg.css` vs `registration.html`). |
| 24 | `registration.js` | 1,524 B | JS | Practical 5 | Form validation logic: name, email, 10-digit mobile, course, department, gender, hobbies, address. |
| 25 | `README.md` | 699 B | Markdown | Documentation | Initial minimal documentation. |

---

## 3. Detailed Audit Findings & Defects

### 3.1 Critical Functional Defects
1. **Missing `contact.js` Script**:
   - `contact.html` line 168 loads `<script src="contact.js"></script>` and attaches `onsubmit="return submitMessage()"` (line 97) and `onclick="resetMessage()"` (line 140).
   - `contact.js` was completely missing from the directory.
   - **Impact:** Submitting or resetting the contact form triggers an uncaught `ReferenceError: submitMessage is not defined`, breaking form functionality.

2. **Broken and Inconsistent Navigation Links**:
   - `campuslife.html` line 14 has a typo: `<a href="ADMINSTRATIVE.html">` (missing the second 'I'). On case-sensitive web servers (Linux/Apache), this results in a 404 Not Found error.
   - `index.html` references uppercase `ADMINISTRATIVE.html`, `CAMPUSLIFE.html`, and `COURSEENROLLMENT.html`.
   - 9 out of 10 pages lacked a top navigation bar. Users clicking into Course Enrollment, Dashboard, Events, Login, About, Registration, or Administrative were trapped on those pages with no menu to return to Home or jump to other sections.

### 3.2 HTML Syntax Errors
1. **Unclosed `<link>` tag in `COURSEENROLLMENT.html`**:
   - Line 5: `<link rel="stylesheet" href="COURSEENROLLMENT.css"` lacked the closing `>` character.
2. **Orphaned `</a>` tag in `login.html`**:
   - Line 24 contains a floating `</a>` tag with no opening anchor element.

### 3.3 Dead Code & Hygiene Issues
1. **Commented-Out Legacy Blocks**:
   - `about.html` (lines 1–28): 28 lines of old unstyled HTML.
   - `contact.html` (lines 1–33): 33 lines of an old HTML table.
   - `faq.html` (lines 1–74): 74 lines of old inline-scripted prototype.
   - `registration.html` (lines 1–71): 71 lines of original prototype form.
   - `home.css` (lines 1–61): 61 lines of discarded initial CSS.
   - `COURSEENROLLMENT.html` (lines 12–15): commented out navigation markup.
   - Inlined `<style>` blocks in `campuslife.html` and `COURSEENROLLMENT.html` conflicting with linked CSS files.

### 3.4 CSS Duplication & Design Drift
- Colors and typography are duplicated across all 11 CSS stylesheets:
  - Primary blue: `#1E3A8A`
  - Accent blue: `#2563EB`
  - Body background: `#F4F7FC`
  - Text color: `#333333`
  - Font family: `Arial, Helvetica, sans-serif`
- However, three older pages (`dashboard.css`, `events.css`, `login.css`) did not adopt this design system, using `background-color: aliceblue`, raw black borders, and dark blue headers without responsive styling or card shadows.
- No central CSS variables or shared design token stylesheet existed.

### 3.5 Security & Production Readiness
- **No Directory Separation:** HTML files, stylesheets, scripts, and documentation all shared the root folder. Future PHP backend code and uploaded files would mix dangerously with web-accessible static assets.
- **No `.gitignore`:** Development artifacts, OS files, and environment files could accidentally be committed.
- **No `.env.example`:** No structured mechanism for storing database credentials or application environment settings.
- **No Upload Protection:** No upload storage folder or `.htaccess` security rules preventing script execution in writable directories.

---

## 4. Phase 1 Remediation & Restructuring Strategy

1. **Adopt Standard Tiered Web Architecture:**
   - Place all public entry points and static assets into `public/`.
   - Organize stylesheets into `public/assets/css/` with a shared `main.css` containing design tokens and components.
   - Organize scripts into `public/assets/js/` and create the missing `contact.js`.
   - Place subpages cleanly into `public/pages/` using consistent lowercase filenames (`administrative.html`, `course-enrollment.html`, `campuslife.html`, etc.).
2. **Universal Navigation & Branding:**
   - Equip all pages with the complete StudentHub navigation bar and unified footer crediting **Daksh Harkhani (25AIML019, CSPIT CHARUSAT)**.
   - Standardize all relative paths across pages and assets.
3. **Backend & Modular Architecture Preparation:**
   - Create `app/config/db.php` with secure PDO connection management and `.env` loader.
   - Create `app/includes/` with reusable PHP components (`header.php`, `nav.php`, `footer.php`, `auth_check.php`).
   - Create `app/middleware/` and `app/services/` for subsequent practicals.
   - Create `api/` resource routing folders (`auth/`, `students/`, `events/`).
   - Create `database/schema.sql` and `database/seed.sql` supporting the required schemas.
   - Create `storage/uploads/` protected by `.htaccess` and `.gitignore`.
4. **Verification:**
   - Create test suites verifying navigation, asset resolution, and registration form validation.
