# StudentHub — InfinityFree PHP & MySQL Compatibility Assessment

**Author:** Daksh Harkhani (25AIML019)  
**Course:** AIUE203 — Web Development Fundamentals  
**Target Hosting Environment:** InfinityFree (Free cPanel / VistaPanel Hosting)  

---

## 1. PHP Runtime Compatibility

| Parameter | InfinityFree Specification | StudentHub Requirement | Compatibility Status | Notes |
|---|---|---|---|---|
| **PHP Version** | PHP 8.2 (default) / 8.1 | PHP 7.4+ / 8.0+ | **100% Compatible** | StudentHub tested on PHP 8.2+ and PHP 8.5 |
| **PDO & MySQLi** | Enabled (`pdo_mysql`, `mysqli`) | Requires dual PDO & MySQLi | **100% Compatible** | Both database drivers supported out-of-the-box |
| **Fileinfo (MIME)** | Enabled (`ext-fileinfo`) | Requires `finfo(FILEINFO_MIME_TYPE)` | **100% Compatible** | Migrated from deprecated `finfo_close` to `new finfo(...)` |
| **JSON & Sessions** | Native PHP modules | Session cookies, `json_encode` | **100% Compatible** | Built-in session security and JSON API endpoints |
| **Bcrypt Hashing** | Native `password_hash()` | Bcrypt cost 10 (`$2y$10$`) | **100% Compatible** | Compatible with `password_verify` |
| **Error Handling** | Configurable via script | `APP_DEBUG=false` display off | **100% Compatible** | Errors redirected to `storage/logs/` |

---

## 2. MySQL / Database Compatibility

| Parameter | InfinityFree Specification | StudentHub Database | Compatibility Status | Notes |
|---|---|---|---|---|
| **Engine** | MySQL 8.0 / MariaDB 10.5+ | MySQL 8.0.46 | **100% Compatible** | Standard InnoDB tables with UTF8MB4 |
| **Charset & Collation** | `utf8mb4_unicode_ci` | `utf8mb4_unicode_ci` | **100% Compatible** | Full emoji and special character support |
| **SQL Portability** | phpMyAdmin Web Import | `studenthub_infinityfree_migration.sql` | **100% Compatible** | Contains no hardcoded `CREATE DATABASE` or `USE` |
| **Foreign Keys** | Supported (InnoDB) | `ON DELETE CASCADE` / `RESTRICT` | **100% Compatible** | Relational integrity preserved across tables |
| **Max SQL File Size** | 40 MB via phpMyAdmin | 151 KB migration file | **100% Compatible** | Fits well within import thresholds |

---

## 3. Hosting Platform Constraints & Mitigations

1. **Host Connection string:**
   - *Constraint:* InfinityFree MySQL host is never `localhost`.
   - *Mitigation:* `DB_HOST` in `.env` accepts remote hostnames like `sqlXXX.infinityfree.com`.
2. **Document Root Limitation:**
   - *Constraint:* Root is fixed to `htdocs/`.
   - *Mitigation:* The bundle includes a root `.htaccess` and `index.php` that routes traffic safely into `public/` while returning HTTP 403 for `app/`, `database/`, and `storage/`.
3. **Execution & File Size Limits:**
   - *Constraint:* 10 MB per file upload limit and 30-second execution timeout.
   - *Mitigation:* StudentHub enforces a 5 MB upload limit and sub-100ms request lifecycles.
