# StudentHub Test Suite

This directory contains test runners and scripts to verify page structure, navigation links, and client-side form validation.

## Available Tests
1. **In-Browser Test Runner:**
   - File: `tests/validation_test.html`
   - How to run: Open `tests/validation_test.html` in any web browser.
   - Verifies: Regular expressions for mobile and email validation, function availability for `registerForm()`, `resetForm()`, `submitMessage()`, `resetMessage()`, `faq()`, and `theme()`.

2. **Automated Link & Asset Verification Script:**
   - File: `tests/verify_project.py`
   - How to run: `python tests/verify_project.py`
   - Verifies: Non-broken relative links across all HTML files, existence of all linked CSS and JS assets, absence of 404 targets.
