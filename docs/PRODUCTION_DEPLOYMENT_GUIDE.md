# StudentHub — Production Deployment & Complete Database Migration Manual

**Project:** StudentHub College Management & Student Information Portal  
**Institution:** Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT  
**Course:** AIUE203 — Web Development Fundamentals  
**Author:** Anshika Badala (25AIML002, FYAIML)  
**Intended Git Identity:** `anshikabadala <anshikabadala2@gmail.com>`  
**Production Bundle:** `studenthub_production_bundle.zip` (SHA-256: `bad82d7e93371d8a33c3ae1f3e5ded7094825ce67c413944ad2f91131d1d1ef0`)  
**Database Migration Script:** `database/production_complete_migration.sql`

---

## 1. Executive Summary & Verification Matrix

The StudentHub deployment package preserves 100% of the existing application functionality, architecture, data schemas, and verified user accounts without relying on mock data or structural compromises.

### Core Data Integrity Audit:
| Category | Total Count | Verification Status |
|---|---|---|
| **AIML Official Students** | **78 Students** | Preserved (All 78 linked with College IDs `25AIML001` - `25AIML078`) |
| **All Student Accounts** | **100 Records** | Preserved (78 AIML roster + 22 seeded students from Practicals 7–11) |
| **User Authentication Accounts** | **82 Users** | Preserved (78 students + 3 demo/test users + 1 admin) |
| **Campus Events** | **16 Events** | Preserved (All technical, cultural, sports events synced with status) |
| **Event Registrations** | **5 Registrations** | Preserved (Atomic DB persistence in `registrations` table) |
| **Semester Academic Results** | **156 Records** | Preserved (78 students &times; 2 semesters official SGPAs) |
| **Unassigned Academic Quarantine** | **13 Records** | Preserved (Records for `25AIML079` - `25AIML090` + anomalous rows) |
| **Semester 3 Timetable Slots** | **51 Slots** | Preserved (Full Division I schedule for AY 2026–27, Odd Term) |
| **Student Batches & Counselors** | **4 Batches** | Preserved (Batch A1, B1, C1, D1 with designated faculty counselors) |
| **Student Clubs & Announcements** | **4 Clubs, 3 Notices** | Preserved (Coding, Music, Sports, Photography) |
| **Marksheet Uploads** | **32 Records** | Preserved (Extracted, Confirmed, and Historical records intact) |
| **Audit Logs** | **283 Entries** | Preserved (Full audit trail of user actions) |

---

## 2. Production Deployment Steps

### Phase A: Uploading the Application Files
1. Extract the pre-built `studenthub_production_bundle.zip` into your web hosting directory (e.g. `/var/www/studenthub` or `public_html`).
2. **Web Root Configuration:**
   - **Recommended (VirtualHost / Nginx / Apache):** Set the server's `DocumentRoot` directly to `/path/to/studenthub/public`.
   - **Shared Hosting (cPanel / DirectAdmin where root is `public_html`):** The bundle includes an automated root `.htaccess` and `index.php` that routes traffic safely into `public/` while strictly blocking direct HTTP access to internal directories (`app/`, `database/`, `storage/`).

### Phase B: Production Database Migration
1. Log in to your hosting control panel (cPanel phpMyAdmin, AWS RDS, DigitalOcean, or MySQL CLI).
2. Create your production database with `utf8mb4` encoding:
   ```sql
   CREATE DATABASE `your_production_dbname` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Create a dedicated MySQL user and grant all privileges on `your_production_dbname`.
4. Import `database/production_complete_migration.sql`:
   - **Using phpMyAdmin:** Select the database &rarr; Click **Import** &rarr; Choose `database/production_complete_migration.sql` &rarr; Click **Import**.
   - **Using MySQL CLI:**
     ```bash
     mysql -h your_production_host -P your_production_port -u your_production_user -p your_production_dbname < database/production_complete_migration.sql
     ```
5. Confirm row count:
   ```sql
   SELECT COUNT(*) FROM students WHERE student_id IS NOT NULL; -- Must return 78
   SELECT COUNT(*) FROM events;                                -- Must return 16
   SELECT COUNT(*) FROM semester_results;                     -- Must return 156
   ```

### Phase C: Environment Configuration (`.env`)
1. In the project root, create your production `.env` file from `.env.production.example`:
   ```bash
   cp .env.production.example .env
   ```
2. Configure your live production values:
   ```ini
   APP_NAME="StudentHub"
   APP_ENV="production"
   APP_DEBUG=false
   APP_URL="https://your-domain.com"

   # Production MySQL Database Credentials
   DB_HOST="your_db_hostname_or_ip"
   DB_PORT=3306
   DB_NAME="your_production_dbname"
   DB_USER="your_production_db_user"
   DB_PASS="your_secure_db_password"
   DB_CHARSET="utf8mb4"

   # Session Hardening
   SESSION_LIFETIME=3600
   SESSION_SECURE=true

   # Upload Restrictions
   UPLOAD_MAX_SIZE=5242880
   UPLOAD_ALLOWED_TYPES="jpg,jpeg,png,webp,pdf"
   ```

### Phase D: Directory Permissions
Ensure that PHP-FPM or Apache has write permissions to the `storage/` directory:
```bash
chmod -R 755 storage
chmod -R 775 storage/logs
chmod -R 775 storage/uploads
chmod -R 775 storage/data
```
Verify that `.htaccess` files inside `storage/logs/` and `storage/uploads/marksheets/` prevent direct browser execution of scripts.

---

## 3. Production Security Hardening

1. **Error Hiding:** `APP_DEBUG=false` suppresses public display of PHP errors, notices, and stack traces. All exceptions are securely written to `storage/logs/production_error.log`.
2. **Session Security:**
   - `HttpOnly=true`: Blocks client-side JavaScript from accessing session cookies.
   - `SameSite=Lax`: Mitigates Cross-Site Request Forgery.
   - `Secure=true`: Forces cookie delivery exclusively over HTTPS.
3. **Admin Authentication:**
   - Admin username: `admin`
   - Admin password: `admin123` (hashed using standard bcrypt with cost 10).
4. **Student Account Security & First-Login Password Change:**
   - 77 student accounts are seeded with `must_change_password = 1`.
   - On initial login using their temporary college ID, students are immediately intercepted and redirected to `/pages/change-password.php` to choose a private password.
5. **Cross-Student Privacy:**
   - Phone numbers and personal emails are hidden in the Student Directory.
   - Marksheet download endpoint `/api/marksheets/view.php` enforces owner verification (HTTP 403 Forbidden if student B requests student A's marksheet).

---

## 4. Post-Deployment Smoke Test Checklist (22 Items)

Run these checks after publishing the website:

- [ ] **1. Homepage:** Open `https://your-domain.com/` and confirm responsive banner, announcement pills, and news cards load.
- [ ] **2. Navigation:** Verify links to Administrative, Campus Life, Events, About Us, Contact Us, and Login work.
- [ ] **3. Admin Login:** Sign in with `admin` / `admin123` at `/pages/login.html` &rarr; Redirects to `/admin/index.php`.
- [ ] **4. Student Login:** Sign in with `25AIML002` / `25AIML002` &rarr; Redirects to `/student/index.php`.
- [ ] **5. First-Login Password Change:** Sign in with `25AIML001` / `25AIML001` &rarr; Prompted with mandatory password update at `/pages/change-password.php`.
- [ ] **6. Student Dashboard:** Verify Student Name (Anshika Badala), Roll No (`25AIML002`), Batch (`Batch A`), and Counselor (`Prof. Gaurav Kumar`).
- [ ] **7. 78 Student Accounts:** In the directory tab, verify batch filters: All (78), Batch A (20), Batch B (20), Batch C (20), Batch D (18).
- [ ] **8. Class Directory Privacy:** Confirm phone numbers and personal emails are hidden from the directory table.
- [ ] **9. Academic Records:** Verify Semester 1 SGPA (`8.05`), Semester 2 SGPA (`8.77`), and weighted CGPA (`8.44`).
- [ ] **10. Semester 3 Timetable:** Confirm schedule renders Division I timetable, Monday Slot 1 (OS in Room 218) and today's schedule card.
- [ ] **11. Course Enrollment:** Access `/pages/course-enrollment.html` and verify subjects and enrolled courses render.
- [ ] **12. Marksheets Upload:** Upload a valid PDF marksheet &rarr; Upload completes with HTTP 200 without PHP errors.
- [ ] **13. CGPA Confirmation:** Confirm the extracted SGPA &rarr; Status changes to `confirmed` and updates student record.
- [ ] **14. All 16 Events:** Open `/pages/events.html` &rarr; Confirm all 16 events render with correct dates and categories.
- [ ] **15. Event Registration:** Click an upcoming open event &rarr; Modal opens and allows registration.
- [ ] **16. Duplicate Registration:** Try registering again for the same event &rarr; Blocked with "Already Registered".
- [ ] **17. Concluded Event Rule:** Open Event 15 (Monsoon Music) &rarr; Registration button disabled ("Event Concluded").
- [ ] **18. Admin Permissions:** Open `/admin/index.php` as an unauthenticated user &rarr; Blocked with redirect to login.
- [ ] **19. Contact Form:** Submit an inquiry on `/pages/contact.html` &rarr; Form persists to `contact_messages` table.
- [ ] **20. Responsive Layout:** Test layout at 1920px (desktop), 1366px (laptop), 768px (tablet), and 390px (mobile).
- [ ] **21. HTTPS:** Verify SSL lock icon is green and HTTP redirects to HTTPS.
- [ ] **22. Persistence:** Log out, log in again, and confirm registrations and marksheets persist.

---

## 5. Rollback & Disaster Recovery Plan

If an unexpected server failure occurs during deployment:
1. **Database Rollback:**
   - Execute the verified backup located at `database/production_complete_migration.sql`:
     ```bash
     mysql -u your_user -p your_database < database/production_complete_migration.sql
     ```
2. **File Rollback:**
   - Re-extract the clean `studenthub_production_bundle.zip`.
3. **Environment Rollback:**
   - Reset `.env` with validated development settings.
