# WT19 backend additions (Daksh)

## UI/UX preservation

Your original WT19 frontend is kept exactly as supplied: every original file under `25aiml019/`, the root `first.html`, and the original README are unchanged. No WT02 homepage, page templates, CSS theme, fonts, colors, layout, or frontend assets have been copied over those files.

The added folders provide the WT02-style PHP/MySQL backend: authentication/session helpers, API endpoints, admin/student server modules, database schema/migrations, upload storage, and deployment configuration. The separate PHP admin portal is available at `/public/admin/` after deployment.

## Setup (XAMPP)

1. Install PHP 8.1+ with `pdo_mysql`, `mysqli`, `fileinfo` and `mbstring`, plus MySQL/MariaDB.
2. Copy `.env.example` to `.env` in this project root and set `DB_HOST`, `DB_NAME`, `DB_USER`, and `DB_PASS`.
3. Create a MySQL database named `studenthub` (or use the name in `.env`). Import `database/schema.sql` in phpMyAdmin. Import `database/extended_schema.sql` only after the base schema, if its additional tables are needed.
4. Start Apache and MySQL. Keep the project root as the application root; the PHP modules expect `app/`, `api/`, `admin/`, `database/` and `storage/` at this level.
5. Ensure `storage/` is writable by PHP. Do not make `storage/` publicly executable.
6. Open the original WT19 UI at `http://localhost/WT_project-main/25aiml019/`.

## Important integration note

The WT19 HTML forms and page styling have deliberately not been rewritten. Adding a backend does not automatically connect every old static form to the new endpoints. The available server endpoints are under `api/` (and public proxy routes under `public/api/`). To make a particular WT19 form submit to the backend, connect that form's existing fields to the matching endpoint; this can be done without changing its visual design. Do not replace the original HTML/CSS with the WT02 `public/pages` redesign.

## Security

- Do not upload `.env` to GitHub.
- Change all database credentials before deployment.
- Create a real administrator account; no demo student roster or source-project seed accounts are included.
- Use HTTPS in production and set secure session cookies.
- Never use sample student data from another person's project.

## Identity

Project documentation and backend comments use the requested author name `Daksh`. Student ID remains `25AIML019`, matching the WT19 project folder. Update this only if your official ID differs.
