<!-- Redirect reference to docs/PROJECT_AUDIT.md -->
# Project Audit: StudentHub (Wt_Project)

Please see the full audit report in [docs/PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md).

**Summary of Key Findings:**
- 25 files previously placed in a single flat directory `Wt_Project/`.
- Critical missing script: `contact.js` referenced in `contact.html` causing `ReferenceError`.
- Syntax errors: Unclosed `<link>` in `COURSEENROLLMENT.html`, orphaned `</a>` in `login.html`.
- Casing & typos: `ADMINISTRATIVE.html`, `COURSEENROLLMENT.html`, and `ADMINSTRATIVE.html` typo in `campuslife.html`.
- Dead code: Hundreds of lines of commented-out legacy code in `about.html`, `contact.html`, `faq.html`, `registration.html`, and `home.css`.
- Inconsistent styling & navigation: 9 out of 10 pages lacked a top navigation bar.
- Security: Missing `.gitignore`, `.env.example`, secure DB config, and upload protection.

For full audit details, tables, and issue breakdowns, see [docs/PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md).
