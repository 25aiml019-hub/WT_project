# StudentHub — Phase 1 Test & Verification Report

**Course:** AIUE203 - Web Development Fundamentals (WDF)  
**Student Name:** Daksh Harkhani  
**Student ID:** 25AIML019  
**Institute:** CSPIT, CHARUSAT  
**Test Date:** October 2026  
**Test Execution Engine:** Python 3.14 & In-Browser JavaScript Suite  

---

## 1. Test Summary

| Test Category | Items Checked | Passed | Failed | Status |
|---|---|---|---|---|
| **HTML Page Syntax & Accessibility** | 11 pages (1 root + 10 subpages) | 11 | 0 | **PASSED** |
| **Local Stylesheet Linking** | 22 stylesheet inclusions | 22 | 0 | **PASSED** |
| **Local JavaScript Linking** | 16 script inclusions | 16 | 0 | **PASSED** |
| **Navigation & Anchor Links** | 120 relative navigation links | 120 | 0 | **PASSED** |
| **Architecture Tiers & Files** | 38 mandatory structure targets | 38 | 0 | **PASSED** |
| **Practical 5 Mobile Regex Validation** | 8 test cases (valid + invalid) | 8 | 0 | **PASSED** |
| **Practical 5 Email Regex Validation** | 7 test cases (valid + invalid) | 7 | 0 | **PASSED** |
| **Client-Side Functions Availability** | 6 functions | 6 | 0 | **PASSED** |
| **Total Test Assertions** | **228 assertions** | **228** | **0** | **100% PASS** |

---

## 2. Page-by-Page Verification Results

### 2.1 `public/index.html` (Home Portal)
- **Status:** Verified (PASS)
- **Assets Loaded:** `assets/css/main.css`, `assets/css/home.css`, `assets/js/main.js`
- **Branding:** Logo SVG fallback present (`assets/images/logo.svg`), 4 campus hero cards intact with hover zoom animations.
- **Navigation:** Universal navigation links active to all 10 subpages.

### 2.2 `public/pages/administrative.html` (Administrative Services)
- **Status:** Verified (PASS)
- **Original Filename:** `ADMINISTRATIVE.html` (normalized to lowercase)
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/admin.css`, `../assets/js/main.js`
- **Features Verified:** Administrative services list, office timings table (Monday–Friday, Saturday, Sunday), contact details.
- **Navigation:** Return link to `../index.html` and cross-links to all 9 sibling pages verified.

### 2.3 `public/pages/campuslife.html` (Campus Life)
- **Status:** Verified (PASS)
- **Bug Fixed:** Repaired broken link typo `ADMINSTRATIVE.html` (missing 'I'). Removed obsolete embedded `<style>` block.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/campuslife.css`, `../assets/js/main.js`
- **Features Verified:** Clubs directory (Sports, Music, Coding, Photography) with animated hover effects.

### 2.4 `public/pages/course-enrollment.html` (Course Enrollment)
- **Status:** Verified (PASS)
- **Original Filename:** `COURSEENROLLMENT.html` (normalized to lowercase kebab-case)
- **Syntax Error Fixed:** Repaired unclosed `<link>` tag on line 5. Uncommented navigation bar.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/course-enrollment.css`, `../assets/js/main.js`
- **Features Verified:** Available courses table (Java Programming - Jalpesh Vasa, Web Development - Mukti Patel, Python - Prajyot Tugaonkar).

### 2.5 `public/pages/dashboard.html` (Student Dashboard)
- **Status:** Verified (PASS)
- **Visual Upgrade:** Migrated from primitive `aliceblue` styling to branded StudentHub theme.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/dashboard.css`, `../assets/js/main.js`
- **Features Verified:** Student profile details (Name: Daksh Harkhani, Course: B.Tech AIML, Semester: 3, Result: 8.77 SGPA) and Quick Links grid (Attendance, Results, Assignments, Events).

### 2.6 `public/pages/events.html` (Upcoming Events)
- **Status:** Verified (PASS)
- **Visual Upgrade:** Migrated from plain black border table to responsive data-table tokens.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/events.css`, `../assets/js/main.js`
- **Features Verified:** Events schedule table (Hackathon 15 August, Sports Day 22 August, Tech Fest 10 September).

### 2.7 `public/pages/login.html` (Student Login)
- **Status:** Verified (PASS)
- **Syntax Error Fixed:** Removed orphaned `</a>` tag on line 24.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/login.css`, `../assets/js/main.js`
- **Features Verified:** Input fields (`uname`, `pword`), validation logic (`admin` / `123`), Sign Up button redirecting to `registration.html`.

### 2.8 `public/pages/registration.html` (Student Registration)
- **Status:** Verified (PASS)
- **Hygiene Fixed:** Removed 71 lines of dead commented-out prototype code.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/registration.css`, `../assets/js/registration.js`, `../assets/js/main.js`
- **Features Verified:** Name, email, mobile, course, gender radio buttons, department dropdown, hobbies checkboxes, address textarea, submit validation, and form reset.

### 2.9 `public/pages/contact.html` (Contact Us)
- **Status:** Verified (PASS)
- **Critical Defect Fixed:** Created missing `public/assets/js/contact.js` script to resolve `ReferenceError: submitMessage is not defined`. Removed 33 lines of dead table markup.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/contact.css`, `../assets/js/contact.js`, `../assets/js/main.js`
- **Features Verified:** Contact info grid (email, phone, office, timing), message form, reset button, and FAQ callout button.

### 2.10 `public/pages/faq.html` (Frequently Asked Questions)
- **Status:** Verified (PASS)
- **Hygiene Fixed:** Removed 74 lines of obsolete commented prototype code.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/faq.css`, `../assets/js/faq.js`, `../assets/js/main.js`
- **Features Verified:** All 5 question accordion toggles (`faq()`, `faq1()`, `faq2()`, `faq3()`, `faq4()`), theme toggle button (`theme()`), dark-theme styling, and local storage state persistence.

### 2.11 `public/pages/about.html` (About Us)
- **Status:** Verified (PASS)
- **Hygiene Fixed:** Removed 28 lines of dead legacy HTML.
- **Assets Loaded:** `../assets/css/main.css`, `../assets/css/about.css`, `../assets/js/main.js`
- **Features Verified:** Intro, Our Purpose, What Student Hub Provides, Creator card (Daksh Harkhani, LinkedIn, GitHub), Suggestions & Feedback.

---

## 3. Practical 5 Form Validation Test Suite

### 3.1 Mobile Number Validation Test Matrix
Regex: `/^[0-9]{10}$/`
| Input Tested | Expected Outcome | Actual Outcome | Status |
|---|---|---|---|
| `9876543210` | Match (Valid) | Matched | **PASS** |
| `6354069434` | Match (Valid) | Matched | **PASS** |
| `7043100708` | Match (Valid) | Matched | **PASS** |
| `12345` (5 digits) | Reject (Invalid) | Rejected | **PASS** |
| `98765432100` (11 digits) | Reject (Invalid) | Rejected | **PASS** |
| `98765abcde` (letters) | Reject (Invalid) | Rejected | **PASS** |
| `""` (empty) | Reject (Invalid) | Rejected | **PASS** |
| `abcdefghij` (alpha 10) | Reject (Invalid) | Rejected | **PASS** |

### 3.2 Email Address Validation Test Matrix
Regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
| Input Tested | Expected Outcome | Actual Outcome | Status |
|---|---|---|---|
| `dakshharkhani18@gmail.com` | Match (Valid) | Matched | **PASS** |
| `admin@studenthub.com` | Match (Valid) | Matched | **PASS** |
| `student@charusat.edu.in` | Match (Valid) | Matched | **PASS** |
| `plainaddress` | Reject (Invalid) | Rejected | **PASS** |
| `missing@domain` | Reject (Invalid) | Rejected | **PASS** |
| `@missinguser.com` | Reject (Invalid) | Rejected | **PASS** |
| `has space@domain.com` | Reject (Invalid) | Rejected | **PASS** |

---

## 4. Conclusion

All 158 local asset and link references, 15 regex validation test cases, and 11 semantic pages pass verification without errors. The application is completely functional in zero-dependency static mode and fully scaffolded for subsequent PHP and MySQL practicals.
