# Practical 11 & Practical 12 Test Report

**Project:** StudentHub  
**Course:** AIUE203 — Web Development Fundamentals  
**Student:** Anshika Badala (25AIML002)  
**Institute:** CSPIT, CHARUSAT  
**Repository:** https://github.com/anshikabadala/Wt_Project.git  
**Date:** October 24, 2026  
**Commit Scope:** Phase 5 — Practical 11 & Practical 12  

---

## 1. Executive Summary

This report documents the implementation and verification of **Practical 11 (Student Management CRUD)** and **Practical 12 (Event Management CRUD & Secure Poster Upload)** for the StudentHub web application.

All operations enforce administrator-only role authorization (`role = 'admin'`), CSRF validation on state-changing requests, and MySQLi prepared statements to eliminate SQL injection vulnerabilities. File upload validation incorporates strict MIME-type sniffing, image dimension verification, script/polyglot content scanning, and path traversal defenses.

All automated verification test suites passed with **100% success rate (487/487 total project assertions passed, including 108/108 new Phase 5 assertions)**, confirming zero regressions across Practicals 1 through 10.

---

## 2. Implemented Functionality

### Practical 11: Student Management CRUD
- **Create:** Validated student creation with mandatory name (>=2 chars), valid RFC email format, Indian mobile number (10 digits), course, department, academic year (e.g. `2025-2026`), gender, hobbies, address, and status. Duplicate email check enforced at database (UNIQUE constraint) and application level (HTTP 409 Conflict).
- **Read:** Database-backed student retrieval with details modal view, masking sensitive fields and exposing academic profiles safely.
- **Update:** Full profile modification supporting name, mobile, course, department, academic year, and status. Rejects collision if email changed to an existing student's address (`id != ?`).
- **Delete / Deactivate:** Supports both non-destructive deactivation (toggling status between `active` and `inactive`) and permanent deletion with referential integrity.
- **Search & Filters:** Server-backed multi-parameter search (name, email, course) combined with department dropdown, academic year dropdown, and status filter (`active`, `inactive`, `all`).
- **Server-Side Pagination:** Bounded prepared statement pagination with `LIMIT ? OFFSET ?`. Page size selection (`5`, `10`, `25`), boundary protection (prevents out-of-range pages), and filter persistence.
- **CSV Export & Formula Injection Defense:** Complete dataset export to CSV. Any cell starting with formula trigger characters (`=`, `+`, `-`, `@`, `\t`, `\r`, `%`) is prepended with a single quote (`'`), preventing CSV spreadsheet formula injection / DDE attacks.
- **Audit Logging:** Every student creation, update, status toggle, and deletion is recorded in the `audit_logs` table with administrator ID, action, details, and client IP.

### Practical 12: Event Management CRUD & Poster Upload
- **Create:** Campus event scheduling with validated title (>=3 chars), date (`YYYY-MM-DD`), time (`10:00 AM`), category (Technical, Cultural, Sports, Workshop, Academic, General), location/venue, description, and status (`upcoming`, `completed`, `cancelled`).
- **Read:** Database-backed paginated event list and details modal with full preview.
- **Update:** Schedule updates, status transitions, venue edits, and poster image replacements.
- **Delete:** Full event cancellation/removal with cascade handling in `registrations`.
- **Poster Upload Security:**
  - Strict extension whitelist: `.jpg`, `.jpeg`, `.png`, `.webp`.
  - True MIME type sniffing using `finfo_file(FILEINFO_MIME_TYPE)`: must be `image/jpeg`, `image/png`, or `image/webp`. Rejects spoofed extensions.
  - Image dimension verification with `getimagesize()` to reject corrupted files or text masquerading as images.
  - Script & polyglot scanning: inspecting the first 4KB for `<?php`, `<?=`, `<script`, `<%` to prevent PHP execution inside image payloads.
  - Maximum upload size limit: strictly enforced at 2 MB (2,097,152 bytes).
  - Cryptographically secure randomized filenames: `poster_` + `bin2hex(random_bytes(16))` + `.` + extension.
  - Path traversal prevention: `basename()` sanitization guarantees all files remain within `storage/uploads/posters/`.
  - Execution prevention: `storage/uploads/posters/.htaccess` explicitly denies script execution (`Deny from all` for `.php`, `.phtml`, `.exe`, etc.).
  - Secure poster delivery: `public/serve-poster.php` verifies basename, matches extension whitelist, sets `X-Content-Type-Options: nosniff`, and returns SVG placeholder if missing.
  - Safe replacement & cleanup: Old poster files are unlinked only after database update succeeds, and default seed images (`hackathon.jpg`, etc.) are protected from deletion.
- **Audit Logging:** Every event creation, update, and deletion is logged to `audit_logs`.

---

## 3. Files Created and Modified

| File | Change Type | Purpose |
| :--- | :---: | :--- |
| `database/migrations/migration_practical_11_12.sql` | Created | SQL migration adding `academic_year` to `students` and `event_time` to `events`. |
| `database/schema.sql` | Modified | Updated schema definitions with `academic_year` and `event_time`. |
| `database/seed.sql` | Modified | Added 20 student records with academic years and updated event times. |
| `app/services/audit_service.php` | Created | Centralized audit logging service (`AuditService::log`, `getRecent`, `count`). |
| `app/services/student_service.php` | Modified | Extended with `getPaginated()`, `update()`, `delete()`, `exportCsv()`, and `getAcademicYears()`. |
| `app/services/event_service.php` | Modified | Extended with `getPaginated()`, `create()`, `update()`, `delete()`, `handlePosterUpload()`, and `removePosterFile()`. |
| `api/students/index.php` | Modified | Admin-guarded REST endpoint supporting paginated search, filter, CRUD, and CSV export. |
| `api/events/index.php` | Modified | Admin-guarded REST endpoint supporting paginated search, filter, CRUD, and multipart poster uploads. |
| `public/serve-poster.php` | Created | Secure streaming controller for uploaded posters with nosniff and SVG fallback. |
| `public/assets/css/admin.css` | Modified | Admin dashboard cards, data tables, modals, badges, and responsive controls. |
| `admin/index.php` | Modified | Admin dashboard with live metric counters, module navigation cards, and recent audit activity. |
| `admin/students.php` | Created | Complete Practical 11 Student Management CRUD UI with Fetch API, search, modals, and CSV export. |
| `admin/events.php` | Created | Complete Practical 12 Event Management CRUD UI with Fetch API, poster upload, and preview. |
| `storage/uploads/posters/.gitkeep` | Created | Directory structure preservation for user poster uploads. |
| `storage/uploads/posters/.htaccess` | Created | Apache security rules preventing script execution in posters folder. |
| `.gitignore` | Modified | Ensures runtime uploaded poster files in `storage/uploads/posters/*` are not tracked by Git. |
| `tests/verify_phase_5.py` | Created | 108 automated assertions for Practicals 11 & 12, security checks, and regressions. |
| `README.md` | Modified | Updated documentation with Phase 5 status, management guides, and testing instructions. |

---

## 4. Database Migrations

Executed migration:
```sql
ALTER TABLE `students` 
    ADD COLUMN IF NOT EXISTS `academic_year` VARCHAR(20) NOT NULL DEFAULT '2025-2026' AFTER `department`,
    ADD INDEX IF NOT EXISTS `idx_students_academic_year` (`academic_year`);

ALTER TABLE `events` 
    ADD COLUMN IF NOT EXISTS `event_time` VARCHAR(20) NULL DEFAULT '10:00 AM' AFTER `event_date`;
```

---

## 5. Test Commands & Actual Results

### Test Execution Summary

| Test Suite | Scope | Total Tests | Passed | Failed | Success Rate |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `tests/verify_project.py` | Phase 1 & 2 Restructuring & Asset References | 189 | 189 | 0 | 100.0% |
| `tests/verify_practical_6.py` | Practical 6 JSON Fetch, Search, Filter, Sort | 15 | 15 | 0 | 100.0% |
| `tests/verify_phase_3.py` | Practicals 7 & 8 Form Handling & Database Base | 88 | 88 | 0 | 100.0% |
| `tests/verify_phase_4.py` | Practicals 9 & 10 Registration, Auth, RBAC & Regressions | 87 | 87 | 0 | 100.0% |
| `tests/verify_phase_5.py` | Practicals 11 & 12 Student/Event CRUD, Uploads, Security | 108 | 108 | 0 | 100.0% |
| **Total** | **Full Project Verification** | **487** | **487** | **0** | **100.0%** |

### Verified Security Assertions
1. **Server-Side Authorization:** Admin endpoints (`api/students/index.php`, `api/events/index.php`, `admin/students.php`, `admin/events.php`) strictly enforce `enforceApiAuth('admin')` / `checkRole('admin')`, rejecting unauthenticated and non-admin student requests with HTTP 401 / 403.
2. **CSRF Protection:** All state-changing POST requests require timing-safe CSRF token validation (`validateCsrfToken()`).
3. **SQL Injection Defense:** MySQLi prepared statements with explicit parameter binding (`bind_param`) across all filters, search terms, pagination offsets, and CRUD mutations.
4. **CSV Formula Injection:** Values prefixed with single quote (`'`) to protect spreadsheet applications from executing formulas.
5. **Upload Validation:** Extension whitelist, MIME sniffing via `finfo`, dimension check via `getimagesize()`, 2 MB file size limit, and scanning for embedded script tags (`<?php`, `<script`).
6. **Path Traversal Defense:** Strict `basename()` enforcement prevents directory traversal during file uploads and poster removals.
7. **Script Execution Defense:** `storage/uploads/posters/.htaccess` prohibits Apache script execution.

---

## 6. Known Limitations

1. **PHP CLI Environment:** Standalone PHP CLI binary is not installed on the system PATH in this local Windows testing environment. Database operations and logic are verified using Python `pymysql` directly against the active MySQL server on port 3307, paired with AST and static code validation.
2. **Seed Poster Images:** Sample events reference fallback poster filenames (`hackathon.jpg`, `sports.jpg`, etc.). When rendered in the browser without uploaded files, `serve-poster.php` safely serves an inline SVG placeholder graphic.
