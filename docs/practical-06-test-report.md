# Practical 6: Dynamic JSON Rendering with Fetch API — Test & Implementation Report

**Course:** AIUE203 — Web Development Fundamentals (WDF)  
**Student Name:** Anshika Badala  
**Student ID:** 25AIML002  
**Department:** Artificial Intelligence & Machine Learning (AIML)  
**Institute:** Chandubhai S. Patel Institute of Technology (CSPIT), CHARUSAT  
**Implementation Date:** October 2026  
**Status:** Completed & 100% Verified  

---

## 1. Summary of Changes

In Practical 6, the static student hub was upgraded with asynchronous client-side data rendering using JavaScript's native Fetch API, dynamic client-side filtering, multi-field search, column sorting, accessible pagination, loading indicators, error recovery with retry controls, and offline-capable localStorage caching.

### 1.1 Files Created
| File Path | Purpose |
|---|---|
| `public/assets/data/events.json` | 16 realistic campus event records across 5 categories with dates, venues, and status. |
| `public/assets/data/students.json` | 18 realistic fictional student records across courses, departments, and academic years. |
| `public/assets/data/faqs.json` | 16 campus FAQ records preserving original Practical 4 questions + 11 new entries. |
| `public/assets/js/data-loader.js` | Reusable data-fetching utility with error handling, localStorage caching, and stale fallback. |
| `public/assets/js/pagination.js` | Reusable client-side pagination engine and safe DOM control generator. |
| `public/assets/js/events-renderer.js` | Dynamic events manager (search, category/status filters, date/title sort, pagination). |
| `public/assets/js/faq-renderer.js` | Dynamic FAQ manager (search, category filter, accessible accordion, pagination). |
| `public/assets/js/students-renderer.js` | Dynamic student directory manager (search, course/year filters, name sort, pagination). |
| `public/assets/css/dynamic-data.css` | Styling for control bars, loading spinners, error alerts, cache badges, and pagination. |
| `public/pages/students.html` | Dedicated standalone student directory page with universal navigation. |
| `tests/practical_6_test.html` | In-browser interactive test suite for live Fetch API validation. |
| `tests/verify_practical_6.py` | Automated CLI test suite validating datasets, search/filter/sort, pagination, and DOM safety. |
| `docs/practical-06-test-report.md` | Practical 6 implementation and verification report. |

### 1.2 Files Modified
| File Path | Modification Summary |
|---|---|
| `public/pages/events.html` | Mounted `#events-app`, linked `dynamic-data.css`, `data-loader.js`, `pagination.js`, `events-renderer.js`. Retained Practical 2 `<noscript>` static schedule. |
| `public/pages/faq.html` | Mounted `#faq-app`, linked `dynamic-data.css`, `data-loader.js`, `pagination.js`, `faq-renderer.js`. Retained theme toggle and `<noscript>` static questions. |
| `public/pages/dashboard.html` | Integrated dynamic Campus Student Directory section with search/filter/pagination under Quick Links. |
| `tests/validation_test.html` | Added navigation link to `practical_6_test.html`. |
| `tests/verify_project.py` | Added Practical 6 dataset and script paths to critical architecture verification. |
| `README.md` | Documented Practical 6 features, Fetch API requirements, and local HTTP server commands. |

---

## 2. Feature Implementation Details

### 2.1 Reusable Fetch API & Cache Architecture (`data-loader.js`)
- **HTTP Status Check:** Uses `fetch()` with explicit verification of `response.ok`. Throws structured errors on non-200 responses.
- **Robust Error Recovery:** Handles network disconnects, 404 missing files, and malformed JSON syntax.
- **Client Caching:** Stores successful payloads in `localStorage` under namespaced keys (`studenthub_events_cache`, `studenthub_students_cache`, `studenthub_faqs_cache`) alongside millisecond timestamps.
- **Configurable TTL:** 10-minute cache validity window. If a network request fails (e.g., offline or browser restrictions), stale cached data is served automatically alongside a warning badge.
- **Safe Storage Handling:** All `localStorage` calls are wrapped in `try/catch` blocks to prevent crashes in private browsing or disabled-cookie environments.
- **Non-Authoritative:** Explicitly isolated from future database CRUD operations; never used as a source of truth for backend writes.

### 2.2 Reusable Client-Side Pagination (`pagination.js`)
- **Configurable Page Sizing:** 5 records per page for Events and 6 records per page for FAQs and Students.
- **Safe DOM Rendering:** Uses `document.createElement()`, `textContent`, and `setAttribute()` exclusively. Zero untrusted `innerHTML`.
- **Boundary Clamping:** Prevents navigation beyond valid ranges (`currentPage <= 1` or `currentPage >= totalPages`).
- **Dynamic Reset:** Automatically returns to page 1 whenever search queries or filters alter the active dataset size.
- **Accessibility:** Generates `<nav aria-label="Pagination Navigation">`, disabled button states, `aria-current="page"`, and `aria-label` descriptions.

### 2.3 Search, Filter & Sort Matrices
| Feature | Events Page | FAQ Page | Student Directory |
|---|---|---|---|
| **Search Fields** | Title, Description | Question, Answer | Name, Course, Department, Roll No |
| **Primary Filter** | Category (Technical, Cultural, Sports, Academic, Workshop) | Category (General, Admissions, Academics, Campus Life, Administrative) | Course (B.Tech, BCA, M.Tech, MCA) |
| **Secondary Filter**| Status (Upcoming, Ongoing, Completed) | — | Academic Year (1st, 2nd, 3rd, 4th Year) |
| **Sorting** | Date (Asc/Desc), Title (A–Z / Z–A) | — | Name (A–Z / Z–A) |
| **Reset Filter** | Instant reset button clearing all fields | Instant reset button | Instant reset button |
| **Live Announcer** | `aria-live="polite"` result counter | `aria-live="polite"` result counter | `aria-live="polite"` result counter |

### 2.4 UI States & Accessibility
- **Loading State:** Centered animated CSS spinner (`.spinner`) and accessible text (`role="status"`).
- **Error State:** High-contrast alert banner (`role="alert"`) displaying the exact failure cause and an interactive "Retry Connection" button.
- **Empty State:** Dashed card with guidance message and "Clear All Filters" button when queries match 0 records.
- **Cache Badges:** Visual indicator pills:
  - `<span class="data-badge live">Live Data (HH:MM:SS)</span>`
  - `<span class="data-badge cached">Cached Data (HH:MM:SS)</span>`
- **Dark Theme Compatibility:** Fully themed under `body.dark-theme` matching Practical 4 appearance styles.

---

## 3. Test Execution and Verification

### 3.1 Automated Python Test Suite (`tests/verify_practical_6.py`)
Executed command:
```bash
python tests/verify_practical_6.py
```
**Outcome: PASSED (100%)**

#### Detailed Test Assertions:
1. **Dataset Integrity:**
   - `events.json`: 16 records parsed successfully. All 16 contain `id`, `title`, `description`, `category`, `date`, `time`, `venue`, `status`.
   - `students.json`: 18 records parsed successfully. All 18 contain `id`, `name`, `course`, `year`, `department`.
   - `faqs.json`: 16 records parsed successfully. All 16 contain `id`, `question`, `answer`, `category`.
2. **Search, Filter & Sort Logic:**
   - Events title/description search for "hackathon" matched 2 records.
   - Events category filter for "Technical" returned 3 records.
   - Events combined filter ("Technical" + "Upcoming") returned 2 records.
   - Events date sorting validated (Earliest: `2026-07-15`, Latest: `2026-12-04`).
   - Students search for "artificial intelligence" returned 3 records.
   - Students combined filter ("B.Tech" + "3rd Year") returned 4 records.
   - Students name sorting validated (`Aarav Patel` to `Sanya Malhotra`).
   - FAQs search for "theme" returned 1 record.
   - FAQs category filter for "Administrative" returned 4 records.
3. **Pagination Boundaries:**
   - Verified 16 items sliced into 4 pages of size 5 with partial last page.
   - Empty array produces `totalPages = 1` and 0 items.
4. **Security & Safe DOM Inspection:**
   - Scanned all 4 JavaScript files (`events-renderer.js`, `faq-renderer.js`, `students-renderer.js`, `pagination.js`).
   - Zero occurrences of `innerHTML` with untrusted data.
5. **Practicals 1–5 Backward Compatibility:**
   - `faq.js`: `theme()`, `faq()`, `faq1()`, `faq2()`, `faq3()`, `faq4()` preserved.
   - `registration.js`: `registerForm()`, `resetForm()`, regexes preserved.
   - `contact.js`: `submitMessage()`, `resetMessage()` preserved.
   - `<noscript>` fallback content preserved on `events.html` and `faq.html`.

### 3.2 Overall Architecture Verification (`tests/verify_project.py`)
Executed command:
```bash
python tests/verify_project.py
```
**Outcome: PASSED (100%)**
- 189 local HTML, CSS, JavaScript, and relative navigation references verified with zero broken paths.

---

## 4. Known Limitations & Operating Guidance

### Browser Security on `file://` Protocol
Modern web browsers (Google Chrome, Microsoft Edge, Mozilla Firefox) apply strict Cross-Origin Request Security (CORS) policies that block `fetch()` requests made directly against the `file://` URI scheme:
```
Access to fetch at 'file:///.../events.json' from origin 'null' has been blocked by CORS policy.
```
**Operating Recommendation:**
To view dynamic Fetch API rendering, launch StudentHub using a lightweight local HTTP server as documented in the README:
```bash
# Option 1: Python HTTP Server (Built-in)
python -m http.server 8000

# Option 2: PHP Built-in Server
php -S localhost:8000 -t public
```
When opened over HTTP/HTTPS (`http://localhost:8000`), the Fetch API loads datasets cleanly and populates the `localStorage` cache.
If opened directly via `file://`, the graceful offline cache fallback and semantic `<noscript>` fallbacks display user-friendly instructions.
