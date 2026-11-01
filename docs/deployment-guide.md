# StudentHub — Production Deployment & Architecture Guide

**Project:** StudentHub College Management & Student Information Portal  
**Institution:** Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT  
**Course:** AIUE203 — Web Development Fundamentals  
**Student Author:** Daksh Harkhani (25AIML019, FYAIML)  
**Intended Git Identity:** `25aiml019-hub <dakshharkhani18@gmail.com>`  

---

## 1. System Architecture Overview

StudentHub is structured as a two-tier enterprise web application:

1. **Public Web Experience (Logged-out visitors):**
   - **Aesthetic:** Inspired by premier university designs (Adelaide University layout with grand hero banner, deep blue/gold palette, clean typography, fast-access highlights, and full-width content grids).
   - **Navigation & Pages:**
     - Home (`public/index.html` and `public/index.php`)
     - Campus Life (`public/pages/campuslife.html`)
     - 4 Dedicated Student Club detail pages (`public/pages/clubs/sports.html`, `music.html`, `coding.html`, `photography.html`)
     - Public Events Directory & Modal / Standalone Detail View (`public/pages/events.html`, `public/pages/event-detail.html`)
     - About Us (`public/pages/about.html`)
     - Contact Us (`public/pages/contact.html`)
     - Student Registration (`public/pages/registration.html` & `public/pages/registration.php`)
     - Sign In (`public/pages/login.html` & `public/pages/login.php`)
   - **Access Control:** Course Enrollment is **strictly hidden** from visitor navigation and protected server-side and client-side.

2. **Authenticated Student Portal (`student/index.php`):**
   - **Tab 1: Profile & Counselor Tab** — Verified student credentials, Student ID (`25AIML019`), Temp Student ID (`25TAIMLGGE`), Batch (`Batch A`), and assigned Faculty Counselor card (`Prof. Gaurav Kumar`, Cabin 204).
   - **Tab 2: Academic & SGPA Summary Tab** — Verified Semester 1 SGPA (`8.05`, 19 credits), Semester 2 SGPA (`8.77`, 22 credits), and mathematically weighted CGPA (`8.44`, 41 credits). Missing indicator for pending records (e.g. `25AIML011`).
   - **Tab 3: Semester 3 Timetable Tab** — Live Today's Schedule card, Next Upcoming Class alert, and full Monday-Saturday weekly schedule for Division I (Academic Year 2026-27, Odd Term).
   - **Tab 4: FYAIML Class Directory Tab** — Complete 78-student class roster with batch filtering (All: 78, Batch A: 20, Batch B: 20, Batch C: 20, Batch D: 18) and search. *Strict student privacy defense: zero phone numbers or personal emails exposed.*
   - **Tab 5: Marksheet Upload & CGPA OCR Tracker Tab** — File upload form (PDF, PNG, JPG, WEBP), server-side regex extraction of CGPA/SGPA, interactive grade confirmation modal, and archive of previous uploads.
   - **Tab 6: Registered Campus Events Tab** — Live event registrations queried from MySQL `registrations` table.

3. **Administrative Portal (`admin/index.php`, `admin/students.php`, `admin/events.php`):**
   - RBAC protected via `checkRole('admin')`.
   - Practical 11: Full Student CRUD with formula injection defense and CSV export.
   - Practical 12: Full Event CRUD with multipart poster upload verification (MIME, size, extension, image headers).
   - Audit Logging: Tracks administrative operations in `audit_logs` table.

---

## 2. Port & Database Isolation (Critical Scope Boundary)

> [!IMPORTANT]
> **Strict Port Isolation:**
> - **Antigravity MySQL Instance:** Runs exclusively on **Port 3307** (`127.0.0.1:3307`, Database: `studenthub`, User: `root`, Password: none).
> - **Codex MariaDB / XAMPP Instance:** Runs on Port 3308. It is **completely untouched** by this project.

### Database Connection Configuration
Configured in `app/config/config.php` and `app/config/db.php`:
```php
DB_HOST = '127.0.0.1'
DB_PORT = 3307
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'studenthub'
```

---

## 3. Database Schema Enhancements

### New Columns in `users`
- `must_change_password` (TINYINT(1) DEFAULT 0): Indicates user must set personal password on first login.
- `failed_login_attempts` (INT DEFAULT 0): Tracks consecutive bad passwords for brute-force rate limiting.
- `lockout_until` (DATETIME NULL): Account lockout timestamp after 5 consecutive bad login attempts.

### New Tables Created
1. `semester_results`:
   - `id INT AUTO_INCREMENT PRIMARY KEY`
   - `student_id INT NOT NULL` (Foreign key to `students.id`)
   - `roll_no VARCHAR(50) NOT NULL`
   - `semester INT NOT NULL` (1 or 2)
   - `sgpa DECIMAL(4,2) NULL`
   - `credits DECIMAL(4,2) NOT NULL DEFAULT 0.00`
   - `is_missing TINYINT(1) NOT NULL DEFAULT 0`
   - `remarks VARCHAR(255) NULL`
   - `UNIQUE KEY unique_student_semester (student_id, semester)`

2. `unassigned_academic_records`:
   - `id INT AUTO_INCREMENT PRIMARY KEY`
   - `roll_no VARCHAR(50) NOT NULL`
   - `semester INT NOT NULL`
   - `sgpa DECIMAL(4,2) NULL`
   - `credits DECIMAL(4,2) NOT NULL DEFAULT 0.00`
   - `quarantine_reason VARCHAR(255) NOT NULL`
   - `imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

3. `timetable_slots`:
   - `id INT AUTO_INCREMENT PRIMARY KEY`
   - `academic_year VARCHAR(20) NOT NULL` (`2026-2027`)
   - `semester INT NOT NULL` (`3`)
   - `term VARCHAR(20) NOT NULL` (`Odd Term`)
   - `division VARCHAR(20) NOT NULL` (`Div I`)
   - `effective_date DATE NOT NULL` (`2026-07-06`)
   - `day_of_week VARCHAR(15) NOT NULL`
   - `slot_number INT NOT NULL`
   - `start_time TIME NOT NULL`
   - `end_time TIME NOT NULL`
   - `slot_type VARCHAR(50) NOT NULL`
   - `batch VARCHAR(20) NOT NULL` (`ALL`, `A1`, `B1`, `C1`, `D1`, `E1`)
   - `subject_code VARCHAR(20) NOT NULL`
   - `subject_name VARCHAR(100) NOT NULL`
   - `subject_abbrev VARCHAR(20) NOT NULL`
   - `room_no VARCHAR(50) NOT NULL`
   - `faculty_abbrev VARCHAR(20) NOT NULL`
   - `faculty_name VARCHAR(100) NOT NULL`

---

## 4. Root-Cause Analysis: Login/CSRF Failure & Fix

### Root Cause
1. **Empty Token Submission / Fetch Race Condition:**  
   In `public/pages/login.html`, `#csrf_token` input was statically initialized to `""`. Client JavaScript in `main.js` fetched `../csrf-token.php` asynchronously. If a user entered credentials and submitted the form before the fetch resolved (or if the AJAX fetch encountered a network stall), an empty `csrf_token` was transmitted.  
   In `process-login.php`:
   ```php
   if (!empty($csrfToken) || !empty($_SESSION['csrf_token'])) {
       if (!validateCsrfToken($csrfToken)) {
           sendLoginResponse(403, false, 'CSRF verification failed. Login request rejected.');
       }
   }
   ```
   If a session already existed on the server with a CSRF token, an empty submitted token triggered `CSRF verification failed. Login request rejected.`

2. **Inconsistent Login State / Broken Logout:**  
   `main.js` and `student/index.php` pointed logout links to `../public/process-logout.php`. Because the PHP built-in server runs with docroot `-t public`, navigating to `http://localhost:8000/public/process-logout.php` 404'd (falling back to `index.php`). The session was **never destroyed**. When navigating to `login.html`, the prior student session remained active in header status while attempting an admin login!

### Remedy Implemented
- In `login.html` & `login.php`: Pre-fetch CSRF token on `DOMContentLoaded` and immediately before form dispatch in `validateForm(event)`:
  ```javascript
  const csrfInput = document.getElementById("csrf_token");
  if (csrfInput && !csrfInput.value) {
      const tokenRes = await fetch("../csrf-token.php");
      const tokenData = await tokenRes.json();
      if (tokenData && tokenData.csrf_token) csrfInput.value = tokenData.csrf_token;
  }
  ```
- Added **Demo Login Instructions** card on both `login.html` and `login.php`.
- Corrected `logoutUrl` in `main.js`, `nav.php`, and `student/index.php` to `../process-logout.php`.
- Hardened `process-logout.php`: Destroys session variables, clears cookies, calls `session_destroy()`, and initializes a fresh unauthenticated session with a new CSRF token.
- Implemented brute-force lockout: 5 consecutive failed attempts lock the account for 15 minutes (`lockout_until`).

---

## 5. Root-Cause Analysis: Student Portal Missing CSS / Raw HTML

### Root Cause
- In `student/index.php` and `admin/*.php`, `$basePath` was set to `'../public/'`.
- In `header.php`, stylesheets are linked via `<link rel="stylesheet" href="<?= $basePath ?>assets/css/main.css">`.
- In browser at `http://localhost:8000/student/index.php`, this resolved to `http://localhost:8000/public/assets/css/main.css`.
- Because the server document root is `public/`, `/public/...` did not exist as a physical file. The server returned the root `index.php` fallback HTML with `Content-Type: text/html`.
- Modern browsers strictly refuse to apply stylesheets with `text/html` MIME types:
  `Refused to apply style from 'http://localhost:8000/public/assets/css/main.css' because its MIME type ('text/html') is not a supported stylesheet MIME type.`
- The entire page fell back to raw, unstyled HTML.

### Remedy Implemented
- Changed `$basePath = '../'` in `student/index.php`, `admin/index.php`, `admin/students.php`, and `admin/events.php`.
- In browser, `../assets/css/main.css` resolves to `http://localhost:8000/assets/css/main.css`, returning HTTP 200 with `Content-Type: text/css`.
- Full Adelaide aesthetic renders instantly across public, student, and admin views.

---

## 6. Account Provisioning Summary (78 Students)

- **Total Roster Accounts:** 78 Students (`25AIML001` through `25AIML078`).
- **Username Convention:** Official College ID (e.g. `25AIML001`, `25AIML019`, ..., `25AIML078`).
- **Initial Password:** Same as Username (e.g. `25AIML001`, `25AIML019`).
- **Bcrypt Hashing:** Passwords securely hashed with bcrypt cost factor 10.
- **First Login Password Change:** `must_change_password = 1` enforced for all 77 newly provisioned students.
- **Daksh Harkhani Account:** Preserves dual login compatibility (Username `anshika` / Password `student123` for automated test suites, or College ID `25AIML019` / Password `25AIML019` for demo verification).
- **Password Change Workflow:** `pages/change-password.php` and `process-change-password.php` allow students to set new secure passwords (minimum 6 characters) and clear `must_change_password`.

---

## 7. Academic Data Reconciliation & Weighted CGPA

### Inputs
- **Semester 1 CSV:** 19.00 Credits.
  - 77 valid records mapped to official roster.
  - Student `25AIML011` is **flagged as missing** (`is_missing = 1`, Remarks: `'Official Semester 1 result record pending'`).
  - 1 extra record (`25AIML079`) quarantined in `unassigned_academic_records`.
- **Semester 2 CSV:** 22.00 Credits.
  - 78 valid records mapped to official roster.
  - 12 extra records (`25AIML079` - `25AIML090`) quarantined in `unassigned_academic_records` (`Outside official 78-student FYAIML roster`).
- **Total Quarantined Records:** 13 records in `unassigned_academic_records`.

### Weighted CGPA Formula
$$\text{CGPA} = \frac{\sum (\text{SGPA} \times \text{Credits})}{\sum \text{Credits}} = \frac{19 \times \text{SGPA}_1 + 22 \times \text{SGPA}_2}{41}$$

### Verification for Daksh Harkhani (25AIML019)
- **Semester 1 SGPA:** `8.05` (19.00 Credits) &rarr; $19 \times 8.05 = 152.95$ grade points.
- **Semester 2 SGPA:** `8.77` (22.00 Credits) &rarr; $22 \times 8.77 = 192.94$ grade points.
- **Weighted CGPA:**
  $$\frac{152.95 + 192.94}{41.00} = \frac{345.89}{41.00} = 8.4363... \approx \mathbf{8.44}$$
- Updated in `students.cgpa = 8.44`.

---

## 8. Official Semester 3 Timetable Integration

Extracted directly from the official CSPIT CHARUSAT AIML Odd Term 2026-27 Division I Timetable:
- **Term:** Odd Term 2026–27 &bull; **Division:** Div I &bull; **Classroom:** Room 218 &bull; **Effective Date:** 06/07/2026.
- **Daily Slots:**
  - 09:10 - 10:10: Slot 1 (Lecture)
  - 10:10 - 11:10: Slot 2 (Lecture)
  - 11:10 - 12:10: Slot 3 (Lecture)
  - 12:10 - 13:10: Lunch Break
  - 13:10 - 15:10: Slot 4 & 5 (Lab / Practical)
  - 15:15 - 17:15: Slot 6 & 7 (Counseling / Mentorship / Extracurriculars)
- **Batch Allocations:**
  - **Batch A1:** Students 25AIML001 to 25AIML020 (Counselor: Prof. Gaurav Kumar, Cabin 204).
  - **Batch B1:** Students 25AIML021 to 25AIML040 (Counselor: Prof. Niyati Patel, Cabin 205).
  - **Batch C1:** Students 25AIML041 to 25AIML060 (Counselor: Prof. Bhargav Sobhana, Cabin 206).
  - **Batch D1:** Students 25AIML061 to 25AIML078 (Counselor: Prof. Gaurang Patel, Cabin 207).
- **Service Layer (`TimetableService`):**
  - `getTimetableForBatch($batch)`
  - `getTodayClasses($batch)`
  - `getNextUpcomingClass($batch)`
  - `getWeeklySchedule($batch)`

---

## 9. Student Directory Privacy Defense

- **Protected Columns:** Contact mobile numbers, personal email addresses, and passwords are **strictly excluded** from the directory table.
- **Public Visible Columns:** `#`, `College ID`, `Student Name`, `Batch`, `Counselor`.
- **Batch Cohort Summary:**
  - **All Batches:** 78 Students
  - **Batch A:** 20 Students (`25AIML001` - `25AIML020`)
  - **Batch B:** 20 Students (`25AIML021` - `25AIML040`)
  - **Batch C:** 20 Students (`25AIML041` - `25AIML060`)
  - **Batch D:** 18 Students (`25AIML061` - `25AIML078`)

---

## 10. Credentials & Demonstration Guide

| Portal | Username | Password | Notes |
|---|---|---|---|
| **Admin Portal** | `admin` | `admin123` | Administrative CRUD & audit logs |
| **Student (Anshika)** | `25AIML019` | `25AIML019` | Daksh Harkhani student portal (CGPA 8.44) |
| **Student (Anshika Legacy)**| `anshika` | `student123` | Preserves existing automated test suites |
| **Student (Any Roster)** | `25AIML001` | `25AIML001` | Prompts for mandatory initial password change |

---

## 11. How to Test and Verify

### Automated Test Suite Execution
Run all 8 comprehensive test suites (Practicals 1–12 + Phase Remedy):
```powershell
python tests/run_all_tests.py
```

Run Phase Remedy suite directly:
```powershell
python tests/verify_phase_remedy.py
```

### Manual Browser Verification URLs
1. **Home Page:** `http://localhost:8000/index.html`
2. **Login Page:** `http://localhost:8000/pages/login.html` (view Demo Instructions card)
3. **Student Portal:** `http://localhost:8000/student/index.php` (login with `25AIML019` / `25AIML019`)
4. **Admin Portal:** `http://localhost:8000/admin/index.php` (login with `admin` / `admin123`)
5. **Change Password:** `http://localhost:8000/pages/change-password.php`
