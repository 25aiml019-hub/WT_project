# StudentHub — InfinityFree Production Security Audit

**Author:** Daksh Harkhani (25AIML019)  
**Course:** AIUE203 — Web Development Fundamentals  
**Scope:** Public Web Security, Uploads, Sessions, Credentials, and Academic Privacy  

---

## 1. Credentials & Configuration Isolation

1. **Environment File Protection:**
   - Database credentials, encryption keys, and environment variables are strictly loaded from `.env`.
   - Root `.htaccess` contains:
     ```apache
     <FilesMatch "(^\.env|\.sql$|\.log$|\.json$|\.md$)">
         Require all denied
     </FilesMatch>
     ```
   - Attempting to access `https://your-domain.com/.env` in a browser returns **HTTP 403 Forbidden**.
2. **Exclusion of Secrets from Public Bundles:**
   - The production bundle excludes local development `.env` files and Git repositories.
   - A template with placeholders (`.env.infinityfree.example`) is provided so credentials are only set on the live server.

---

## 2. Session Hardening & Authentication

1. **Cookie Security Attributes:**
   - `HttpOnly = 1`: Blocks client-side JavaScript from reading `PHPSESSID`.
   - `SameSite = 'Lax'`: Defends against Cross-Site Request Forgery (CSRF).
   - `Secure = 1`: Forces transmission exclusively over HTTPS connections.
2. **Session Hijacking Defenses:**
   - `session_regenerate_id(true)` is called immediately upon successful student and admin login.
   - Server-enforced inactivity timeout invalidates stale sessions after 3600 seconds (1 hour).
3. **Password Security:**
   - Password hashes use standard Bcrypt (`PASSWORD_BCRYPT`, cost 10).
   - First-login password change is strictly enforced for all 77 roster students with temporary college ID passwords.
   - Admin password updated to strong password `admin123`.

---

## 3. File Upload & Storage Security

1. **Multi-Stage File Validation:**
   - Extension whitelist: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`.
   - Deep MIME verification using `finfo(FILEINFO_MIME_TYPE)`: Detects and rejects executable or spoofed files (e.g. `.exe` disguised as `.pdf`).
   - File size restriction: Hard limit of 5 MB (`5242880` bytes).
2. **Direct Execution Neutralization:**
   - Upload directories (`storage/uploads/marksheets/` and `storage/uploads/posters/`) contain `.htaccess` preventing Apache from interpreting PHP scripts:
     ```apache
     <FilesMatch "\.(php|phtml|php3|php4|php5|php7|phps)$">
         Require all denied
     </FilesMatch>
     ```
   - Marksheet files are stored with unpredictable random hashes (`marksheet_{student_id}_sem{sem}_{hash}.ext`).
3. **Document Access Control:**
   - Uploaded files are served exclusively through `/api/marksheets/view.php`.
   - The endpoint checks authenticated session identity: Student B attempting to view Student A's marksheet is blocked with **HTTP 403 Forbidden**.

---

## 4. Student Directory & Privacy Defenses

1. **Directory Protection:**
   - The Student Directory table in `student/index.php` displays only `#`, `College ID`, `Student Name`, `Batch`, and `Counselor`.
   - Personal phone numbers, home addresses, and private emails are completely excluded from the rendered DOM.
2. **Audit Logging:**
   - Every administrative modification, student registration, and marksheet confirmation is recorded in the `audit_logs` table with user ID, action, and timestamp.
