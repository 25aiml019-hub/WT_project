# 🎓 Web Technology Project — Student Hub

<div align="center">

[![Student](https://img.shields.io/badge/Author-Daksh%20Harkhani%20(25AIML019)-4f46e5.svg?style=for-the-badge&logo=github)](https://github.com/25aiml019-hub)
[![Institution](https://img.shields.io/badge/Institution-CSPIT%20%7C%20CHARUSAT-0284c7.svg?style=for-the-badge)](https://charusat.ac.in)
[![Course](https://img.shields.io/badge/Course-Web%20Technology%20(WT)-059669.svg?style=for-the-badge)](https://charusat.ac.in)
[![Live Site](https://img.shields.io/badge/Live%20Website-GitHub%20Pages-blue.svg?style=for-the-badge&logo=github)](https://25aiml019-hub.github.io/WT_project/)

<p align="center">
  <strong>Comprehensive Web Technology Laboratory Practicals &amp; Campus Information Portal.</strong><br>
  Built with semantic HTML5, CSS3 styling, JavaScript client validation, modular PHP backend, and MySQL database integration.
</p>

[🌐 Live Website](https://25aiml019-hub.github.io/WT_project/) • [📑 Practical Lab Pages](#-laboratory-practicals-25aiml019) • [🏗️ Architecture &amp; Backend](#️-system-architecture--backend) • [🚀 Setup Guide](#-local-setup-guide-xampp--php)

</div>

---

## 👤 Student &amp; Course Details

| Attribute | Details |
|---|---|
| **Student Name** | **Daksh Harkhani** |
| **Student ID / Roll No.** | **25AIML019** |
| **Institution** | Chandubhai S. Patel Institute of Technology (CSPIT) |
| **University** | Charotar University of Science and Technology (CHARUSAT) |
| **Subject / Course** | Web Technology (WT) |
| **GitHub Profile** | [@25aiml019-hub](https://github.com/25aiml019-hub) |
| **Repository** | [https://github.com/25aiml019-hub/WT_project](https://github.com/25aiml019-hub/WT_project) |
| **Live Web Portal** | [https://25aiml019-hub.github.io/WT_project/](https://25aiml019-hub.github.io/WT_project/) |

---

## 📑 Laboratory Practicals (`25aiml019/`)

All original frontend lab exercises are organized inside [`25aiml019/`](25aiml019/):

| Page | Description | Direct Link |
|---|---|---|
| **Home Portal** | Main campus landing portal with hero cards and navigation | [`25aiml019/index.html`](25aiml019/index.html) |
| **Student Profile** | Student developer bio and contact badge | [`25aiml019/profile.html`](25aiml019/profile.html) |
| **Student Registration** | Comprehensive registration form with validation | [`25aiml019/register.html`](25aiml019/register.html) |
| **User Login** | Form authentication interface with regex validation | [`25aiml019/login.html`](25aiml019/login.html) |
| **Events Portal** | Campus tech, cultural, and sports events showcase | [`25aiml019/event.html`](25aiml019/event.html) |
| **Student Dashboard** | Central student activity dashboard | [`25aiml019/dashboard.html`](25aiml019/dashboard.html) |
| **Admin Panel** | Administrative operations panel | [`25aiml019/admin.html`](25aiml019/admin.html) |
| **About Us** | About StudentHub platform and mission | [`25aiml019/about.html`](25aiml019/about.html) |
| **Contact Us** | Helpdesk and campus communication form | [`25aiml019/contact.html`](25aiml019/contact.html) |
| **FAQ** | Frequently asked questions accordion | [`25aiml019/faq.html`](25aiml019/faq.html) |
| **Feedback** | Campus service review and feedback form | [`25aiml019/feedback.html`](25aiml019/feedback.html) |
| **Introductory Page** | First introductory HTML document | [`first.html`](first.html) |

---

## 🏗️ System Architecture &amp; Backend

```
WT_project/
├── 25aiml019/                   # Core frontend practical lab pages & assets
│   ├── index.html               # Main laboratory portal
│   ├── about.html, admin.html   # Campus subpages
│   ├── login.html, register.html# Authentication & form pages
│   └── *.jpg, *.avif            # Campus images & media
├── app/                         # Protected PHP backend core
│   ├── config/                  # DB credentials (PDO/MySQLi) & session security
│   ├── includes/                # Shared header, navbar, footer partials
│   ├── middleware/              # RBAC & authentication guards
│   └── services/                # Student, event, and audit data services
├── api/                         # RESTful API endpoints
│   ├── auth/                    # JSON login & session endpoints
│   ├── students/                # Student directory API
│   └── events/                  # Event listing & registration API
├── admin/                       # Admin backoffice portal (CRUD operations)
├── student/                     # Student self-service portal
├── database/                    # MySQL database schema & migrations
│   ├── schema.sql               # Base database tables
│   ├── extended_schema.sql      # Extended tables & features
│   └── create_admin.php         # Admin account initialization script
├── storage/                     # Secure upload storage (.htaccess protected)
├── public/                      # Web server public proxy handlers
├── .gitignore                   # Ignore rules for credentials & temp files
├── .env.example                 # Environment configuration template
├── index.html                   # Root entrypoint (redirects to 25aiml019/index.html)
└── index.php                    # PHP entrypoint (redirects to 25aiml019/index.html)
```

---

## 🚀 Local Setup Guide (XAMPP / PHP)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/25aiml019-hub/WT_project.git
   cd WT_project
   ```

2. **Configure Database**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Open phpMyAdmin (`http://localhost/phpmyadmin/`), create a database named `studenthub`.
   - Import `database/schema.sql`.

3. **Run Local Server**:
   - Move project to `xampp/htdocs/WT_project/` OR start PHP's built-in server:
     ```bash
     php -S localhost:8000
     ```
   - Open in your browser:  
     👉 **`http://localhost:8000/25aiml019/index.html`** or **`http://localhost/WT_project/`**

---

## 📜 Author &amp; License

Developed by **Daksh Harkhani (`25AIML019`)**  
Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT University.  
Academic Year 2025–2026.
