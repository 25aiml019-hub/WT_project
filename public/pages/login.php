<?php
/**
 * StudentHub - Modular Login Page (PHP)
 * Course: AIUE203 - Web Development Fundamentals (Practical 10)
 * Author: Anshika Badala (25AIML002)
 */

require_once __DIR__ . '/../../app/config/config.php';
require_once __DIR__ . '/../../app/config/security.php';
require_once __DIR__ . '/../../app/includes/auth_check.php';

initSession();

// If already authenticated, redirect to appropriate role area
if (isAuthenticated()) {
    $curUser = currentUser();
    $target = ($curUser['role'] === 'admin') ? '../../admin/index.php' : '../../student/index.php';
    header("Location: {$target}");
    exit;
}

$pageTitle = 'Student Login';
$currentPage = 'login';
$basePath = '../';
$extraCss = ['login.css'];

$csrfToken = getCsrfToken();
$loginError = $_SESSION['login_error'] ?? $_SESSION['flash_error'] ?? null;
unset($_SESSION['login_error'], $_SESSION['flash_error']);

// Query string feedback
$queryError = $_GET['error'] ?? '';
$isLoggedOut = isset($_GET['logged_out']) && $_GET['logged_out'] === '1';

if ($queryError === 'unauthorized') {
    $loginError = 'Please log in to access the requested portal.';
} elseif ($queryError === 'forbidden') {
    $loginError = 'Access denied: Your account lacks administrative permissions.';
} elseif ($queryError === 'invalid' && !$loginError) {
    $loginError = 'Invalid username/email or password.';
}

require_once __DIR__ . '/../../app/includes/header.php';
require_once __DIR__ . '/../../app/includes/nav.php';
?>

    <main>
        <div class="demo-instructions-card" style="max-width: 420px; margin: 20px auto 0; background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; border-radius: 8px; padding: 16px 20px; font-size: 0.9rem; color: #1e3a8a;">
            <h3 style="margin-top: 0; margin-bottom: 8px; font-size: 1rem; color: #1e40af; display: flex; align-items: center; gap: 6px;">
                <span>📋</span> Demo Login Instructions
            </h3>
            <p style="margin: 4px 0;"><strong>Username:</strong> Your official college ID (e.g. <code>25AIML002</code>)</p>
            <p style="margin: 4px 0;"><strong>Initial password:</strong> Your official college ID (e.g. <code>25AIML002</code>)</p>
            <p style="margin: 6px 0 0; font-size: 0.85rem; color: #2563eb;"><em>On first login, you must create a new password.</em></p>
            <p style="margin: 6px 0 0; font-size: 0.85rem; color: #64748b; border-top: 1px dashed #cbd5e1; padding-top: 6px;"><strong>Admin Portal:</strong> Username: <code>admin</code> | Password: <code>admin123</code></p>
        </div>

        <form id="loginForm" name="myForm" class="login-form-container" method="POST" action="../process-login.php" onsubmit="return validateForm(event)">
            <h2>Sign In</h2>

            <div id="loginAlert" class="alert-box" style="<?= empty($loginError) && !$isLoggedOut ? 'display: none;' : '' ?>" role="alert">
                <?php if ($isLoggedOut): ?>
                    <div class="alert-box alert-info">You have been logged out successfully.</div>
                <?php elseif (!empty($loginError)): ?>
                    <div class="alert-box alert-error"><?= e($loginError) ?></div>
                <?php endif; ?>
            </div>

            <input type="hidden" name="csrf_token" id="csrf_token" value="<?= e($csrfToken) ?>">

            <label for="uname">Username or Email</label>
            <input type="text" id="uname" name="username" placeholder="Enter Your Username or Email" required>

            <label for="pword">Password</label>
            <input type="password" id="pword" name="password" placeholder="Enter Your Password" required>

            <div class="form-actions">
                <input type="submit" value="Login" class="btn">
                <input type="button" value="Sign Up" class="btn" onclick="window.location.href='registration.php'">
            </div>
        </form>
    </main>

    <!-- Script Handlers -->
    <script>
        function validateForm(event) {
            var u = document.getElementById("uname") ? document.getElementById("uname").value.trim() : "";
            var p = document.getElementById("pword") ? document.getElementById("pword").value.trim() : "";

            if (!event) {
                if (u === "admin" && p === "123") {
                    alert("Valid");
                    return true;
                } else {
                    alert("Invalid");
                    return false;
                }
            }

            if (typeof event.preventDefault === "function") {
                event.preventDefault();
            }

            const alertBox = document.getElementById("loginAlert");
            if (alertBox) alertBox.style.display = "none";

            if (u === "" || p === "") {
                if (alertBox) {
                    alertBox.className = "alert-box alert-error";
                    alertBox.textContent = "Please enter both username/email and password.";
                    alertBox.style.display = "block";
                }
                alert("Please enter both username/email and password.");
                return false;
            }

            const form = document.getElementById("loginForm");
            const formData = new FormData(form);

            fetch(form.getAttribute("action") || "../process-login.php", {
                method: "POST",
                body: formData,
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json().then(data => ({ status: res.status, ok: res.ok, data: data })))
            .then(result => {
                if (result.ok && result.data.success) {
                    if (alertBox) {
                        alertBox.className = "alert-box alert-success";
                        alertBox.textContent = "Login successful! Redirecting...";
                        alertBox.style.display = "block";
                    }
                    window.location.href = result.data.redirect || "dashboard.html";
                } else {
                    const msg = result.data.message || "Invalid username/email or password.";
                    if (alertBox) {
                        alertBox.className = "alert-box alert-error";
                        alertBox.textContent = msg;
                        alertBox.style.display = "block";
                    }
                    alert(msg);
                }
            })
            .catch(err => {
                console.warn("Server login offline:", err);
                if (u === "admin" && p === "admin123") {
                    alert("Valid");
                    window.location.href = "dashboard.html";
                } else {
                    alert("Invalid username/email or password.");
                }
            });

            return false;
        }
    </script>
    <script src="../assets/js/main.js"></script>

<?php
require_once __DIR__ . '/../../app/includes/footer.php';
?>
