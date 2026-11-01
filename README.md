# StudentHub — Web Development Project (WT)

**Course:** AIUE203 — Web Development Fundamentals (WDF)  
**Student Name:** Daksh Harkhani  
**Student ID:** 25AIML019  
**Branch:** B.Tech AIML (FYAIML)  
**Institution:** Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT  
**Repository:** [https://github.com/25aiml019-hub/WT_project](https://github.com/25aiml019-hub/WT_project)

---

## 📖 Project Overview

**StudentHub** is an integrated college campus portal and student information management system developed for the Web Technology course. It provides a centralized platform for academic information, administrative services, course enrollment, campus life, upcoming events, student self-service dashboard, and administrative management.

The repository accommodates both:
1. **The Modern Tiered Web Application:** Production-ready HTML5, CSS3, JavaScript, modular PHP backend, RESTful JSON APIs, MySQL database integration, and security controls.
2. **Student Practicals Directory (`25aiml019/`):** Original lab practicals, exercises, static pages, and assets created throughout the semester.

---

## 📂 Repository Directory Layout

```
WT_project/
├── 25aiml019/                       # Original Student Practical Files & Media
│   ├── index.html                   # Original StudentHub static homepage
│   ├── about.html                   # About page
│   ├── admin.html                   # Admin services page
│   ├── contact.html                 # Contact us page
│   ├── dashboard.html               # Student dashboard
│   ├── event.html                   # Campus events page
│   ├── faq.html                     # Frequently asked questions
│   ├── feedback.html                # Student feedback form
│   ├── first.html                   # Introductory HTML exercise
│   ├── login.html                   # Login form with validation
│   ├── profile.html                 # Creator profile card
│   ├── register.html                # Registration form
│   ├── register.css                 # Form styling
│   ├── Main.java                    # Java practical utility
│   ├── Doc1.docx                    # Course practical documentation
│   └── *.jpg, *.avif                # Campus and event imagery
├── public/                          # Public Document Root (Web-Accessible)
│   ├── index.html                   # Static HTML entry point (Zero-dependency)
│   ├── index.php                    # Modular PHP entry point (Consumes app/includes)
│   ├── pages/                       # Semantic subpages
│   │   ├── about.html               # About Us & platform overview
│   │   ├── administrative.html      # Administrative timings & services
│   │   ├── campuslife.html          # Student clubs & campus activities
│   │   ├── course-enrollment.html   # Course enrollment & curriculum
│   │   ├── dashboard.html           # Student self-service overview
│   │   ├── event-detail.html        # Detailed event registration view
│   │   ├── events.html              # Upcoming events schedule
│   │   ├── login.html & login.php   # Dual static & PHP auth forms
│   │   ├── registration.html & .php # Student registration forms
│   │   ├── contact.html & .php      # Contact message forms
│   │   └── faq.html                 # Accordion FAQ with theme toggle
│   ├── assets/                      # Static assets
│   │   ├── css/                     # Centralized design system (main.css, home.css, etc.)
│   │   ├── js/                      # Modular client logic (main.js, registration.js, etc.)
│   │   └── images/                  # Branding, icons, and logos
│   └── process-*.php                # Form processing controllers
├── app/                             # Application Core (Protected from Direct Web Access)
│   ├── config/                      # Environment (.env) & Singleton PDO DB connection
│   ├── includes/                    # Reusable view partials (header, nav, footer, auth_check)
│   ├── middleware/                  # Auth and Role-Based Access Control (Admin/Student)
│   └── services/                    # StudentService & EventService query models
├── api/                             # RESTful JSON API Endpoints
│   ├── auth/                        # /api/auth/login.php & logout.php
│   ├── students/                    # /api/students/ (GET list/search, POST create)
│   └── events/                      # /api/events/ (GET list, POST create)
├── admin/                           # Administrative Backoffice Portal (RBAC Protected)
├── student/                         # Student Self-Service Portal (Auth Protected)
├── database/                        # Database Schemas & Migrations
│   ├── schema.sql                   # MySQL DDL (users, students, events, registrations, audit_logs)
│   ├── seed.sql                     # Seed dataset with sample students and events
│   └── production_complete_migration.sql # Full migration script
├── storage/                         # Writable file storage
│   └── uploads/                     # Upload directory (protected by script-execution blocking .htaccess)
├── tests/                           # Verification test suites & automated health checkers
├── docs/                            # Full technical documentation, deployment guides & test reports
├── .env.example                     # Environment configuration template
├── .htaccess                        # Apache security & URL routing rules
├── .gitignore                       # Git ignore rules for credentials, uploads, and temp files
├── index.html                       # Root redirector forwarding to public/index.html
├── index.php                        # Root proxy forwarding to public/index.html
└── README.md                        # Master project documentation
```

---

## 🚀 Getting Started

### Method 1: Instant Static Preview (No Server Required)
You can directly open any of the following HTML files in any web browser:
- Root landing redirector: `index.html`
- Modern public portal: `public/index.html`
- Original practical homepage: `25aiml019/index.html`

### Method 2: Running with Local PHP Built-in Server
1. Ensure PHP 8.0+ is installed on your computer.
2. Open terminal in the project root directory and start the server:
   ```bash
   php -S localhost:8000
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

### Method 3: Running on Apache / XAMPP
1. Move or clone the `WT_project` folder into `xampp/htdocs/`.
2. Start **Apache** and **MySQL** from the XAMPP Control Panel.
3. Import the database:
   - Open `http://localhost/phpmyadmin`
   - Create a database named `studenthub`
   - Import `database/schema.sql` and `database/seed.sql`
4. Copy `.env.example` to `.env` and configure your database credentials:
   ```ini
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=studenthub
   DB_USER=root
   DB_PASS=
   ```
5. Access the application at:
   ```
   http://localhost/WT_project/
   ```

---

## 🔒 Security Best Practices Implemented

- **Prepared Statements (PDO):** Eliminates SQL injection risk across all database operations.
- **Credential Protection:** Secrets and database credentials reside strictly in `.env` (excluded via `.gitignore`).
- **File Upload Hardening:** `storage/uploads/.htaccess` disables PHP script execution (`php_flag engine off`) to prevent remote code execution.
- **Session Hardening:** HTTP-only cookies, strict session expiration, and CSRF token verification.
- **RBAC:** Strict separation of Student and Administrator privileges via middleware guards.

---

## 👨‍💻 Author & Credits

- **Student:** Daksh Harkhani
- **Roll Number:** 25AIML019
- **Department:** Artificial Intelligence & Machine Learning (AIML)
- **Institution:** CSPIT, CHARUSAT University
- **GitHub:** [@25aiml019-hub](https://github.com/25aiml019-hub)
