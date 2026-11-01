# Practical 9 & 10 Test & Implementation Report

**Project:** StudentHub  
**Course:** AIUE203 — Web Development Fundamentals (WDF)  
**Student Name:** Daksh Harkhani (25AIML019)  
**Institute:** Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT  
**Date:** October 2026  
**Status:** **Completed & Verified (100% Tests Passing)**

---

## 1. Executive Summary

Phase 4 completes **Practical 9** (Database-Backed Secure User Registration with Multi-Table Transactions) and **Practical 10** (Secure Authentication, Session Hardening, and Role-Based Access Control) for the StudentHub portal.

The implementation transitions user account management from file storage into an authoritative MySQL relational store with strict constraint enforcement, timing-safe bcrypt password verification, session fixation defense, inactivity timeouts, and route-level authorization guards for `admin` and `student` roles.

---

## 2. Practical 9 — Secure User Registration & Transactional Integrity

### 2.1 Backend Architecture & Implementation
- **Registration Processor (`public/process-registration.php`):**
  - **HTTP Method Enforcement:** Rejects GET and other HTTP verbs with HTTP `405 Method Not Allowed`.
  - **CSRF Token Verification:** Validates session CSRF token using timing-safe `hash_equals()`; invalid submissions rejected with HTTP `403 Forbidden`.
  - **Server-Side Validation:** Validates required fields: name, email, mobile (10 digits), course, department, gender, hobbies, address, password (minimum 6 characters), and password confirmation.
  - **Duplicate Prevention:** Pre-checks email and username uniqueness across `users` and `students` tables via prepared statements. Duplicates trigger HTTP `409 Conflict` with clear, accessible feedback.
  - **Multi-Table Atomic Transactions:**
    - Handled via `UserService::registerStudent()`.
    - Starts a transaction (`$mysqli->begin_transaction()`).
    - Inserts user account into `users` table with role `'student'` and status `'active'`.
    - Inserts student profile into `students` table, linking foreign key `students.user_id = users.id`.
    - Writes an audit log record in `audit_logs` capturing client IP and action `USER_REGISTRATION`.
    - Commits transaction atomically (`$mysqli->commit()`).
    - Rolls back completely (`$mysqli->rollback()`) if any failure occurs, leaving zero orphaned user or student records.
  - **Authoritative Storage & Privacy:**
    - MySQL is the sole authoritative store for user accounts.
    - Plaintext passwords and password hashes are **never** written to CSV or JSON registration files.
    - Secondary CSV logging in `storage/data/registrations.csv` records only non-sensitive registration metadata.

### 2.2 Frontend Registration Integration
- **`public/pages/registration.html` & `public/pages/registration.php`:**
  - Added username, password, and confirm password input fields.
  - Form action set to `../process-registration.php` with `method="POST"`.
  - Alert banner container `#registrationAlert` renders dynamic server and client feedback.
  - Preserved all Practical 5 regex validation rules (10-digit mobile, RFC email).
  - Client-side validation in `public/assets/js/registration.js` verifies password length and password match before initiating Fetch API `POST`.

---

## 3. Practical 10 — Login, Logout & Session Management

### 3.1 Authentication & Credential Verification
- **Login Processor (`public/process-login.php`):**
  - Accepts username or email interchangeably (`WHERE username = ? OR email = ? LIMIT 1`).
  - Utilizes MySQLi prepared statements to prevent SQL injection.
  - Verifies passwords using `password_verify()` against stored bcrypt hashes.
  - Mitigates timing attacks by evaluating a dummy hash when an account does not exist.
  - Returns a unified, generic error message for invalid credentials: `"Invalid username/email or password."`
  - Blocks deactivated/inactive accounts (`status !== 'active'`) with a descriptive message.
  - Updates `last_login = NOW()` upon successful authentication.

### 3.2 Session Hardening & Security Guarantees
- **Session Fixation Prevention:** Calls `session_regenerate_id(true)` immediately after successful login to rotate session tokens.
- **Cookie Security Parameters (`app/config/config.php`):**
  - `session.cookie_httponly = 1`: Blocks client-side JavaScript access to session cookies (mitigates XSS cookie theft).
  - `session.cookie_samesite = 'Lax'`: Mitigates Cross-Site Request Forgery (CSRF).
  - `session.cookie_secure = 1`: Automatically enabled when HTTPS is detected.
- **Server-Enforced Inactivity Timeout:**
  - Configurable via `SESSION_LIFETIME` in `.env` (default: 3600 seconds).
  - Compares `time() - $_SESSION['last_activity'] > $lifetime`.
  - Inactive sessions are cleared, cookies expired, and destroyed on the server.
- **Minimal Session Footprint:**
  - Stores only `user_id`, `username`, `email`, `role`, and `student_id`.
  - No passwords, tokens, or hashes are stored in the session.

### 3.3 Logout Flow (`public/process-logout.php` & `api/auth/logout.php`)
- Unsets and clears `$_SESSION = []`.
- Deletes the session cookie on the client by setting an expiration date in the past (`time() - 42000`) with exact path and domain parameters.
- Destroys server-side session via `session_destroy()`.
- Redirects users to `pages/login.html?logged_out=1`.

---

## 4. Role-Based Access Control (RBAC)

### 4.1 Authorization Guards (`app/includes/auth_check.php` & `app/middleware/`)
- `isAuthenticated(): bool`: Checks active session state.
- `hasRole(string $role): bool`: Validates current role.
- `requireLogin(string $redirect)`: Redirects unauthenticated web requests with `?error=unauthorized`.
- `requireRole(string $role, string $redirect)`: Blocks unauthorized roles with HTTP `403` / redirects with `?error=forbidden`.
- `enforceApiAuth(?string $requiredRole)`: Enforces JSON status `401 Unauthorized` and `403 Forbidden` for REST API endpoints.

### 4.2 Protected Portal Routing
1. **Admin Portal (`admin/index.php`):**
   - Protected with `checkRole('admin', '../public/pages/login.html')`.
   - Direct URL access without admin privileges is blocked.
   - Displays authorized admin username, role, and logout action.
2. **Student Portal (`student/index.php`):**
   - Protected with `checkAuth('../public/pages/login.html')`.
   - Displays authorized student details, personalized greeting, and portal links.
3. **Dynamic Navigation (`app/includes/nav.php`):**
   - Automatically renders "Admin Portal" for admin users.
   - Automatically renders "My Portal" for student users.
   - Replaces "Login" link with "Logout (username)" link for active sessions.

---

## 5. Development Test Accounts & Seeding Policy

In compliance with AIUE203 guidelines, no public admin registration is permitted. Pre-seeded test accounts are hashed with bcrypt:

| Username | Email | Role | Development Password |
|---|---|---|---|
| `admin` | `admin@studenthub.com` | `admin` | `admin123` |
| `anshika` | `dakshharkhani18@gmail.com` | `student` | `student123` |
| `demo_student` | `student@studenthub.com` | `student` | `student123` |

*Note: Seed scripts use `INSERT IGNORE INTO` syntax and never overwrite existing user passwords when re-executed.*

---

## 6. Automated Test Results

### 6.1 Phase 4 Test Suite (`tests/verify_phase_4.py`)
Executed against live MySQL server on port 3307:

```
===========================================================================
SECTION 1: Practical 9 - Secure User Registration & Transactional Integrity
===========================================================================
  [PASS] File Exists: public\process-registration.php
  [PASS] File Exists: app\services\user_service.php
  [PASS] File Exists: app\services\student_service.php
  [PASS] File Exists: app\config\security.php
  [PASS] File Exists: public\pages\registration.html
  [PASS] File Exists: public\pages\registration.php
  [PASS] File Exists: public\assets\js\registration.js
  [PASS] UserService: registerStudent() method implemented
  [PASS] UserService: Uses begin_transaction() and commit()
  [PASS] UserService: Uses rollback() on failure
  [PASS] UserService: Hashes password with bcrypt before insert
  [PASS] UserService: Prepared statement used for users insert
  [PASS] UserService: Prepared statement used for students insert
  [PASS] UserService: Sets role strictly to 'student' (no privilege escalation)
  [PASS] process-registration: Enforces HTTP POST check (405)
  [PASS] process-registration: Enforces CSRF Token validation (403)
  [PASS] process-registration: Validates password confirmation match
  [PASS] process-registration: Enforces duplicate email check (409 Conflict)
  [PASS] process-registration: Does NOT write password or password_hash to CSV file
  [PASS] Live Registration: User and Student records inserted atomically in transaction
  [PASS] Live Registration: User role is 'student' and status is 'active'
  [PASS] Live Registration: Password stored as valid bcrypt hash (not plaintext)
  [PASS] Live Registration: Student foreign key user_id correctly references users.id
  [PASS] Live Registration: Duplicate email rejected by database UNIQUE constraint
  [PASS] Live Registration: Duplicate username rejected by database UNIQUE constraint
  [PASS] Transactional Integrity: Transaction rolls back on error (zero orphaned users)

===========================================================================
SECTION 2: Practical 10 - Login, Logout & Session Management
===========================================================================
  [PASS] File Exists: public\process-login.php
  [PASS] File Exists: public\process-logout.php
  [PASS] File Exists: public\pages\login.html
  [PASS] File Exists: public\pages\login.php
  [PASS] File Exists: api\auth\login.php
  [PASS] File Exists: api\auth\logout.php
  [PASS] File Exists: app\includes\auth_check.php
  [PASS] File Exists: app\middleware\auth_middleware.php
  [PASS] File Exists: app\middleware\role_middleware.php
  [PASS] process-login: Enforces HTTP POST check (405)
  [PASS] process-login: Enforces CSRF token check (403)
  [PASS] process-login: Calls UserService::authenticate()
  [PASS] process-login: Regenerates session ID on login (session_regenerate_id)
  [PASS] process-login: Stores minimal identity (user_id, username, email, role)
  [PASS] process-login: Performs RBAC redirect routing (admin vs student)
  [PASS] process-logout: Clears session array ($_SESSION = [])
  [PASS] process-logout: Expires session cookie in past (time() - 42000)
  [PASS] process-logout: Calls session_destroy()
  [PASS] process-logout: Redirects to login with logged_out status
  [PASS] Authentication: Seeded admin account verifies with password 'admin123'
  [PASS] Authentication: Seeded student account verifies with password 'student123'
  [PASS] Authentication: Incorrect password rejected safely
  [PASS] Authentication: Inactive status correctly recorded in DB
  [PASS] Authentication: Prepared statement resolves user by both username and email
  [PASS] Session Hardening: session.cookie_httponly set to 1
  [PASS] Session Hardening: session.cookie_samesite set to 'Lax'
  [PASS] Session Hardening: session.cookie_secure enabled on HTTPS
  [PASS] Session Hardening: Inactivity timeout enforcement logic present

===========================================================================
SECTION 3: Role-Based Access Control (RBAC) & Endpoint Guards
===========================================================================
  [PASS] RBAC: isAuthenticated() helper declared
  [PASS] RBAC: hasRole() role check helper declared
  [PASS] RBAC: currentUser() identity accessor declared
  [PASS] RBAC: requireLogin() redirect guard declared
  [PASS] RBAC: requireRole() role enforcement guard declared
  [PASS] RBAC: enforceApiAuth() API status 401/403 guard declared
  [PASS] RBAC: admin/index.php invokes checkRole('admin')
  [PASS] RBAC: admin/index.php displays authenticated user details and sign out
  [PASS] RBAC: student/index.php invokes checkAuth() guard
  [PASS] RBAC: student/index.php displays authenticated student details and sign out
  [PASS] RBAC: nav.php dynamically displays Admin Portal link for admin users
  [PASS] RBAC: nav.php dynamically displays Logout link for authenticated users

===========================================================================
SECTION 4: Practical 1-8 Regressions Verification
===========================================================================
  [PASS] All 11 HTML pages verified
  [PASS] All JSON datasets verified (events.json: 16, students.json: 18, faqs.json: 16)
  [PASS] All JavaScript modules verified

===========================================================================
PHASE 4 VERIFICATION SUMMARY: 87/87 PASSED (100.0%)
===========================================================================
SUCCESS: All Practical 9 and 10 requirements and regressions PASSED!
```

### 6.2 Full Regression Suite Summary
- **`tests/verify_project.py`:** 189 local references verified. **Result: 100% PASS**.
- **`tests/verify_practical_6.py`:** 15 assertions on JSON data and safe DOM rendering verified. **Result: 100% PASS**.
- **`tests/verify_phase_3.py`:** 88 assertions on form validation, CSV/JSON storage, MySQLi connectivity, and schema constraints verified. **Result: 100% PASS**.
- **`tests/verify_phase_4.py`:** 87 assertions on registration, authentication, sessions, and RBAC verified. **Result: 100% PASS**.
- **Total Assertions Across Test Suites:** **379 / 379 PASSED (100%)**.

---

## 7. Verification Commands

```bash
# 1. Run Phase 4 verification (Practical 9 & 10)
python tests/verify_phase_4.py

# 2. Run Phase 3 verification (Practical 7 & 8)
python tests/verify_phase_3.py

# 3. Run Practical 6 Fetch API verification
python tests/verify_practical_6.py

# 4. Run Complete Project Link Integrity verification
python tests/verify_project.py
```
