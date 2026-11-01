# Practical 7 & 8 Test & Implementation Report

**Project:** StudentHub  
**Course:** AIUE203 — Web Development Fundamentals (WDF)  
**Student Name:** Anshika Badala (25AIML002)  
**Institute:** Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT  
**Date:** October 2026  
**Status:** **Completed & Verified (100% Tests Passing)**

---

## 1. Executive Summary

Phase 3 delivers the complete server-side foundation for **Practical 7** (PHP Form Processing and Safe Persistent Storage) and **Practical 8** (MySQL Database Foundation and MySQLi/PDO Connectivity) for the StudentHub portal.

All implementations strictly adhere to web security best practices, AIUE203 syllabus requirements, and maintain complete backward compatibility with Practicals 1–6.

---

## 2. Practical 7 — PHP Form Processing & Safe Persistent File Storage

### 2.1 Form Processing Architecture
- **Registration Processor (`public/process-registration.php`):**
  - **HTTP Method Enforcement:** Rejects non-POST requests with HTTP `405 Method Not Allowed`.
  - **CSRF Token Verification:** Validates session CSRF token with `validateCsrfToken()` using timing-safe `hash_equals()`; invalid tokens yield HTTP `403 Forbidden`.
  - **Server-Side Validation:** Validates required fields, checks full name length, enforces exactly 10-digit mobile numbers (`/^[0-9]{10}$/`), and validates RFC email formats (`/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/`).
  - **Data Sanitization:** Strips HTML/PHP tags, removes null bytes, trims whitespace, and escapes outputs safely with `htmlspecialchars()`.
  - **Safe Password Hashing:** Uses `password_hash($rawPassword, PASSWORD_BCRYPT)` with cost factor 10. Passwords are never stored in plaintext.
  - **Duplicate Prevention:** Inspects existing records in both CSV storage and MySQL database before writing; duplicate emails yield HTTP `409 Conflict`.
  - **Persistent CSV Storage:** Stored in `storage/data/registrations.csv` outside public webroot.
  - **Concurrent Write Safety:** Uses `flock($fp, LOCK_EX)` for exclusive locking during reads/writes. Formats entries safely using `fputcsv()`.
  - **Dual Response Support:** Returns clean JSON for Fetch API/AJAX submissions and handles HTML redirects with session flash messages for standard form submissions.

- **Contact Form Processor (`public/process-contact.php`):**
  - **HTTP Method Enforcement:** Rejects non-POST requests with HTTP `405`.
  - **CSRF Token Verification:** Protects against cross-site request forgery.
  - **Field Validation:** Validates sender name, email, subject (min 3 chars), and message (min 5 chars).
  - **Persistent JSON Storage:** Stored in `storage/data/messages.json` with exclusive file locking (`flock`).
  - **Error Handling:** Gracefully handles filesystem permission errors with HTTP `500` without exposing server paths.

### 2.2 Security & Helper Modules
- **`app/config/security.php`:**
  - `generateCsrfToken()` & `getCsrfToken()`: Cryptographically secure 32-byte pseudo-random tokens stored in `$_SESSION['csrf_token']`.
  - `validateCsrfToken(?string $token)`: Timing-safe token comparison.
  - `sanitizeString()`, `sanitizeEmail()`: Input sanitization helpers.
  - `validateEmail()`, `validateMobile()`: Regular expression validators.
  - `hashPassword()`, `verifyPassword()`: Bcrypt hashing and verification.
  - `e(?string $str)`: Safe HTML entity escaping.
  - `getClientIp()`: Safe client IP extraction.
- **`public/csrf-token.php`:** Dynamic endpoint providing CSRF tokens for static client-side views.
- **Storage Isolation:** `storage/data/.htaccess` denies all public web access (`Require all denied`). `.gitignore` excludes user data while keeping directory structure via `.gitkeep`.

---

## 3. Practical 8 — MySQL Database Foundation & Connectivity

### 3.1 Unified Database Connection Module (`app/config/db.php`)
Supports both **MySQLi** (as required by the AIUE203 syllabus) and **PDO** (PHP Data Objects), configured seamlessly from `.env`:
- **Object-Oriented MySQLi:** `Database::getMySQLi()` returning `mysqli` instance with utf8mb4 charset and ping liveness check.
- **Procedural MySQLi:** `Database::getProcedural()` / `getMySQLiProcedural()` wrapper utilizing `mysqli_connect()`.
- **PDO Singleton:** `Database::getConnection()` / `getDB()` with prepared statement emulation disabled and `ERRMODE_EXCEPTION`.
- **Secure Error Masking:** Catches connection exceptions, logs detailed diagnostic messages privately via `error_log()`, and presents masked generic error messages to clients without leaking database usernames, passwords, or hostnames.

### 3.2 Database Schema (`database/schema.sql`)
All tables use the **InnoDB** storage engine with `utf8mb4` character set and `utf8mb4_unicode_ci` collation:
1. **`users`:** User authentication, role-based access control (`admin`, `student`), bcrypt password storage.
2. **`students`:** Student profile records, foreign key reference to `users.id` with `ON DELETE SET NULL`, `email` unique constraint, indexes on `name` and `department`.
3. **`events`:** Campus event records, dates, categories, locations, poster images, indexes on `event_date` and `status`.
4. **`registrations`:** Event registrations with foreign keys to `events.id` and `students.id` (`ON DELETE CASCADE`), composite unique constraint `unique_student_event(event_id, student_id)`.
5. **`audit_logs`:** Observability and admin action audit logs with client IP and timestamps.
6. **`contact_messages`:** Contact form inquiries with status tracking (`unread`, `read`, `archived`) and timestamps.

### 3.3 Database Seeds (`database/seed.sql`)
- Fully **idempotent** using `INSERT IGNORE INTO` syntax.
- **Seeded Students:** Exactly 20 realistic student records across B.Tech departments (CE, IT, ME, CL) fulfilling Practical 11 prerequisites.
- **Seeded Events:** 5 campus events (Hackathon, Sports Day, Tech Fest, Workshop, Cultural Night).
- **Seeded Users:** Admin and student test accounts with bcrypt hashed passwords.
- **Sample Registrations & Audit Logs:** Pre-populated relational linkages.

### 3.4 Data Access Services (`app/services/`)
- **`StudentService` (`app/services/student_service.php`):**
  - `getAllMySQLi(string $search, string $department): array` using MySQLi prepared statements (`prepare()`, `bind_param()`, `get_result()`).
  - `findByEmail(string $email): ?array` parameterized search for duplicate prevention.
  - `create(array $data): int` parameterized insert returning generated student ID.
  - `count(): int` total student counter.
  - Backward-compatible PDO `getAll()` and `getById()`.
- **`EventService` (`app/services/event_service.php`):**
  - `getAllMySQLi(string $status): array` using MySQLi prepared statements.
  - Backward-compatible PDO `getAll()` and `getById()`.

---

## 4. Automated Test Results

### 4.1 Phase 3 Test Suite (`tests/verify_phase_3.py`)
Executed against active MySQL 8.0.46 instance on port 3307:

```
======================================================================
SECTION 1: Practical 7 - PHP Form Processing & Validation
======================================================================
  [PASS] File Exists: public\process-registration.php
  [PASS] File Exists: public\process-contact.php
  [PASS] File Exists: public\csrf-token.php
  [PASS] File Exists: app\config\security.php
  [PASS] File Exists: app\config\db.php
  [PASS] File Exists: storage\data\.htaccess
  [PASS] File Exists: storage\data\.gitkeep
  [PASS] File Exists: .gitignore
  [PASS] CSRF generateCsrfToken() declared
  [PASS] CSRF validateCsrfToken() declared
  [PASS] Timing-safe hash_equals used in CSRF check
  [PASS] Sanitization function sanitizeString declared
  [PASS] Email validation function validateEmail declared
  [PASS] Mobile validation function validateMobile declared
  [PASS] Password hashing function hashPassword declared
  [PASS] Password verification verifyPassword declared
  [PASS] Validation: 10-Digit Mobile Accepted
  [PASS] Validation: Invalid Mobiles Rejected
  [PASS] Validation: RFC/Format Valid Emails Accepted
  [PASS] Validation: Malformed Emails Rejected
  [PASS] process-registration: Enforces HTTP POST check (rejects GET with 405)
  [PASS] process-registration: Enforces CSRF Token Verification
  [PASS] process-registration: Uses flock(..., LOCK_EX) for CSV concurrency safety
  [PASS] process-registration: Uses fputcsv for safe CSV escaping
  [PASS] process-registration: Hashes password with bcrypt (never plaintext)
  [PASS] process-registration: Checks for duplicate registration
  [PASS] process-registration: Integrates with StudentService MySQL database
  [PASS] process-contact: Enforces HTTP POST check (rejects GET with 405)
  [PASS] process-contact: Enforces CSRF Token Verification
  [PASS] process-contact: Uses flock(..., LOCK_EX) for JSON concurrency safety
  [PASS] process-contact: Validates contact fields (name, email, subject, message)
  [PASS] process-contact: Stores in messages.json outside public root
  [PASS] registration.html: Form uses POST to ../process-registration.php
  [PASS] registration.html: Inputs have name attributes
  [PASS] registration.html: Hidden CSRF token field present
  [PASS] registration.html: Alert feedback container present
  [PASS] contact.html: Form uses POST to ../process-contact.php
  [PASS] contact.html: Inputs have name attributes
  [PASS] contact.html: Hidden CSRF token field present
  [PASS] contact.html: Alert feedback container present
  [PASS] CSV Storage: Row correctly formatted with CSV escaping
  [PASS] CSV Storage: Passwords hashed with bcrypt (never plaintext)
  [PASS] CSV Storage: Duplicate detection via email lookup succeeds
  [PASS] Storage Concurrency: 10 concurrent writes recorded safely without data corruption

======================================================================
SECTION 2: Practical 8 - MySQL Database Foundation & Connectivity
======================================================================
  [PASS] db.php: PDO singleton getConnection() / getDB() implemented
  [PASS] db.php: Object-Oriented MySQLi getMySQLi() implemented
  [PASS] db.php: Procedural MySQLi getProcedural() / getMySQLiProcedural() implemented
  [PASS] db.php: Credentials loaded dynamically via env()
  [PASS] db.php: Secure connection error handling (credentials masked from output)
  [PASS] StudentService: getAllMySQLi() uses prepared statements
  [PASS] StudentService: findByEmail() uses prepared statement
  [PASS] StudentService: create() uses prepared statement with bind_param
  [PASS] StudentService: count() total count method implemented
  [PASS] Live MySQL Connection: Connected to MySQL on port 3307 - Server: 8.0.46
  [PASS] Database Schema: database/schema.sql imported cleanly
  [PASS] Database Seeds: database/seed.sql imported cleanly
  [PASS] Table Presence: All 6 tables exist (users, students, events, registrations, audit_logs, contact_messages)
  [PASS] Table Engine: All tables configured with InnoDB engine
  [PASS] Seed Verification: Minimum 20 students seeded (Found: 20)
  [PASS] Seed Verification: Sample events seeded (Found: 5)
  [PASS] Database Constraints: Duplicate student email rejected with UNIQUE constraint
  [PASS] Database Constraints: Duplicate user username rejected with UNIQUE constraint
  [PASS] Database Constraints: Foreign key violation on non-existent event rejected
  [PASS] Database Constraints: Cascading delete on student registrations verified
  [PASS] Prepared Statements: Parameterized INSERT and SELECT query successful
  [PASS] Contact Messages Table: Parameterized message insertion successful
  [PASS] Security: Database connection failure hides raw password from display

======================================================================
SECTION 3: Practical 1-6 Regression Verification
======================================================================
  [PASS] Regression: public/pages/about.html exists
  [PASS] Regression: public/pages/administrative.html exists
  [PASS] Regression: public/pages/campuslife.html exists
  [PASS] Regression: public/pages/contact.html exists
  [PASS] Regression: public/pages/course-enrollment.html exists
  [PASS] Regression: public/pages/dashboard.html exists
  [PASS] Regression: public/pages/events.html exists
  [PASS] Regression: public/pages/faq.html exists
  [PASS] Regression: public/pages/login.html exists
  [PASS] Regression: public/pages/registration.html exists
  [PASS] Regression: public/pages/students.html exists
  [PASS] Regression: public/assets/data/events.json valid JSON (16 items)
  [PASS] Regression: public/assets/data/students.json valid JSON (18 items)
  [PASS] Regression: public/assets/data/faqs.json valid JSON (16 items)
  [PASS] Regression: public/assets/js/data-loader.js exists
  [PASS] Regression: public/assets/js/pagination.js exists
  [PASS] Regression: public/assets/js/events-renderer.js exists
  [PASS] Regression: public/assets/js/faq-renderer.js exists
  [PASS] Regression: public/assets/js/students-renderer.js exists
  [PASS] Regression: public/assets/js/registration.js exists
  [PASS] Regression: public/assets/js/contact.js exists

======================================================================
VERIFICATION SUMMARY: 88/88 PASSED (100.0%)
======================================================================
SUCCESS: All Phase 3 (Practical 7 & 8) requirements and regressions PASSED!
```

### 4.2 Full Regression Suite Summary
- **`tests/verify_project.py`:** 189 local URL/asset references verified; Practical 5 regex validation confirmed; all architecture tier files confirmed. **Result: 100% PASS**.
- **`tests/verify_practical_6.py`:** JSON datasets, search/filter/sort algorithms, pagination boundary slicing, safe DOM rendering (0 untrusted `innerHTML`), and legacy Practical 1–5 JavaScript handlers verified. **Result: 100% PASS**.
- **`tests/verify_phase_3.py`:** Form validation, CSRF, flock locking, password hashing, MySQLi prepared statements, schema import, seeds, foreign keys, unique constraints, and error masking. **Result: 88/88 (100%) PASS**.

---

## 5. Verification Commands

To reproduce the verification at any time:

```bash
# 1. Run Phase 3 automated verification
python tests/verify_phase_3.py

# 2. Run Practical 6 verification
python tests/verify_practical_6.py

# 3. Run complete project link integrity verification
python tests/verify_project.py
```
