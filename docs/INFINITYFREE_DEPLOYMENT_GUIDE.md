# StudentHub — InfinityFree Production Deployment & Migration Guide

**Project:** StudentHub College Management System  
**Institution:** CSPIT, CHARUSAT  
**Author:** Anshika Badala (25AIML002)  
**Target Host:** InfinityFree (Free PHP & MySQL Web Hosting)  
**Bundle Archive:** `studenthub_infinityfree_bundle.zip` (1.51 MB, SHA-256: `c87dcf28aa882215bef49b4ab6a378863b119d82c38f2b142e27f5116bc4b8b1`)  
**Database SQL:** `database/verified_backups/studenthub_infinityfree_migration.sql` (151 KB)

---

## 1. Prerequisites on InfinityFree

1. Sign in to your [InfinityFree Client Area](https://app.infinityfree.com/).
2. Create a new hosting account (or select your existing account).
   - Choose a free subdomain (e.g. `yourname.infinityfreeapp.com` or `studenthub.rf.gd`).
3. Note your account details from the Client Area:
   - **Account Username:** e.g. `epiz_12345678`
   - **Account Password:** (click "Show" to reveal)
   - **FTP Hostname:** e.g. `ftpupload.net`
   - **Main Domain / Website URL:** e.g. `https://yourname.infinityfreeapp.com`

---

## 2. Step 1: Create & Import the MySQL Database

> [!IMPORTANT]
> **InfinityFree MySQL Host Caveat:**  
> On InfinityFree, the database server is **NEVER** `localhost` or `127.0.0.1`. You must find your unique database hostname in the Control Panel (it starts with `sql...`).

1. In the InfinityFree Client Area, click **Control Panel** (cPanel / VistaPanel).
2. Under the **Databases** section, click **MySQL Databases**.
3. Under **Create New Database**, enter `studenthub` into the field and click **Create Database**.
   - Your full database name will be generated as: `epiz_XXXXXXXX_studenthub`.
4. Note your database connection credentials shown on that page:
   - **MySQL Database:** `epiz_XXXXXXXX_studenthub`
   - **MySQL Username:** `epiz_XXXXXXXX`
   - **MySQL Hostname:** e.g. `sql100.infinityfree.com` or `sql200.epizy.com`
   - **MySQL Port:** `3306`
   - **MySQL Password:** Your InfinityFree account password.
5. In the Control Panel, click **phpMyAdmin** next to your new database (or click the phpMyAdmin icon in the main menu).
6. Once phpMyAdmin opens, click your database name (`epiz_XXXXXXXX_studenthub`) in the left sidebar.
7. Click the **Import** tab at the top.
8. Click **Choose File** and select `database/verified_backups/studenthub_infinityfree_migration.sql` (or extracted from `studenthub_infinityfree_bundle.zip`).
9. Keep character set as `utf-8` and click **Import** (or **Go**) at the bottom.
10. Confirm success: You should see 21 tables created, including:
    - `students` (100 rows, 78 AIML roster students)
    - `users` (82 rows)
    - `events` (16 rows)
    - `semester_results` (156 rows)
    - `timetable_slots` (51 rows)

---

## 3. Step 2: Upload Application Files

You can upload files using either **FileZilla (FTP)** or the **Online File Manager**.

### Method A: Using FileZilla FTP (Recommended for Speed)
1. Open FileZilla.
2. Enter your connection credentials:
   - **Host:** `ftpupload.net`
   - **Username:** `epiz_XXXXXXXX`
   - **Password:** Your InfinityFree account password
   - **Port:** `21`
3. Click **Quickconnect**.
4. In the remote pane, open the **`htdocs/`** directory.
5. Extract `studenthub_infinityfree_bundle.zip` locally on your computer.
6. Drag and drop all extracted contents directly into the remote **`htdocs/`** folder:
   ```
   htdocs/
   ├── .htaccess
   ├── index.php
   ├── index.html
   ├── .env.infinityfree.example
   ├── README.md
   ├── admin/
   ├── api/
   ├── app/
   ├── database/
   ├── public/
   ├── storage/
   └── student/
   ```

### Method B: Using InfinityFree Online File Manager
1. In the Control Panel, click **Online File Manager** (MonstaFTP).
2. Navigate into **`htdocs/`**.
3. Click **Upload** &rarr; Select files/folders from the extracted bundle.

---

## 4. Step 3: Configure `.env` on InfinityFree

1. In `htdocs/`, create a new file named **`.env`** (or rename `.env.infinityfree.example` to `.env`).
2. Populate `.env` with your actual InfinityFree values:
   ```ini
   APP_NAME="StudentHub"
   APP_ENV="production"
   APP_DEBUG=false
   APP_URL="https://yourname.infinityfreeapp.com"

   # InfinityFree MySQL Credentials
   DB_HOST="sqlXXX.infinityfree.com"
   DB_PORT=3306
   DB_NAME="epiz_XXXXXXXX_studenthub"
   DB_USER="epiz_XXXXXXXX"
   DB_PASS="YourAccountPassword"
   DB_CHARSET="utf8mb4"

   # Session Hardening
   SESSION_LIFETIME=3600
   SESSION_SECURE=true

   # Upload Restrictions
   UPLOAD_MAX_SIZE=5242880
   UPLOAD_ALLOWED_TYPES="jpg,jpeg,png,webp,pdf"
   ```
3. Save the `.env` file.

---

## 5. Step 4: Verify Directory Permissions & Security

1. Ensure `storage/` directory permissions are set to `755` (or `775`):
   - `storage/logs/` (writeable by PHP)
   - `storage/uploads/marksheets/` (writeable by PHP)
   - `storage/uploads/posters/` (writeable by PHP)
   - `storage/data/` (writeable by PHP)
2. Verify that `.htaccess` exists in `storage/logs/` and `storage/uploads/marksheets/` to prevent direct script execution.

---

## 6. Step 5: Free SSL Certificate (HTTPS)

1. In the InfinityFree Client Area, click **Free SSL Certificates**.
2. Click **New SSL Certificate**.
3. Select your domain (`yourname.infinityfreeapp.com`).
4. Select the **Let's Encrypt** or **ZeroSSL** provider.
5. Follow the automatic DNS CNAME verification (takes 2–5 minutes).
6. Click **Install SSL Certificate Automatically**.
7. Once active, your website will be served securely over `https://`.

---

## 7. Step 6: Live Smoke Test Verification

Open `https://yourname.infinityfreeapp.com` in your browser and verify:

1. **Homepage:** Grand hero banner, announcements, and university navigation load with responsive layout.
2. **Student Login:** Log in with `25AIML002` / `25AIML002` &rarr; Opens Student Portal with verified CGPA 8.44.
3. **First-Login Security:** Log in with `25AIML001` / `25AIML001` &rarr; Redirects to change-password interface.
4. **Admin Portal:** Log in with `admin` / `admin123` &rarr; Opens Administrative CRUD modules.
5. **Academic Records:** View Sem 1 (8.05), Sem 2 (8.77), and Sem 3 Timetable.
6. **Campus Events:** View all 16 events. Verify Event 15 is disabled ("Event Concluded") while upcoming events allow registration.
7. **Marksheets:** Upload a PDF marksheet &rarr; Confirms SGPA without errors.
