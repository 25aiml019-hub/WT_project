# StudentHub — Project Structure & Architectural Specification

**Course:** AIUE203 - Web Development Fundamentals (WDF)  
**Student Name:** Anshika Badala  
**Student ID:** 25AIML002  
**Institute:** CSPIT, CHARUSAT  
**Version:** Phase 1 Architecture (October 2026)  

---

## 1. Architectural Overview

StudentHub has been refactored from a flat single-directory layout (`Wt_Project/`) into a clean, feature-based, tiered architecture. The new structure strictly separates public-facing assets from private configuration, server-side services, data storage, and administrative controllers.

This structure is designed to support:
- Static HTML5/CSS3/JavaScript execution for Practicals 1 through 5.
- Asynchronous Fetch API endpoints for Practical 6 and Practical 13.
- Modular PHP backend, sessions, and RBAC authentication for Practicals 7 through 10 and 14.
- Secure MySQL database operations (PDO/MySQLi) and file uploads for Practicals 11 and 12.
- Clean deployment with XAMPP or Apache Virtual Hosts for Practical 15.

```
25aiml002_studentHub/
├── public/                          # Public document root (web-accessible)
│   ├── index.html                   # Static HTML entry point (Practicals 1–5)
│   ├── index.php                    # Modular PHP entry point (uses app/includes)
│   ├── pages/                       # Semantic subpages
│   │   ├── about.html               # About Us & creator profile
│   │   ├── administrative.html      # Administrative services & timings
│   │   ├── campuslife.html          # Campus life & student clubs
│   │   ├── course-enrollment.html   # Course enrollment & faculty listings
│   │   ├── dashboard.html           # Student details & quick links
│   │   ├── events.html              # Upcoming campus events schedule
│   │   ├── login.html               # Student login form & validation
│   │   ├── registration.html        # Student registration form
│   │   ├── contact.html             # Contact information & message form
│   │   └── faq.html                 # Collapsible FAQ & light/dark theme
│   └── assets/                      # Static web assets
│       ├── css/                     # Organized stylesheets
│       │   ├── main.css             # Unified brand tokens, nav, tables, buttons, footer
│       │   ├── home.css             # Home hero grid & card hover styles
│       │   ├── about.css            # About page container & profile styles
│       │   ├── admin.css            # Administrative service lists & table
│       │   ├── campuslife.css       # Clubs list & interactive hover states
│       │   ├── course-enrollment.css# Course enrollment table styling
│       │   ├── dashboard.css        # Student details card & quick links grid
│       │   ├── events.css           # Events schedule table
│       │   ├── login.css            # Login form card & responsive actions
│       │   ├── registration.css     # Registration form, options flex layout
│       │   ├── contact.css          # Contact info cards grid & message form
│       │   └── faq.css              # Collapsible accordion & dark-theme styles
│       ├── js/                      # Modular JavaScript
│       │   ├── main.js              # Global active nav highlighting & utilities
│       │   ├── registration.js      # Practical 5 regex validation & reset logic
│       │   ├── faq.js               # Practical 4 accordion & theme toggle
│       │   └── contact.js           # Contact form submission & reset handler
│       └── images/                  # Visual assets & vector branding
│           ├── logo.svg             # Vector StudentHub logo (offline fallback)
│           └── README.md            # Asset guidance
├── app/                             # Private Application Core (restricted from direct URL access)
│   ├── config/                      # System configuration
│   │   ├── config.php               # .env loader, app constants, session setup
│   │   └── db.php                   # Secure PDO singleton database connection
│   ├── includes/                    # Reusable PHP view components
│   │   ├── header.php               # Shared HTML head, branding & meta tags
│   │   ├── nav.php                  # Shared navigation bar with active highlighting
│   │   ├── footer.php               # Shared footer with author credentials
│   │   └── auth_check.php           # Session check & authentication helpers
│   ├── middleware/                  # Interceptor middleware
│   │   ├── auth_middleware.php      # User authentication verification
│   │   └── role_middleware.php      # Role-Based Access Control (Admin vs Student)
│   └── services/                    # Business logic and database access services
│       ├── student_service.php      # Student data queries (Practical 11 scaffolding)
│       └── event_service.php        # Event data queries (Practical 12 scaffolding)
├── api/                             # RESTful JSON API endpoints
│   ├── auth/                        # Authentication endpoints
│   │   ├── login.php                # JSON login endpoint
│   │   └── logout.php               # Session termination endpoint
│   ├── students/                    # Student resource endpoints
│   │   └── index.php                # GET (list/search) & POST student handlers
│   └── events/                      # Event resource endpoints
│       └── index.php                # GET (list/status) & POST event handlers
├── admin/                           # Administrative Backoffice Portal
│   ├── index.php                    # Admin dashboard placeholder (RBAC guarded)
│   └── README.md                    # Admin module specifications
├── student/                         # Student Self-Service Portal
│   ├── index.php                    # Student dashboard placeholder (Auth guarded)
│   └── README.md                    # Student portal specifications
├── storage/                         # Writable file storage
│   └── uploads/                     # Upload destination (posters, avatars)
│       ├── .htaccess                # Script execution protection (disables PHP engine)
│       ├── .gitignore               # Excludes uploaded media from git tracking
│       └── README.md                # Upload directory guidelines
├── database/                        # Database definitions & test data
│   ├── schema.sql                   # MySQL DDL for users, students, events, registrations, audit_logs
│   └── seed.sql                     # Seed data with 20 sample students & sample events
├── tests/                           # Verification and testing
│   ├── validation_test.html         # Interactive in-browser regex & script test runner
│   ├── verify_project.py            # Automated link and asset verification script
│   └── README.md                    # Test instructions
├── docs/                            # Project Documentation
│   ├── PROJECT_AUDIT.md             # Complete pre-restructuring audit report
│   ├── PROJECT_STRUCTURE.md         # Architecture blueprint & directory specs
│   └── MIGRATION_MAP.md             # Mapping of original files to new destinations
├── .gitignore                       # Git ignore rules for secrets, uploads & system files
├── .env.example                     # Environment template for DB credentials & app settings
├── index.html                       # Root redirector forwarding to public/index.html
└── README.md                        # Master project documentation & local setup guide
```

---

## 2. Directory Responsibilities & Design Patterns

### 2.1 `public/` (Web Root)
- Acts as the web server's DocumentRoot in production or local Apache Virtual Host setup.
- Only publicly readable files (HTML, CSS, client-side JS, images) reside here.
- Subpages are organized under `public/pages/` with consistent lowercase kebab-case naming.
- `public/assets/` isolates CSS, JS, and images into structured subdirectories.
- Provides dual entry points:
  - `public/index.html`: Fully static entry point allowing zero-dependency opening via web browsers.
  - `public/index.php`: Modular PHP entry point utilizing reusable includes from `app/includes/`.

### 2.2 `app/` (Application Core)
- Completely isolated from direct web requests. When the DocumentRoot is pointed to `public/`, files in `app/` cannot be directly downloaded by users.
- **Config (`app/config/`):** Contains `config.php` (environment loader and session initializer) and `db.php` (singleton PDO database connection with prepared statements).
- **Includes (`app/includes/`):** Reusable layout partials (`header.php`, `nav.php`, `footer.php`) eliminate markup duplication across PHP pages.
- **Middleware (`app/middleware/`):** Houses `auth_middleware.php` and `role_middleware.php` for RBAC protection.
- **Services (`app/services/`):** Implements business logic and query encapsulation (`StudentService`, `EventService`).

### 2.3 `api/` (Resource-Based REST Endpoints)
- Predictable URI structure matching modern REST conventions:
  - `/api/auth/login.php` & `/api/auth/logout.php`
  - `/api/students/` (supports GET search/filtering and POST creation)
  - `/api/events/` (supports GET status filtering and POST creation)
- All endpoints emit standardized JSON responses with explicit HTTP status codes (`200`, `400`, `405`, `500`).

### 2.4 `storage/uploads/` (Writable Secure Storage)
- Serves as the storage directory for event posters and user avatar uploads in Practical 12.
- **Security Rule:** Protected by `.htaccess` which disables script execution (`php_flag engine off`, denies access to `.php`, `.phtml`, `.cgi`, `.exe`).
- **VCS Rule:** Protected by `.gitignore` so user uploaded files are not tracked in git.

### 2.5 `database/` (Data Tier)
- `schema.sql`: Contains the complete MySQL DDL creating tables with proper indexes and foreign keys:
  - `users`: Authentication credentials and role flags (`admin`, `student`).
  - `students`: Detailed student records.
  - `events`: Event schedules and poster references.
  - `registrations`: Student-to-event many-to-many relationship with unique constraint.
  - `audit_logs`: Observability and traceability log for admin operations.
- `seed.sql`: Seeds 20 student records (fulfilling Practical 11 criteria), default users, and sample campus events.

---

## 3. Security Hardening Measures

1. **Credential Isolation:**
   - Secrets and database passwords are never hardcoded. They are read from `.env` via `app/config/config.php`.
   - `.env` is excluded in `.gitignore`. A clean template is provided in `.env.example`.
2. **Database Protection:**
   - Database operations use PDO with `PDO::ATTR_EMULATE_PREPARES => false` to prevent SQL injection vulnerabilities.
   - Connection failures log safe errors to server logs without leaking database passwords to end-user browsers.
3. **Upload Protection:**
   - The uploads directory is isolated from executable PHP scripts.
   - Apache `.htaccess` denies execution of PHP and CGI files inside `storage/uploads/`.
4. **Session Hardening:**
   - `initSession()` enables `session.cookie_httponly` and `session.use_only_cookies` to mitigate XSS session hijacking.

---

## 4. Migration Mapping Summary

| Original File (`Wt_Project/`) | Restructured Location | Notes / Enhancements |
|---|---|---|
| `index.html` | `public/index.html` & `public/index.php` | Linked to `main.css`, `home.css`, unified nav, fallback SVG logo |
| `home.css` | `public/assets/css/home.css` | Removed 61 lines of dead commented CSS; uses CSS variables |
| `about.html` | `public/pages/about.html` | Removed 28 lines of dead commented HTML; added full nav & footer |
| `about.css` | `public/assets/css/about.css` | Scoped container and creator card styles |
| `ADMINISTRATIVE.html` | `public/pages/administrative.html` | Normalized to lowercase; added full nav, styled table & footer |
| `admin.css` | `public/assets/css/admin.css` | Reusable admin services list & table styles |
| `campuslife.html` | `public/pages/campuslife.html` | Fixed typo `ADMINSTRATIVE.html`; removed inline styles; added full nav |
| `campuslife.css` | `public/assets/css/campuslife.css` | Clubs list hover animation and responsive padding |
| `COURSEENROLLMENT.html` | `public/pages/course-enrollment.html` | Fixed unclosed `<link>` tag; uncommented nav; normalized lowercase |
| `COURSEENROLLMENT.css` | `public/assets/css/course-enrollment.css` | Normalized lowercase; course table styles |
| `dashboard.html` | `public/pages/dashboard.html` | Added full nav; upgraded from primitive styles to primary theme |
| `dashboard.css` | `public/assets/css/dashboard.css` | Replaced `aliceblue` with branded card, quick links grid |
| `events.html` | `public/pages/events.html` | Added full nav; styled events table |
| `events.css` | `public/assets/css/events.css` | Replaced black borders with clean responsive data-table |
| `login.html` | `public/pages/login.html` | Removed orphaned `</a>`; added full nav; responsive card |
| `login.css` | `public/assets/css/login.css` | Responsive login form styles |
| `registration.html` | `public/pages/registration.html` | Removed 71 lines of dead prototype code; added full nav |
| `reg.css` | `public/assets/css/registration.css` | Renamed for consistency; options group flex layout |
| `registration.js` | `public/assets/js/registration.js` | Preserved mobile (10 digits) & email regex validation |
| `contact.html` | `public/pages/contact.html` | Removed 33 lines of dead table code; added full nav |
| `contact.css` | `public/assets/css/contact.css` | Contact info grid and message form styles |
| *(Missing script)* | `public/assets/js/contact.js` | **Created new script:** implements `submitMessage()` & `resetMessage()` |
| `faq.html` | `public/pages/faq.html` | Removed 74 lines of dead prototype code; added full nav |
| `faq.css` | `public/assets/css/faq.css` | Accordion & dark-theme styles |
| `faq.js` | `public/assets/js/faq.js` | Preserved accordion logic; added persistent localStorage theme |
| *(New centralized CSS)* | `public/assets/css/main.css` | **Created new stylesheet:** central design tokens, nav, tables, buttons |
| *(New global JS)* | `public/assets/js/main.js` | **Created new script:** active navigation item highlighter |
| `README.md` | `README.md` | Updated with full setup guide, project architecture, and author credits |
