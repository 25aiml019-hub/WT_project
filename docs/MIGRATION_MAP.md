# Migration Map: Wt_Project to Restructured Architecture

**Date:** October 2026  
**Author:** Anshika Badala (25AIML002)  
**Project:** StudentHub  

This document tracks every original file from `Wt_Project/` and details its new location, status, and modifications.

| Original File Path | New File Path | Status | Changes & Enhancements |
|---|---|---|---|
| `Wt_Project/index.html` | `public/index.html` | Moved & Refactored | Linked to `main.css` and `home.css`. Added vector SVG fallback logo. Retained all 4 hero cards and welcome message. |
| `Wt_Project/index.html` | `public/index.php` | New (Companion) | Added modular PHP version consuming `app/includes/` partials. |
| `Wt_Project/home.css` | `public/assets/css/home.css` | Moved & Cleaned | Removed 61 lines of commented-out initial styles. Refactored hero grid and cards using CSS variables. |
| `Wt_Project/about.html` | `public/pages/about.html` | Moved & Cleaned | Removed 28 lines of dead legacy markup at the top. Added universal navigation bar and footer. |
| `Wt_Project/about.css` | `public/assets/css/about.css` | Moved & Cleaned | Refactored container, creator card, and social links to use centralized CSS variables. |
| `Wt_Project/ADMINISTRATIVE.html` | `public/pages/administrative.html` | Moved & Renamed | Normalized filename to lowercase. Added universal navigation bar and footer. Styled services list and timing table. |
| `Wt_Project/admin.css` | `public/assets/css/admin.css` | Moved & Cleaned | Integrated with centralized design tokens in `main.css`. |
| `Wt_Project/campuslife.html` | `public/pages/campuslife.html` | Moved & Fixed | Fixed broken link typo (`ADMINSTRATIVE.html` -> `administrative.html`). Removed duplicate inline `<style>` tags. Added universal navigation bar and footer. |
| `Wt_Project/campuslife.css` | `public/assets/css/campuslife.css` | Moved & Cleaned | Refactored clubs list with clean hover animation and responsive padding. |
| `Wt_Project/COURSEENROLLMENT.html` | `public/pages/course-enrollment.html` | Moved, Fixed & Renamed | Fixed unclosed `<link>` tag on line 5. Uncommented navigation and integrated universal navigation bar and footer. |
| `Wt_Project/COURSEENROLLMENT.css` | `public/assets/css/course-enrollment.css` | Moved & Renamed | Normalized uppercase filename to kebab-case `course-enrollment.css`. Scoped course table styles. |
| `Wt_Project/dashboard.html` | `public/pages/dashboard.html` | Moved & Upgraded | Preserved student details and quick links. Upgraded layout to modern responsive card with universal navigation and footer. |
| `Wt_Project/dashboard.css` | `public/assets/css/dashboard.css` | Moved & Upgraded | Replaced primitive `aliceblue` styling with branded primary blue theme and grid layout. |
| `Wt_Project/events.html` | `public/pages/events.html` | Moved & Upgraded | Added universal navigation bar and footer. Preserved upcoming events table. |
| `Wt_Project/events.css` | `public/assets/css/events.css` | Moved & Upgraded | Replaced plain borders with responsive data-table design tokens. |
| `Wt_Project/login.html` | `public/pages/login.html` | Moved & Fixed | Fixed orphaned `</a>` on line 24. Added universal navigation bar and footer. Styled login card with responsive actions. |
| `Wt_Project/login.css` | `public/assets/css/login.css` | Moved & Upgraded | Modernized form card to responsive layout using CSS variables. |
| `Wt_Project/registration.html` | `public/pages/registration.html` | Moved & Cleaned | Removed 71 lines of dead prototype markup at the top. Added universal navigation bar and footer. Connected to `registration.js`. |
| `Wt_Project/reg.css` | `public/assets/css/registration.css` | Moved & Renamed | Renamed from abbreviated `reg.css` to `registration.css`. Modernized radio and checkbox options alignment. |
| `Wt_Project/registration.js` | `public/assets/js/registration.js` | Moved & Preserved | Preserved complete Practical 5 validation: name, email, 10-digit mobile regex, course, department, gender, hobbies, address, and reset handler. |
| `Wt_Project/contact.html` | `public/pages/contact.html` | Moved & Fixed | Removed 33 lines of commented-out table code. Added universal navigation bar and footer. Fixed missing script reference. |
| `Wt_Project/contact.css` | `public/assets/css/contact.css` | Moved & Cleaned | Scoped contact info cards grid and message form styles. |
| *(None - Missing File)* | `public/assets/js/contact.js` | Created | **Bug fix:** Created missing script to implement `submitMessage()` and `resetMessage()` preventing browser console errors. |
| `Wt_Project/faq.html` | `public/pages/faq.html` | Moved & Cleaned | Removed 74 lines of commented-out prototype code. Added universal navigation bar and footer. Maintained all 5 questions and answers. |
| `Wt_Project/faq.css` | `public/assets/css/faq.css` | Moved & Cleaned | Cleaned accordion and dark-theme stylesheet. |
| `Wt_Project/faq.js` | `public/assets/js/faq.js` | Moved & Enhanced | Preserved functions `theme()`, `faq()`, `faq1()`, `faq2()`, `faq3()`, `faq4()`. Added persistent dark theme via `localStorage`. |
| `Wt_Project/README.md` | `README.md` | Replaced & Upgraded | Expanded with complete project documentation, practical mapping, local development guide, and author credits. |
| *(None)* | `public/assets/css/main.css` | Created | Central design system stylesheet containing CSS variables, base reset, universal navigation, table, form, and footer components. |
| *(None)* | `public/assets/js/main.js` | Created | Global script providing automatic active navigation link highlighting. |
| *(None)* | `public/assets/images/logo.svg` | Created | Vector SVG logo for StudentHub providing offline fallback. |
| *(None)* | `index.html` (root) | Created | Root landing redirector forwarding visitors to `public/index.html`. |
| *(None)* | `app/config/config.php` | Created | Base configuration, `.env` file loader, session initializer, and app constants. |
| *(None)* | `app/config/db.php` | Created | Secure singleton PDO database connection with prepared statements and safe error handling. |
| *(None)* | `app/includes/header.php` | Created | Reusable PHP header template with branding and meta tags. |
| *(None)* | `app/includes/nav.php` | Created | Reusable PHP navigation partial with dynamic active state highlighting. |
| *(None)* | `app/includes/footer.php` | Created | Reusable PHP footer partial with copyright and author credentials. |
| *(None)* | `app/includes/auth_check.php` | Created | Authentication guard helpers and session inspectors. |
| *(None)* | `app/middleware/auth_middleware.php` | Created | Authentication enforcement middleware. |
| *(None)* | `app/middleware/role_middleware.php` | Created | Role-based access control middleware (Admin vs Student). |
| *(None)* | `app/services/student_service.php` | Created | Data access service for student records (Practical 11 scaffolding). |
| *(None)* | `app/services/event_service.php` | Created | Data access service for campus events (Practical 12 scaffolding). |
| *(None)* | `api/auth/login.php` & `logout.php` | Created | Resource-based JSON authentication endpoints. |
| *(None)* | `api/students/index.php` | Created | Resource-based JSON API endpoint for student data. |
| *(None)* | `api/events/index.php` | Created | Resource-based JSON API endpoint for event data. |
| *(None)* | `admin/index.php` & `README.md` | Created | Administrative dashboard portal scaffold. |
| *(None)* | `student/index.php` & `README.md` | Created | Student self-service portal scaffold. |
| *(None)* | `storage/uploads/.htaccess` | Created | Security rule disabling script execution in the uploads directory. |
| *(None)* | `storage/uploads/.gitignore` | Created | Excludes uploaded files from version control. |
| *(None)* | `database/schema.sql` | Created | MySQL DDL schema for users, students, events, registrations, and audit logs. |
| *(None)* | `database/seed.sql` | Created | Seed data including 20 sample students, sample events, and users. |
| *(None)* | `tests/validation_test.html` | Created | Interactive in-browser test runner. |
| *(None)* | `tests/verify_project.py` | Created | Automated verification script checking 158 asset and link references. |
| *(None)* | `.gitignore` | Created | Comprehensive git ignore rules for secrets, uploads, and temporary files. |
| *(None)* | `.env.example` | Created | Environment variable configuration template. |
| *(None)* | `docs/PROJECT_AUDIT.md` | Created | Comprehensive audit of initial project state and defects. |
