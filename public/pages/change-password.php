<?php
/**
 * StudentHub - Password Change Interface
 * Course: AIUE203 - Web Development Fundamentals
 * Author: Daksh Harkhani (25AIML019)
 */

require_once __DIR__ . '/../../app/config/config.php';
require_once __DIR__ . '/../../app/config/security.php';
require_once __DIR__ . '/../../app/includes/auth_check.php';

initSession();

// Require login
if (empty($_SESSION['user_id'])) {
    header('Location: login.html?error=unauthorized');
    exit;
}

$pageTitle = 'Update Your Password - StudentHub';
$currentPage = 'change-password';
$basePath = '../';
$extraCss = ['login.css'];

$csrfToken = getCsrfToken();
$flashError = $_SESSION['flash_error'] ?? null;
unset($_SESSION['flash_error']);

$user = currentUser();
$isFirstLogin = !empty($_SESSION['must_change_password']);

require_once __DIR__ . '/../../app/includes/header.php';
require_once __DIR__ . '/../../app/includes/nav.php';
?>

<main class="page-container" style="max-width: 540px; margin: 2rem auto; padding: 0 1rem;">
    <div class="card" style="background: var(--surface, #fff); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <h2 style="margin-top: 0; color: var(--text-heading, #1e293b); font-size: 1.5rem;">
            <?= $isFirstLogin ? 'First Time Login — Update Password' : 'Change Your Password' ?>
        </h2>

        <?php if ($isFirstLogin): ?>
            <div class="alert-box alert-info" style="margin-bottom: 1.25rem; padding: 0.75rem 1rem; border-left: 4px solid #0284c7; background: #f0f9ff; color: #0369a1; border-radius: 4px; font-size: 0.9rem;">
                <strong>Welcome!</strong> As this is your first time logging in with your college ID, please set a secure personal password before accessing your student portal.
            </div>
        <?php else: ?>
            <p style="color: var(--text-muted, #64748b); font-size: 0.9rem; margin-bottom: 1.25rem;">
                Enter your current temporary password followed by your chosen new password.
            </p>
        <?php endif; ?>

        <div id="changeAlert" class="alert-box" style="<?= empty($flashError) ? 'display: none;' : '' ?> margin-bottom: 1rem; padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.9rem;" role="alert">
            <?php if (!empty($flashError)): ?>
                <div class="alert-box alert-error" style="border-left: 4px solid #dc2626; background: #fef2f2; color: #991b1b;"><?= e($flashError) ?></div>
            <?php endif; ?>
        </div>

        <form id="changePasswordForm" method="POST" action="../process-change-password.php" onsubmit="return handlePasswordChange(event)">
            <input type="hidden" name="csrf_token" id="csrf_token" value="<?= e($csrfToken) ?>">

            <div style="margin-bottom: 1rem;">
                <label for="current_password" style="display: block; font-weight: 500; margin-bottom: 0.35rem; color: var(--text-heading, #1e293b);">Current Password</label>
                <input type="password" id="current_password" name="current_password" required placeholder="Enter current temporary password" style="width: 100%; padding: 0.6rem 0.75rem; border: 1px solid var(--border-color, #cbd5e1); border-radius: 6px; box-sizing: border-box;">
            </div>

            <div style="margin-bottom: 1rem;">
                <label for="new_password" style="display: block; font-weight: 500; margin-bottom: 0.35rem; color: var(--text-heading, #1e293b);">New Password (minimum 6 characters)</label>
                <input type="password" id="new_password" name="new_password" required minlength="6" placeholder="Enter new strong password" style="width: 100%; padding: 0.6rem 0.75rem; border: 1px solid var(--border-color, #cbd5e1); border-radius: 6px; box-sizing: border-box;">
            </div>

            <div style="margin-bottom: 1.5rem;">
                <label for="confirm_password" style="display: block; font-weight: 500; margin-bottom: 0.35rem; color: var(--text-heading, #1e293b);">Confirm New Password</label>
                <input type="password" id="confirm_password" name="confirm_password" required minlength="6" placeholder="Confirm new password" style="width: 100%; padding: 0.6rem 0.75rem; border: 1px solid var(--border-color, #cbd5e1); border-radius: 6px; box-sizing: border-box;">
            </div>

            <div style="display: flex; gap: 0.75rem;">
                <button type="submit" class="btn" style="flex: 1; padding: 0.75rem; background: var(--primary-color, #2563eb); color: #fff; border: none; border-radius: 6px; font-weight: 600; cursor: pointer;">
                    Set New Password &amp; Proceed
                </button>
            </div>
        </form>
    </div>
</main>

<script>
async function handlePasswordChange(event) {
    event.preventDefault();
    const alertBox = document.getElementById("changeAlert");
    alertBox.style.display = "none";

    const cur = document.getElementById("current_password").value.trim();
    const np = document.getElementById("new_password").value.trim();
    const cp = document.getElementById("confirm_password").value.trim();

    if (!cur || !np || !cp) {
        alertBox.innerHTML = '<div style="color: #991b1b; background: #fef2f2; padding: 0.75rem; border-radius: 4px;">Please fill in all fields.</div>';
        alertBox.style.display = "block";
        return false;
    }

    if (np !== cp) {
        alertBox.innerHTML = '<div style="color: #991b1b; background: #fef2f2; padding: 0.75rem; border-radius: 4px;">New password and confirm password do not match.</div>';
        alertBox.style.display = "block";
        return false;
    }

    if (np.length < 6) {
        alertBox.innerHTML = '<div style="color: #991b1b; background: #fef2f2; padding: 0.75rem; border-radius: 4px;">New password must be at least 6 characters.</div>';
        alertBox.style.display = "block";
        return false;
    }

    const form = document.getElementById("changePasswordForm");
    const formData = new FormData(form);

    try {
        const res = await fetch("../process-change-password.php", {
            method: "POST",
            body: formData,
            headers: {
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            }
        });
        const data = await res.json();
        if (res.ok && data.success) {
            alertBox.innerHTML = '<div style="color: #166534; background: #f0fdf4; padding: 0.75rem; border-radius: 4px;">Password changed successfully! Redirecting...</div>';
            alertBox.style.display = "block";
            setTimeout(() => {
                window.location.href = data.redirect || "../student/index.php";
            }, 800);
        } else {
            alertBox.innerHTML = `<div style="color: #991b1b; background: #fef2f2; padding: 0.75rem; border-radius: 4px;">${data.message || 'Failed to update password.'}</div>`;
            alertBox.style.display = "block";
        }
    } catch (e) {
        console.error("Change password error:", e);
        alertBox.innerHTML = '<div style="color: #991b1b; background: #fef2f2; padding: 0.75rem; border-radius: 4px;">Network or server error. Please try again.</div>';
        alertBox.style.display = "block";
    }

    return false;
}
</script>

<?php require_once __DIR__ . '/../../app/includes/footer.php'; ?>
